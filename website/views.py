from django.template.defaulttags import register
from database.search import search
import website
from OpenWeb.components import Components

from django.contrib import messages
from django.contrib.auth import logout
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import (render, redirect)
from django.views.generic import (RedirectView, TemplateView, ListView, DetailView)
from django.views.generic.edit import FormView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetDoneView


# Need some logging functionality for debugging.
import logging
logger = logging.getLogger(__name__)

from website.forms import (
    UploadForm,
    LoginForm,
    AccountCreationForm,
    SearchForm,
    UserPrivilegeModificationForm,
    AdminFileDeletionForm,
    AdminFileRecoveryForm,
    AccountPasswordChangeForm,
    AccountPasswordResetForm,
    AccountPasswordResetConfirmForm
)

from website.models import (ProcessingJob, AsyncJob, FileDeletionJob)

from django.contrib.auth.mixins import (PermissionRequiredMixin, LoginRequiredMixin)

class HomepageView(TemplateView):
    # All we really need to do here is provide the name of the template.
    template_name = 'website/index.html'

class UploadView(PermissionRequiredMixin, FormView):
    # Permissions based on the following reference:
    # https://docs.djangoproject.com/en/2.2/topics/auth/default/#programmatically-creating-permissions
    permission_required = 'website.upload'

    template_name = 'website/upload.html'
    form_class = UploadForm
    success_url = '/status'

    job = None
    fs_manager = None

    def get_success_url(self):
        return self.success_url + "/" + str(self.job.id)

    def form_valid(self, form):
        # TODO During integration phrase, we may or may not add a descriptive file
        # name. In the meantime, we will just use auto-increment integer IDs.
        #file_name = form.determine_filename()

        # Set up the data that we are going to use.
        # First, we need to increment the upload number.
        # This number corresponds to the transaction ID.

        # Process the valid form.
        # This will save the file and create a job to process it.
        filename, job = form.process_file(self.request.user)
        self.job = job

        # Use the superclass's validation methods.
        return super(UploadView, self).form_valid(form)

class JobStatusView(DetailView):
    # The DetailView is showing the details of a model.
    # TODO make sure this works with the integration.
    model = website.models.AsyncJob

    # Use the generic 'status' template by default.
    template_name = 'website/status.html'

    type_to_template = {
        website.models.ProcessingJob: 'website/status_processing.html',
        website.models.FileDeletionJob: 'website/status_deletion.html',
        website.models.FileRecoveryJob: 'website/status_recovery.html',
    }

    def get_template_names(self, **kwargs):
        ret = self.template_name
        if self.ItemType is not None and self.ItemType in self.type_to_template:
            ret = self.type_to_template[self.ItemType]
        return ret

    def get_context_data(self, **kwargs):
        # Process a GET request and respond according to the job type.
        context = super(JobStatusView, self).get_context_data(**kwargs)

        if self.item is not None:
            fieldset = self.item.get_status_fields()
            context['item'] = fieldset

        return context

    def get(self, request, *args, **kwargs):
        self.item = None
        self.ItemType = None
        if (kwargs['pk'] is not None):
            pk = kwargs['pk']
            types = [ k for k in self.type_to_template ]
            i = 0
            while ((i < len(types)) and (self.item is None)):
                curr_type = types[i]
                if (curr_type.objects.filter(pk=pk)):
                    self.item = curr_type.objects.get(pk=pk)
                    self.ItemType = curr_type
                i += 1
        else:
            # TODO Error?
            pass

        return super(JobStatusView, self).get(request, *args, **kwargs)

class ProcessingJobStatusView(JobStatusView):
    template_name = 'website/status'

    # Reference:
    # https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        context = super(ProcessingJobStatusView, self).get_context_data(**kwargs)

        self.fields = {
            'file': ''
        }

        context['fields'] = self.fields

        return context

    @staticmethod
    def matches(**kwargs):
        return ProcessingJob.objects.filter(job_base_id=kwargs['pk']).exists()

class FileDeletionJobStatusView(JobStatusView):
    # Reference:
    # https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        context = super(FileDeletionJobStatusView, self).get_context_data(**kwargs)

        self.job = FileDeletionJob.get(pk=self.object.id)
        self.fields = {
            'files': DeletionRequestItem.filter(request=self.job.request)
        }

        context['fields'] = self.fields
        return context

    @staticmethod
    def matches(**kwargs):
        return FileDeletionJob.objects.filter(job_base_id=kwargs['pk']).exists()

    def get(*args, **kwargs):
        super().get(*args, **kwargs)

