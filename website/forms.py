# Unix timestamp is needed for priority.
import time

from OpenWeb.components import Components

import website
import search

from website.models import (PrivilegeModification, FileDeletionRequest,
    FileRecoveryRequest, ProcessingJob, UploadedFile, AsyncJob, FileDeletionJob,
    FileRecoveryJob, DeletionRequestItem)

from django import forms
from django.forms.widgets import DateInput
from django.forms.fields import Field
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm
)
#from django.contrib.auth.views import PasswordResetConfirmView

# Email verification.
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

import logging
logger = logging.getLogger(__name__)

# This will set the is_checkbox method to the Field class,
# derived from here: https://stackoverflow.com/a/14570648
setattr(Field, 'is_checkbox', lambda self: isinstance(self.widget, forms.CheckboxInput ))

def get_unix_timestamp():
    return time.time()

# TODO Test Validity
class CustomRequiredModelForm(forms.ModelForm):
    """
    This class allows us to create form fields corresponding to models but with the
    optional overriding of the required attribute of fields. Other implementations
    would allow NULL values in the database tables due to the way Django handles
    optional fields, i.e. Django requires null=True, blank=True Django models which
    implies that optional values would be entered as NULL, even when NULL is
    inappropriate.

    Usage:
    - Extend this class and provide a Meta class as an attribute of the class itself.
    - The Meta.required field should specify what required attributes should change,
      as a dictionary of <Field_Name : String, Required_Value : Boolean>.
    """

    # Provide a default implementation of the Meta class.
    class Meta:
        # The default required override is to not change anything.
        # In actual use, required['field_name'] = True would allow overriding
        # field_name's required value to be True instead of what it originally was.
        required = {}
        disabled = {}
        
    # Changes the required attribute of the field according to the is_required parameter.
    # If is_required is True, the field will be marked as required.
    # If is_required is False, the field will be marked as not required.
    # This is called for each field and can be overridden to provide custom behaviours.
    # TODO write tests for this.
    def set_field_required(self, field, is_required):
        # Override the parent's fields to set the field as either required or not.
        self.fields[field].required = is_required

    def set_field_disabled(self, field, is_disabled):
        # Override the parent's fields to set the field as either disabled or not.
        self.fields[field].disabled = is_disabled

    # Gets the fields that are required.
    # Returns a dictionary mapping of <Field Name, Is Required>.
    # This method is provided for extensibility - i.e. overloading possibility.
    # TODO write tests for this.
    def _check_meta(self, field):

        # Default value in case there is no supported configuration.
        req = {}
        # Check if the object has a Meta child class.
        if hasattr(self, 'Meta'):
            # Check if the Meta child class has the specified field.
            if hasattr(self.Meta, field):
                # Looks like we have a supported configuration, so get the fields from
                # it as required.
                req = getattr(self.Meta, field)

        return req

    def get_fields_required(self):
        return self._check_meta('required')

    def get_fields_disabled(self):
        return self._check_meta('disabled')

    # Initializes all of the required attributes of fields created within this form
    # according to the Meta that is defined for the object.
    # If no Meta is found or the Meta has no required field, this method does nothing.
    # TODO write tests for this.
    def set_fields_required(self, required_obj=None):
        # Initialize the required_obj if necessary.
        if required_obj is None:
            required_obj = self.get_fields_required()

        # Iterate across all of the required fields and set them as required or
        # not required depending on required_obj[Field_Name].
        for field in required_obj:
            self.set_field_required(field, required_obj[field])

    def set_fields_disabled(self, disabled_obj=None):
        # Initialize the disabled_obj if necessary.
        if disabled_obj is None:
            disabled_obj = self.get_fields_disabled()

        # Iterate across all of the required fields and set them as disabled or not
        # depending on disabled_obj[Field_Name].
        for field in disabled_obj:
            self.set_field_disabled(field, disabled_obj[field])

    def __init__(self, *args, **kwargs):
        # Use the default behaviours, but provide the added functionality.
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.set_fields_required()
        self.set_fields_disabled()

