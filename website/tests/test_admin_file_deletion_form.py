from django.test import TestCase

from website.forms import AdminFileDeletionForm
from website.models import (UploadedFile, FileDeletionJob)

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
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin"

class TestUploadForm(TestCase):
    """ Testing suite for website.forms.UploadForm """

    def setUp(self):
        management.call_command("initperms")
        management.call_command("initusers")

        obj = UploadedFile.objects.create(
            file="1.pdf",
            filename="1.pdf",
            type=0,
            document_category="generic",
            uploader=User.objects.get(username="admin")
        )
        obj.save()

    # 
    def create_afd_filename_form(self, 
        delete_by=0, target_file="1", target_uploader=None):
        """ Creates a valid AFD form with a set of values for deleting by filename."""

        return AdminFileDeletionForm({
            'delete_by': delete_by,
            'target_file': target_file,
            'target_uploader': target_uploader
        })
 
    # 
    def create_afd_uploader_form(self, 
        delete_by=1, target_file=None, target_uploader="admin"):
        """ Creates a valid AFD form with a set of values for deleting by uploader."""

        return AdminFileDeletionForm({
            'delete_by': delete_by,
            'target_file': target_file,
            'target_uploader': target_uploader
        })
    
    # Test is_valid for the default form produced by create_afd_filename_form.
    # If this test fails then most other tests are likely to fail,
    # so test this separately.
    def test_create_afd_filename_form(self):
        afd_filename_form = self.create_afd_filename_form()

        self.assertTrue(afd_filename_form.is_valid())
    
    # Test is_valid for the default form produced by create_afd_uploader_form.
    # If this test fails then most other tests are likely to fail,
    # so test this separately.
    def test_create_afd_uploader_form(self):
        afd_uploader_form = self.create_afd_uploader_form()

        self.assertTrue(afd_uploader_form.is_valid())

    # Test is_valid for invalid input:
    #   target_uploader = Invalid uploader (Not empty).
    #   target_filename = Valid filename.
    #   delete_by       = Delete by filename.
    # This is invalid because delete_by = filename implies that uploader has no effect
    # but the user seems to want to delete by uploader.
    def test_invalid_form_1(self):
        afd_filename_form = self.create_afd_filename_form(
            target_uploader = "admin"
        )

        self.assertFalse(afd_filename_form.is_valid())

    # Test is_valid for invalid input:
    #   target_uploader = Valid uploader.
    #   target_filename = Invalid filename (Not empty).
    #   delete_by       = Delete by uploader.
    # This is invalid because delete_by = filename implies that uploader has no effect
    # but the user seems to want to delete by uploader.
    def test_invalid_form_2(self):
        afd_uploader_form = self.create_afd_uploader_form(
            target_file = "1"
        )

        self.assertFalse(afd_uploader_form.is_valid())

    # Test is_valid for invalid input:
    #   target_uploader = Invalid uploader (Empty).
    #   delete_by       = Delete by uploader.
    def test_invalid_form_3(self):
        afd_uploader_form = self.create_afd_uploader_form(
            target_uploader = ""
        )

        self.assertFalse(afd_uploader_form.is_valid())

    # Test is_valid for invalid input:
    #   target_uploader = Invalid uploader (None).
    #   delete_by       = Delete by uploader.
    def test_invalid_form_4(self):
        afd_uploader_form = self.create_afd_uploader_form(
            target_uploader = None
        )

        self.assertFalse(afd_uploader_form.is_valid())

    # Test is_valid for invalid input:
    #   target_file     = Invalid filename (Empty)
    #   delete_by       = Delete by file.
    def test_invalid_form_5(self):
        afd_filename_form = self.create_afd_filename_form(
            target_file = ""
        )

        self.assertFalse(afd_filename_form.is_valid())

    # Test that a job is actually created by process_request
    # (when delete_by = filename).
    def test_job_created_filename_1(self):
        afd_filename_form = self.create_afd_filename_form()

        job = afd_filename_form.process_request()
        instance = afd_filename_form.instance
        expectedJob = FileDeletionJob.objects.get(request__id=instance.id)

        self.assertEqual(job, expectedJob)

    # Test that a job is actually created by process_request
    # (when delete_by = uploader).
    def test_job_created_uploader_1(self):
        afd_uploader_form = self.create_afd_uploader_form()

        job = afd_uploader_form.process_request()
        instance = afd_uploader_form.instance
        expectedJob = FileDeletionJob.objects.get(request__id=instance.id)

        self.assertEqual(job, expectedJob)
