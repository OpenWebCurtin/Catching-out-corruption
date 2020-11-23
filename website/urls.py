from django.urls import path

from website.views import (
    HomepageView,
    UploadView,
    JobStatusView,
    SearchView,
    DocumentSearchResultsView,
    RelationSearchResultsView,
    # Account page view.
    AccountView,
    LoginView,
    LoginSuccessfulView,
    AccountCreationView,
    AccountPasswordChangeView,
    AccountPasswordResetView,
    AccountPasswordResetConfirmView,
    AccountPasswordResetCompleteView,
    AccountPasswordResetDoneView,
    LogoutView,
    # Admin
    AdminView,
    # Admin delete.
    AdminFileDeletionView,
    # Admin recover.
    AdminFileRecoveryView,
    # Admin permissions.
    UserPrivilegeModificationView,
    # Job list.
    JobListView,
    # Uploads view.
    serve_uploaded_document
)

urlpatterns = [

    # Homepage.
    path('',
        HomepageView.as_view(),
        name='index'),

    # PDF Minute Parser - Upload Service.
    path('upload',
        UploadView.as_view(),
        name='upload-service'),

    # PDF Minute Parser - Processing Job Status.
    path('status/<int:pk>',
        JobStatusView.as_view(),
        name='status'),

    # Agenda Item Searchability - Search Page.
    path('search',
        SearchView.as_view(),
        name='search'),

    # Agenda Item Searchability - Search Page.

    # TODO bring this up with the client - changed from spec.
    path('search/document/<int:pk>',
        DocumentSearchResultsView.as_view(),
        name='search-results-by-document'),

    # TODO bring this up with the client - changed from spec.
    path('search/relation/<int:pk>',
        RelationSearchResultsView.as_view(),
        name='search-results-by-relation'),

    path('account',
        AccountView.as_view(),
        name='account'),

    path('account/change-password',
        AccountPasswordChangeView.as_view(),
        name='change-password'),

    # Reset password - provide an option for a person who has lost their
    # credentials to change their password.
    path('account/reset-password',
        AccountPasswordResetView.as_view(),
        name='reset-password'),
    
    path('account/reset-password/done',
        AccountPasswordResetDoneView.as_view(),
        name='reset-password-done'),

    path('account/reset-password/confirm/<uidb64>/<token>',
        AccountPasswordResetConfirmView.as_view(),
        name='reset-password-confirm'),

    path('account/reset-password/confirm/<uidb64>',
        AccountPasswordResetConfirmView.as_view(),
        name='reset-password-done'),

    path('account/creation',
        AccountCreationView.as_view(),
        name='create-account'),

    # TODO figure out how to implement this - based on user interaction specification.
    #path('search/<...>', views.search, name='search'),

    # Login system is to be provided by the internal app provided by Django.
    path('login',
        LoginView.as_view(),
        name='login'),

    # Login confirmation / redirection page.
    path('login/success',
        LoginSuccessfulView.as_view(),
        name='login-successful'),

    # Allow logging out of the system.
    path('logout',
        LogoutView.as_view(),
        name='logout'),

    path('admin',
        AdminView.as_view(),
        name='admin'),

    path('admin/delete',
        AdminFileDeletionView.as_view(),
        name='admin-file-deletion'),

    path('admin/recover',
        AdminFileRecoveryView.as_view(),
        name='admin-file-recovery'),

    path('admin/permissions',
        UserPrivilegeModificationView.as_view(),
        name='user-privilege-modification'),

    path('jobs',
        JobListView.as_view(),
        name='job-list'),

    # Email confirmation. TODO
    #path('confirmemail/<...>')

    path('uploads/<int:pk>',
        serve_uploaded_document,
        name='uploaded-document')
]
