from database.models import is_within
from database.models import is_within_nm
from database.models import key_phrases
from database.get import get
from itertools import combinations
import sys
"""
"class name: search
"description: a class to search for connections between key phrases
"either in agendas,documents or both
"""
class search():
	"""
	"method name: checkFilter
	"imports: filterType(int),phrase(string)
	"exports:result(boolean)
	"description: checks if the filter is the right type base on. 
	"if it isnt then a false is returned. the type should be specified
	"by the user. if no type was specified a 1 should be imported.
	"
	"""
	def checkFilter(filterType,phrase):
		result = False
		
		if(key_phrases.objects.filter(keyPhrase__exact=phrase).exists()):#if the key phrase exists
			if(filterType == 0):
				result = True
			if(filterType == 1):
				if(key_phrases.objects.get(keyPhrase__exact=phrase).phraseType=='Councillors'):
					result = True
			if(filterType == 2):
				if(key_phrases.objects.get(keyPhrase__exact=phrase).phraseType=='Person' or key_phrases.objects.get(keyPhrase__exact=phrase).phraseType=='councillor'):
					result = True
			if(filterType == 3):
				if(key_phrases.objects.get(keyPhrase__exact=phrase).phraseType=='Buisness Name'):
					result = True
			if(filterType == 4):
				if(key_phrases.objects.get(keyPhrase__exact=phrase).phraseType=='Address'):
					result = True
		return result
	"""
	"method name: single
	"imports: inPhrase(string),phraseType(int)
	"exports:outList(list of information of searched item, for 
	"agenda based it is [agenda code,document name]for document based it
	"is [document name])
	"description: will search for all agendas and documents for a single
	"phrase and return them
	"""
	def single(inPhrase,phraseType):
		search = is_within.objects.filter(keyPhrase__exact=inPhrase)#find all agendas connected to the phrase
		outList = []
		normAgenda = dict()
		agendaDoc = dict()
		for agendas in search:
			normAgenda[agendas.agendaCode.agendaCode] = agendas.wordCount/agendas.agendaCode.wordCount
			agendaDoc [agendas.agendaCode.agendaCode] = agendas.agendaCode.documentName.documentName
		sortedAgenda = list({k: v for k, v in sorted(normAgenda.items(), key=lambda x: x[1],reverse=True)}.keys())
		for agenda in sortedAgenda:
			outList.append([agenda,agendaDoc[agenda]])
		search = is_within_nm.objects.filter(keyPhrase__exact=inPhrase)#finding all non-minute documents connected to the phrase
		normDocs = dict()
		for documents in search:
			normDocs[documents.documentName.documentName] = documents.wordCount/documents.documentName.wordCount
		sortedDocs = list({k: v for k, v in sorted(normDocs.items(), key=lambda x: x[1],reverse=True)}.keys())
		for docs in sortedDocs:
			outList.append(docs)
		return outList
	"""
	"method name: sortedAgenda
	"imports: inPhrases(list in the format of [phrase(string),importance(float)])
	"exports:outAgenda(list of information of searched items in the format
	" of [agendacode,documentname]
	"description: will search for all agendas using the importated key phrases
	" and use the imported importance and the average appearance of the phrase
	" in the agenda to calculate and order based on relative importance
	"""
	def sortedAgendas(inPhrases,inCouncil,dateBottom,dateTop):
		fullTable = is_within.objects.all()
		if(dateBottom != None):
			fullTable = fullTable.filter(agendaCode__documentName__documentDate__gte=dateBottom)
		if(dateTop != None):
			fullTable = fullTable.filter(agendaCode__documentName__documentDate__lte=dateTop)
		if(inCouncil != ""):
			fullTable = fullTable.filter(agendaCode__documentName__council__iexact=inCouncil)
		outSearch = fullTable.distinct("agendaCode")
		agendas = []
		outValues = dict()
		outDocs = dict()
		for object in outSearch:
			agendas.append(object.agendaCode.agendaCode)
			outValues[object.agendaCode.agendaCode] = 0	
		for agenda in agendas:
			keyPhraseFilter = fullTable.filter(agendaCode__agendaCode__exact=agenda)
			phrases = []
			for phrase in keyPhraseFilter:
				phrases.append(phrase.keyPhrase.keyPhrase)
				
			for phrase in inPhrases:
				if phrase[0] in phrases:
					if(search.checkFilter(phrase[2],phrase[0])):
						iW = fullTable.filter(agendaCode__agendaCode__exact=agenda).get(keyPhrase__exact=phrase[0])
					
						outValues[agenda] = outValues[agenda]+(phrase[1]*(iW.wordCount/iW.agendaCode.wordCount))
					
						outDocs[agenda] = iW.agendaCode.documentName.documentName
			
		removeItems = []
		for value in outValues:
			if(outValues[value] == 0):
				removeItems.append(value)
		for item in removeItems:
			outValues.pop(item)
		outSorted = list({k: v for k, v in sorted(outValues.items(), key=lambda x: x[1],reverse=True)}.keys())
		outAgenda = []
		for agenda in outSorted:
			outAgenda.append([agenda,outDocs[agenda]])
		return outAgenda
	"""
	"method name: sortedDocuments
	"imports: inPhrases(list in the format of [phrase(string),importance(float)])
	"exports:outDocument(list of strings)
	"description: will search for all documents using the importated key phrases
	" and use the imported importance and the average appearance of the phrase
	" in the document to calculate and order based on relative importance
	"""
	def sortedDocuments(inPhrases,inCouncil,dateBottom,dateTop):
		fullTable = is_within_nm.objects.all()
		if(dateBottom != None):
			fullTable = fullTable.filter(documentName__documentDate__gte=dateBottom)
		if(dateTop != None):
			fullTable = fullTable.filter(documentName__documentDate__lte=dateTop)
		if(inCouncil != ""):
			fullTable = fullTable.filter(documentName__council__iexact=inCouncil)
		outSearch = fullTable.distinct("documentName")
		
		documents = []
		outValues = dict()
		for object in outSearch:
			documents.append(object.documentName.documentName)
			outValues[object.documentName.documentName] = 0	
		for document in documents:
			keyPhraseFilter = fullTable.filter(documentName__documentName__exact=document)
			phrases = []
			for phrase in keyPhraseFilter:
				phrases.append(phrase.keyPhrase.keyPhrase)
				print(phrases)
			for phrase in inPhrases:
				if phrase[0] in phrases:
					if(search.checkFilter(phrase[2],phrase[0])):
						iW = fullTable.filter(documentName__documentName__exact=document).get(keyPhrase__exact=phrase[0])
					
						outValues[document] = outValues[document]+(phrase[1]*(iW.wordCount/iW.documentName.wordCount))
			print(outValues[document])
		removeItems = []
		for value in outValues:
			if(outValues[value] == 0):
				removeItems.append(value)
		for item in removeItems:
			outValues.pop(item)
		outSorted = list({k: v for k, v in sorted(outValues.items(), key=lambda x: x[1],reverse=True)}.keys())
		outDocument = []
		for document in outSorted:
			outDocument.append(document)
		return outDocument
	"""
	"method name: minuteSearch
	"imports: phrases(list of lists in the form of [phrase(string),importantance(float),phraseType(int)])
	"exports:agendaSet(list of lists in the form of [agendaCode(string),documentName(string),keyPhrases(list of strings)])
	"description: will take a 2d array of phrases with relevent information
	"and give it to sortedagendas. it will then use the sorted input and build
	"a list to be exported
	"""
	def minuteSearch(phrases,inCouncil,dateBottom,dateTop):
		sortedAgendas = search.sortedAgendas(phrases,inCouncil,dateBottom,dateTop)
	
		fullTable = is_within.objects.all()
		
		outResults = []
		for agenda in sortedAgendas:
			phrasesUsed = []
			for phrase in phrases:
				if(search.checkFilter(phrase[2],phrase[0])):
					if(fullTable.filter(agendaCode__agendaCode__exact=agenda[0]).filter(keyPhrase__keyPhrase__exact=phrase[0]).exists()):
						phrasesUsed.append(phrase[0])
					outResults.append([agenda[0],agenda[1],phrasesUsed])	
		return outResults
	"""
	"method name: nonMinuteSearch
	"imports: phrases(list of lists in the form of [phrase(string),importantance(float),phraseType(int)])
	"exports:agendaSet(list of lists in the form of [documentName(string),keyPhrases(list of strings)])
	"description: will take a 2d array of phrases with relevent information
	"and give it to sortedDocs. it will then use the sorted input and build
	"a list to be exported
	"""
	def nonMinuteSearch(phrases,inCouncil,dateBottom,dateTop):

		sortedDocs = search.sortedDocuments(phrases,inCouncil,dateBottom,dateTop)
		fullTable = is_within_nm.objects.all()
		outResults = []
		for documents in sortedDocs:
			phrasesUsed = []
			for phrase in phrases:
				if(search.checkFilter(phrase[2],phrase[0])):
					if(fullTable.filter(documentName__documentName__exact=documents).filter(keyPhrase__keyPhrase__exact=phrase[0]).exists()):
						phrasesUsed.append(phrase[0])
					outResults.append([documents,phrasesUsed])	
		return outResults
		
	"""
	"method name: nonMinuteSearch
	"imports: phrases(list of lists in the form of [phrase(string),importantance(float),phraseType(int)])
	"exports:agendaSet(list of lists in the form of either [agendaCode(string),documentName(string),keyPhrases(list of strings)], or [documentName(string),keyPhrases(list of strings)])
	"description: will take a 2d array of phrases with relevent information
	"and give it to sortedAgenda and sortedDocs. it will then use the sorted input and build
	"a list to be exported
	"""
	def combinedSearch(phrases):
		combinedSet = []
		###
		sortedAgendas = search.sortedAgendas(phrases)
		inPhrases = []
		for phrase in phrases:
			inPhrases.append(phrases[0])	
		fullTable = is_within.objects.all()
		for agenda in sortedAgendas:
			phrasesUsed = []
			for phrase in phrases:
				if(fullTable.filter(agendaCode__agendaCode__exact=agenda[0]).filter(keyPhrase__keyPhrase__exact=phrase[0]).exists()):
					phrasesUsed.append(phrase[0])
			combinedSet.append([agenda[0],agenda[1],phrasesUsed])
		###
		sortedDocs = search.sortedDocuments(phrases)
		inPhrases = []
		for phrase in phrases:
			inPhrases.append(phrases[0])	
		fullTable = is_within_nm.objects.all()
		for documents in sortedDocs:
			phrasesUsed = []
			for phrase in phrases:
				if(fullTable.filter(documentName__documentName__exact=documents).filter(keyPhrase__keyPhrase__exact=phrase[0]).exists()):
					phrasesUsed.append(phrase[0])
			combinedSet.append([documents,phrasesUsed])	
		return combinedSet