class SearchView(PermissionRequiredMixin, FormView):
    permission_required = 'website.search'

    template_name = 'website/search.html'
    form_class = SearchForm
    success_url = '/search'

    # This seems to be the best place to put this.
    # This maps the form's valid values (0, 1) to the redirect URL.
    success_url_by_type = {
        0: '/search/relation/%d',
        1: '/search/document/%d'
    }

    def set_success_url_from_form(self, form, search_request):
       
        new_success_url = "/"
        search_type = form.cleaned_data['search_by']
        search_id = search_request.id

        if search_type in self.success_url_by_type:
            new_success_url = (self.success_url_by_type[search_type] % (search_id,))
        self.success_url = new_success_url

    def form_valid(self, form):
        # In order to redirect to the correct page, we need to first receive the
        # form, validate it, and then redirect the user.

        # Set up the data that we are going to use.
        # Create the search request.
        search_request = form.save()

        # Find and set the destination (success_url) that the user will be
        # directed to.
        self.set_success_url_from_form(form, search_request)

        return super(SearchView, self).form_valid(form)


class RegisterSearchView(PermissionRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = ""

    def get_redirect_url(self, *args, **kwargs):
        # TODO this is probably bad - shouldn't the form be responsible for redirecting
        # to /document/x?
       
        pattern_name = "search-results-by-document"
        return super(RedirectView, self).get_redirect_url(*args, **kwargs)

# TODO clarify requirements - seems the most feasible:
# Instead of a single search being used and discarded, we might want to save the
# search, and then the results view would actually return the result of that specific
# search? (In other words, we would receive at /Search the search to add to the database,
# and then redirect the user to /Search/Results/X where X is a number corresponding to
# those search criteria?
class AbstractSearchResultsView(PermissionRequiredMixin, ListView):
    permission_required = 'website.search'
    def make_search_query(self):
        pass

    def perform_search(self, search):
        pass

    def get_queryset(self):
        id = self.kwargs.get('pk')
        search_instance = website.models.Search.objects.get(id=id)
        
        query = self.make_search_query()

        results = self.perform_search(query)

        return results

class DocumentSearchResultsView(AbstractSearchResultsView):
    template_name = "website/search_results_document.html"
     
    def perform_search(self, search):
        searchEng = Components.get_search_engine()
        id = self.kwargs.get('pk')
        search_instance = website.models.Search.objects.get(id=id)
        searchInput = searchEng.create_search(search_instance)
        res = search.nonMinuteSearch(searchInput)
        print(res)
        #out = searchEng.create_results(res)
        
        return search.document_search(search)

class RelationSearchResultsView(AbstractSearchResultsView):
    template_name = "website/search_results.html"

    def perform_search(self, searchEng):
        
        searchEng = Components.get_search_engine()
        id = self.kwargs.get('pk')
        search_instance = website.models.Search.objects.get(id=id)
        searchInput = searchEng.create_search(search_instance)
        a = search_instance.search_t
        print()
        out = None
        print(a)
        if(a == 0):
            res = search.minuteSearch(searchInput,search_instance.fbc_council,search_instance.fbc_publish_date_start,search_instance.fbc_publish_date_end)
            out = searchEng.create_results_minute(res)
            print(out)
        if(a == 1):
            res = search.nonMinuteSearch(searchInput,search_instance.fbc_council,search_instance.fbc_publish_date_start,search_instance.fbc_publish_date_end)
            out = searchEng.create_results_non_minute(res)
            
       # return searchEng.relation_search(search)
        return out

# When this is implemented we might want to use Django's built-in support for user accounts:
# https://docs.djangoproject.com/en/2.2/topics/auth/default/
class LoginView(FormView):
    template_name = "website/login.html"
    form_class = LoginForm
    success_url = '/login'

    def form_valid(self, form):
        # Authenticate to get the user.
        user = form.authenticate_user(self.request)

        if user is not None:
            self.success_url = '/login/success'

        # Perform the FormView's validity checks.
        return super(LoginView, self).form_valid(form)

"""
LoginSuccessfulView. Displays a template that confirms login and redirects
the user.
"""
class LoginSuccessfulView(TemplateView):
    """
    This inherits from TemplateView and not RedirectView because RedirectView is a
    hard redirect, so it would never display the template. Instead we will use
    TemplateView and use a HTTP header.
    """
    template_name = "website/login_successful.html"

################################################
#                Account Creation              #
################################################
class AccountCreationView(FormView):
    template_name = "website/create_account.html"
    form_class = AccountCreationForm
    success_url = '/'

    def form_valid(self, form):
        # Authenticate to get the user.
        form.create_user(self.request)

        # Perform the FormView's validity checks.
        return super(AccountCreationView, self).form_valid(form)

################################################
#          Account Password Recovery           #
################################################
class AccountPasswordResetDoneView(PasswordResetDoneView):
    """
    Represents the view shown when the user resets their password.

    This class is provided for extensibility only.
    """

    def form_valid(self, form):
        super(AccountPasswordResetDoneView, self).form_valid()

class AccountPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Represents the view shown when confirming a password reset.

    This class is provided for extensibility only.
    """
    template_name = "website/reset_password_new.html"
    form_class = AccountPasswordResetConfirmForm
    success_url = '/account/reset-password/confirmed'

    def form_valid(self, form):
        # Perform the FormView's validity checks.
        return super(AccountPasswordResetConfirmView, self).form_valid(form)

class AccountPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Represents the view shown when the password reset is done.

    This class is provided for extensibility only.
    """
    pass

class AccountPasswordResetView(PasswordResetView):
    """
    Represents the view shown when the password is reset.

    This class is provided for extensibility only.
    """
    template_name = "website/reset_password.html"
    form_class = AccountPasswordResetForm
    success_url = '/account/reset-password/done'
    email_template_name = "website/reset_password_email_link.html"

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        # Perform the formView's validity checks.
        return super(AccountPasswordResetView, self).form_valid(form)

class AccountPasswordResetDoneView(PasswordResetDoneView):
    template_name = "website/reset_password_done.html"
    
class AccountPasswordChangeView(PasswordChangeView):
    template_name = "website/change_password.html"
    form_class = AccountPasswordChangeForm
    success_url = '/'

    def form_valid(self, form):
        # Perform the FormView's validity checks.
        return super(AccountPasswordChangeView, self).form_valid(form)

class LogoutView(RedirectView):
    # Reference:
    # https://docs.djangoproject.com/en/2.2/ref/class-based-views/base/#django.views.generic.base.View
    # Don't permanently redirect, this would cause issues.
    permanent = False

    # We don't need the information - the logout has been performed.
    query_string = False

    # Redirect to the homepage upon logout.
    pattern_name = 'index'

    # Log the user out and redirect.
    # Reference:
    # https://gist.github.com/laozhu/8250910
    def get_redirect_url(self, *args, **kwargs):
        # The source states that this is a function, but it seems like it's
        # an attribute.
        if self.request.user is not None:
            logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)
    
