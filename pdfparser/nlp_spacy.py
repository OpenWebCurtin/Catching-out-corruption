"""
    A dummy class for nlp_spaCy, this returns pre-defined keywords.
"""

class nlp_spacy(object):

    def __init__ (self, input):
        self.councillors = ["Cr Yong", "Cr Chen"]
        self.persons = ["Margaret Smith", "Rebecca Moore"]
        self.businesses = ["Business 1", "Business 2"]
        self.addresses = ["Address 1", "Address 2"]

