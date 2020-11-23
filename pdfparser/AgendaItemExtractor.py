class AgendaExtractor(object):
    """
        AgendaExtractor is an interface to be inherited from by the AgendaItemExtractor 
        Class so it can implement teh Dependency Injection Pattern.
    """
    def parse(self): pass

'''
TODO
    When you come back here, remove the print loop with xml_data, and 
    make a call to the factory class.

    Needs another method to determine which factory to make, need to see in the xml doc what I can see
    from that, the xml doc should be named after the council its from.

    Find a way to pass the XML documents name into the Handler class
'''

'''
NOTE:
    For every keyword tagged out, I need to search through all the sentences returned from the 
    Extractor to see how many times it appears.
    However keywords will return multiple times, should the AIE have a function to ignore 
    duplicates on a per agenda item basis?
'''

import xml.sax
from os import path
from pdfparser.XMLData import XMLData
from pdfparser.ExtractedData import ExtractedData
from pdfparser.CouncilExtractorFactory import CouncilExtractorFactory
from pdfparser.PerthExtractor import PerthExtractor
from pdfparser.VincentExtractor import VincentExtractor
from pdfparser.nlp_spacy import nlp_spacy

from esp.esp import esp
#from pdfparser.insert import insert

#imports for database
from datetime import datetime
import pytz

import sys, os
"""sys.path.append(os.path.abspath('../esp'))
"""

# import from the database
#sys.path.append(os.path.abspath('../database'))
import database
#from database.models import *
from database.insert import insert