class AccountView(TemplateView):
    template_name = "website/account.html"

class AdminView(TemplateView):
    template_name = 'website/admin.html'

class AdminFileDeletionView(FormView):
    template_name = 'website/admin-file-deletion.html'
    form_class = AdminFileDeletionForm
    success_url = '/status/'

    def form_valid(self, form):
        job = form.process_request()
        base_job = job.job_base

        self.success_url = '/status/' + str(base_job.id)
        return super(AdminFileDeletionView, self).form_valid(form)

class AdminFileRecoveryView(FormView):
    template_name = 'website/admin-file-recovery.html'
    form_class = AdminFileRecoveryForm
    success_url = '/status/'

    def form_valid(self, form):
        # Delete any DeletionRequests that are scheduling this file for deletion.
        job = form.process_request()
        base_job = job.job_base

        # Perform the job immediately.
        job.perform_job()

        self.success_url = '/status/' + str(base_job.id)

        return super(AdminFileRecoveryView, self).form_valid(form)

class UserPrivilegeModificationView(FormView):
    template_name = "website/user-privilege-modification.html"
    form_class = UserPrivilegeModificationForm
    success_url = "/admin/permissions"

    def form_valid(self, form):
        error_code = form.change_permissions()
        if not error_code:
            messages.add_message(self.request, messages.INFO,
                "Permissions successfully changed.")


        # Perform the FormView's validity checks.
        return super(UserPrivilegeModificationView, self).form_valid(form)
    
#def user_privilege_modification(request):
#    if request.method == "POST":
#        return render(request, 'website/user-privilege-modification.html',
#            get_params(DEBUG_PARAMS_MAP, {
#                'permissions': [ 'search', 'upload', 'delete-file', 'recover-file' ],
#                'status': 'successful'
#            })
#        )
#    return render(request, 'website/user-privilege-modification.html',
#        get_params(DEBUG_PARAMS_MAP, {
#            'permissions': [ 'search', 'upload', 'delete-file', 'recover-file' ]
#        })
#    )

def serve_uploaded_document(request, pk):
    # From https://stackoverflow.com/questions/11779246/how-to-show-a-pdf-file-in-a-django-view
    with open(settings.UPLOADS_DIR + '/' + str(pk) + '.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=' + str(pk) + '.pdf'
        return response
    pdf.closed

class JobListView(ListView):
    model = AsyncJob
    template_name = "website/job-list.html"
    context_object_name = "job_list"
    queryset = AsyncJob.objects.all()

    """
    Filter for the template - to map job status to its name.
    """
    @register.filter
    def get_status(job_id):
        return AsyncJob.STATUSES[job_id][1]
