from database.models import key_phrases
from database.models import documents
from database.models import agenda_items
from database.models import found_in
from database.models import is_within
from database.models import files
from database.models import jobs
from database.models import is_from
from database.models import completes_with
from database.models import is_within_nm
from database.models import attended
"""
"class name: get
"description: a class for safely retreiving data from the database
"minimising access to the models themselves by other classes.
"""
class get():
	"""
	"method name: getKeyPhraseObject
	"imports: inPhrase(string)
	"exports:out(None or keyPhrase Object)
	"description: a method to retrieve an object of a key phrase
	"using the keyPhrase key to find it. it returns a None if no
	"keyPhrase of that key is found
	"""
	def getKeyPhraseObject(inPhrase):
		out = None
		if(key_phrases.objects.filter(keyPhrase__exact=inPhrase).exists()):
			out = key_phrases.objects.get(keyPhrase__exact=inPhrase)
		return out
	"""
	"method name: getKeyPhraseType
	"imports: inPhrase(string)
	"exports: outType(None or String)
	"description: a method to retrieve the phrase type of a key phrase
	"using the keyPhrase key to find it. it returns a None if no
	"keyPhrase of that key is found
	"""
	def getKeyPhraseType(inPhrase):
		outType = None
		phraseObject = get.getKeyPhraseObject(inPhrase)
		if(phraseObject != None): 
			outType = phraseObject.phraseType
		return outType
	"""
	"method name: getAgendaItemObject
	"imports: inAgendaCode(string),inDocumentName(string)
	"exports: out(None or agendaItem Object)
	"description: a method to retrieve an object a agenda item
	"using the agendacode and documentname keys. it will return
	"none if no agenda item is found
	"""
	def getAgendaItemObject(inAgendaCode,inDocumentName):
		out = None
		if(agenda_items.objects.filter(agendaCode__exact=inAgendaCode).filter(documentName__documentName__exact=inDocumentName).exists()):
			out = agenda_items.objects.filter(agendaCode__exact=inAgendaCode).get(documentName__documentName__exact=inDocumentName)
		return out
	"""
	"method name: getAgendaItemDocument
	"imports: inAgendaCode(string),inDocumentName(string)
	"exports: outDocument(None or string)
	"description: a method to retrieve the document name of
	"the document from the foreign key, if no agenda is
	"found a none is returned
	"""
	def getAgendaItemDocument(inAgendaCode,inDocumentName):
		outDocument = None
		agendaObject = get.getAgendaItemObject(inAgendaCode,inDocumentName)
		if(agendaObject != None): 
			outDocument = agendaObject.documentName.documentName
		return outDocument
	"""
	"method name: getAgendaName
	"imports: inAgendaCode(string),inDocumentName(string)
	"exports: outName(None or string)
	"description: a method to retrieve the agenda name of
	"agenda, if no agenda is found a none is returned
	"""
	def getAgendaName(inAgendaCode,inDocumentName):
		outName = None
		
		agendaObject = get.getAgendaItemObject(inAgendaCode,inDocumentName)
		if(agendaObject != None): 
			outName = agendaObject.agendaName
		return outName
	"""
	"method name: getAgendaItemWordCount
	"imports: inAgendaCode(string),inDocumentName(string)
	"exports: outCount(None or int)
	"description: a method to retrieve the word count of
	"agenda, if no agenda is found a none is returned
	"""
	def getAgendaItemWordCount(inAgendaCode,inDocumentName):
		outCount = None
		
		agendaObject = get.getAgendaItemObject(inAgendaCode,inDocumentName)
		if(agendaObject != None): 
			outCount = agendaObject.wordCount
		return outCount
	"""
	"method name: getDocumentObject
	"imports:inDocumentName(string)
	"exports:out(None or documentObject)
	"description: a method to retrieve an object of a document
	"using the documentname key. it will return none if no 
	"document is found
	"""
	def getDocumentObject(inDocumentName):
		out = None
		if(documents.objects.filter(documentName__exact=inDocumentName).exists()):
			out = documents.objects.get(documentName__exact=inDocumentName)
		return out
	"""
	"method name: getDocumentDate
	"imports:inDocumentName(string)
	"exports:outDate(None or timstamp)
	"description: a method to retrieve a documents creation date
	"using the documentname key. it will return none if no 
	"document is found
	"""
	def getDocumentDate(inDocumentName):
		outDate = None
		documentObject = get.getDocumentObject(inDocumentName)
		if(documentObject != None): 
			outDate = documentObject.documentDate
		return outDate
	"""
	"method name: getDocumentWordCount
	"imports:inDocumentName(string)
	"exports:outCount(None or int)
	"description: a method to retrieve a documents wordcount
	"using the documentname key. it will return none if no 
	"document is found
	"""
	def getDocumentWordCount(inDocumentName):
		outCount = None
		documentObject = get.getDocumentObject(inDocumentName)
		if(documentObject != None): 
			outCount = documentObject.wordCount
		return outCount
	"""
	"method name: getDocumentCouncil
	"imports:inDocumentName(string)
	"exports:outCouncil(None or string)
	"description: a method to retrieve a documents council
	"using the documentname key. it will return none if no 
	"document is found
	"""
	def getDocumentCouncil(inDocumentName):
		outCouncil = None
		documentObject = get.getDocumentObject(inDocumentName)
		if(documentObject != None): 
			outCouncil = documentObject.council
		return outCouncil
	"""
	"method name: getDocumentIsMinute
	"imports:inDocumentName(string)
	"exports:outMinute(None or boolean)
	"description: a method to retrieve wether a document is
	"a minute or not using the documentname key. it will 
	"return none if no document is found
	"""
	def getDocumentIsMinute(inDocumentName):
		outMinute = None
		
		documentObject = get.getDocumentObject(inDocumentName)
		if(documentObject != None):
			outMinute = documentObject.isMinute
		return outMinute
	"""
	"method name: getFileObject
	"imports:inFileName(string)
	"exports:out(None or fileObject)
	"description: a method to retrieve an object of a file
	"using the filename key. it will return none if no 
	"file is found
	"""
	def getFileObject(inFileName):
		out = None
		if(files.objects.filter(fileName__exact=inFileName).exists()):
			out = files.objects.get(fileName__exact=inFileName)
	
		return out
	"""
	"method name: getFileDirectory
	"imports:inFileName(string)
	"exports:outDirectory(None or string)
	"description: a method to retrieve the directory of
	"a file using the filename key. it will return none 
	"if no file is found
	"""
	def getFileDirectory(inFileName):
		outDirectory = None
		fileObject = get.getFileObject(inFileName)
		if(fileObject != None):
			outDirectory = fileObject.docFile
		return outDirectory
	"""
	"method name: getFileVirtualName
	"imports:inFileName(string)
	"exports:outName(None or string)
	"description: a method to retrieve the directory of
	"a file using the filename key. it will return none 
	"if no file is found
	"""
	def getFileVirtualName(inFileName):
		outName = None
		fileObject = get.getFileObject(inFileName)
		if(fileObject != None):
			outName = fileObject.virtualName
		return outName
	"""
	"method name: getFileDate
	"imports:inFileName(string)
	"exports:outDate(None or timestamp)
	"description: a method to retrieve the uploadte timestamp
	"of a file using the filename key. it will return none 
	"if no file is found
	"""
	def getFileDate(inFileName):
		outDate = None
		fileObject = get.getFileObject(inFileName)
		if(fileObject != None):
			outDate = fileObject.uploadDateTime
		return outDate
	"""
	"method name: getJobObject
	"imports:inJobNumber(int),inJobCreation(timestamp)
	"exports:out(None or job Object)
	"description: a method to retrieve an object of a job
	"using the jobnumber and jobcreation keys. it will 
	"return none if no job is found
	"""
	def getJobObject(inJobNumber,inJobCreation):
		out = None
		if(jobs.objects.filter(jobNumber__exact=inJobNumber).filter(jobCreation__exact=inJobCreation).exists()):
			return jobs.objects.filter(jobCreation__exact=inJobCreation).get(jobNumber__exact=inJobNumber)
		return out
	"""
	"method name: getJobStatus
	"imports:inJobNumber(int),inJobCreation(timestamp)
	"exports:outStatus(None or string)
	"description: a method to retrieve the status of a job
	"using the jobnumber and jobcreation keys. it will 
	"return none if no job is found
	"""
	def getJobStatus(inJobNumber,inJobCreation):
		outStatus = None
		jobObject = get.getJobObject(inJobNumber,inJobCreation)
		if(jobObject != None):
			outStatus = jobObject.jobStatus
		return outStatus
	"""
	"method name: getJobType
	"imports:inJobNumber(int),inJobCreation(timestamp)
	"exports:outType(None or string)
	"description: a method to retrieve the type of a job
	"using the jobnumber and jobcreation keys. it will 
	"return none if no job is found
	"""
	def getJobType(inJobNumber,inJobCreation):
		outType = None
		jobObject = get.getJobObject(inJobNumber,inJobCreation)
		if(jobObject != None):
			outType = jobObject.jobType
		return outType
	"""
	"method name: getJobCreation
	"imports:inJobNumber(int),inJobCreation(timestamp)
	"exports:outDate(None or timestamp)
	"description: a method to retrieve the creation timestamp 
	"of a job using the jobnumber and jobcreation keys. it will 
	"return none if no job is found
	"""
	def getJobCreation(inJobNumber,inJobCreation):
		outDate = None
		jobObject = get.getJobObject(inJobNumber,inJobCreation)
		if(jobObject != None):
			outDate = jobObject.jobCreation
		return outDate
	"""
	"method name: getJobStartDate
	"imports:inJobNumber(int),inJobCreation(timestamp)
	"exports:outDate(None or timestamp)
	"description: a method to retrieve the start timestamp 
	"of a job using the jobnumber and jobcreation keys. it will 
	"return none if no job is found
	"""
	def getJobStartDate(inJobNumber,inJobCreation):
		outDate = None
		jobObject = get.getJobObject(inJobNumber,inJobCreation)
		if(jobObject != None):
			outDate = jobObject.startDateTime
		return outDate
	"""
	"method name: getJobCompletionDate
	"imports:inJobNumber(int),inJobCreation(timestamp)
	"exports:outDate(None or timestamp)
	"description: a method to retrieve the completion timestamp 
	"of a job using the jobnumber and jobcreation keys. it will 
	"return none if no job is found
	"""
	def getJobCompletionDate(inJobNumber,inJobCreation):
		outDate = None
		jobObject = get.getJobObject(inJobNumber,inJobCreation)
		if(jobObject != None):
			outDate = jobObject.completionDateTime
		return outDate
	"""
	"method name: getJobFileName
	"imports:inJobNumber(int),inJobCreation(timestamp)
	"exports:outFile(None or string)
	"description: a method to retrieve the filename of a file
	"from a foreign key of a job using the jobnumber and 
	"jobcreation keys. it will return none if no job is found
	"""
	def getJobFileName(inJobNumber,inJobCreation):
		outFile = None
		jobObject = get.getJobObject(inJobNumber,inJobCreation)
		if(jobObject != None):
			if(jobObject.fileName != None):
				outFile = jobObject.fileName.fileName
		return outFile
	"""
	"method name: getIsWithinObject
	"imports:inPhrase(string),inAgendaCode(string)
	"exports:out(None or isWithin Object)
	"description: a method to retrieve an object of an isWithin
	"relationship using the keyphrase and agendaitems keys. it will 
	"return none if no isWithin object is found
	"""
	def getIsWithinObject(inPhrase,inAgendaCode):
		out = None
		if(is_within.objects.filter(keyPhrase__keyPhrase__exact=inPhrase).filter(agendaCode__agendaCode__exact=inAgendaCode).exists()):
			out = is_within.objects.filter(keyPhrase__keyPhrase__exact=inPhrase).get(agendaCode__agendaCode__exact=inAgendaCode)
			
		
		return out
	"""
	"method name: getIsWithinWordCount
	"imports:inPhrase(string),inAgendaCode(string)
	"exports:out(None or string)
	"description: a method to retrieve an the wordcount of an isWithin
	"relationship using the keyphrase and agendaitems keys. it will 
	"return none if no isWithin object is found
	"""
	def getIsWithinWordCount(inPhrase,inAgendaCode):
		outCount = None
		iWObject = get.getIsWithinObject(inPhrase,inAgendaCode)
		if(iWObject != None):
			outCount = iWObject.wordCount
		return outCount
	"""
	"method name: getIsWithinNMObject
	"imports:inPhrase(string),inDocumentName(string)
	"exports:out(None or isWithinNM Object)
	"description: a method to retrieve the object of an isWithinNM
	"relationship using the keyphrase and document keys. it will 
	"return none if no isWithinNM object is found
	"""
	def getIsWithinNMObject(inPhrase,inDocumentName):
		out = None
		if(is_within_nm.objects.filter(keyPhrase__keyPhrase__exact=inPhrase).filter(documentName__documentName__exact=inDocumentName).exists()):
			out = is_within_nm.objects.filter(keyPhrase__keyPhrase__exact=inPhrase).get(documentName__documentName__exact=inDocumentName)
		return out
	"""
	"method name: getIsWithinNMWordCount
	"imports:inPhrase(string),inDocumentName(string)
	"exports:out(None or int)
	"description: a method to retrieve the wordcount of an isWithinNM
	"relationship using the keyphrase and document keys. it will 
	"return none if no isWithinNM object is found
	"""
	def getIsWithinNMWordCount(inPhrase,inAgendaCode):
		outCount = None
		iWNMObject = get.getIsWithinNMObject(inPhrase,inAgendaCode)
		if(iWObject != None):
			outCount = iWNMObject.wordCount
		return outCount
	"""
	"method name: getAttendedObject
	"imports:inPhrase(string),inDocumentName(string)
	"exports:out(None or attended Object)
	"description: a method to retrieve the object of an attended
	"relationship using the keyphrase and document keys. it will 
	"return none if no attended object is found
	"""
	def getAttendedObject(inPhrase,inDocumentName):
		out = None
		if(attended.objects.filter(keyPhrase__keyPhrase__exact=inPhrase).filter(documentName__documentName__exact=inDocumentName).exists()):
			out = attended.objects.filter(keyPhrase__keyPhrase__exact=inPhrase).get(documentName__documentName__exact=inDocumentName)
		return out
	"""
	"method name: getCouncilAttendees
	"imports:inDocumentName(string)
	"exports:out(None or list of strings)
	"description: a method to retrieve a list of all the councillors
	"that attended a minute using the keyphrase and document keys. 
	"it will return none if no attended object is found
	"""
	def getCouncilAttendees(inDocumentName):
		outList = None
		if(attended.objects.filter(documentName__documentName__exact=inDocumentName).exists()):
			query = attended.objects.filter(documentName__documentName__exact=inDocumentName)#will return all councillors at the minute
			outList = []
			for phrase in query:
				outList.append(phrase.keyPhrase.keyPhrase)#adds councillors name to a list of strings
		return outList
	"""
	"method name: getCouncilAttendence
	"imports:inPhrase(string)
	"exports:out(None or list of strings)
	"description: a method to retrieve a list of all the minutes
	"that were attended by a councillor using the keyphrase and 
	"document keys. it will return none if no attended object is found
	"""
	def getCouncilAttendence(inPhrase):
		outList = None
		if(attended.objects.filter(keyPhrase__keyPhrase__exact=inPhrase).exists()):
			query = attended.objects.filter(keyPhrase__keyPhrase__exact=inPhrase)#will return all minutes the councillor was in
			outList = []
			for phrase in query:
				outList.append(phrase.documentName.documentName)#adds minutes name to the list of strings
		return outList
	"""
	"method name: getIsFromObjectd
	"imports:inFileName(string),inDocumentName(string)
	"exports:out(None or isFrom Object)
	"description: a method to retrieve the object of an isFrom
	"relationship using the document and file keys. it will 
	"return none if no isFrom object is found
	"""
	def getIsFromObject(inDocumentName,inFileName):
		out = None
		if(is_from.objects.filter(fileName__fileName__exact=inFileName).filter(documentName__documentName__exact=inDocumentName).exists()):
			out = is_from.objects.filter(fileName__fileName__exact=inFileName).get(documentName__documentName__exact=inDocumentName)
		return out
	"""
	"method name: getFoundInObject
	"imports:inAgendaCode(string),inDocumentName(string)
	"exports:out(None or foundIn Object)
	"description: a method to retrieve the object of an foundIn
	"relationship using the agendaCode and document keys. it will 
	"return none if no attended object is found
	"""
	def getFoundInObject(inAgendaCode,inDocumentName):
		out = None
		if(found_in.objects.filter(agendaCode__agendaCode__exact=inAgendaCode).filter(documentName__documentName__exact=inDocumentName).exists()):
			out = found_in.objects.get(agendaCode__agendaCode__exact=inAgendaCode).get(documentName__documentName__exact=inDocumentName)
		return out
	"""
	"method name: getCompletesWithObject
	"imports:inJobNumber(string),inFileName(string)
	"exports:out(None or attended Object)
	"description: a method to retrieve the object of an completesWith
	"relationship using the jobs and files keys. it will 
	"return none if no completesWith object is found
	"""
	def getCompletesWithObject(inJobNumber):
		out = None
		if(completes_with.objects.filter(jobNumber__jobNumber__exact=inJobNumber).exists()):
		
			out = completes_with.objects.get(jobNumber__jobNumber__exact=inJobNumber)	
		return out