class AgendaItemExtractor ( xml.sax.ContentHandler, AgendaExtractor ):
    """
        This class will:
            1. Take an XML File.
            2. Extract Data, creating a list of XMLData objects from the XML File.
            3. Determine which council the minutes document is for.
            4. Send the XMLData to a CouncilExtractor of the Council its from.
            5. Retreive a list of Strings from the CouncilExtractor.
            6. Send the list of Strings to the English Syntax Parser.
            7. Retrieve the tagged data and send it to the database.

        Attributes:
            current_char: The current character we are processing from the XML document.
            b_box: A String representing the position of the character in the PDF document.
            font: A String representing the font of the current character.
            size: A float representing the size of the current character.
            bold: A Boolean representing whether the character was boldened or not.
            italics: A Boolean reprsenting whether the character is in italics or not.
            extractor: The CouncilExtractor that will parse the list of XMLData.

    """

    # Needs to be passed the dependency injection of the File Manager, ESP, and Database Interface.
    # Currently it does not look like anyone else has been implementing the Dependency Injection Pattern.
    def __init__(self):
        self.tag=""
        self.document_name = ""
        self.agenda_code = ""
        # Letter/XMLData fields
        self.current_char = ""
        self.b_box = ""
        self.font = ""
        self.size = 0
        self.bold = False
        self.italics = False
        self.extractor = None


        # This is the compilations of all sentences
        self.sentences = []

        # List for the data extracted from the XML document, 
        # this will be passed to a Council Parser
        self.xml_data = []

        # This is the next sentence being made, it will be added to sentences
        self.next_sentence = ""

        # Stores the agenda's name
        self.file_name = ""

    

    # For letter that gets parsed, this is where we will get the actual attributes
    def startElement(self, tag, attributes):
        """At the start of every element, run this function.

        This function will check if the current line in the XML document if of 
        a "text" type AND has the b_box attribute. This guarentees that this particular line 
        in the XML document is an actual character, so its safe to store the current line's
        attributes in the Class's attributes.

        Args:
            tag: The tag of the XML line (e.g. "text", "text_box")
            attributes: A List of all the attributes from the current XML line.

        Returns:
            Void.

        """

        # 1
        # Here we get all the data we can from the XML
        # If its a text tag, we want the content
        if (tag == "text"):
            # but only if it has a bbox value
            if "bbox" in attributes:
                self.b_box = attributes["bbox"]
                self.tag = tag
                self.font = attributes["font"]
                self.size = float(attributes["size"])
                self.bold = "Bold" in attributes["font"]
                self.italics = "Italic" in attributes["font"]
                

    def characters(self, content):
        """ For each character, add it to the XMLData list.

            Parse out the data from each line in the XML document if it has a character.
            If any invalid data is passed to XMLData class, skip that character.

            Args:
                content: The character that is being parsed.

            Returns:
                Void
        """
        if (self.tag == "text" and self.b_box != ""):
            self.current_char = content


            b_box_values = self.process_b_box((self.b_box))

            ' Commented this out, just for now - Pushed back 19 lines'
            #if not "\n" in content:
            if "\n" not in content:
                    #print("Keep the \n")
                next_letter = XMLData(content, b_box_values[0], b_box_values[1], self.font, 
                                        self.size, self.bold, self.italics)
                if(next_letter.valid == True):
                    self.xml_data.append(next_letter)

            else: # It is a \n

                if(len(self.xml_data) > 1):
                    # If the previous letter was a \n keep it, else, ignore // Used to be a "." that we check to keep it
                    if (self.xml_data[-1]).character == "\n":
                        next_letter = XMLData(content, b_box_values[0], b_box_values[1], self.font, 
                                                self.size, self.bold, self.italics)
                        
                        if(next_letter.valid == True):
                            self.xml_data.append(next_letter)


            self.next_sentence = self.next_sentence + content

            # If we reach a full stop then finish the sentence and add it to sentences
            if content == ".":
                self.sentences.append(self.next_sentence)
                self.next_sentence = ""

            #print(self.current_char);
            #print("Goodbye");

    # Given the b_box String, this will parse them out to get the
    # two individual numbers and pass them back as an array of length 2
    def process_b_box(self, b_box):
        """ Parse out the values from the b_box String.

            Extract the first x and y b_box values from the b_box String.
            Only extract it if the b_box String has 4 values, doesn't contain a negative, and 
            isn't an empty String.

            Returns:
                b_box_number: A list of length 2, with the x_b_box value and the y_b_box value.
        """
        try:
            position = b_box.split(',')
            b_box_number = [None] * 2

            # If b_box is passed in with bad data just return None, catch it in character, to skip the rest of the letter
            if b_box != "" and b_box.count(",") == 3 and "-" not in b_box:
                for ii in range(2):
                    position[ii].strip(" ");
                    position[ii].replace(" ", "")
                    b_box_number[ii] = float(position[ii])
            else:
                b_box_number = None
        except AttributeError as e:
            b_box_number = None
            #print("Invalid b_box string was parsed from the XML document: %s" %(e.args))

        return b_box_number

    def endDocument(self):
        """Execute once the whole XML file has been processed.
        
        After the XMLData has been extracted, send it to a Council Extractor,
        then pass it to the English Syntax Parser, then send the tagged data to the database.
        Only Parse the XMLData if the list has at least one entry in it.

        Args:
            None.

        Returns:
            Void.
        """
        #print("This is the end of the XML file")
        #print(self.next_sentence);
        #for line in self.sentences:
            #print("\n", line)
        """for data in self.xml_data:
            print(data.print_all_data())
        """
        # Call determine Factory
        #extractor = PerthExtractor()
        try:
            if len(self.xml_data) != 0: 
                #extractor = self.determine_factory(self.file_name)

                # List for storing what the council extractor gives
                sentences = []

                # This will have the sentences from one of the Council Extractors (Perth/Vincent/Stirling)
                sentences = self.extractor.create_sentences(self.xml_data)

                # Next send it to the ESP for tagging
                self.create_extracted_data(sentences)

                # Finally send it to the Database

        except (ValueError, AttributeError) as e:
            print("File did not contain a recognised council name: %s" %(e.args))


    # This determines which factory class we want to use to parse the data
    # extracted from the XML document
    def determine_factory(self, file_name):
        """Determine which CouncilExtractor will parse the XMLData.

        Using the name of the file passed in, determine which factory class,
        a CouncilExtractor, will parse the XMLData list.

        Args:
            file_name: The name of the file being parsed.

        Returns: PerthExtractor() or some other CouncilExtractor once they are implemented.

        """

        try:
            file_name = file_name.lower()
            if "perth" in file_name:
                #print("Do the Perth one")
                return PerthExtractor()

            # Add a return Vincent class once we make a Vincent parser.
            elif "vincent" in file_name:
                return VincentExtractor()
                #print("do the vincent one")

            # Add a return Stirling class once we make the Stirling parser.
            elif "stirling" in file_name:
                print("Do the Stirling one")
            

            # If there isn't a recognised council in the file_name string then (for now), 
            # raise an error, and later possibly later it will be changed to just parse
            # it for Perth.
            # If None is passed, throw a type error
            else:
                raise ValueError(file_name)
        except (TypeError, AttributeError) as e:
            message = "File_Name is not a String type: %s" %(e.args)
            raise TypeError(e.__str__() + "\n"+ message)
            


    """
        This is where the parsed agenda sentences is sent to the ESP,
        one line at a time.
        A list of Council Member attendees also needs to be passed to the ESP
    """
    def create_extracted_data(self, sentences):
        """ Send the tagged data to the ESP and then prepare_for_database() function.

        Send the created sentences from a Council Extractor to the English Syntax Parser.
        For each type of keyword(Councillors, Persons, Addresses, and Businesses), send
        them to the prepare_for_database function with the appropriate keyword_type String.

        NOTE: To integrate this with the English Syntax Parser, replace the for loop declaration 
        with the one that is hashed out.

        Args:
            sentneces: A list of Strings created by a Council Extractor.

        """

        # A list of Extracted Data (for the data base)
        #all_tagged_data
        created_data = []
        #for line in sentences:
            # TODO - Send to the ESP

        # Get the document_name and agenda_code/name
        file_names = self.extract_agenda_code()
        #TODO set these variables to use the parameters passed in by the PDFParser instead
        #document_name = file_names[0]
        #agenda_code = file_names[1]
        document_name = "DOC_NAME"
        agenda_code = "AGENDA_CODE"
        try:
            for line in sentences:
                print(line)
            #line = "A line that will be replaced with what the ESP gives"
            #for x in range(1):
                try:
                    tagged_content = esp.nlp_spacy(line)
                    #tagged_content = nlp_spacy(line)

                    # For each type of keyword send it to the prepare_for_database()
                    # Councillors
                    self.send_to_database(tagged_content.councillors, "Councillors", document_name, agenda_code, sentences)

                    # Persons
                    self.send_to_database(tagged_content.persons, "Person", document_name, agenda_code, sentences)

                    # Business Names
                    self.send_to_database(tagged_content.businesses, "Business Name", document_name, agenda_code, sentences)

                    # Addresses
                    self.send_to_database(tagged_content.addresses, "Address", document_name, agenda_code, sentences)
                except(AttributeError, TypeError, Exception) as e:
                    message = "Invalid content passed to ESP returned: %s" %(e.args)
                    print(message)
                    created_data = None
        except(AttributeError, TypeError) as e:
            message = "Could not connect to the English Syntax Parser: %s" %(e.args)
            print(message)
            created_data = None
         
        self.sentences = []
        self.xml_data = []

        return created_data

    # TODO the agenda_code, agenda_name, document_name needs to become actual variables
    """ prepare_for_database converts the key word given into an ExtractedData class, then if
        there was some invalid data passed to this point, the ExtractedData will catch it, and
        that key word will be skipped"""
    def send_to_database(self, keywords, keyword_type, document_name, agenda_code, sentences):
        """ Create the Extracted Data type, send it to send_database function.

        Create an Extracted Data object for each value in keywords, and send them
        to send_extracted_data_to_database function only if the ExtractedData object
        has valid data.

        Args:
            keywords: A list of tagged keywords.

            keyword_type: A String representing the type that the keywords are.
            (Councillor, Person, Address, Business Name).

        Returns:
            Void.
        """

        database = insert()
        try:
            for keyword in keywords:
                try:
                    print("Key Word Type: %s || %s " %(keyword_type, keyword))
                    extracted_data = ExtractedData(agenda_code, agenda_code, document_name, keyword, keyword_type)
                    if extracted_data.valid == False:
                        raise AttributeError

                except(TypeError) as e:
                    message = "None Type was passed in: %s" %(e.args)
                    print(message)

                keyword_frequency = 0
                for line in sentences:
                    keyword_frequency += line.count(keyword)
                print("Frequency: %s" %(keyword_frequency))

                # send the data to the method that will pass it to the database
                #self.send_extracted_data_to_database(extracted_data)

                insert.insertKeyPhrase(extracted_data.key_phrase, extracted_data.type_key_phrase)
                insert.insertIsWithin(extracted_data.key_phrase, self.agenda_code, self.document_name, keyword_frequency)
                #insert.insertIsWithin(extracted_data.key_phrase, self.agenda_code, self.document_name, keyword_frequency)
        except(TypeError) as e:
            message = "None Type was passed in: %s" %(e.args)
            print(message)
        

    """
        This will send the data tagged by the ESP to the database

        To send things to the Database, I need to call insert from insert,
        Which has all the methods needed to put data into the data base.

        insert itself has all the imports for protApp.models, which has all the
        tables needed for the database.

        So I need to call the methods from insert.

        NOTE: After learning that the database only has "insertKeyWord()"), and doesn't
        need to know what specifically is being inserted into it, this function may be deleted 
        and its functionality given to prepare_for_database(), if this function only executes one line.
    """
    def send_extracted_data_to_database(self, created_data):
        pass


    def extract_agenda_code(self):
        """ Extract the PDF name and the Agenda name from the self.file_name.
        """
        try:
            file_names = self.file_name.split('~')

            if len(file_names) == 2:
                # Get the PDF name in position 1, get the agenda name in position 2.
                for ii in range(2):
                    file_names[ii] = file_names[ii].strip(".xml")
                    #print("%s" %(file_names[ii]))

            elif len(file_names) > 2:
                file_names = file_names[:2]
                for ii in range(2):
                    file_names[ii] = file_names[ii].strip(".xml")

            else:
                name = self.file_name.strip(".xml")
                file_names = None
                if len(name) != 0:
                    file_names = [name, name]
                else:
                    file_names = ["Empty String", "Empty String"]
        except AttributeError as e:
            print("None type given as file_name %s: " %(e.args))
            file_names = None

        return file_names



    def parse(self, file_name,documentName,agendaCode):
        """ Begin the parsing process.

        Create a new SAX object, and set its Handler as an AgendaItemExtractor class (this class).
        Start parsing the file that has been passed in. Determine the factory immediately to 
        determine whether or not this file can be parsed.

        Args:
            file_name: The XML file that is needing to be parsed.

        Returns:
            Void.

        """
        try:
            self.extractor = self.determine_factory(file_name)
            parser = xml.sax.make_parser()
            parser.setFeature(xml.sax.handler.feature_namespaces, 0)
            parser.setContentHandler(self)
            self.file_name = file_name
            self.document_name = documentName
            self.agenda_code = agendaCode
            try:   
                parser.parse("pdfparser/minute_store/" + file_name)
                #self.extract_agenda_code("PDF Name~Agenda Code")
            except (ValueError, xml.sax._exceptions.SAXParseException) as e:
                print("Initial parsing could not begin: %s" %(e.args))
                
        except (ValueError, TypeError) as e:
            print("File does not contain a recognised council name: %s" %(e.args))
            