class UploadForm(forms.ModelForm):
    class Meta:
        model = website.models.UploadedFile
        fields = [ "file", "type", "document_category" ]

        labels = {
            "document_category": "Category"
        }

        help_texts = {
            "file": "Supported file types: PDF"
        }

    # TODO Implement more sophisticated algorithm to determine filename
    # if time permits.
    def determine_filename(self, model):
        """
        Determines the internal filename for the uploaded document.

        This function should be used only if the PDF Minute Parser can
        accurately determine the filename accurately and efficiently enough.
        Until such time, this function should not be used.

        It was determined that for starters we should just use an automatically
        incrementing integer for safety of misclassification and also time
        constraints. This is provided by the model's id field. At a later time,
        the filename can be determined using more sophisticated algorithms.
        """
        return model.id

    def process_file(self, user):
        """
        Processes a file based on the valid form contents.

        This function will save the file using Django's built-in form save
        functionality, and then create a job to process it.
        """
        # Save the file. Django will take care of the uploads.
        uploaded_file = self.save_file(user)

        # Register the job to process this file.
        job = self.create_job(uploaded_file.file)

        return (uploaded_file, job)


    def save_file(self, user):
        """
        Saves the file uploaded according to the form data provided.

        This file simply delegates the responsibility to the file manager.
        The file manager requires the filename, which will be generated using
        an auto-incremented integer.
        """
        model = None

        if (user is not None):
            perms = user.get_all_permissions()
            if not (user.has_perm("website.upload")):
                raise ValueError("Provided user does not have permission to upload.")

            # Save the model for future reference.
            # This is necessary to generate the id for the file, but may also be
            # important to keep for documenting purposes (e.g. knowing who uploaded).
            self.instance.uploader = user
            # Use the auto-incrementing ID provided by the model.
            model = self.save()

            fs_manager = Components.get_file_manager()
            if not fs_manager.file_exists(model.filename):
                # Delegate the file-saving to the file manager.
                # This is important to provide a layer of abstraction between the
                # file system and the app.
                fs_manager.add_file(model.filename, self.cleaned_data['file'])
        return model

    def create_job(self, file_name):
        """
        Creates a job for the uploaded document to be processed.
        Uses the data contained within the form to populate the job.
        """
        job_base = AsyncJob.objects.create(
            priority=get_unix_timestamp()
        )
        job = ProcessingJob.objects.create(
            job_base=job_base,
            file_name=file_name
        )

        return job_base

    """
    def clean(self):
        errors = 0
        cleaned_data = self.cleaned_data

        document_category = cleaned_data['document_category']

        if (document_category == ""):
            msg = ('Document category cannot be empty.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1

        return cleaned_data
    """


class LoginForm(forms.Form):
    # Fields

    # TODO This should be updated to comply with security requirements.
    # This should become a separate task, as it requires further research.
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def authenticate_user(self, request):
        user = authenticate(username=self.cleaned_data['username'],
            password=self.cleaned_data['password'])

        if user is not None:
            # User is authenticated, log them in.
            login(request, user)

        # Allow the caller to determine the user's permissions.
        return user
    
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        errors = 0

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                msg = ('Username and password do not match.')
                ex = forms.ValidationError(msg, code='authentication-error')
                self.add_error(None, ex)
                errors += 1

        return cleaned_data

class AccountPasswordResetConfirmForm(SetPasswordForm):
    """
    Represents the reset confirmation form - the form that lets the user
    select a password after they have clicked the confirmation link.
    """
    pass

class AccountPasswordResetForm(PasswordResetForm):
    """
    Represents the password reset form.

    This class is provided for extensibility.
    """
    pass

class AccountPasswordChangeForm(PasswordChangeForm):
    """
    Represents the password change form.

    This class is provided for extensibility.
    """
    pass

