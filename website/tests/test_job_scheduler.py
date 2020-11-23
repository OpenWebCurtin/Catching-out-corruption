from django.test import TestCase

# Has file copying operations.
from shutil import copyfile

from website.jobs import JobScheduler
from OpenWeb.components import Components
from django.contrib.staticfiles import finders
from django.contrib.auth import get_user_model

from django.core import management

from website.models import (AsyncJob, ProcessingJob, FileDeletionJob, UploadedFile,
    FileDeletionRequest)

from website.management.commands.runjob import Command as Command_JS
User = get_user_model()

class TestJobScheduler(TestCase):
    """ Testing suite for website.jobs.JobScheduler"""

    def setUp(self):
        management.call_command("initperms")
        management.call_command("initusers")

    # Tests that get_next_job returns (None, None) if no jobs have
    # been scheduled.
    def test_valid_get_next_job_1(self):
        js = Components.get_job_scheduler()
        job, instance = js.get_next_job()

        self.assertIsNone(job)
        self.assertIsNone(instance)

    # Test that get_next_job returns the correct job if one job has
    # been scheduled.
    def test_valid_get_next_job_2(self):
        js = Components.get_job_scheduler()

        expected_job = AsyncJob.objects.create(
            priority=1
        )

        expected_instance = ProcessingJob.objects.create(
            job_base=expected_job,
            file_name="1.pdf"
        )

        job, instance = js.get_next_job()

        self.assertEquals(job, expected_job)
        self.assertEquals(instance, expected_instance)

    # Integration test.
    # Tests that the 'run job' command will correctly return an error when
    # the PDF parser returns an error due to the input file not existing.
    # TODO once the PDF parser has been integrated with the job scheduler
    # the error codes will change for legal / illegal.
    def test_error_command_runjob_pdfparser_1(self):
        js = Components.get_job_scheduler()

        expected_job = AsyncJob.objects.create(
            priority=1
        )
        expected_instance = ProcessingJob.objects.create(
            job_base=expected_job,
            file_name="1.pdf"
        )

        job, instance = js.get_next_job()

        Command_JS().perform_next_job()
        # If we reach this point, the test passes. perform_next_job()
        # could have thrown an exception.
        
    # Integration test.
    # Tests that the 'runjob' command will correctly return an error when
    # the file deletion system returns an error due to the input file not
    # existing.
    # TODO once the PDF parser has been integrated with the job scheduler,
    # the error codes will change for legal / illegal.
    def test_error_command_runjob_fsm_1(self):
        js = Components.get_job_scheduler()
        fsm = Components.get_file_manager()

        #fsm.add_file()

        expected_job = AsyncJob.objects.create(
            priority=1
        )

        expected_instance = FileDeletionJob.objects.create(
            job_base=expected_job,
            file_name="1.pdf"
        )

        Command_JS().perform_next_job()
        # If we reach this point, the test passes. perform_next_job()
        # could have thrown an exception.

    # Integration test.
    # Tests that the 'runjob' command will correctly return an error when
    # the file deletion system returns an error due to the input file not
    # existing.
    # TODO once the PDF parser has been integrated with the job scheduler,
    # the error codes will change for legal / illegal.
    def test_error_command_runjob_fsm_1(self):
        js = Components.get_job_scheduler()
        fsm = Components.get_file_manager()

        copy_filename = finders.find('website/test/valid_pdf_document.pdf')
        test_filename = 'static/website/test/test_file_for_deletion.pdf'


        copyfile(copy_filename, test_filename)

        # Create the uploaded file.
        # TODO remove once FSM has been integrated.
        UploadedFile.objects.create(
            file=test_filename,
            filename=1,
            type=UploadedFile.FILE_TYPES[0][0],
            document_category="generic",
            uploader=User.objects.get(username="privileged")
        )

        # Add it to the file system manager.
        #fsm.add_file()

        job = AsyncJob.objects.create(
            priority=1
        )

        request = FileDeletionRequest.objects.create(
            admin = "admin",
            delete_by = FileDeletionRequest.BY_FILENAME,
            target_file = finders.find('website/test/test_file_for_deletion.pdf'),
            target_uploader = None
        )

        instance = FileDeletionJob.objects.create(
            job_base=job,
            request=request
        )

        Command_JS().perform_next_job()
        # If we reach this point, the test passes. perform_next_job()
        # could have thrown an exception.

