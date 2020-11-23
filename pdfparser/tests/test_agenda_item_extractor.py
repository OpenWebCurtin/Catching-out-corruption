from django.test import TestCase

import unittest, sys, logging, io

from pdfparser.XMLData import XMLData
from pdfparser.PerthExtractor import PerthExtractor
from pdfparser.VincentExtractor import VincentExtractor

class TestUnit(TestCase):

    def setUp(self):
        agenda_methods = AgendaItemExtractor()

    # PROCESS_B_BOX TESTS ======================================================
    def test_process_b_valid_data(self):
        b_box_text = "182.123, 23.32, 231.23, 123.43"
        b_box_expected = [182.123, 23.32]
        b_box_result = AgendaItemExtractor.process_b_box(self, b_box_text)
        self.assertTrue(b_box_expected == b_box_result)

    def test_process_b_no_data(self):
        b_box_text = ""
        b_box_expected = None
        b_box_result = AgendaItemExtractor.process_b_box(self, b_box_text)
        self.assertTrue(b_box_expected == b_box_result)

    def test_process_b_none(self):
        b_box_text = None
        b_box_expected = None
        b_box_result = AgendaItemExtractor.process_b_box(self, b_box_text)
        self.assertTrue(b_box_expected == b_box_result)

    def test_process_b_number(self):
        b_box_text = 5
        b_box_expected = None
        b_box_result = AgendaItemExtractor.process_b_box(self, b_box_text)
        self.assertTrue(b_box_expected == b_box_result)
    
    def test_process_b_single(self):
        b_box_text = "543.23"
        b_box_expected = None
        b_box_result = AgendaItemExtractor.process_b_box(self, b_box_text)
        self.assertTrue(b_box_expected == b_box_result)

    def test_process_b_negative(self):
        b_box_text = "-231.34, 54.32, 23.4, 76.78"
        b_box_expected = None
        b_box_result = AgendaItemExtractor.process_b_box(self, b_box_text)
        self.assertTrue(b_box_expected == b_box_result)

    def test_process_b_negative_second(self):
        b_box_text = "231.34, -54.32, 23.4, 76.78"
        b_box_expected = None
        b_box_result = AgendaItemExtractor.process_b_box(self, b_box_text)
        self.assertTrue(b_box_expected == b_box_result)

    def test_process_b_spaces(self):
        b_box_text = "231.34,54.32,23.4,76.78"
        b_box_expected = [231.34, 54.32]
        b_box_result = AgendaItemExtractor.process_b_box(self, b_box_text)
        self.assertTrue(b_box_expected == b_box_result)

    # DETERMINE_FACTORY TESTS =========================================================
    def test_determine_factory_perth(self):
        parser_type = AgendaItemExtractor.determine_factory(self, "Contains Perth")
        self.assertIsInstance(parser_type, PerthExtractor)

    def test_determine_factory_vincent(self):
        parser_type = AgendaItemExtractor.determine_factory(self, "Contains Vincent")
        self.assertIsInstance(parser_type, VincentExtractor)

    " For now, capture the standard output by redirecting sys.stdout to a StringIO"
    def test_determine_factory_stirling(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        AgendaItemExtractor.determine_factory(self, "Contains Stirling")
        sys.stdout = sys.__stdout__
        expected_result = "Do the Stirling one\n"
        self.assertTrue(capturedOutput.getvalue() == expected_result)

    def test_determine_factory_invalid(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        self.assertRaises(ValueError, 
                AgendaItemExtractor.determine_factory, self, "does_not_contain_an_identifier.txt")
        sys.stdout = sys.__stdout__

    " Passing None should throw a TypeError"
    def test_determine_factoty_none(self):
        self.assertRaises(TypeError,
                AgendaItemExtractor.determine_factory, self, None)

    def test_determine_factoy_not_string(self):
        self.assertRaises(TypeError,
                AgendaItemExtractor.determine_factory, self, 55)


    # startDocument TESTS ==============================================================

    def test_start_element_valid(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        parser.parse("pdfparser/static/pdfparser/test/one_letter_Perth~Agenda_code.xml")

        sys.stdout = sys.__stdout__
        correct_data = False
        # Loop through the xml data, and check the data of the one that is 'a'
        for xml_char in parser.xml_data:
            if xml_char.character == 'a':
                if xml_char.b_x == 72.024 and xml_char.b_y == 756.840:
                    correct_data = True
        self.assertTrue(correct_data)

    def test_start_element_no_bbox(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        parser.parse("pdfparser/static/pdfparser/test/no_bbox_Perth~Agenda_code.xml")
        sys.stdout = sys.__stdout__

        correct_result = True
        for xml_char in parser.xml_data:
            if xml_char.character == 'a':
                correct_result = False
        self.assertTrue(correct_result)

    # parse TESTS ======================================================================

    def test_parse_invalid_xml(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        parser.parse("pdfparser/static/pdfparser/test/invalid~Agenda_code.xml")

        sys.stdout = sys.__stdout__
        expected = "File does not contain a recognised council name: pdfparser/static/pdfparser/test/invalid~agenda_code.xml\n"
        self.assertEqual(expected, capturedOutput.getvalue())

    def test_parse_valid_xml(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        parser.parse("pdfparser/static/pdfparser/test/one_letter_Perth~Agenda_code.xml")
        sys.stdout = sys.__stdout__

        correct_result = False
        for xml_char in parser.xml_data:
            if xml_char.character == 'a':
                correct_result = True
        sys.stdout = sys.__stdout__
        self.assertTrue(correct_result)

    def test_parse_null(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        parser = AgendaItemExtractor()
        parser.parse(None)
        expected = "File does not contain a recognised council name:"\
                    " 'NoneType' object has no attribute 'lower'\n"\
                    "File_Name is not a String type: 'NoneType' object has no attribute 'lower'\n"

        sys.stdout = sys.__stdout__
        #print(expected)
        #print(capturedOutput.getvalue())

        self.assertTrue(expected == capturedOutput.getvalue())

    def test_parse_not_string(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        # Now that the file_name is converted to lower case, it should crash at file_name.lower
        parser = AgendaItemExtractor()
        parser.parse(23)
        expected = "File does not contain a recognised council name:"\
                    " 'int' object has no attribute 'lower'\n"\
                    "File_Name is not a String type: 'int' object has no attribute 'lower'\n"
        sys.stdout = sys.__stdout__

        self.assertTrue(expected == capturedOutput.getvalue())
        #self.assertRaises(AttributeError,
         #       parser.parse, 23)

    def test_parse_empty_string(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        parser.parse("")

        sys.stdout = sys.__stdout__
        expected = "File does not contain a recognised council name: \n"
        #print(expected)
        #print(capturedOutput.getvalue())
        self.assertTrue(expected == capturedOutput.getvalue())

    def test_parse_empty_file(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        parser.parse("pdfparser/static/pdfparser/test/empty_Perth~Agenda_code.xml")

        sys.stdout = sys.__stdout__
        expected_result = False
        if len(parser.xml_data) == 0:
            expected_result = True

        self.assertTrue(expected_result)

    # characters TESTS ==============================================================================

    def test_character_twice(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        #path = "pdfparser/tests/twice_Perth.xml"
        path = "pdfparser/static/pdfparser/test/double_Perth~Agenda_code.xml"
        parser.parse(path)
        sys.stdout = sys.__stdout__

        expected_result = False
        for char in parser.xml_data:
            if char.character == " ":
                expected_result = True

        self.assertTrue(expected_result)

    def test_character_single_new_line(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        #path = "pdfparser/tests/twice_Perth.xml"
        path = "pdfparser/static/pdfparser/test/one_letter_Perth~Agenda_code.xml"
        parser.parse(path)
        sys.stdout = sys.__stdout__

        expected_result = True
        for char in parser.xml_data:
            if char.character == "\n":
                expected_result = false
        self.assertTrue(expected_result)

    def test_character_double_new_line(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        parser.parse("pdfparser/static/pdfparser/test/double_Perth~Agenda_code.xml")
        sys.stdout = sys.__stdout__

        expected_result = False
        for char in parser.xml_data:
            #print("%s || AFTER" %(char.character))
            if char.character == " ":
                expected_result = True
        self.assertTrue(expected_result)

    def test_character_non_repeated_new_line(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        parser.parse("pdfparser/static/pdfparser/test/single_Perth~Agenda_code.xml")
        sys.stdout = sys.__stdout__

        expected_result = True
        for char in parser.xml_data:
            #print("%s || AFTER" %(char.character))
            if char.character == "\n":
                expected_result = False

        self.assertTrue(expected_result)

    def test_character_no_text_tag(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        parser.parse("pdfparser/static/pdfparser/test/no_text_tag_Perth~Agenda_code.xml")
        sys.stdout = sys.__stdout__

        self.assertTrue(len(parser.xml_data) == 0)

    # create_extracted_data Tests =======================================================

    def test_create_extracted_data_succeeds(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        parser.file_name = "pdfparser/static/pdfparser/test/no_text_tag_Perth~Agenda_code.xml"
        data = ["one", "two"]
        result = parser.create_extracted_data(data)
        expected_result = False

        if isinstance(data, list):
            expected_result = True

        sys.stdout = sys.__stdout__
        self.assertTrue(expected_result)


    # send_to_database Tests ===========================================================

    def test_database_valid(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()
        data1 = ["one", "two"]
        data2 = "Councillor"
        parser.send_to_database(data1, data2, "document_name", "agenda_name")

        expected_result = False
        if "None Type" not in capturedOutput.getvalue():
            expected_result = True

        sys.stdout = sys.__stdout__
        self.assertTrue(expected_result)

    def test_database_None(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        parser = AgendaItemExtractor()

        data2 = "Councillor"
        parser.send_to_database(None, data2, "document_name", "agenda_name")

        expected_result = "None Type was passed in: 'NoneType' object is not iterable\n"
        sys.stdout = sys.__stdout__
        result = False


        if (expected_result == capturedOutput.getvalue()):
            result = True

        self.assertTrue(result)

    # extract_agenda_code Tests ============================================================

    # EA1
    def test_extract_agenda_code(self):
        parser = AgendaItemExtractor()
        parser.file_name = "one_letter_Perth~Agenda_code.xml"
        actual_result = parser.extract_agenda_code()
        expected_result = ["one_letter_Perth", "Agenda_code"]
        self.assertEqual(actual_result, expected_result)

    # EA2
    def test_no_tildes(self):
        parser = AgendaItemExtractor()
        parser.file_name = "Perth.xml"
        actual_result = parser.extract_agenda_code()
        expected_result = ["Perth", "Perth"]
        self.assertEqual(actual_result, expected_result)

    # EA3
    def test_three_tildes(self):
        parser = AgendaItemExtractor()
        parser.file_name = "Perth~Agenda~Third.xml"
        actual_result = parser.extract_agenda_code()
        expected_result = ["Perth", "Agenda"]
        self.assertEqual(actual_result, expected_result)

    # EA4
    def test_file_name_none_extract(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput

        parser = AgendaItemExtractor()
        parser.file_name = None
        actual_result = parser.extract_agenda_code()
        expected_result = None

        sys.stdout = sys.__stdout__

        self.assertEqual(actual_result, expected_result)

    # EA5
    def test_empty_file_name_extract(self):
        parser = AgendaItemExtractor()
        parser.file_name = ""
        actual_result = parser.extract_agenda_code()
        expected_result = ["Empty String", "Empty String"]
        self.assertEqual(actual_result, expected_result)


