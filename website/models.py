import os
import time

from django.db import models

from django.contrib.auth.models import AbstractUser

from OpenWeb.components import Components

# Notes for future maintainers.
# Django best practice is to prefer non-null CharFields, see:
#   https://docs.djangoproject.com/en/2.2/ref/models/fields/#null

# Create your models here.

# This is based on the following reference:
# https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#extending-the-existing-user-model
# Creating a custom user model allows us to extend it in the future.
UPLOADS_DIR="uploads/"
class User(AbstractUser):
    class Meta:
        pass

class UploadedFile(models.Model):
    FILE_TYPES = [
        (0, 'Public minutes document.'),
        (1, 'Public non-minutes document.'),
        (2, 'Private non-minutes document.')
    ]

    file = models.FileField(
        upload_to=UPLOADS_DIR
    )

    filename = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=False
    )

    type = models.IntegerField(
        choices=FILE_TYPES,
        default=0
    )

    document_category = models.CharField(
        max_length=128,
        default="generic",
        blank=False,
        null=False
    )

    uploader = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    @property
    def type_desc(self):
        return self.FILE_TYPES[self.type][1]

    def save(self, *args, **kwargs):
        super(UploadedFile, self).save(*args, **kwargs)

        # We canonly set the filename after we save, because the database
        # needs to calculate its ID. Set the filename and save again.
        self.filename = str(self.id)
        super(UploadedFile, self).save()

        return self

    def delete(self):
        status = 0
        try:
            os.remove(self.file.name)
            super(UploadedFile, self).delete()
        except IOError:
            status = 1

        return status


# Processing Jobs
class AsyncJob(models.Model):
    priority = models.IntegerField(null=False)

    STATUS_UNPROCESSED = 0
    STATUS_FINISHED = 1
    STATUS_ERROR = 2
    STATUS_UNSUPPORTED = 3
    STATUSES = (
        (STATUS_UNPROCESSED, 'Unprocessed'),
        (STATUS_FINISHED, 'Finished'),
        (STATUS_ERROR, 'Error'),
        (STATUS_UNSUPPORTED, 'Unsupported')
    )
    status = models.IntegerField(choices=STATUSES, default=0)

    def get_instance(self):
        obj = None
        if ProcessingJob.objects.filter(job_base=self).exists():
            obj = ProcessingJob.objects.get(job_base=self)

        elif FileDeletionJob.objects.filter(job_base=self).exists():
            obj = FileDeletionJob.objects.get(job_base=self)

        return obj

class AsyncJobType(models.Model):
    job_base = models.OneToOneField(
        AsyncJob,
        on_delete=models.CASCADE,
        primary_key=True)

    def get_job_base(self):
        return AsyncJob.objects.get(pk=self.job_base)

class ProcessingJob(AsyncJobType):
    file_name = models.CharField(
        max_length=128
    )

    def perform_job(self):
        pdfparser = Components.get_pdf_parser()

        status = pdfparser.parse(self.file_name)

        # Resolve the status to one of AsyncJob's.
        if (status == 0):
            status = AsyncJob.STATUS_FINISHED
        elif (status == 1):
            status = AsyncJob.STATUS_UNSUPPORTED
        elif (status == 2):
            status = AsyncJob.STATUS_ERROR

        return status

    def get_status_fields(self):
        return {
            'filename': self.file_name
        }

# Searches
class DocumentResult(models.Model):
    document = models.CharField(max_length=128)
    occurs_total = models.IntegerField(default=0)
    occurs_agenda_items = models.IntegerField(default=0)
    normalised_score = models.IntegerField(default=0)

class File(models.Model):
    filename = models.CharField(
        max_length=128
    )
    class Meta:
        permissions = [
            ("upload", "Can upload documents using the PDF upload service."),
            ("delete", "Can delete documents using the file deletion service."),
            ("recover", "Can recover deleted documents using the file recovery service."),
        ]

class RelationResult(models.Model):
    kp1 = models.CharField(max_length=128)
    kp2 = models.CharField(max_length=128)
    kp3 = models.CharField(max_length=128)
    kp4 = models.CharField(max_length=128)
    kp5 = models.CharField(max_length=128)
    document = models.CharField(
        max_length=128,
        blank=True,
        default=""
    )
    agenda_item_file = models.CharField(
        max_length=128,
        blank=True,
        default=""
    )
    agenda_item = models.CharField(
        max_length=128,
        blank=True,
        default=""
    )
    description = models.CharField(
        max_length=128,
        blank=True,
        default=""
    )
    search_type = models.IntegerField()

