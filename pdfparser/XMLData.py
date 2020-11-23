"""
    This class stores data extracted from XML Documents. It will be used by Council Extractor
    type Classes to parse data further.

    character:
        The character/letter that was processed.

    b_x:
        The b_box x value of the bottom right corner of the character.

    b_y:
        The b_box y value of the bottom right corner of the character.

    font:
        The font of the character.

    size:
        The size of the character.

    bold:
        A boolean stating whether the character was bolded or not.

    italics:
        A boolean stating whether the character was italicized.

    valid:
        A boolean representing whether or not valid data was passed in, with false meaning 
        invalid data.
"""

class XMLData(object):
    def __init__ (self, in_character, in_b_x, in_b_y, in_font, in_size, in_bold, in_italics):
        valid = True
        if isinstance(in_character, str):
            self.character = in_character
        else:
            self.character = None
            valid = False

        if isinstance(in_b_x, float):
            self.b_x = in_b_x
        else:
            self.b_x = None
            valid = False

        if isinstance(in_b_y, float):
            self.b_y = in_b_y
        else:
            self.b_y = None
            valid = False
        
        if isinstance(in_font, str):
            self.font = in_font
        else:
            self.font = None
            valid = False

        if isinstance(in_size, float):
            self.size = in_size
        else:
            self.size = None
            valid = False

        if isinstance(in_bold, bool):
            self.bold = in_bold
        else:
            self.bold = None
            valid = False

        if isinstance(in_italics, bool):
            self.italics = in_italics
        else:
            self.italics = None
            valid = False

        self.valid = valid

    " A method that returns all the data in the XML Object as a String. "
    def print_all_data(self):
        output = "Character: %s || b_x: %s || b_y: %s || Font: %s || Size: %s || Bold: %s || Italics: %s" %\
        (self.character, self.b_x, self.b_y, self.font, self.size, self.bold, self.italics)
        return(output);

        #print("Character: ", self.character, " || b_x: ", self.b_x, " || b_y: ", self.b_y, " Font: ", self.font, "\n",
          #      " || Size: ", self.size, " || Bold: ", in_bold, " Italics: ", self.italics)

        
