from django.test import TestCase

from pdfparser.VincentExtractor import VincentExtractor
from pdfparser.XMLData import XMLData

import unittest, sys, logging, io

# Create your tests here.

class TestUnit(TestCase):

    def setUp(self):
        self.xml_data_space = XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True)
        self.xml_data_B = XMLData("B", 15.0, 70.0, "Font", 23.0, False, True)
        self.xml_data_y_1 = XMLData(" ", 10.0, 10.0, "Font", 25.0, False, True)
        self.xml_data_y_2 = XMLData(" ", 10.0, 15.0, "Font", 25.0, False, True)
        self.xml_data_y_3 = XMLData(" ", 10.0, 20.0, "Font", 25.0, False, True)
        self.xml_data_list = [ 
            XMLData("a", 150.0, 60.0, "Font", 23.0, False, True), #0
            XMLData("b", 150.0, 60.0, "Font", 23.0, False, True), #1
            XMLData("b", 150.0, 60.0, "Font", 23.0, False, True), #2
            XMLData("b", 150.0, 60.0, "Font", 23.0, False, True), #3
            #XMLData(" ", 150.0, 70.0, "Font", 23.0, False, True),
            XMLData(" ", 150.0, 70.0, "Font", 23.0, False, True), #4
            XMLData(" ", 150.0, 60.0, "Font", 23.0, False, True), #5
            XMLData(" ", 150.0, 60.0, "Font", 23.0, False, True), #6
            XMLData(" ", 160.0, 60.0, "Font", 23.0, False, True)] #7
        self.v = VincentExtractor()


    # NOTE These tests are unchanged from the Vincent Tests
    # =============================== GET_SPACE_SIZE Tests ============================
    def test_finding_space_gap(self):
        xml_data = []
        xml_data.append(self.xml_data_space)
        xml_data.append(self.xml_data_B)

        expected_result = 5.0
        actual_result = VincentExtractor.get_space_size(self, xml_data)

        self.assertTrue(expected_result == actual_result)

    def test_execute_false_if(self):
        xml_data = []

        xml_data.append(self.xml_data_space)
        xml_data.append(self.xml_data_space)
        xml_data.append(self.xml_data_B)

        expected_result = 5.0
        actual_result = VincentExtractor.get_space_size(self, xml_data)

        self.assertTrue(expected_result == actual_result)

    def test_immediate_exit(self):
        xml_data = []

        xml_data.append(self.xml_data_space)
        expected_result = 13.0
        actual_result = VincentExtractor.get_space_size(self, xml_data)

        self.assertTrue(expected_result == actual_result)

    # GS-4
    def test_xml_none(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        xml_data = None
        expected_result = 0.0
        actual_result = VincentExtractor.get_space_size(self, xml_data)
        sys.stdout = sys.__stdout__
        self.assertTrue(expected_result == actual_result)

    # GS-5
    def test_xml_empty(self):
        xml_data = []
        expected_result = 13.0
        actual_result = VincentExtractor.get_space_size(self, xml_data)
        self.assertTrue(expected_result == actual_result)

    # GS-6
    def test_xml_no_space(self):
        xml_data = []
        xml_data.append(XMLData("b", 270.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))
        expected_result = 13.0
        actual_result = VincentExtractor.get_space_size(self, xml_data)
        self.assertTrue(expected_result == actual_result)

    # GS-7
    def test_xml_only_bold(self):
        xml_data = []
        xml_data.append(XMLData("b", 270.0, 10.0, "Bold", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Bold", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Bold", 23.0, False, True))
        expected_result = 13.0
        actual_result = VincentExtractor.get_space_size(self, xml_data)
        self.assertTrue(expected_result == actual_result)

    # GS-8
    def test_false_on_space(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 100.0, "Font", 23.0, False, True))
        expected_result = 0.0
        actual_result = VincentExtractor.get_space_size(self, xml_data)
        self.assertTrue(expected_result == actual_result)

    # GS-9
    def test_false_on_second_space(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 100.0, "Font", 23.0, False, True))
        expected_result = 0.0
        actual_result = VincentExtractor.get_space_size(self, xml_data)
        self.assertTrue(expected_result == actual_result)

        tured_output = io.StringIO()

    # NOTE These tests are unchanged from the Vincent Tests.
    # =========================== check_for_repeated_phrases Tests ===================================
    def test_reach_list_end_immediately(self):
        xml_data = []
        xml_data.append(self.xml_data_space)

        expected_result = 1
        actual_result = VincentExtractor.check_for_repeated_phrases(self, xml_data, 1)

        self.assertTrue(expected_result == actual_result)

    def test_removed_character(self):
        xml_data = []
        xml_data.append(self.xml_data_y_1)
        xml_data.append(self.xml_data_y_2)
        xml_data.append(self.xml_data_y_3)

        expected_result = 2.0
        actual_result = VincentExtractor.check_for_repeated_phrases(self, xml_data, 0)

        self.assertTrue(expected_result == actual_result)

    def test_immediate_different_line(self):
        xml_data = []
        xml_data.append(self.xml_data_y_1)
        xml_data.append(self.xml_data_space)

        expected_result = 1.0
        actual_result = VincentExtractor.check_for_repeated_phrases(self, xml_data, 0)

        self.assertTrue(expected_result == actual_result)

    def test_double_loop(self):
        xml_data = []
        xml_data.append(self.xml_data_y_1)
        xml_data.append(self.xml_data_y_1)
        xml_data.append(self.xml_data_y_1)
        xml_data.append(self.xml_data_space)

        expected_result = 3.0
        actual_result = VincentExtractor.check_for_repeated_phrases(self, xml_data, 0)

        self.assertTrue(expected_result == actual_result)

    # RP5
    def test_repeated_xml_none(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        xml_data = None
        expected_result = 0.0
        actual_result = VincentExtractor.check_for_repeated_phrases(self, xml_data, 0)
        sys.stdout = sys.__stdout__
        self.assertTrue(expected_result == actual_result)

    # RP6
    def test_xml_empty(self):
        xml_data = []
        expected_result = 0.0
        actual_result = VincentExtractor.check_for_repeated_phrases(self, xml_data, 0)
        self.assertTrue(expected_result == actual_result)

    # RP7
    def test_false_on_size(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 10.0, 10.0, "Font", 24.0, False, True))
        expected_result = 1
        actual_result = VincentExtractor.check_for_repeated_phrases(self, xml_data, 0)
        self.assertTrue(expected_result == actual_result)

    # RP8
    def test_false_on_font(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 24.0, False, True))
        xml_data.append(XMLData("b", 10.0, 10.0, "NotFont", 24.0, False, True))
        expected_result = 1
        actual_result = VincentExtractor.check_for_repeated_phrases(self, xml_data, 0)
        self.assertTrue(expected_result == actual_result)

    # RP9
    def test_false_on_y_gap(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 24.0, False, True))
        xml_data.append(XMLData("b", 10.0, 100.0, "Font", 24.0, False, True))
        expected_result = 1
        actual_result = VincentExtractor.check_for_repeated_phrases(self, xml_data, 0)
        self.assertTrue(expected_result == actual_result)

    # RP10
    def test_true_on_end(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        expected_result = 2
        actual_result = VincentExtractor.check_for_repeated_phrases(self, xml_data, 0)
        self.assertTrue(expected_result == actual_result)

    # NOTE Same as the Vincent Tests.
    # ======================== add_sentences Tests ========================================
    def test_return_empty_String(self):
        letter = self.xml_data_space
        next_sentence = "Hello"
        p = VincentExtractor()

        expected_result = ""
        actual_result = p.add_sentence(next_sentence, letter)
        self.assertTrue(expected_result == actual_result)

    # AD2
    def test_add_sentence(self):
        letter = XMLData("b", 10.0, 10.0, "Font", 23.0, True, False)
        next_sentence = "aaa"
        p = VincentExtractor()
        expected_result = ["aaab"]
        actual_result = p.test_add_sentence(next_sentence, letter)
        self.assertTrue(expected_result == actual_result)

    # AD3
    def test_add_empty_next_sentence(self):
        letter = XMLData("b", 10.0, 10.0, "Font", 23.0, True, False)
        next_sentence = ""
        p = VincentExtractor()
        expected_result = ["b"]
        actual_result = p.test_add_sentence(next_sentence, letter)
        self.assertTrue(expected_result == actual_result)

    # AD4
    def test_none_next_sentence(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output

        letter = XMLData("b", 10.0, 10.0, "Font", 23.0, True, False)
        next_sentence = None
        p = VincentExtractor()
        expected_result = []
        actual_result = p.test_add_sentence(next_sentence, letter)

        sys.stdout = sys.__stdout__

        self.assertTrue(expected_result == actual_result)

    # AD5
    def test_letter_none(self):
        next_sentence = "aaa"
        letter = None
        p = VincentExtractor()
        expected_result = ["aaa"]
        actual_result = p.test_add_sentence(next_sentence, letter)
        self.assertTrue(expected_result == actual_result)

    # ======================== remove_bad_sentences Test ==================================

    # RS1
    def test_one_character_rb(self):
        sentences = ["a   "]
        expected_result = ["a   "]
        v = VincentExtractor()
        actual_result = v.call_remove(sentences)

        self.assertEqual(expected_result, actual_result)

    # RS2
    def test_empty_sentences_rb(self):
        sentences = [""]
        expected_result = []
        v = VincentExtractor()
        actual_result = v.call_remove(sentences)

        self.assertEqual(expected_result, actual_result)

    # RS3
    def test_empty_empty_rb(self):
        sentences = []
        expected_result = []
        v = VincentExtractor()
        actual_result = v.call_remove(sentences)

        self.assertEqual(expected_result, actual_result)
    
    # RS4
    def test_empty_two_characters_rb(self):
        sentences = ["ab  "]
        expected_result = ["ab  "]
        v = VincentExtractor()
        actual_result = v.call_remove(sentences)

        self.assertEqual(expected_result, actual_result)

    # RS5
    def test_less_than_three_rb(self):
        sentences = ["a "]
        expected_result = []
        v = VincentExtractor()
        actual_result = v.call_remove(sentences)

        self.assertEqual(expected_result, actual_result)

    # RS6
    def test_one_remove_rb(self):
        sentences = ["a"]
        expected_result = []
        v = VincentExtractor()
        actual_result = v.call_remove(sentences)

        self.assertEqual(expected_result, actual_result)

    # RS7
    def test_triple_letter_rb(self):
        sentences = ["aaa"]
        expected_result = ["aaa"]
        v = VincentExtractor()
        actual_result = v.call_remove(sentences)

        self.assertEqual(expected_result, actual_result)
        
    # RS8
    def test_empty_rb(self):
        sentences = [""]
        expected_result = []
        v = VincentExtractor()
        actual_result = v.call_remove(sentences)

        self.assertEqual(expected_result, actual_result)

    # ========================= create_sentences Test =================================
    
    # CS1
    def test_empty_list_cs(self):
        xml_data = []
        v = VincentExtractor()
        expected_result = []
        actual_result = v.create_sentences(xml_data)

        self.assertEqual(expected_result, actual_result)
    
    # CS2 - Uses the default data as is.
    def test_remove_header_cs(self):
        xml_data = self.xml_data_list
        xml_data[0].b_y = 781.0
        v = VincentExtractor()
        expected_result = ["bbb"]
        actual_result = v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS3
    def test_remove_footer_cs(self):
        xml_data = self.xml_data_list
        xml_data[0].b_y = 49
        v = VincentExtractor()
        expected_result = ["bbb"]
        actual_result = v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS4
    def test_three_gap_add(self):
        xml_data = self.xml_data_list
        xml_data[1].character = " "
        xml_data[2].character = " "
        xml_data[3].character = " "
        xml_data[4].character = "b"
        xml_data[4].b_y = 60
        xml_data[5].b_y = 70.0
        xml_data[7].b_x = 150.0
        xml_data.append(XMLData(" ", 160.0, 60.0, "Font", 23.0, False, True))
        v = VincentExtractor()
        expected_result = ["a   b"]
        actual_result = v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS5
    def test_three_bracket_cs(self):
        xml_data = self.xml_data_list
        xml_data[0].character = "("
        xml_data[1].character = " "
        xml_data[2].character = " "
        xml_data[3].character = " "
        xml_data[4].character = ")"
        xml_data.append(XMLData(" ", 170.0, 60.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 180.0, 60.0, "Font", 23.0, False, True))
        expected_result = ["(   ) "]
        actual_result = self.v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS6
    def test_two_bracket_cs(self):
        xml_data = self.xml_data_list
        xml_data[0].character = "("
        xml_data[1].character = " "
        xml_data[2].character = " "
        xml_data[3].character = ")"
        xml_data.append(XMLData(" ", 170.0, 60.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 180.0, 60.0, "Font", 23.0, False, True))
        expected_result = ["(  ) "]
        actual_result = self.v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS7
    def test_one_bracket_cs(self):
        xml_data = self.xml_data_list
        xml_data[0].character = "("
        xml_data[1].character = " "
        xml_data[2].character = ")"
        xml_data[3].character = " "
        xml_data.append(XMLData(" ", 170.0, 60.0, "Font", 23.0, False, True))
        expected_result = ["( ) "]
        actual_result = self.v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS8
    def test_no_space_cs(self):
        xml_data = self.xml_data_list
        xml_data[2].character = " "
        xml_data[3].character = " "
        expected_result = ["ab  "]
        actual_result = self.v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS9
    def test_two_gap_add_cs(self):
        xml_data = self.xml_data_list
        xml_data[2].character = " "
        xml_data[4].character = " "
        xml_data[5].character = "c"
        xml_data[5].b_x = 176.0
        xml_data[6].b_x = 170.0
        xml_data[7].b_x = 190.0
        expected_result = ["ab b"]
        actual_result = self.v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS10
    def test_bracket_no_gap_cs(self):
        xml_data = self.xml_data_list
        xml_data[0].character = "("
        xml_data[2].character = ")"
        xml_data[3].character = " "
        xml_data[4].b_x = 120.0
        xml_data[5].b_x = 176.0
        expected_result = ["(b) "]
        actual_result = self.v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS11
    def test_decimal_add_cs(self):
        xml_data = self.xml_data_list
        xml_data[0].character = "."
        xml_data[2].character = "."
        xml_data[3].character = " "
        xml_data[4].b_x = 120.0
        xml_data[5].b_x = 176.0
        expected_result = [".b."]
        actual_result = self.v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS12
    def test_doule_decimal_cs(self):
        xml_data = self.xml_data_list
        xml_data[0].character = "."
        xml_data[1].character = "."
        xml_data[2].b_y = 70.0
        xml_data[3].character = " "
        xml_data[4].b_x = 120.0
        xml_data[5].b_x = 176.0
        expected_result = ["b"]
        actual_result = self.v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS13
    def test_semi_cs(self):
        xml_data = self.xml_data_list
        xml_data[0].character = "("
        xml_data[1].character = ")"
        xml_data[2].character = ";"
        xml_data[3].character = " "
        xml_data[4].b_x = 120.0
        xml_data[5].b_x = 176.0
        expected_result = ["();"]
        actual_result = self.v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS13
    def test_semi_cs(self):
        xml_data = self.xml_data_list
        xml_data[0].character = "("
        xml_data[1].character = ";"
        xml_data[2].character = ")"
        xml_data[3].character = " "
        xml_data[4].b_x = 120.0
        xml_data[5].b_x = 176.0
        expected_result = ["(;) "]
        actual_result = self.v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # CS14
    def test_none_cs(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        xml_data = None
        expected_result = []
        actual_result = self.v.create_sentences(xml_data)

        sys.stdout = sys.__stdout__

        self.assertEqual(expected_result, actual_result)

    # CS15
    def test_too_short_sentence_cs(self):
        xml_data = self.xml_data_list
        xml_data[0].character = "("
        xml_data[1].character = ")"
        xml_data[2].character = " "
        xml_data[2].b_y = 100.0
        xml_data[2].b_x = 500.0
        xml_data[3].character = " "
        xml_data[4].b_x = 120.0
        xml_data[5].b_x = 176.0
        expected_result = ["() "]
        actual_result = self.v.create_sentences(xml_data)
        self.assertEqual(expected_result, actual_result)

    # Functions for create_sentences.
    def add_three_gap(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 100.0, "Font", 23.0, False, True))
        return xml_data

    def add_two_gap(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 100.0, "Font", 23.0, False, True))
        return xml_data
