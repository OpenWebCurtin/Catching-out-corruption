from django.test import TestCase

from website.forms import LoginForm

from django.contrib.auth import get_user_model

import logging, sys, unittest

from django.core import management

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from django.contrib import auth

User = get_user_model()

# Use the regular account for testing the login system.
# The admin needs to change these after deployment, so it should
# be fine to use them for testing.
VALID_USERNAME = "regular"
VALID_PASSWORD = "regular"

class TestUploadForm(TestCase):
    """ Testing suite for website.forms.UploadForm """

    def setUp(self):
        management.call_command("initperms")
        management.call_command("initusers")

    # 
    def create_login_form(self, in_username=VALID_USERNAME,
        in_password=VALID_PASSWORD):
        """ Creates a login form with a set of values. """

        return LoginForm({
            'username': in_username,
            'password': in_password
        })
    
    # Test is_valid for the default form produced by create_login_form.
    # If this test fails then most other tests are likely to fail,
    # so test this separately.
    def test_create_login_form(self):
        login_form = self.create_login_form()

        self.assertTrue(login_form.is_valid())

    ##################################
    #  Test Single-Field validation  #
    ##################################

    # Test is_valid for invalid input:
    #   username = Valid username.
    #   password = Invalid password (Blank).
    def test_valid_form_2(self):
        login_form = self.create_login_form(
            in_password = ""
        )

        self.assertFalse(login_form.is_valid())

    # Test is_valid for invalid input:
    #   username = Valid username.
    #   password = Invalid password (Null).
    def test_valid_form_3(self):
        login_form = self.create_login_form(
            in_password = None
        )

        self.assertFalse(login_form.is_valid())

    # Test is_valid for invalid input:
    #   username = Invalid username (Blank).
    #   password = Valid password.
    def test_valid_form_4(self):
        login_form = self.create_login_form(
            in_username = ""
        )

        self.assertFalse(login_form.is_valid())

    # Test is_valid for invalid input:
    #   username = Invalid username (Null).
    #   password = Valid password.
    def test_valid_form_5(self):
        login_form = self.create_login_form(
            in_username = None
        )

        self.assertFalse(login_form.is_valid())

    # Test is_valid for invalid input:
    #   username = Valid username, but nonexistent.
    #   password = Valid password, but not for the (nonexistent) user.
    def test_invalid_form_6(self):
        login_form = self.create_login_form(
            in_username = "FakeUserAccount",
            in_password = VALID_PASSWORD
        )

        self.assertFalse(login_form.is_valid())

    # Test is_valid for invalid input:
    #   username = Valid username that exists.
    #   password = Valid password, but incorrect.
    def test_invalid_form_7(self):
        login_form = self.create_login_form(
            in_username = VALID_USERNAME,
            in_password = "IncorrectPassword"
        )

        self.assertFalse(login_form.is_valid())

    # Test is_valid for invalid input:
    #   username = Valid username that does not exist.
    #   password = Valid password but incorrect for (nonexistent) user.
    def test_invalid_form_8(self):
        login_form = self.create_login_form(
            in_username = "FakeUserAccount",
            in_password = "IncorrectPassword"
        )

        self.assertFalse(login_form.is_valid())


    # Test that authenticate_user correctly authenticates for correct
    # user credentials.
    def test_authenticate_user_1(self):
        response = self.client.post('/login', {
            'username': VALID_USERNAME,
            'password': VALID_PASSWORD
        })

        expected = User.objects.get(username=VALID_USERNAME)

        actual = auth.get_user(self.client)

        self.assertEqual(expected, actual)
        self.assertFalse(actual.is_anonymous)
        self.assertTrue(actual.is_authenticated)

    # Test that authenticate_user correctly fails to authenticate for incorrect
    # user credentials.
    def test_authenticate_user_2(self):
        response = self.client.post('/login', {
            'username': VALID_USERNAME,
            'password': "invalid_password"
        })

        actual = auth.get_user(self.client)

        self.assertTrue(actual, actual.is_anonymous)
        self.assertFalse(actual.is_authenticated)

