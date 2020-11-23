from django.test import TestCase

from pdfparser.ExtractedData import ExtractedData

import unittest, sys, logging

# Create your tests here.

class TestUnit(TestCase):

    def setUp(self):
        self.type_key_phrases = "Citizen"#, "Some other tag"]
        self.ex_data1 = ExtractedData("Agenda Code", "Agenda Name", "Document Name", "Peter Something", self.type_key_phrases)


    def test_pass_valid_class_fields(self):
        #x = 5
        self.assertTrue(self.ex_data1.valid)
        
        #self.assertTrue(x != x)

    def test_show_data(self):
        expected = "Key Phrase: Peter Something || Type: Citizen || "\
                                    "Agenda Code: Agenda Code" \
                                    " || Agenda Name: Agenda Name || Document Name: Document Name"
        
        self.assertTrue(expected == self.ex_data1.show_data())

    def test_agenda_code(self):
        self.assertTrue(self.ex_data1.agenda_code == "Agenda Code")

    def test_agenda_name(self):
        self.assertTrue(self.ex_data1.agenda_name == "Agenda Name")
    
    def test_docuemnt_name(self):
        self.assertTrue(self.ex_data1.document_name == "Document Name")
    
    def test_key_type(self):
        expected_key_phrases = "Citizen"#, "Some other tag"]
        self.assertTrue(self.ex_data1.type_key_phrase == expected_key_phrases)
    
    def test_key_phrase(self):
        self.assertTrue(self.ex_data1.key_phrase == "Peter Something")

    def test_agenda_code_valid(self):
        bad_data = ExtractedData(12, "Agenda Name", "Document Name", "Peter Something", self.type_key_phrases)
        self.assertFalse(bad_data.valid)

    def test_agenda_code_none(self):
        bad_data = ExtractedData(12, "Agenda Name", "Document Name", "Peter Something", self.type_key_phrases)
        self.assertTrue(bad_data.agenda_code == None)

    def test_agenda_name_valid(self):
        bad_data = ExtractedData("Peter Something", 12.3, "Document Name", "Peter Something", self.type_key_phrases)
        self.assertFalse(bad_data.valid)

    def test_agenda_name_none(self):
        bad_data = ExtractedData("Peter Something", 12.3, "Document Name", "Peter Something", self.type_key_phrases)
        self.assertTrue(bad_data.agenda_name == None)

    def test_document_name_valid(self):
        bad_data = ExtractedData("Peter Something", "Agenda Name", 35, "Peter Something", self.type_key_phrases)
        self.assertFalse(bad_data.valid)

    def test_document_name_none(self):
        bad_data = ExtractedData("Peter Something", "Agenda Name", 35, "Peter Something", self.type_key_phrases)
        self.assertTrue(bad_data.document_name == None)
        
    def test_key_phrase_valid(self):
        bad_data = ExtractedData("Peter Something", "Agenda Name", "Document Name", 23, self.type_key_phrases)
        self.assertFalse(bad_data.valid)

    def test_key_phrase_none(self):
        bad_data = ExtractedData("Peter Something", "Agenda Name", "Document Name", 23, self.type_key_phrases)
        self.assertTrue(bad_data.key_phrase == None)
    
    def test_key_phrase_type_valid(self):
        bad_data = ExtractedData("Peter Something", "Agenda Name", "Document Name", "Peter Something", 23)
        self.assertFalse(bad_data.valid)

    def test_key_phrase_none(self):
        bad_data = ExtractedData("Peter Something", "Agenda Name", "Document Name", "Peter Something", 23)
        self.assertTrue(bad_data.type_key_phrase == None)
