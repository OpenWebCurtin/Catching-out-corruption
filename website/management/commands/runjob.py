from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from OpenWeb.components import Components

from website.models import AsyncJob

class Command(BaseCommand):
    # Runs a job given a job and its more specific job instance.
    def run_job(self, job, instance):
        if instance is not None:
            # If we got an instance, perform the job.
            error_code = instance.perform_job()

            # Save the job either way with the new error code as its status.
            job.status = error_code
            job.save()

        else:
            raise ValueError("No job to perform.")

    # Gets the next job scheduled.
    def get_job(self):
        js = Components.get_job_scheduler()
        job, instance = js.get_next_job()

        return (job, instance)

    # Performs the next job scheduled.
    # This is separated from handle() in order to aid in testing.
    def perform_next_job(self):
        job, instance = self.get_job()
        self.run_job(job, instance)

        return (job, instance)

    # performs the next job and checks for errors.
    # This method is called when running from the command-line, or using
    # Django's call_command method.
    def handle(self, *args, **options):
        try:
            job, instance = self.perform_next_job()
            print("Job " + str(instance.asyncjobtype_ptr_id) + " status = " + str(job.status))
        except RuntimeError as e:
            print("Job not started: " + str(e))
        except ValueError as e:
            print("Job not started: " + str(e))
        except Exception as e:
            print("Internal error: " + str(e))

