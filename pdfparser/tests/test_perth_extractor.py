from django.test import TestCase

from pdfparser.PerthExtractor import PerthExtractor
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


    def test_pass_valid_class_fields(self):
        pass
        #x = 5
        
        #self.assertTrue(x != x)

    # =============================== GET_SPACE_SIZE Tests ============================
    def test_finding_space_gap(self):
        xml_data = []
        xml_data.append(self.xml_data_space)
        xml_data.append(self.xml_data_B)

        expected_result = 5.0
        actual_result = PerthExtractor.get_space_size(self, xml_data)

        self.assertTrue(expected_result == actual_result)

    def test_execute_false_if(self):
        xml_data = []

        xml_data.append(self.xml_data_space)
        xml_data.append(self.xml_data_space)
        xml_data.append(self.xml_data_B)

        expected_result = 5.0
        actual_result = PerthExtractor.get_space_size(self, xml_data)

        self.assertTrue(expected_result == actual_result)

    def test_immediate_exit(self):
        xml_data = []

        xml_data.append(self.xml_data_space)
        expected_result = 13.0
        actual_result = PerthExtractor.get_space_size(self, xml_data)

        self.assertTrue(expected_result == actual_result)

    # GS-4
    def test_xml_none(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        xml_data = None
        expected_result = 0.0
        actual_result = PerthExtractor.get_space_size(self, xml_data)
        sys.stdout = sys.__stdout__
        self.assertTrue(expected_result == actual_result)

    # GS-5
    def test_xml_empty(self):
        xml_data = []
        expected_result = 13.0
        actual_result = PerthExtractor.get_space_size(self, xml_data)
        self.assertTrue(expected_result == actual_result)

    # GS-6
    def test_xml_no_space(self):
        xml_data = []
        xml_data.append(XMLData("b", 270.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))
        expected_result = 13.0
        actual_result = PerthExtractor.get_space_size(self, xml_data)
        self.assertTrue(expected_result == actual_result)

    # GS-7
    def test_xml_only_bold(self):
        xml_data = []
        xml_data.append(XMLData("b", 270.0, 10.0, "Bold", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Bold", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Bold", 23.0, False, True))
        expected_result = 13.0
        actual_result = PerthExtractor.get_space_size(self, xml_data)
        self.assertTrue(expected_result == actual_result)

    # GS-8
    def test_false_on_space(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 100.0, "Font", 23.0, False, True))
        expected_result = 0.0
        actual_result = PerthExtractor.get_space_size(self, xml_data)
        self.assertTrue(expected_result == actual_result)

    # GS-9
    def test_false_on_second_space(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 100.0, "Font", 23.0, False, True))
        expected_result = 0.0
        actual_result = PerthExtractor.get_space_size(self, xml_data)
        self.assertTrue(expected_result == actual_result)

        tured_output = io.StringIO()

    # =========================== check_for_repeated_phrases Tests ===================================
    def test_reach_list_end_immediately(self):
        xml_data = []
        xml_data.append(self.xml_data_space)

        expected_result = 1
        actual_result = PerthExtractor.check_for_repeated_phrases(self, xml_data, 1)

        self.assertTrue(expected_result == actual_result)

    def test_removed_character(self):
        xml_data = []
        xml_data.append(self.xml_data_y_1)
        xml_data.append(self.xml_data_y_2)
        xml_data.append(self.xml_data_y_3)

        expected_result = 2.0
        actual_result = PerthExtractor.check_for_repeated_phrases(self, xml_data, 0)

        self.assertTrue(expected_result == actual_result)

    def test_immediate_different_line(self):
        xml_data = []
        xml_data.append(self.xml_data_y_1)
        xml_data.append(self.xml_data_space)

        expected_result = 1.0
        actual_result = PerthExtractor.check_for_repeated_phrases(self, xml_data, 0)

        self.assertTrue(expected_result == actual_result)

    def test_double_loop(self):
        xml_data = []
        xml_data.append(self.xml_data_y_1)
        xml_data.append(self.xml_data_y_1)
        xml_data.append(self.xml_data_y_1)
        xml_data.append(self.xml_data_space)

        expected_result = 3.0
        actual_result = PerthExtractor.check_for_repeated_phrases(self, xml_data, 0)

        self.assertTrue(expected_result == actual_result)

    # RP5
    def test_repeated_xml_none(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        xml_data = None
        expected_result = 0.0
        actual_result = PerthExtractor.check_for_repeated_phrases(self, xml_data, 0)
        sys.stdout = sys.__stdout__
        self.assertTrue(expected_result == actual_result)

    # RP6
    def test_xml_empty(self):
        xml_data = []
        expected_result = 0.0
        actual_result = PerthExtractor.check_for_repeated_phrases(self, xml_data, 0)
        self.assertTrue(expected_result == actual_result)

    # RP7
    def test_false_on_size(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 10.0, 10.0, "Font", 24.0, False, True))
        expected_result = 1
        actual_result = PerthExtractor.check_for_repeated_phrases(self, xml_data, 0)
        self.assertTrue(expected_result == actual_result)

    # RP8
    def test_false_on_font(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 24.0, False, True))
        xml_data.append(XMLData("b", 10.0, 10.0, "NotFont", 24.0, False, True))
        expected_result = 1
        actual_result = PerthExtractor.check_for_repeated_phrases(self, xml_data, 0)
        self.assertTrue(expected_result == actual_result)

    # RP9
    def test_false_on_y_gap(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 24.0, False, True))
        xml_data.append(XMLData("b", 10.0, 100.0, "Font", 24.0, False, True))
        expected_result = 1
        actual_result = PerthExtractor.check_for_repeated_phrases(self, xml_data, 0)
        self.assertTrue(expected_result == actual_result)

    # RP10
    def test_true_on_end(self):
        xml_data = []
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        expected_result = 2
        actual_result = PerthExtractor.check_for_repeated_phrases(self, xml_data, 0)
        self.assertTrue(expected_result == actual_result)

    # ======================== add_sentences Tests ========================================
    def test_return_empty_String(self):
        letter = self.xml_data_space
        next_sentence = "Hello"
        p = PerthExtractor()

        expected_result = ""
        actual_result = p.add_sentence(next_sentence, letter)
        self.assertTrue(expected_result == actual_result)

    # AD2
    def test_add_sentence(self):
        letter = XMLData("b", 10.0, 10.0, "Font", 23.0, True, False)
        next_sentence = "aaa"
        p = PerthExtractor()
        expected_result = ["aaab"]
        actual_result = p.test_add_sentence(next_sentence, letter)
        self.assertTrue(expected_result == actual_result)

    # AD3
    def test_add_empty_next_sentence(self):
        letter = XMLData("b", 10.0, 10.0, "Font", 23.0, True, False)
        next_sentence = ""
        p = PerthExtractor()
        expected_result = ["b"]
        actual_result = p.test_add_sentence(next_sentence, letter)
        self.assertTrue(expected_result == actual_result)

    # AD4
    def test_none_next_sentence(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output

        letter = XMLData("b", 10.0, 10.0, "Font", 23.0, True, False)
        next_sentence = None
        p = PerthExtractor()
        expected_result = []
        actual_result = p.test_add_sentence(next_sentence, letter)

        sys.stdout = sys.__stdout__

        self.assertTrue(expected_result == actual_result)

    # AD5
    def test_letter_none(self):
        next_sentence = "aaa"
        letter = None
        p = PerthExtractor()
        expected_result = ["aaa"]
        actual_result = p.test_add_sentence(next_sentence, letter)
        self.assertTrue(expected_result == actual_result)

    # ======================== remove_bad_sentences Test ==================================
    # RS1
    def test_remove_short_sentence(self):
        sentences = []
        sentences.append("ab")
        expected_result = []
        actual_result = PerthExtractor.call_remove(self, sentences)

        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # RS2
    def test_empty_sentences(self):
        sentences = []

        expected_result = []
        actual_result = PerthExtractor.call_remove(self, sentences)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # RS3
    def test_only_spaces(self):
        sentences = []
        sentences.append("    ")
        expected_result = sentences
        actual_result = PerthExtractor.call_remove(self, sentences)
        self.assertTrue(expected_result == actual_result)

    # RS4
    def test_two_words_no_removal(self):
        sentences = []
        sentences.append("aaaa")
        sentences.append("bbbb")
        expected_result = sentences
        actual_result = PerthExtractor.call_remove(self, sentences)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # RS5
    def test_one_length(self):
        sentences = []
        sentences.append("a")
        expected_result = []
        actual_result = PerthExtractor.call_remove(self, sentences)
        self.assertTrue(actual_result == expected_result)
        
    # ========================= create_sentences Test =================================
    
    # Checked.
    def test_dont_enter_while(self):
        xml_data = []
        xml_data.append(XMLData("", 10.0, 15.0, "Font", 25.0, False, True))
        xml_data.append(XMLData("", 10.0, 15.0, "Font", 25.0, False, True))
        expected_result = []
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_remove_header(self):
        xml_data = self.add_three_gap()
        xml_data.append(XMLData("", 10.0, 775.0, "Font", 23.0, False, True))
        xml_data.insert(0, XMLData("", 10.0, 775.0, "Font", 23.0, False, True))

        expected_result = []
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_remove_footer(self):
        xml_data = self.add_three_gap()
        xml_data.append(XMLData("", 10.0, 49.0, "Font", 23.0, False, True))
        xml_data.insert(0, XMLData("", 10.0, 49.0, "Font", 23.0, False, True))

        expected_result = []
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))


    # Checked.
    def test_add_on_three_gap(self):
        xml_data = self.add_three_gap()
        xml_data.append(XMLData("a", 16.0, 100.0, "Font", 23.0, False, True))
        xml_data.insert(0, XMLData("a", 10.0, 100.0, "Font", 23.0, False, True))

        expected_result = []
        expected_result.append("a")
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_skip_on_three_gap(self):
        xml_data = self.add_three_gap()
        xml_data.append(XMLData("a", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.insert(0, XMLData("a", 10.0, 100.0, "Font", 23.0, False, True))
        
        expected_result = []
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_add_on_two_gap(self):
        xml_data = self.add_two_gap()
        xml_data.insert(0, XMLData("a", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 26.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 770.0, 100.0, "Font", 23.0, False, True))

        expected_result = []
        expected_result.append("a")
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_skip_on_two_gap(self):
        xml_data = self.add_two_gap()
        xml_data.insert(0, XMLData("a", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 16.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 770.0, 100.0, "Font", 23.0, False, True))

        expected_result = []
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_add_on_one_gap(self):
        xml_data = []
        xml_data.append(XMLData("a", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 26.0, 15.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        
        expected_result = ["a"]
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_skip_on_one_gap(self):
        xml_data = []
        xml_data.append(XMLData("a", 501.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 30.0, 15.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        
        expected_result = []
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_skip_add_one_gap(self):
        xml_data = []
        xml_data.append(XMLData("a", 100.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 30.0, 15.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        
        expected_result = ["a"]
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test__add_one_gap(self):
        xml_data = []
        xml_data.append(XMLData("a", 100.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))
        
        expected_result = ["a"]
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_second_skip_one_gap(self):
        xml_data = []
        xml_data.append(XMLData("a", 100.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 270.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))
        
        expected_result = []
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_second_add_one_gap(self):
        xml_data = []
        xml_data.append(XMLData(".", 100.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 270.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))
        
        expected_result = ["."]
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_third_skip_one_gap(self):
        xml_data = []
        xml_data.append(XMLData(".", 100.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 270.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))
        
        expected_result = []
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_two_gap_add(self):
        #xml_data = self.add_two_gap()
        xml_data = []
        xml_data.append(XMLData("A", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 26.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 26.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))
        
        expected_result = []
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # Checked.
    def test_skip_all_gaps(self):
        xml_data = []
        xml_data.append(XMLData(".", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("a", 270.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 26.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 10.0, "Font", 23.0, False, True))

        expected_result = []
        p = PerthExtractor()

        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # CS17
    def test_add_sentence_add_letter(self):
        xml_data = []
        xml_data.append(XMLData("a", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(".", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("z", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("z", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("z", 10.0, 100.0, "Font", 23.0, False, True))

        p = PerthExtractor()
        expected_result = ["abcd."]
        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # CS18
    def test_create_sentences_none(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output

        xml_data = None
        p = PerthExtractor()
        expected_result = []
        actual_result = p.create_sentences(xml_data)

        sys.stdout = sys.__stdout__

        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # CS19
    def test_remove_header_base(self):
        xml_data = []
        xml_data.append(XMLData("a", 800.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(".", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("z", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("z", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("z", 10.0, 100.0, "Font", 23.0, False, True))

        p = PerthExtractor()
        expected_result = ["bcd."]
        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # CS20
    def test_create_xml_empty(self):
        xml_data = []
        p = PerthExtractor()
        expected_result = []
        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

    # CS21
    def test_create_remove_footer(self):
        xml_data = []
        xml_data.append(XMLData("a", 10.0, 10.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("b", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("c", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("d", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(".", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData(" ", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("z", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("z", 10.0, 100.0, "Font", 23.0, False, True))
        xml_data.append(XMLData("z", 10.0, 100.0, "Font", 23.0, False, True))

        p = PerthExtractor()
        expected_result = ["bcd."]
        actual_result = p.create_sentences(xml_data)
        self.assertTrue(all(elem in expected_result for elem in actual_result))

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
