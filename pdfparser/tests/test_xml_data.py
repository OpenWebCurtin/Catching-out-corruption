from django.test import TestCase

from pdfparser.XMLData import XMLData

class TestXMLData(TestCase):

    def setUp(self):
        self.xmldata1 = XMLData("a", 2.6, 5.2, "sans", 12.0, True, False)

    def test_print_all_data(self):
        xml_expected_output = """Character: a || b_x: 2.6 || b_y: 5.2 || Font: sans || Size: 12.0 || Bold: True || Italics: False"""
        self.assertTrue(self.xmldata1.print_all_data() == xml_expected_output)

    def test_character_expected(self):
        self.assertTrue(self.xmldata1.character == "a")

    def test_x_b_box_expected(self):
        self.assertTrue(self.xmldata1.b_x == 2.6)

    def test_x_y_box_expected(self):
        self.assertTrue(self.xmldata1.b_y == 5.2)


    def test_font_expected(self):
        self.assertTrue(self.xmldata1.font == "sans")

    def test_size_expected(self):
        self.assertTrue(self.xmldata1.size == 12.0)

    def test_bold_expected(self):
        self.assertTrue(self.xmldata1.bold)
    
    def test_italics_expected(self):
        self.assertFalse(self.xmldata1.italics)

    def test_character_invalid(self):
        xml_bad = XMLData(3, 344.22, 554.22, "Some Font", 24, True, True)
        self.assertFalse(xml_bad.valid)

    def test_character_none(self):
        xml_bad = XMLData(3, 344.22, 554.22, "Some Font", 24, True, True)
        self.assertTrue(xml_bad.character == None)

    def test_b_x_invalid(self):
        xml_bad = XMLData("a", 's', 554.22, "Some Font", 24, True, True)
        self.assertFalse(xml_bad.valid)

    def test_b_x_none(self):
        xml_bad = XMLData("a", 's', 554.22, "Some Font", 24, True, True)
        self.assertTrue(xml_bad.b_x == None)

    def test_b_y_invalid(self):
        xml_bad = XMLData("a", 344.22, 'y', "Some Font", 24, True, True)
        self.assertFalse(xml_bad.valid)

    def test_b_y_none(self):
        xml_bad = XMLData("a", 344.22, 'y', "Some Font", 24, True, True)
        self.assertTrue(xml_bad.b_y == None)

    def test_font_invalid(self):
        xml_bad = XMLData("a", 344.22, 544.22, 1, 24, True, True)
        self.assertFalse(xml_bad.valid)

    def test_font_none(self):
        xml_bad = XMLData("a", 344.22, 544.22, 1, 24, True, True)
        self.assertTrue(xml_bad.font == None)
    
    def test_size_invalid(self):
        xml_bad = XMLData("a", 344.22, 544.22, "Some Font", "Size", True, True)
        self.assertFalse(xml_bad.valid)

    def test_size_none(self):
        xml_bad = XMLData("a", 344.22, 544.22, "Some Font", "Size", True, True)
        self.assertTrue(xml_bad.size == None)
    
    def test_bold_invalid(self):
        xml_bad = XMLData("a", 344.22, 544.22, "Some Font", 24, "Bold", True)
        self.assertFalse(xml_bad.valid)

    def test_bold_none(self):
        xml_bad = XMLData("a", 344.22, 544.22, "Some Font", 24, "Bold", True)
        self.assertTrue(xml_bad.bold == None)

    def test_italics_invalid(self):
        xml_bad = XMLData("a", 344.22, 544.22, "Some Font", 24, True, "Italics")
        self.assertFalse(xml_bad.valid)

    def test_italics_none(self):
        xml_bad = XMLData("a", 344.22, 544.22, "Some Font", 24, True, "Italics")
        self.assertTrue(xml_bad.italics == None)
