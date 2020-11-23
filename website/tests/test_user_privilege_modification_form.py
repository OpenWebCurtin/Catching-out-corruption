from django.test import TestCase

from website.forms import (UserPrivilegeModificationForm)

from django.contrib.auth import get_user_model

import logging, sys, unittest

from django.core import management

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from django.contrib import auth

User = get_user_model()

# Use the regular accounts for testing the privilege modification system.
# The admin needs to change these after deployment, so it should
# be fine to use them for testing.
VALID_ADMIN = "admin"
VALID_TARGET_USER = "regular"
VALID_TARGET_GROUP = "regular user"

class TestUserPrivilegeModificationForm(TestCase):
    """ Testing suite for website.forms.UserPrivilegeModificationForm """

    def setUp(self):
        management.call_command("initperms")
        management.call_command("initusers")

    # Creates a basic valid UPM form.
    def create_upm_form(self, admin=VALID_ADMIN, target_user=VALID_TARGET_USER,
        target_group=VALID_TARGET_GROUP):
        """ Creates a valid UPM form with a set of valid values. """

        return UserPrivilegeModificationForm({
            'target_user': target_user,
            'target_group': target_group
        })

    # Test the behaviour of set_user_group:
    # - Test that the user originally has a user group.
    # - Test that the set_user_group method removes that user group.
    # - Test that the set_user_group method assigns the user to the input user group.
    def test_set_user_group_1(self):
        upm_form = self.create_upm_form(target_group="A")

        User = get_user_model()
        user = User.objects.get(username="privileged")
        target_group = Group.objects.get(name="regular user")

        # Test that the user has the "privileged user" group.
        has_priv = False
        for group in user.groups.all():
            if group.name == "privileged user":
                has_priv = True
        self.assertTrue(has_priv)

        # Perform the function.
        upm_form.set_user_group(user, target_group)

        # Test that the user does not have the original group.
        for group in user.groups.all():
            self.assertNotEqual(group.name, "privileged user")

        # Test that the user has the granted permission.
        has_priv = False
        for group in user.groups.all():
            if group.name == "regular user":
                has_priv = True
        self.assertTrue(has_priv)

    # Test that get_group returns the correct group.
    def test_get_group_1(self):
        group_name = "regular user"
        upm_form = self.create_upm_form()
        group = upm_form.get_group("regular user")

        self.assertEquals(group.name, "regular user")

    # Test that get_user returns the correct user.
    def test_get_user_1(self):
        user_name = "privileged"
        upm_form = self.create_upm_form()
        user = upm_form.get_user(user_name)

        self.assertEquals(user.username, "privileged")

    # Test is_valid for the default form produced by create_upm_form.
    # If this test fails then most other tests are likely to fail,
    # so test this separately.
    def test_create_upm_form(self):
        upm_form = self.create_upm_form()

        self.assertTrue(upm_form.is_valid())
    
    # Test is_valid for invalid input:
    #  target_user  = Invalid user.
    #  target_group = Valid group.
    def test_invalid_form_1(self):
        upm_form = self.create_upm_form(target_user="nonexistent")

        self.assertFalse(upm_form.is_valid())

    # Test is_valid for invalid input:
    #  target_user  = Valid user.
    #  target_group = Invalid group.
    def test_invalid_form_2(self):
        upm_form = self.create_upm_form(target_group="nonexistent")

        self.assertFalse(upm_form.is_valid())