class Search(models.Model):
    class Meta:
        permissions = [
            ("search", "Can search using the document search feature.")
        ]

    SEARCH_BY_CHOICES = [
        (0, 'Search by relation'),
        (1, 'Search by document')
    ]
    SEARCH_TYPE_CHOICES = [
        (0, 'Search minutes'),
        (1, 'Search non-minutes')
    ]
    # For this field we are assuming a default value of 0.
    # If we didn't, because of the way ModelForms work, the form would try to insert
    # a new (blank) option with the description "------". Since one of these is
    # required and Django does not seem to recognise that blank=False, null=False
    # implies that this field is required to be 0 or 1, we work around Django's
    # limitation by assuming the default is 0.
    search_by = models.IntegerField(
        choices=SEARCH_BY_CHOICES,
        default=0,
        blank=False,
        null=False
    )
    search_t = models.IntegerField(
        choices=SEARCH_TYPE_CHOICES,
        default=0,
        blank=False,
        null=False
    )
    fbm = models.BooleanField(
        default=False
    )
    fbm_filename = models.CharField(
        max_length=128,
        blank=True,
        default=""
    )
    fbm_uploader = models.CharField(
        max_length=128,
        blank=True,
        default=""
    )
    fbm_upload_date_start = models.DateField(
        null=True
    )
    fbm_upload_date_end = models.DateField(
        null=True
    )

    # Checkbox to filter by contents of the minutes documents.
    fbc = models.BooleanField(
        default=False
    )
    fbc_council = models.CharField(
        max_length=128,
        blank=True,
        default=""
    )

    fbc_publish_date_start = models.DateField(
        null=True
    )
    fbc_publish_date_end = models.DateField(
        null=True
    )

    KEY_PHRASE_TYPES = [
        (0, 'Any keyword type'),
        (1, 'Councillor name'),
        (2, 'Person name'),
        (3, 'Business name'),
        (4, 'Property address')
    ]

    # Searched terms.
    key_phrase1 = models.CharField(max_length=128, blank=True,
        default="")
    key_phrase2 = models.CharField(max_length=128, blank=True,
        default="")
    key_phrase3 = models.CharField(max_length=128, blank=True,
        default="")
    key_phrase4 = models.CharField(max_length=128, blank=True,
        default="")
    key_phrase5 = models.CharField(max_length=128, blank=True,
        default="")

    key_phrase_type1 = models.IntegerField(choices=KEY_PHRASE_TYPES,
        default=0, null=True)
    key_phrase_type2 = models.IntegerField(choices=KEY_PHRASE_TYPES,
        default=0, null=True)
    key_phrase_type3 = models.IntegerField(choices=KEY_PHRASE_TYPES,
        default=0, null=True)
    key_phrase_type4 = models.IntegerField(choices=KEY_PHRASE_TYPES,
        default=0, null=True)
    key_phrase_type5 = models.IntegerField(choices=KEY_PHRASE_TYPES,
        default=0, null=True)

    # There does not seem to be any relevant options to limit
    # the values of DecimalField to a range [0, 100]
    # TODO Check if this is valid - does three digits allow only 0.00 to 1.00?
    key_phrase_importance1 = models.DecimalField(decimal_places=2,
        max_digits=3, null=True)
    key_phrase_importance2 = models.DecimalField(decimal_places=2,
        max_digits=3, null=True)
    key_phrase_importance3 = models.DecimalField(decimal_places=2,
        max_digits=3, null=True)
    key_phrase_importance4 = models.DecimalField(decimal_places=2,
        max_digits=3, null=True)
    key_phrase_importance5 = models.DecimalField(decimal_places=2,
        max_digits=3, null=True)

    def get_queryset(self, stype):
        print("Hello")
        print("SType: %s" % (stype,))
        return self.queryset_result_map[stype]



# This seems to be the best choice - store these separately.
# Then we theoretically don't need to have a limit to the form fields.
# But the front-end needs to handle this flexibility.
# Only other option seems to be to hard-code a large number of fields
# (e.g. 10x3 fields for 10 key phrases)
class KeyPhraseOptionSet(models.Model):
    # A single search term has three components.
    # Phrase
    key_phrase = models.CharField(
        max_length=128,
        blank=True,
        default=""
    )

    KEY_PHRASE_TYPES = [
        (0, 'Any keyword type'),
        (1, 'Councillor name'),
        (2, 'Person name'),
        (3, 'Business name'),
        (4, 'Property address')
    ]

    key_phrase_type = models.IntegerField(
        choices=KEY_PHRASE_TYPES,
        default=0,
        null=True
    )

    # TODO
    # There does not seem to be any relevant options to limit
    # the values of DecimalField to a range [0, 100]
    # TODO Check if this is valid - does three digits allow only 0.00 to 1.00?
    key_phrase_importance = models.DecimalField(
        decimal_places=2,
        max_digits=3,
        null=True
    )

