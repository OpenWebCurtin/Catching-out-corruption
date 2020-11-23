"""
    This class will store the data returned from the English Syntax Parser (SpaCy).

    agenda_code:
        The code name that will identify the agenda.

    // Ask Callum what the agenda_name is
    agenda_name:
        the name of the agenda.

    document_name:
        The identifier of the minutes document.

    key_phrase:
        A key phrase that was identified by the ESP.

    type_key_phrase:
        A List of tags that the key_phrase was identified as.

    valid:
        A boolean that represents whether all the data passed in was of the right type,
        this is used for testing.
"""

class ExtractedData(object):
    def __init__ (self, in_agenda_code, in_agenda_name, in_document_name, in_key_phrase, in_type_key_phrase):

        valid = True

        if isinstance(in_agenda_code, str):
            self.agenda_code = in_agenda_code
        else:
            self.agenda_code = None
            valid = False

        if isinstance(in_agenda_name, str):
            self.agenda_name = in_agenda_name
        else:
            self.agenda_name = None
            valid = False

        if isinstance(in_document_name, str):
            self.document_name = in_document_name
        else:
            self.document_name = None
            valid = False

        if isinstance(in_key_phrase, str):
            self.key_phrase = in_key_phrase
        else:
            self.key_phrase = None
            valid = False

        if isinstance(in_type_key_phrase, str):
            self.type_key_phrase = in_type_key_phrase
        else:
            self.type_key_phrase = None
            valid = False

        self.valid = valid

    """
        Returns all the data of an Extracted Data object as one String, this is used for testing purposes.
    """
    def show_data(self):
        output = "Key Phrase: %s || Type: %s || Agenda Code: %s || Agenda Name: %s || Document Name: %s" \
                  %(self.key_phrase, self.type_key_phrase, self.agenda_code, \
                    self.agenda_name, self.document_name)

        return output
