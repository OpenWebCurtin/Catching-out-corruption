from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from website.forms import UploadForm
from website.models import (UploadedFile, AsyncJob, ProcessingJob)

from django.contrib.staticfiles import finders
from django.contrib.auth import get_user_model

import logging, sys, unittest

from django.core import management

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

# These variables are needed by TestUploadForm,
# but cannot be defined in it.
VALID_FILE_STREAM = open(finders.find('website/test/valid_pdf_document.pdf'), "rb")
VALID_FILE = SimpleUploadedFile(VALID_FILE_STREAM.name, VALID_FILE_STREAM.read())

User = get_user_model()

VALID_TYPE = UploadedFile.FILE_TYPES[0][0]
VALID_DOCUMENT_CATEGORY = "City of Perth Ordinary Council Meeting Minutes"

class TestUploadForm(TestCase):
    """ Testing suite for website.forms.UploadForm """

    def setUp(self):
        management.call_command("initperms")
        management.call_command("initusers")

        # These two class-fields must be obtained only after the permissions have been
        # set up. Otherwise the users do not exist or do not have the permissions
        # that are required for website functionality.
        self.VALID_UPLOADER = User.objects.get(username="privileged")
        self.INVALID_UPLOADER = User.objects.get(username="regular")
    # 
    def create_upload_form(self, in_type=VALID_TYPE,
        in_document_category=VALID_DOCUMENT_CATEGORY,
        in_file=VALID_FILE):
        """ Creates a default upload form with a set of default (valid) values. """

        return UploadForm({
            'type': in_type,
            'document_category': in_document_category,
        }, {
            'file': in_file
        })
    
    # Test is_valid for the default form produced by create_upload_form.
    # If this test fails then most other tests are likely to fail,
    # so test this separately.
    def test_create_upload_form(self):
        upload_form = self.create_upload_form()

        self.assertTrue(upload_form.is_valid())

    ##################################
    #  Test Single-Field validation  #
    ##################################

    # Test is_valid for invalid input:
    #   file = Invalid file.
    #   type = Valid type.
    #   document_category = Valid category.
    def test_invalid_form_1(self):
        upload_form = self.create_upload_form(
            in_file = None
        )

        self.assertFalse(upload_form.is_valid())

    # Test is_valid for invalid input:
    #   file = Valid file.
    #   type = Invalid type (Null).
    def test_invalid_form_2(self):
        upload_form = self.create_upload_form(
            in_type = None
        )

        self.assertFalse(upload_form.is_valid())

    # Test is_valid for invalid input:
    #   file = Valid file.
    #   type = Invalid type (Not null).
    def test_invalid_form_3(self):
        upload_form = self.create_upload_form()
        upload_form.type = "invalid-document-type"

        self.assertFalse(upload_form.is_valid())

    # Test is_valid for invalid input:
    #   file = Valid file.
    #   type = valid type.
    #   document_category = Invalid category (Null).
    def test_invalid_form_3(self):
        upload_form = self.create_upload_form()
        upload_form = self.create_upload_form(
            in_document_category = None
        )

        self.assertFalse(upload_form.is_valid())

    # Test is_valid for invalid input:
    #   file = Valid file.
    #   type = Valid type.
    #   document_category = Invalid category (Not null).
    def test_invalid_form_3(self):
        upload_form = self.create_upload_form(
            in_document_category = ""
        )

        self.assertFalse(upload_form.is_valid())

    # Test save_file for valid input:
    #   file = Valid file.
    #   type = Valid type.
    #   document_category = Valid document category.
    #   uploader = Valid uploader.
    def test_valid_save_form(self):
        # TODO For some reason Django's testing environment does not recognise
        # that privileged users have the permission to upload documents.
        # Doesn't seem to be an issue with the upload system.
        # Need to figure this out.
        upload_form = self.create_upload_form()

        uploaded_file = upload_form.save_file(self.VALID_UPLOADER)

        self.assertIsNotNone(uploaded_file)

        result_entry = UploadedFile.objects.get(pk=uploaded_file.id)

        self.assertEqual(uploaded_file, result_entry)

    # Test save_file for invalid input:
    #   file = Valid file.
    #   type = Valid type.
    #   document_category = Valid document category.
    #   uploader = Invalid uploader (Null).
    def test_invalid_save_form_1(self):
        upload_form = self.create_upload_form()
        uploaded_file = upload_form.save_file(None)

        self.assertIsNone(uploaded_file)

    # Test save_file for invalid input:
    #   file = Valid file.
    #   type = Valid type.
    #   document_category = Valid document category.
    #   uploader = Invalid uploader (Not null).
    def test_invalid_save_form_2(self):
        upload_form = self.create_upload_form()
        uploaded_file = None
        with self.assertRaises(ValueError):
            uploaded_file = upload_form.save_file(self.INVALID_UPLOADER)

        self.assertIsNone(uploaded_file)

    # Test process_file for valid input.
    # Ensure that the method saves the file and creates the job.
    def test_process_file_1(self):
        upload_form = self.create_upload_form()
        user = User.objects.get(username="privileged")

        uploaded_file, job = upload_form.process_file(user)

        # Test that the file and job exist.
        self.assertIsNotNone(uploaded_file)
        self.assertIsNotNone(job)

        specific_job = ProcessingJob.objects.get(job_base__id=job.id)

        # Test that the file and job were registered.
        expected_file = UploadedFile.objects.get(id=uploaded_file.id)
        expected_job = AsyncJob.objects.get(id=job.id)

        self.assertEqual(uploaded_file, expected_file)
        self.assertEqual(job, expected_job)
        self.assertEqual(specific_job.job_base, expected_job)
