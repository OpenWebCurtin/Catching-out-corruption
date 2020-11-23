from django.test import TestCase

from website.forms import SearchForm
from website.models import Search

import logging, sys, unittest

class TestSearchForm(TestCase):
    """ Testing suite for website.forms.SearchForm """

    # 
    def create_search_form(self, search_by = 0, fbm = None, fbm_filename = None,
        fbm_uploader = None,
        fbm_upload_date_start = None, fbm_upload_date_end = None,
        fbc = None, fbc_council = None,
        fbc_publish_date_start = None, fbc_publish_date_end = None,
        key_phrase1 = None, key_phrase_type1 = None, key_phrase_importance1 = None):
        """ Creates a default search form with a set of default (valid) values. """
        return SearchForm({
            'search_by': search_by,
            'fbm': fbm,
            'fbm_filename': fbm_filename,
            'fbm_uploader': fbm_uploader,
            'fbm_upload_date_start': fbm_upload_date_start,
            'fbm_upload_date_end': fbm_upload_date_end,
            'fbc': fbc,
            'fbc_council': fbc_council,
            'fbc_publish_date_start': fbc_publish_date_start,
            'fbc_publish_date_end': fbc_publish_date_end,
            'key_phrase1': key_phrase1,
            'key_phrase_type1': key_phrase_type1,
            'key_phrase_importance1': key_phrase_importance1
        })
    
    # Test is_valid for the default form produced by create_search_form.
    # If this test fails then most other tests are likely to fail,
    # so test this separately.
    def test_create_search_form(self):
        search_form = self.create_search_form()

        self.assertTrue(search_form.is_valid())

    #################################
    #  Test Multi-Field validation  #                                            
    #################################

    # Test is_valid for invalid input:
    #   fbc = True
    #   key_phrase1 = "Test1"
    #   key_phrase_type1 = 0
    #   key_phrase_importance1 = MISSING
    def test_invalid_form_1(self):
        # If fbc is True then either all of the key_phrase* fields are provided,
        # or none are provided.
        search_form = self.create_search_form(
            fbc = True,
            key_phrase1 = "Test1",
            key_phrase_type1 = 0
        )

        self.assertFalse(search_form.is_valid())

    # Test is_valid for invalid input:
    #   key_phrase1 = MISSING
    #   key_phrase_type1 = 0
    #   key_phrase_importance1 = 1.0
    def test_invalid_form_3(self):
        search_form = self.create_search_form(
            fbc = True,
            key_phrase_type1 = 0,
            key_phrase_importance1 = 1.0
        )
        self.assertFalse(search_form.is_valid())

    # Test that all valid inputs for key_phrase_type are supported.
    def test_valid_form_1(self):
        # There are 5 entries, so the inputs range from [0..5]
        for kp_type in range(5):
            search_form = self.create_search_form(
                fbc = True,
                key_phrase1 = "Test1",
                key_phrase_type1 = kp_type,
                key_phrase_importance1 = 1.0
            )

            self.assertTrue(search_form.is_valid())

    # Test is_valid for valid input:
    #   fbc = True
    #   key_phrase1 = "Test1"
    #   key_phrase_type1 = MISSING (Testing default value 0).
    #   key_phrase_importance1 = 1.0
    def test_valid_form_2(self):
        search_form = self.create_search_form(
            fbc = True,
            key_phrase1 = "Test1",
            key_phrase_importance1 = 1.0
        )

        self.assertTrue(search_form.is_valid())

    # Test is_valid for valid input:
    #   fbc = True
    #   key_phrase1 = "" (Default)
    #   key_phrase_type1 = 0 (Default)
    #   key_phrase_importance1 = 0 (Default)
    def test_valid_form_3(self):
        # If fbc is True then either all of the key_phrase* fields are provided,
        # or none are provided (i.e. all are default or null if no default exists).
        # This tests the latter.
        search_form = self.create_search_form(
            fbc = True,
            key_phrase1 = "",
            key_phrase_type1 = 0,
            key_phrase_importance1 = 0
        )

        self.assertTrue(search_form.is_valid())
    
    # Test is_valid for valid input:
    #   fbc = True
    #   key_phrase1 = "Test1"
    #   key_phrase_type1 = 1
    #   key_phrase_importance1 = 1.0
    def test_valid_form_4(self):
        # If fbc is True then either all of the key_phrase* fields are provided,
        # or none are provided (i.e. all are default or null if no default exists).
        # This tests the former.
        search_form = self.create_search_form(
            fbc = True,
            key_phrase1 = "Test1",
            key_phrase_type1 = 1,
            key_phrase_importance1 = 1.0
        )

        self.assertTrue(search_form.is_valid())

    # Test is_valid for invalid input:
    #   fbm = True
    #   fbm_filename = MISSING
    #   fbm_uploader = MISSING
    #   fbm_upload_date_start = MISSING
    #   fbm_upload_date_end = MISSING
    def test_invalid_form_5(self):
        # If fbm is True then at least one criteria from the above list must exist.
        # If they do not exist, it is an invalid form.
        search_form = self.create_search_form(
            fbm = True
        )

        self.assertFalse(search_form.is_valid())

    # Test is_valid for invalid input:
    #   fbm = False
    #   fbm_filename = "Test1"
    #   fbm_uploader = MISSING
    #   fbm_upload_date_start = MISSING
    #   fbm_upload_date_end = MISSING
    def test_invalid_form_6(self):
        # If fbm is False then none of the fbm_* should be set.
        # This test will test fbm_filename.
        search_form = self.create_search_form(
            fbm = False,
            fbm_filename = "Test1"
        )

        self.assertFalse(search_form.is_valid())

    # Test is_valid for invalid input:
    #   fbm = False
    #   fbm_filename = MISSING
    #   fbm_uploader = "Test1"
    #   fbm_upload_date_start = MISSING
    #   fbm_upload_date_end = MISSING
    def test_invalid_form_7(self):
        # If fbm is False then none of the fbm_* should be set.
        # This test will test fbm_uploader.
        search_form = self.create_search_form(
            fbm = False,
            fbm_uploader = "Test1"
        )

        self.assertFalse(search_form.is_valid())

    # Test is_valid for invalid input:
    #   fbm = False
    #   fbm_filename = MISSING
    #   fbm_uploader = MISSING
    #   fbm_upload_date_start = "2019-07-16"
    #   fbm_upload_date_end = "2019-07-17"
    def test_invalid_form_8(self):
        # If fbm is False then none of the fbm_* should be set.
        # This test will test fbm_upload_date_start and fbm_upload_date_end.
        search_form = self.create_search_form(
            fbm = False,
            fbm_upload_date_start = "2019-07-16",
            fbm_upload_date_end = "2019-07-17"
        )

        self.assertFalse(search_form.is_valid())

    # Test is_valid for invalid input:
    #   fbm = True
    #   fbm_upload_date_start = "2019-07-16"
    #   fbm_upload_date_end = MISSING
    def test_invalid_form_9(self):
        # If fbm_upload_date_start is set but fbm_upload_date_end is not set,
        # the form is invalid.
        search_form = self.create_search_form(
            fbm = True,
            fbm_upload_date_start = "2019-07-16"
        )

        self.assertFalse(search_form.is_valid())

    # Test is_valid for invalid input:
    #   fbm = True
    #   fbm_upload_date_start = MISSING
    #   fbm_upload_date_end = "2019-07-16"
    def test_invalid_form_10(self):
        # If fbm_upload_date_end is set but fbm_upload_date_start is not set,
        # the form is invalid.
        search_form = self.create_search_form(
            fbm = True,
            fbm_upload_date_end = "2019-07-17"
        )

        self.assertFalse(search_form.is_valid())

    # Test is_valid for invalid input:
    #   fbc = True
    #   fbc_publish_date_start = "2019-07-16"
    #   fbc_publish_date_end = MISSING
    def test_invalid_form_11(self):
        # If fbc_publish_date_start is set but fbc_publish_date_end is not set,
        # the form is invalid.
        search_form = self.create_search_form(
            fbc = True,
            fbc_publish_date_start = "2019-07-16"
        )

        self.assertFalse(search_form.is_valid())

    # Test is_valid for invalid input:
    #   fbc = True
    #   fbc_publish_date_start = MISSING
    #   fbc_publish_date_end = "2019-07-16"
    def test_invalid_form_12(self):
        # If fbc_publish_date_end is set but fbc_publish_date_start is not set,
        # the form is invalid.
        search_form = self.create_search_form(
            fbc = True,
            fbc_publish_date_end = "2019-07-16"
        )

        self.assertFalse(search_form.is_valid())

