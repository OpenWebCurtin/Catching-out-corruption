from pdfparser.CouncilExtractorFactory import CouncilExtractorFactory
from pdfparser.XMLData import XMLData

"""
    VincentExtractor class parses the extracrted XMLData specifically from Vincent Council Meeting Minutes documents.

    It will parse the XMLData and then return strings with the sentences reconstructed.

    NOTE: Commented out code will be implemented in the future.

    sentences: The Strings that are created using the data from xml_data.
    
    This class was refactored from the Perth Extractor class, completed by Leanna Papavassiliou, obtained through the OpenWeb Project.
"""

class VincentExtractor(CouncilExtractorFactory):

    def __init__(self):
        # This will be all the sentences that we send back, after they've been parsed
        self.sentences = []

    def create_sentences(self, xml_data):
        """ Create sentences from the XML data.

            Using the extracted data from the parsed XML document, re-create sentences to be sent to the 
            English Syntax Parser.

            Args:
                xml_data: An array containing the data that was previouslt extracted from an XML document.

            Returns:
                sentences: An array of the Strings that represent sentences.
        """
        #print(len(xml_data))

        #for thing in xml_data:
         #   print("FIRST: %s" %(thing.print_all_data(),))
        try:
            # Calculate the size of spaces in regular text.
            space_size = self.get_space_size(xml_data)

            current_position = 0

            next_sentence = ""

            # Continue looping through the xml_data[] until its 4 below its length
            while current_position + 4 < len(xml_data):

                # Gets the next letter in xml_data[]
                letter = xml_data[current_position]
                #print("CHARACTER: %s" %(letter.character))

                # Add in the checks to ignore a letter for perth if it appears in a certain section of
                # the screen (so a header or footer.
                # Remove the Header || was 770
                if(letter.b_y > 780.0):
                    #print("Skipped Header: %s"  %(letter.character))
                    # At this point it should go to the "remove_repeated_phrases", and make sure the 
                    current_position = self.check_for_repeated_phrases(xml_data, current_position);
                    # entire header is removed.

                # Remove the Footer
                elif (letter.b_y < 50):
                    current_position = self.check_for_repeated_phrases(xml_data, current_position);
                    #print("Skipped Footer: %s" %(letter.character))

                # else the character isn't in a header or a footer.
                else:

                    # Add to the current sentence if so far there's nothing to 
                    # suggest that the sentence shoud've finished

                    #character = letter.character
                    #if character == "\a" or character == "\b" or character == "\f" or character == "\r" or character == "\t" or character == "\v":
                     #   print("Bleh")
                    # Get the next letter after our current "letter"
                    next_letter = xml_data[current_position + 1]

                    # If the character isn't a full stop and the next letter is not a space, new line, or an empty line, then its a character that
                    # is likely continuing a sentence.
                    # Else its likely that the character is a full stop and signalling the end of a sentence.
                    """if letter.character != "." and (next_letter.character != " " or next_letter.character != "\n" 
                            or next_letter.character == ""):"""
                    if letter.character != "." and letter.character != ';':

                        # True if the next 3 characters are all " "
                        three_gap = (next_letter.character == " " and xml_data[current_position + 2].character == " " 
                                and xml_data[current_position + 3].character == " ")

                        # True if the next 2 characters are all " "
                        two_gap = (next_letter.character == " " and xml_data[current_position + 2].character == " ")

                        # True if the next character is a " "
                        one_gap = (next_letter.character == " ")

                        # There a three " ", then likely this current character is the last character in listed data, and should be treated
                        # as a new sentence.
                        if(three_gap == True):
                            if next_sentence.count('(') == next_sentence.count(')'):
                                x_gap = abs(letter.b_x - next_letter.b_x)

                                # Get the horizontal distance of the character 3 jumps ahead, and the character 4 jumps ahead
                                # if its smaller then or equal to 5 then its more likely continuing on the same horizontal line, and the 
                                # next_sentence should just be appended to.
                                # Else create a new sentence.
                                gap = abs(xml_data[current_position + 3].b_x - xml_data[current_position + 4].b_x)
                                if(gap <= 5):
                                    next_sentence = next_sentence + letter.character
                                else:
                                    next_sentence = self.add_sentence(next_sentence, letter)
                            else:
                                next_sentence = next_sentence + letter.character

                        # There are two " " in a row, the same logic as above applies, but the horizontal gap is larger,
                        # and the character are 2 jumps ahead, and 3 jumps ahead.
                        elif(two_gap == True):
                            if next_sentence.count('(') == next_sentence.count(')'):
                                gap = abs(xml_data[current_position + 2].b_x - xml_data[current_position + 3].b_x)
                                if(gap <= 15):
                                    next_sentence = next_sentence + letter.character
                                else:
                                    next_sentence = self.add_sentence(next_sentence, letter)
                            else:
                                next_sentence = next_sentence + letter.character

                        # There is only one character ahead in the xml_data[] that is a " "
                        elif(one_gap == True):
                            x_gap = abs(next_letter.b_x - xml_data[current_position + 2].b_x)
                            same_b_y = (next_letter.b_y == xml_data[current_position + 2].b_y)

                            # if the horizontal gap between the character 1 jump aheasd, and the one 2 jumps ahead is 
                            # <= 15 or > 400 OR has the same vertical position, then its either two characters in a word,
                            # the end of the page was reached and we've jumped down to the next line, or its just on the same line.
                            if next_sentence.count('(') == next_sentence.count(')'):
                                if((x_gap <= 15 or x_gap > 400) or same_b_y):
                                    next_sentence = next_sentence + letter.character
                                else:
                                    # If the character is near the edge of the right hand side of the page then continue the sentence.
                                    if(letter.b_x > 475):
                                        next_sentence = next_sentence + letter.character
                                    else:
                                        next_sentence = self.add_sentence(next_sentence, letter)
                            else:
                                next_sentence = next_sentence + letter.character

                        # There is not a " " in the next character.
                        else:
                            if next_sentence.count('(') == next_sentence.count(')'):
                                #print(HELLO)
                                #print(letter.character)
                                x_gap = abs(letter.b_x - next_letter.b_x)

                                # If the current letter and the next letter isn't on the same horizontal line or horizontal gap between them
                                # is less than 250, then they're likely from different sentences.
                                if(letter.b_y != next_letter.b_y and x_gap < 250):
                                    next_sentence = self.add_sentence(next_sentence, letter)
                                else:
                                    next_sentence = next_sentence + letter.character

                            else:
                                next_sentence = next_sentence + letter.character

                    # The character is a decimal point and the next character is a " ", or new line,
                    # then its a new sentence.
                    else: 
                        #print("RAAAR")
                        if letter.character != ";":
                            # Only create a new sentence if there is an equal number of open and closed brackets.
                            if next_sentence.count('(') == next_sentence.count(')'):
                                x_gap = abs(letter.b_x - next_letter.b_x)
                                if(next_letter.character == " " or next_letter.character == "\n" or letter.b_y != next_letter.b_y):
                                    next_sentence = self.add_sentence(next_sentence, letter)

                                else:
                                    #print("Letter: %s || Next Letter: %s" %(letter.character, next_letter.character))
                                    #if (letter.character != "." and next_letter.character != "."):
                                    if (next_letter.character != "."):
                                        #print("BMO")
                                        next_sentence = next_sentence + letter.character
                                    #else:
                                        

                                    #next_sentence = next_sentence + letter.character

                            else:
                                next_sentence = next_sentence + letter.character
                        else:
                            if next_sentence.count('(') == next_sentence.count(')'):
                                next_sentence = self.add_sentence(next_sentence, letter)
                            else:
                                next_sentence = next_sentence + letter.character


                    current_position = current_position + 1
                    #print("CURRENT_POSITION: %s" %(current_position))
                # End of While Loop
        except TypeError as e:
                print("Invalid parameter passed in %s" %(e.args))

            
        # Remove any lines if they don't have any characters or have a length of less that 3.
        self.remove_bad_sentences()
            

        # Print the created sentences for viewing/testing
        for line in self.sentences:
            pass
            #print(line)
            #print("\n===========================================\n")

        return self.sentences

    def remove_bad_sentences(self):
        try:
            has_character = False
            for line in self.sentences:

                has_character = False

                #if len(line) > 1:
                for character in line:
                    
                    if character != " " or character != "\n" or character != "":
                        has_character = True

                if has_character == False:
                    self.sentences.remove(line)
                #if has_space == False:
                    #print("No Char")
                    #print(line)
                if has_character == True and len(line) < 3:
                    self.sentences.remove(line)
        except TypeError as e:
            print("Invalid parameter passed: %s" %(e.args,))
        return self.sentences


    def call_remove(self, test_sentences):
        """ Only to be used for testing remove_bad_sentences.
        """
        self.sentences = []
        for line in test_sentences:
            self.sentences.append(line)

        new_sentences = self.remove_bad_sentences()
        return new_sentences



    def get_space_size(self, xml_data):

        # Get the size of the spaces between words. Return 0 if a none type is given.
        ii = 0
        space_size = 0.0

        # Find the length of a space character that is not in a header, and is not part of a title/table.
        found_space_size = False
        try:
            while found_space_size == False and ii < (len(xml_data)-1) and len(xml_data) > 0:
                # Only calculate the gap if the current character is a space, the next character isn't a space,
                # the next character does not contain "Bold" in its font (likely a title), and the next character's 
                # position is defintely not a footer text.
                if xml_data[ii].character == " " and xml_data[ii+1].character != " " and "Bold" not in xml_data[ii+1].font and xml_data[ii+1].b_y > 50:
                    found_space_size = True
                    space_size = abs(xml_data[ii + 1].b_x - xml_data[ii].b_x)
                ii += 1

            # if a "space" wasn't found, then just use a default 13, which is approximately the normal space size in Perth documents.
            if(found_space_size == False):
                space_size = 13.0
        except TypeError as e:
                print("None Type xml passed in %s " %(e.args))
                space_size = 0.0
        return space_size

    # This function will no longer be used.
    def form_table_data(self, potential_table_data):
        """ Flattens tables.

        If data is parsed that is suspected to be part of a table, it will be passed to this
        method which will attempt to flatten the tables.

        Args:
            potential_table_data: A list of XMLData that is believed to be part of a table.

        Returns:
            A List of Strings with the flattened table data or the original list that was 
            given if it was determined that the data was not part of a table.
        """
        print("This is making table data")

    # Instead of identifying a repeated phrase, just start processing in here when the letters are
    # in a certain aread (i.e. headers and footers)
    def check_for_repeated_phrases(self, xml_data, current_position):
        """ Removes certain repeated phrases.

            If a letter has its vertical position very high or very low on the page, then it is 
            likely a header or footer that should be skipped.

            Keep looping through xml_data until the next character isn't the same size, font, or 
            vertically close to the previous letter.

            Args:
                xml_data: The data from the extracted XML document.
                current_position: How far we have gone into xml_data.

            Returns:
                current_position: Return this to the current_position that is local to create_sentences, 
                so that the header and footer have been skipped.
        """

        try:
            if(current_position < len(xml_data)):
                found_font = xml_data[current_position].font
                found_size = xml_data[current_position].size
                found_y = xml_data[current_position].b_y

                current_position = current_position + 1
                letter = xml_data[current_position]
                y_gap = abs(found_y - letter.b_y)

                reached_end = False
                # was 20
                # y_gap < 20
                while(letter.size == found_size and letter.font == found_font and y_gap < 10 and reached_end == False):
                    #print("Skipped: %s || y position: %s || y gap: %s " %(letter.character, letter.b_y, y_gap))
                    if(current_position+1 == len(xml_data)):
                        reached_end = True
                    else:
                        current_position += 1
                        letter = xml_data[current_position]
                        y_gap = xml_data[current_position -1].b_y - letter.b_y
                        #print("REMOVE: %s" %(current_position))
        except TypeError as e:
            print("Invalid parameter passed in: %s" %(e.args))

        #print("CURRENT_POSITION: %s" %(current_position))
        return current_position
        

    
    def add_sentence(self, next_sentence, letter):
        """ Add a sentence to sentence vairable.

            Add the current next_sentence to the sentences global variable and return "",
            this will be used to set next_sentence back to ""

            Args:
                next_sentence: the sentence that has been created thus far.
                letter: Use it to get the final letter to add to next_sentnece.

            Returns:
                "": The only variable using the return of this function is the next_sentence variable local to create_sentences.

        """ 
        try:
            if (letter != None):
                next_sentence = next_sentence + letter.character
                self.sentences.append(next_sentence)
            else:
                self.sentences.append(next_sentence)
        except TypeError as e:
            print("Invalid parameter passed in: %s" %(e.args))

        return ""

    # Use this fucntion only to test add_sentences
    def test_add_sentence(self, next_sentence, letter):
        self.sentences = []
        self.add_sentence(next_sentence, letter)
        return self.sentences

        
    """
    If the next letter after a word is a different y value, with a space 
    """
    def check_ahead(self):
        pass
