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
from database.get import get
"""
"class name: insert
"description: a class for safely deleting information from the database
"""
class delete():
	"""
	"method name: deleteKeyPhrase
	"imports: inPhrase(string)
	"exports:delete(boolean)
	"description: deletes a row in the key_phrases
	"table using the imported information calling the
	"get class. if there is no row based on the imported
	"key, then false will be returned, otherwise it is
	"deleted and true is returned
	"""
	def deleteKeyPhrase(inPhrase):
		deleted = False
		phraseObj = get.getKeyPhraseObject(inPhrase)
		if(phraseObj != None):
			phraseObj.delete()
			deleted = True
		return deleted
	"""
	"method name: deleteAgendaItem
	"imports: inAgendaCode(string),inDocumentName(string)
	"exports:delete(boolean)
	"description: deletes a row in the agenda_items
	"table using the imported information calling the
	"get class. if there is no row based on the imported
	"key, then false will be returned, otherwise it is
	"deleted and true is returned
	"""
	def deleteAgendaItem(inAgendaCode,inDocumentName):
		deleted = False
		agendaObj = get.getAgendaItemObject(inAgendaCode,inDocumentName)
		if(agendaObj != None):
			agendaObj.delete()
			deleted = True
		return deleted
	"""
	"method name: deleteDocument
	"imports:inDocumentName(string)
	"exports:delete(boolean)
	"description: deletes a row in the documents
	"table using the imported information calling the
	"get class. if there is no row based on the imported
	"key, then false will be returned, otherwise it is
	"deleted and true is returned
	"""
	def deleteDocument(inDocumentName):
		deleted = False
		documentObj = get.getDocumentObject(inDocumentName)
		if(documentObj != None):
			documentObj.delete()
			deleted = True
		return deleted
	"""
	"method name: deleteFile
	"imports:inFileName(string)
	"exports:delete(boolean)
	"description: deletes a row in the files
	"table using the imported information calling the
	"get class. if there is no row based on the imported
	"key, then false will be returned, otherwise it is
	"deleted and true is returned
	"""
	def deleteFile(inFileName):
		deleted = False
		fileObj = get.getFileObject(inFileName)
		if(fileObj != None):
			fileObj.delete()
			deleted = True
		return deleted
	"""
	"method name: deleteJob
	"imports:inJobNumber(int),inJobCreation(timestamp)
	"exports:delete(boolean)
	"description: deletes a row in the jobs
	"table using the imported information calling the
	"get class. if there is no row based on the imported
	"key, then false will be returned, otherwise it is
	"deleted and true is returned
	"""
	def deleteJob(inJobNumber,inJobCreation):
		deleted = False
		jobObj = get.getJobObject(inJobNumber,inJobCreation)
		if(jobObj != None):
			jobObj.delete()
			deleted = True
		return deleted
	"""
	"method name: deleteAgendaPhrases
	"imports:inAgendaCode(string)
	"exports:delete(boolean)
	"description: deletes all key_phrase rows
	"associated with an agenda through the is_within
	"relationship.if there is no row based on the imported
	"key, then false will be returned, otherwise it is
	"deleted and true is returned
	"""
	def deleteAgendaPhrases(inAgendaCode):
		deleted = False
		if(is_within.objects.filter(agendaCode__exact=inAgendaCode).exists()):
			phrases = is_within.objects.filter(agendaCode__exact=inAgendaCode)
			for phrase in phrases:
				if(is_within.objects.filter(keyPhrase__exact=phrase).count() == 1):
					phrase.delete()
					deleted = True
		return deleted
	"""
	"method name: deletefileDocument
	"imports:inFileName(string)
	"exports:delete(boolean)
	"description: deletes the document associated with
	"a filename.if there is no row based on the imported
	"key, then false will be returned, otherwise it is
	"deleted and true is returned
	"""
	def deleteFileDocument(inFileName):
		deleted = False
		if(is_from.objects.filter(fileName__exact=inFileName).exists()):
			isFromObj = is_from.objects.get(fileName__exact=inFileName)
			isFromObj.documentName.delete()
			deleted = True
		return deleted
	"""
	"method name: deleteDocumentFile
	"imports:inFileName(string)
	"exports:delete(boolean)
	"description: deletes the file associated with
	"a documentName.if there is no row based on the imported
	"key, then false will be returned, otherwise it is
	"deleted and true is returned
	"""
	def deleteDocumentFile(inDocumentName):
		deleted = False
		if(is_from.objects.filter(documentName__exact=inDocumentName).exists()):
			isFromObj = is_from.objects.get(documentName__exact=inDocumentName)
			isFromObj.fileName.delete()
			deleted = True
		return deleted
	"""
	"method name: deleteJobFile
	"imports:inJobNumber(int),inJobCreation(timestamp)
	"exports:delete(boolean)
	"description: deletes the file associated with
	"a job.if there is no row based on the imported
	"key, then false will be returned, otherwise it is
	"deleted and true is returned
	"""
	def deleteJobFile(inJobNumber,inJobCreation):
		deleted = False
		fileName = get.getJobFileName(inJobNumber,inJobCreation)
		
		if(fileName != None):
			fileObj = get.getFile(fileName)
			if(fileObj != None):
				fileObj.delete()
				deleted = True
		return deleted