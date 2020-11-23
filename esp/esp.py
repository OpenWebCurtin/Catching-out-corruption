
import spacy
#import django
#django.setup()

from django.contrib.staticfiles import finders
#from esp.models import Business

#key items class
class KeyItems:

    def __init__(self):
        self.councillors = []
        self.persons = []
        self.addresses = []
        self.businesses = []

    def add_councillor(self, cname):
        self.councillors.append(cname)

    def add_person(self, pname):
        self.persons.append(pname)

    def add_address(self, adr):
        self.addresses.append(adr)

    def add_business(self, bname):
        self.businesses.append(bname)

class esp(object):
    def nlp_spacy (sentence):
        items = KeyItems()
        if sentence: 
            nlp = spacy.load('en_core_web_sm')
            doc = nlp(sentence)            
            classify_person(doc, items)
            classify_businesses(doc, items)
            classify_addresses(doc, items)
        else:
            items = None
        return items

def classify_person(doc, items):
    titles = ["councillor", "cr", "mayor", "lord", "commissioner"]
    for chunk in doc.noun_chunks:
        if (chunk[0].text.lower() in titles) and (chunk.root.pos_ == "PROPN"):
            items.add_councillor(chunk.text) 
        if (chunk[0].text.lower() not in titles) and (chunk[0].ent_type_ == "PERSON"):        
            if chunk[0].pos_ == "PROPN":
                items.add_person(chunk.text)

def classify_businesses(doc, items):
    for chunk in doc.noun_chunks:
        ents = list(chunk.ents)
        if (ents) and (ents[0].label_ == "ORG"):
            if chunk[0].pos_ == "PROPN":
                items.add_business(chunk.text)
       # else:
        #    result = Business.objects.get(name__iexact=chunk.text)
        #    if result.exists():
         #       items.add_business(chunk.text)
                
def classify_addresses(doc, items):
    with open(finders.find('esp/streettypes.txt')) as f:
        lines = f.read().splitlines()

    for chunk in doc.noun_chunks:
        if chunk.root.text.lower() in lines:
            if chunk[0].like_num:
                items.add_address(chunk.text)
                                
