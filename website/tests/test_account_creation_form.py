from django.test import TestCase

from website.forms import AccountCreationForm

import logging, sys, unittest

VALID_USERNAME = "testuser"
VALID_PASSWORD = "983JF93SKJNF893NSLKGMR;"
# We aren't testing actually sending email, and no validation checks for emails
# are enforced.
VALID_EMAIL = "VALID@example.com"

class TestAccountCreationForm(TestCase):
    """
    Testing suite for website.forms.AccountCreationForm
    """

    def create_account_creation_form(self, username=VALID_USERNAME,
        password1=VALID_PASSWORD, password2=VALID_PASSWORD, email=VALID_EMAIL):
        """
        Creates a valid account creation form.
        """
        return AccountCreationForm({
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email
        })
    
    def test_create_account_creation_form(self):
        """
        Test that create_account_creation_form by default returns a valid
        form.
        """
        account_creation_form = self.create_account_creation_form(
            
        )

    def test_get_verification_email_recipients(self):
        """
        Tests that get_verification_email_recipients actually uses the correct
        email and nothing more.
        """
        uac_form = self.create_account_creation_form()
        # We need to "save" the form otherwise it won't have access to the
        # cleaned_data.
        uac_form.save()

        # Ensure that uac_form gives a list with just the single element:
        # the email entered.
        self.assertEquals(uac_form.get_verification_email_recipients(), [ VALID_EMAIL ])

    def get_verification_email_subject(self):
        """
        Tests that the subject is the expected value.
        """
        uac_form = self.create_account_creation_form()

        self.assertEquals(
            uac_form.get_verification_email_subject(),
            "Welcome to OpenWeb"
        )
