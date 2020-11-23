from django.test import TestCase
from esp.esp 

import pytest

	def test_empty_input():
	    items = esp.nlp_spacy("")
	    assert items == None,"test passed"

	def test_nlp_spacy():
	    person_sample = "Cr Yong and Cr Chen previously disclosed a Proximity Interest. Margaret Smith and Rebecca Moore are also present."
	    items = esp.nlp_spacy(person_sample)
	    assert items.councillors == ['Cr Yong', 'Cr Chen'],"test passed"
	    assert items.persons == ['Margaret Smith', 'Rebecca Moore'],"test passed"

	def test_bisnames():
	    bisnames_sample = "$2,536,468.70 to Broad Construction Services (WA) Pty Ltd for the construction of the Elder Street car park."
	    items = esp.nlp_spacy(bisnames_sample)
	    assert items.businesses == ['Broad Construction Services'],"test passed"