class AccountCreationForm(UserCreationForm):
    """
    Represents the account creation form.
    """
    class Meta:
        # Fields
        model = get_user_model()
        fields = [ "username", "password1", "password2", "email" ]

    def get_verification_email(self, subject, message, recipients):
        return EmailMessage(subject, message, to=recipients)

    def get_verification_email_message(self, data):
        return render_to_string(self.get_verification_email_template(), data)

    def get_verification_email_recipients(self):
        return [ self.cleaned_data.get('email') ]

    def get_verification_email_subject(self):
        return "Welcome to OpenWeb"
    
    def get_verification_email_data(self, request):
        return {
            'user': request.user
        }

    def get_verification_email_data(self, user, request):
        return {
            'user': user,
            'domain': get_current_site(request),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }

    # Sends email verification to the user at the email specified.
    def send_email_verification(self, user, request):
        user = self.get_user_from_form()

        # Get the data from the user & request.
        message_data = self.get_verification_email_data(user, request)

        # Get the message given the previously obtained message data.
        message = self.get_verification_email_message(message_data)

        # Get the recipient email based on the form data.
        recipients = self.get_verification_email_recipients()

        # Finally, create the email and send it.
        email = self.get_verification_email(subject, message, recipients)

        email.send()

    def create_user_from_form(self):
        User = get_user_model()
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email']
        )
        user.save()

        return user

    # Create a user from the user's request.
    def create_user(self, request):
        # Create the user.
        user = self.create_user_from_form()

        # Check if the user was actually valid.
        if user is not None:
            login(request, user)

        # Send the email verification.
        self.send_email_verification(user, request)

        # Allow the caller to determine the user's permissions.
        return user

