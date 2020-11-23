from datetime import datetime
import pytz
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
from database.uploadFile import uploadFile
from database.get import get
"""
"class name: insert
"description: a class for adding rows of information to tables within the database
"""
class insert():
	"""
	"method name: insertKeyPhrase
	"imports: inPhrase(string),inType(string)
	"exports:valid(boolean)
	"description: inserts a row into the key_phrases
	"table using the imported information, initially
	"checking if the row already exists. if the row
	"already exists a false will be returned
	"otherwise a true will.
	"""
	def insertKeyPhrase(inPhrase,inType):
		valid = True
		if(key_phrases.objects.filter(keyPhrase__exact=inPhrase).exists()):
			valid = False
		else:
			key_phrases.objects.create(keyPhrase=inPhrase, phraseType=inType)
		return valid
	"""
	"method name: insertAgendaItem
	"imports: inAgendaCode(string),inAgendaName(string),inDocumentName(string),inWordCount(int)
	"exports:valid(boolean)
	"description: inserts a row into the agenda_items
	"table using the imported information, initially
	"checking if the row already exists. if the row
	"already exists a false will be returned
	"otherwise a true will.
	"""
	def insertAgendaItem(inAgendaCode,inDocumentName,inWordCount):
		valid = True
		
		
		if(agenda_items.objects.filter(agendaCode__exact=inAgendaCode).filter(documentName__documentName__exact=inDocumentName).exists()):
		
			valid = False
		else:
			doc = documents.objects.get(documentName__exact=inDocumentName)
			agenda_items.objects.create(agendaCode=inAgendaCode,agendaName=inAgendaCode,documentName=doc,wordCount = inWordCount)
		return valid
	"""
	"method name: insertDocument
	"imports: inDocumentName(string),inDate(timestamp),inWordCount(int),inIsMinute(boolean),inCouncil(string or None)
	"exports:valid(boolean)
	"description: inserts a row into the documents
	"table using the imported information, initially
	"checking if the row already exists. if the row
	"already exists a false will be returned
	"otherwise a true will.
	"""
	def insertDocument(inDocumentName,inDate,inWordCount,inIsMinute,inCouncil):
		valid = True
		if(documents.objects.filter(documentName__exact=inDocumentName).exists()):
			valid = False
		else:
			documents.objects.create(documentName = inDocumentName,documentDate = inDate,wordCount = inWordCount,isMinute = inIsMinute,council = inCouncil)
		return valid
	"""
	"method name: insertFile
	"imports: inDateTime(timestamp),inDocFile(file),inVirtualName(string)
	"exports:valid(boolean)
	"description: inserts a row into the files
	"table using the imported information, as
	"well as creating the unique filename byte
	"using an incremental number file name
	"""
	def insertFile(inDateTime,inDocFile,inVirtualName):
		valid = True
		num = uploadFile.getHighestFileNum()+1
		inFileName = str(num)+".pdf"
		files.objects.create(virtualName = inVirtualName,fileName = inFileName,uploadDateTime= inDateTime,docFile = inDocFile)
		return valid
	"""
	"method name: insertJob
	"imports: inFileName(string),inJobNumber(int),inJobStatus(string),inJobType(string),inCompletionTime(timestamp),inStartTime(timestamp),inJobCreation(timestamp)
	"exports:valid(boolean)
	"description: inserts a row into the jobs
	"table using the imported information, initially
	"checking if the row already exists. if the row
	"already exists a false will be returned
	"otherwise a true will.
	"""
	def insertJob(inFileName,inJobNumber,inJobStatus,inJobType,inCompletionTime,inStartTime,inJobCreation):
		valid = True
		if(jobs.objects.filter(jobNumber__exact=inJobNumber).filter(jobCreation__exact=inCompletionTime).exists()):
			
			valid = False
		else:
			if(files.objects.filter(fileName__exact=inFileName).exists()):#if there is a file that exists for the foreign key
				file = files.objects.get(fileName__exact=inFileName)
				jobs.objects.create(fileName = file,jobNumber = inJobNumber,jobStatus = inJobStatus,jobType = inJobType,completionDateTime = inCompletionTime,startDateTime = inStartTime,jobCreation = inJobCreation)
			elif(inFileName == None):#if there is no associated file
				jobs.objects.create(fileName = inFileName,jobNumber = inJobNumber,jobStatus = inJobStatus,jobType = inJobType,completionDateTime = inCompletionTime,startDateTime = inStartTime,jobCreation = inJobCreation)
			else:
				valid = False
		return valid
	"""
	"method name: insertIsWithin
	"imports: inPhrase(string),inAgendaCode(string),inDocumentName(string),inWordCount(int)
	"exports:valid(boolean)
	"description: inserts a row into the isWithin relationship
	"table using the imported information, initially
	"checking if the row already exists. if the row
	"already exists a false will be returned
	"otherwise a true will.
	"""
	def insertIsWithin(inPhrase,inAgendaCode,inDocumentName,inWordCount):
		valid = False
		if(is_within.objects.filter(keyPhrase__keyPhrase__exact=inPhrase).filter(agendaCode__agendaCode__exact=inAgendaCode).exists() == False):
			if(key_phrases.objects.filter(keyPhrase__exact=inPhrase).exists()):
				if(agenda_items.objects.filter(agendaCode__exact=inAgendaCode).filter(documentName__documentName__exact=inDocumentName).exists()):
					valid = True
					agenda = agenda_items.objects.get(agendaCode__exact=inAgendaCode)
					phrase = key_phrases.objects.get(keyPhrase__exact=inPhrase)
					agenda.isWithin.add(phrase)
					iW = is_within.objects.filter(keyPhrase__exact=phrase.keyPhrase).get(agendaCode__agendaCode__exact=agenda.agendaCode)
					iW.wordCount = inWordCount
					iW.save()
		return valid
	"""
	"method name: insertIsWithinNM
	"imports: inPhrase(string),inDocumentName(string),inWordCount(int)
	"exports:valid(boolean)
	"description: inserts a row into the isWithinNM relationship
	"table using the imported information, initially
	"checking if the row already exists. if the row
	"already exists a false will be returned
	"otherwise a true will.
	"""
	def insertIsWithinNM(inPhrase,inDocumentName,inWordCount):
		valid = False
		if(is_within_nm.objects.filter(keyPhrase__keyPhrase__exact=inPhrase).filter(documentName__documentName__exact=inDocumentName).exists() == False):

			if(key_phrases.objects.filter(keyPhrase__exact=inPhrase).exists()):

				if(documents.objects.filter(documentName__exact=inDocumentName).exists()):

					valid = True
					document = documents.objects.get(documentName__exact=inDocumentName)
					phrase = key_phrases.objects.get(keyPhrase__exact=inPhrase)
					phrase.isWithinNM.add(document)
					iWNM = is_within_nm.objects.filter(keyPhrase__exact=phrase.keyPhrase).get(documentName__exact=document.documentName)
					iWNM.wordCount = inWordCount
					iWNM.save()
		return valid
	"""
	"method name: insertIsFrom
	"imports: inFileName(string),inDocumentName(string)
	"exports:valid(boolean)
	"description: inserts a row into the isFrom relationship
	"table using the imported information, initially
	"checking if the row already exists. if the row
	"already exists a false will be returned
	"otherwise a true will.
	"""
	def insertIsFrom(inDocumentName,inFileName):
		valid = False
		if(is_from.objects.filter(fileName__fileName__exact=inFileName).filter(documentName__documentName__exact=inDocumentName).exists() == False):

			if(files.objects.filter(fileName__exact=inFileName).exists()):

				if(documents.objects.filter(documentName__exact=inDocumentName).exists()):

					valid = True
					document = documents.objects.get(documentName__exact=inDocumentName)
					file = files.objects.get(fileName__exact=inFileName)
					is_from.objects.create(documentName=document,fileName=file)
		return valid
	"""
	"method name: insertFoundIn
	"imports: inAgendaCode(string),inDocumentName(string)
	"exports:valid(boolean)
	"description: inserts a row into the foundIn relationship
	"table using the imported information, initially
	"checking if the row already exists. if the row
	"already exists a false will be returned
	"otherwise a true will.
	"""
	def insertFoundIn(inAgendaCode,inDocumentName):
		valid = False
		if(found_in.objects.filter(agendaCode__agendaCode__exact=inAgendaCode).filter(documentName__documentName__exact=inDocumentName).exists() == False):
			if(documents.objects.filter(documentName__exact=inDocumentName).exists()):
				if(agenda_items.objects.filter(agendaCode__exact=inAgendaCode).filter(documentName__documentName__exact=inDocumentName).exists()):

					valid = True
					document = documents.objects.get(documentName__exact=inDocumentName)
					agenda = agenda_items.objects.get(agendaCode__exact=inAgendaCode)
					found_in.objects.create(agendaCode=agenda,documentName=document)
		return valid
	"""
	"method name: insertCompletesWith
	"imports: inJobCreation(timestamp),inJobNumber(int),inFileName(string)
	"exports:valid(boolean)
	"description: inserts a row into the completesWith relationship
	"table using the imported information, initially
	"checking if the row already exists. if the row
	"already exists a false will be returned
	"otherwise a true will.
	"""
	def insertCompletesWith(inJobCreation,inJobNumber,inFileName):
		valid = False
		if(completes_with.objects.filter(jobNumber__jobNumber__exact=inJobNumber).exists() == False):
			if(files.objects.filter(fileName__exact=inFileName).exists()):
				if(jobs.objects.filter(jobNumber__exact=inJobNumber).exists()):

					valid = True
					file = files.objects.get(fileName__exact=inFileName)
					job = jobs.objects.get(jobNumber__exact=inJobNumber)
					completes_with.objects.create(jobCreation=job,fileName=file,jobNumber=job)

		return valid
	"""
	"method name: insertAttended
	"imports:inPhrase(string),inDocumentName(string)
	"exports:valid(boolean)
	"description: inserts a row into the attended relationship
	"table using the imported information, initially
	"checking if the row already exists. if the row
	"already exists a false will be returned
	"otherwise a true will.
	"""
	def insertAttended(inPhrase,inDocumentName):
		valid = False
		if(attended.objects.filter(keyPhrase__keyPhrase__exact=inPhrase).filter(documentName__documentName__exact=inDocumentName).exists() == False):

			if(key_phrases.objects.filter(keyPhrase__exact=inPhrase).exists()):
				phrase = key_phrases.objects.get(keyPhrase__exact=inPhrase)
				if(get.getKeyPhraseType(phrase.keyPhrase) == "councillor"):
					if(documents.objects.filter(documentName__exact=inDocumentName).exists()):

						valid = True
						document = documents.objects.get(documentName__exact=inDocumentName)
						
						phrase.attended.add(document)
						
		
		return valid