# A class to register privilege modifications.
class PrivilegeModification(models.Model):
    # Which user enacted this modification.
    # This needs to be a reference to the admin, i.e. a FK to a (Custom) User.
    admin = models.CharField(max_length=128)

    # Which user's privileges are being modified.
    # This needs to be a reference to the user, i.e. a FK to a (Custom) User.
    #target_user = models.
    target_user = models.CharField(max_length=128)

    USER_CLASS_CHOICES = [
        ('regular user', 'Regular user'),
        ('privileged user', 'Privileged user'),
        ('administrator', 'Administrator')
    ]

    # Which user class to give to the target user.
    target_group = models.CharField(
        max_length=32,
        choices=USER_CLASS_CHOICES,
        default=0,
        null=False,
        blank=False
    )

class FileDeletionRequest(models.Model):
    """
    FileDeletionRequest - a request for deletion. This exists to store a record of
    past deletions in the database. It is used by the website to create a ModelForm
    using this model as a base.
    """
    # Which user enacted this deletion request.
    admin = models.CharField(max_length=128)
    BY_FILENAME=0
    BY_USERNAME=1

    DELETION_FILTER_TYPES = [
        (BY_FILENAME, 'Delete files by filename.'),
        (BY_USERNAME, 'Delete files by uploader.')
    ]

    delete_by = models.IntegerField(choices=DELETION_FILTER_TYPES, default=BY_FILENAME)

    target_file = models.CharField(max_length=128, null=True, blank=True)
    target_uploader = models.CharField(max_length=128, null=True, blank=True)

class FileRecoveryRequest(models.Model):
    """
    FileRecoveryRequest - a request for recovery. This exists to store a record of
    past recoveries in the database. It is used by the website to create a ModelForm
    using this model as a base.
    """
    # Which user enacted this recovery request.
    admin = models.CharField(max_length=128)
    BY_FILENAME=0
    BY_USERNAME=1

    RECOVERY_FILTER_TYPES = [
        (BY_FILENAME, 'Recover files by filename.'),
        (BY_USERNAME, 'Recover files by uploader.')
    ]

    recover_by = models.IntegerField(choices=RECOVERY_FILTER_TYPES, default=BY_FILENAME)
    target_file = models.CharField(max_length=128, null=True, blank=True)

    target_uploader = models.CharField(max_length=128, null=True, blank=True)

class DeletionRequestItem(models.Model):
    request = models.ForeignKey(
        FileDeletionRequest,
        on_delete=models.CASCADE
    )
    
    target_file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE
    )

class RecoveryRequestItem(models.Model):
    request = models.ForeignKey(
        FileRecoveryRequest,
        on_delete=models.CASCADE
    )
    
    target_file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE
    )

class FileDeletionJob(AsyncJobType):
    # Minimum length to wait is 30 days.
    # This duration is in seconds.
    MIN_LENGTH = 60 * 60 * 24 * 30

    request = models.ForeignKey(
        FileDeletionRequest,
        on_delete=models.CASCADE
    )
    scheduled_time = models.FloatField()

    def get_files(self):
        files = []
        for req in DeletionRequestItem.objects.filter(request=self.request):
            files.append(req.target_file)
        return files

    def can_perform_job(self):
        return (time.time() - self.scheduled_time) > self.MIN_LENGTH

    def perform_job(self):
        # Don't change from UNPROCESSED if we cannot perform the job.
        status = AsyncJob.STATUS_UNPROCESSED

        if (self.can_perform_job()):
            # Assume it finishes, and check + correct if it doesn't.
            status = AsyncJob.STATUS_FINISHED

            files = self.get_files()

            for uploaded_file in files:
                ufile_collection = UploadedFile.objects.filter(pk=f_entry.target_file)
                if (ufile_collection.exists()):
                    for ufile in ufile_collection:
                        if (ufile.delete()):
                            # Deletion returned an error code.
                            # Set the status to error so that we can move on.
                            # Otherwise this job will be repeated infinitely.
                            status = AsyncJob.STATUS_ERROR
                        # We don't want to throw an error if it doesn't exist, because
                        # that is an indication that our state is fine - maybe some other
                        # deletion request deleted it. Either way - it's gone.
                        if (os.path.exists(ufile.file)):
                            # Delete from file system.
                            os.remove(ufile.file)
                            # Delete from database.
                            ufile.delete()
        return status

    def get_status_fields(self):
        return {
            'files': self.get_files(),
        }

class FileRecoveryJob(AsyncJobType):
    request = models.ForeignKey(
        FileRecoveryRequest,
        on_delete=models.CASCADE
    )

    def get_files(self):
        files = []
        for req in RecoveryRequestItem.objects.filter(request=self.request):
            files.append(req.target_file)
        return files

    def perform_job(self):
        status = 0
        files = self.get_files()
        for f in files:
            # Get any deletion requests referencing this file.
            request = DeletionRequestItem.objects.filter(target_file=f)
            request.delete()

        return status

    def get_status_fields(self):
        return {
            'files': self.get_files()
        }