# TODO Test Validity
class SearchForm(CustomRequiredModelForm):

    class Meta:
        model = website.models.Search
        fields = [ "search_by","search_t", "fbm", "fbm_filename", "fbm_uploader",
            "fbm_upload_date_start", "fbm_upload_date_end", "fbc", "fbc_council",
            "fbc_publish_date_start", "fbc_publish_date_end",
            "key_phrase1", "key_phrase_type1", "key_phrase_importance1",
            "key_phrase2", "key_phrase_type2", "key_phrase_importance2",
            "key_phrase3", "key_phrase_type3", "key_phrase_importance3",
            "key_phrase4", "key_phrase_type4", "key_phrase_importance4",
            "key_phrase5", "key_phrase_type5", "key_phrase_importance5"
        ]

        labels = {
            'search_by': "Search by",
            'search_t': "Search type",
            "fbm": "Filter by document",
            "fbc": "Filter by contents",
            "fbc_council": "Council",
            "fbc_publish_date_start": "Published",
            "fbc_publish_date_end": "until",
            "fbm_filename": "Filename",
            "fbm_uploader": "Uploaded by",
            "fbm_upload_date_start": "Uploaded",
            "fbm_upload_date_end": "until",
            "key_phrase1": "Search Term",
            "key_phrase2": "Search Term",
            "key_phrase3": "Search Term",
            "key_phrase4": "Search Term",
            "key_phrase5": "Search Term",
            "key_phrase_type1": "Type",
            "key_phrase_type2": "Type",
            "key_phrase_type3": "Type",
            "key_phrase_type4": "Type",
            "key_phrase_type5": "Type",
            "key_phrase_importance1": "Importance",
            "key_phrase_importance2": "Importance",
            "key_phrase_importance3": "Importance",
            "key_phrase_importance4": "Importance",
            "key_phrase_importance5": "Importance",
        }
        required = {
            'search_t': False,
            'fbm_filename': False,
            'fbm_uploader': False,
            'fbc_council': False,
            'key_phrase1': False,
            'key_phrase2': False,
            'key_phrase3': False,
            'key_phrase4': False,
            'key_phrase5': False,
            'key_phrase_type1': False,
            'key_phrase_type2': False,
            'key_phrase_type3': False,
            'key_phrase_type4': False,
            'key_phrase_type5': False,
            'key_phrase_importance1': False,
            'key_phrase_importance2': False,
            'key_phrase_importance3': False,
            'key_phrase_importance4': False,
            'key_phrase_importance5': False,
            'fbc_publish_date_start': False,
            'fbc_publish_date_end': False,
            'fbm_upload_date_start': False,
            'fbm_upload_date_end': False
        }
        widgets = {
            'search_by': forms.RadioSelect,
            'search_t': forms.RadioSelect,
            'fbm_upload_date_start': DateInput(
                attrs={'type': 'date'}
            ),
            'fbm_upload_date_end': DateInput(
                attrs={'type': 'date'}
            ),
            "fbc_publish_date_start": DateInput(
                attrs={'type': 'date'}
            ),
            "fbc_publish_date_end": DateInput(
                attrs={'type': 'date'}
            )
        }
        
    def clean(self):
        # Validate inter-dependent fields.
        cleaned_data = super(SearchForm, self).clean()
        errors = 0

        fbm = cleaned_data.get('fbm')
        fbm_uploader = cleaned_data.get('fbm_uploader')
        fbm_filename = cleaned_data.get('fbm_filename')
        fbm_upload_date_start = cleaned_data.get('fbm_upload_date_start')
        fbm_upload_date_end = cleaned_data.get('fbm_upload_date_end')

        fbc = cleaned_data.get('fbc')
        fbc_publish_date_start = cleaned_data.get('fbc_publish_date_start')
        fbc_publish_date_end = cleaned_data.get('fbc_publish_date_end')
        fbc_council = cleaned_data.get('fbc_council')

        key_phrase1 = cleaned_data.get('key_phrase1')
        key_phrase2 = cleaned_data.get('key_phrase2')
        key_phrase3 = cleaned_data.get('key_phrase3')
        key_phrase4 = cleaned_data.get('key_phrase4')
        key_phrase5 = cleaned_data.get('key_phrase5')

        key_phrase_type1 = cleaned_data.get('key_phrase_type1')
        key_phrase_type2 = cleaned_data.get('key_phrase_type2')
        key_phrase_type3 = cleaned_data.get('key_phrase_type3')
        key_phrase_type4 = cleaned_data.get('key_phrase_type4')
        key_phrase_type5 = cleaned_data.get('key_phrase_type5')

        key_phrase_importance1 = cleaned_data.get('key_phrase_importance1')
        key_phrase_importance2 = cleaned_data.get('key_phrase_importance2')
        key_phrase_importance3 = cleaned_data.get('key_phrase_importance3')
        key_phrase_importance4 = cleaned_data.get('key_phrase_importance4')
        key_phrase_importance5 = cleaned_data.get('key_phrase_importance5')

        if (fbc and (
            (bool(key_phrase1) != bool(key_phrase_importance1)) or
            (bool(key_phrase2) != bool(key_phrase_importance2)) or
            (bool(key_phrase3) != bool(key_phrase_importance3)) or
            (bool(key_phrase4) != bool(key_phrase_importance4)) or
            (bool(key_phrase5) != bool(key_phrase_importance5)))):
            msg = ('You must provide all key phrase information in order to search by ' +
                'key phrase.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1

        if ((not fbc) and (fbc_publish_date_start or fbc_publish_date_end)):
            msg = ('You must enable filtering by contents to support ' +
                'filtering by publish date.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1
        if ((not fbc) and (fbc_council)):
            msg = ('You must enable filtering by content to support ' +
                'filtering by council.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1
        
        if ((not fbc) and (
            (key_phrase1 or key_phrase_importance1) or
            (key_phrase2 or key_phrase_importance2) or
            (key_phrase3 or key_phrase_importance3) or
            (key_phrase4 or key_phrase_importance4) or
            (key_phrase5 or key_phrase_importance5))):
            msg = ('You must enable filtering by content to support ' +
                'filtering by key phrases.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1
        if (
            ((not key_phrase1) and key_phrase_importance1) or
            ((not key_phrase2) and key_phrase_importance2) or
            ((not key_phrase3) and key_phrase_importance3) or
            ((not key_phrase4) and key_phrase_importance4) or
            ((not key_phrase5) and key_phrase_importance5)):
            msg = ('Key phrases must have an importance value ranging from 0 to 100.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1
        
        if (fbm and not any([fbm_filename, fbm_uploader, fbm_upload_date_start,
            fbm_upload_date_end])):
            msg = ('You must specify at least one file filtering criteria to support ' +
                'filtering by document.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1
            
        if ((not fbm) and fbm_filename):
            msg = ('You must enable filtering by document to support ' +
                'filtering by file name.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1

        if ((not fbm) and fbm_uploader):
            msg = ('You must enable filtering by document to support ' +
                'filtering by uploader.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1

        if ((not fbm) and (fbm_upload_date_start or fbm_upload_date_end)):
            msg = ('You must enable filtering by document to support ' +
                'filtering by upload date.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1

        if (fbm and (bool(fbm_upload_date_start) != bool(fbm_upload_date_end))):
            msg = ('You must provide both the start and end upload date or neither ' +
                'to support filtering by upload date.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1

        if (fbc and (bool(fbc_publish_date_start) != bool(fbc_publish_date_end))):
            msg = ('You must provide both the start and end publish date or neither ' +
                'to support filtering by publish date.')
            ex = forms.ValidationError(msg, code='invalid-filtering')
            self.add_error(None, ex)
            errors += 1

        return cleaned_data

class UserPrivilegeModificationForm(CustomRequiredModelForm):
    class Meta:
        model = PrivilegeModification
        fields = [ "target_user", "target_group" ]

        widgets = {
            #"target_group": forms.RadioSelect
        }

        labels = {
            "target_user": "User",
            "target_group": "Group"
        }

    def set_user_group(self, target_user, target_group):
        # Remove all (OpenWeb-) assigned permission groups.
        # Don't remove any others, as this may limit extensibility.
        for choice_perm in PrivilegeModification.USER_CLASS_CHOICES:
            # Get the privilege internal ID.
            group_name = choice_perm[0]

            # Remove all of the relevant groups, to "replace" any with
            # the target group.
            group = self.get_group(group_name)
            target_user.groups.remove(group)

        # Add the one that the target user was designated to have.
        target_user.groups.add(target_group)

        # Save the changes to the user in the database.
        target_user.save()

    def get_group(self, group_name):
        return Group.objects.get(name=group_name)

    def get_user(self, user_name):
        # We use a custom User model, get it from Django settings.
        User = get_user_model()

        return User.objects.get(username=user_name)

    def change_permissions(self):
        error_code = 0

        # Get data from form.
        target_user = self.cleaned_data['target_user']
        target_group = self.cleaned_data['target_group']

        # Get the user & target group.
        user = self.get_user(target_user)
        group = self.get_group(target_group)

        # Assign upload permission to Privileged Users and Administrators.
        error_code = self.set_user_group(user, group)

        return error_code

    def clean(self):
        cleaned_data = super(UserPrivilegeModificationForm, self).clean()
        errors = 0

        username = cleaned_data.get("target_user")
        if username:
            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                msg = ('User does not exist.')
                ex = forms.ValidationError(msg, code='invalid-selection')
                self.add_error(None, ex)
                errors += 1

        return cleaned_data

class AdminFileDeletionForm(CustomRequiredModelForm):
    class Meta:
        model = FileDeletionRequest
        fields = [ "delete_by", "target_file", "target_uploader" ]
        widgets = {
            "delete_by": forms.RadioSelect
        }

        labels = {
            "target_uploader": "Uploader",
            "target_file": "Filename"
        }

    def process_request(self):
        inst = self.save()
        files = self.get_target_files()

        for f in files:
            self.instance.deletionrequestitem_set.create(
                request = inst,
                target_file = f
            )

        job = self.create_job(inst)

        return job

    def get_target_files(self):
        delete_by = self.cleaned_data["delete_by"]
        files = []

        if (delete_by == FileDeletionRequest.BY_USERNAME):
            uploader = self.cleaned_data["target_uploader"]
            files = UploadedFile.objects.filter(uploader__username=uploader)
        elif (delete_by == FileDeletionRequest.BY_FILENAME):
            filename = self.cleaned_data["target_file"]
            files = UploadedFile.objects.filter(filename=filename)
        return files

    def create_job(self, del_request):
        utime = get_unix_timestamp()
        job_base = AsyncJob.objects.create(
            priority = utime + FileDeletionJob.MIN_LENGTH
        )

        return FileDeletionJob.objects.create(
            job_base=job_base,
            request=del_request,
            scheduled_time=utime
        )

    def clean(self):
        cleaned_data = super(AdminFileDeletionForm, self).clean()
        errors = 0

        delete_by = cleaned_data.get('delete_by')
        target_uploader = cleaned_data.get('target_uploader')
        target_file = cleaned_data.get('target_file')

        if ((delete_by == 0) and (target_file is None)):
            msg = ('No filename was specified for deletion.')
            ex = forms.ValidationError(msg, code='invalid-deletion')
            self.add_error(None, ex)
            errors += 1

        if ((delete_by == 1) and (target_uploader is None)):
            msg = ('No uploader name was specified for deletion.')
            ex = forms.ValidationError(msg, code='invalid-deletion')
            self.add_error(None, ex)
            errors += 1

        if ((delete_by == 0) and (target_uploader is not None)):
            msg = ('Uploader field is not relevant to deleting by filename.')
            ex = forms.ValidationError(msg, code='invalid-deletion')
            self.add_error(None, ex)
            errors += 1

        if ((delete_by == 1) and (target_file is not None)):
            msg = ('Filename field is not relevant to deleting by uploader.')
            ex = forms.ValidationError(msg, code='invalid-deletion')
            self.add_error(None, ex)
            errors += 1

        return cleaned_data

class AdminFileRecoveryForm(CustomRequiredModelForm):
    class Meta:
        model = FileRecoveryRequest
        fields = [ "recover_by", "target_file", "target_uploader" ]
        widgets = {
            'recover_by': forms.RadioSelect
        }
        labels = {
            'target_uploader': 'Uploader',
            'target_file': 'Filename'
        }

    def process_request(self):
        inst = self.save()
        files = self.get_target_files()

        for f in files:
            self.instance.recoveryrequestitem_set.create(
                request=inst,
                target_file=f
            )

        base, job = self.create_job(inst)
        status = job.perform_job()
        if (status == 0):
            base.status = AsyncJob.STATUS_FINISHED
            base.save()

        return job

    def get_target_files(self):
        recover_by = self.cleaned_data["recover_by"]
        files = []

        if (recover_by == FileDeletionRequest.BY_USERNAME):
            uploader = self.cleaned_data["target_uploader"]
            files = UploadedFile.objects.filter(uploader__username=uploader)
        elif (recover_by == FileDeletionRequest.BY_FILENAME):
            filename = self.cleaned_data["target_file"]
            files = UploadedFile.objects.filter(filename=filename)
        return files

    def create_job(self, rec_request):
        # This job will be performed immediately, so just give it any priority.
        job_base = AsyncJob.objects.create(
            priority = 0
        )

        job_inst = FileRecoveryJob.objects.create(
            job_base=job_base,
            request=rec_request
        )

        return (job_base, job_inst)

    def clean(self):
        cleaned_data = super(AdminFileRecoveryForm, self).clean()
        errors = 0

        recover_by = cleaned_data.get('recover_by')
        target_uploader = cleaned_data.get('target_uploader')
        target_file = cleaned_data.get('target_file')

        if ((recover_by == 0) and (target_file is None)):
            msg = ('No filename was specified for recovery.')
            ex = forms.ValidationError(msg, code='invalid-recovery')
            self.add_error(None, ex)

        if ((recover_by == 1) and (target_uploader is None)):
            msg = ('No uploader name was specified for recovery.')
            ex = forms.ValidationError(msg, code='invalid-recovery')
            self.add_error(None, ex)
            errors += 1

        if ((recover_by == 0) and (target_uploader is not None)):
            msg = ('Uploader field is not relevant to recovering by filename.')
            ex = forms.ValidationError(msg, code='invalid-recovery')
            self.add_error(None, ex)
            errors += 1

        if ((recover_by == 1) and (target_file is not None)):
            msg = ('Filename field is not relevant to recovering by uploader.')
            ex = forms.ValidationError(msg, code='invalid-recovery')
            self.add_error(None, ex)
            errors += 1

        return cleaned_data

