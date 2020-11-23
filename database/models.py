"""
"filename: models
"description: a file containing all the models to be used
"by the database, each model represents a table in the database
"it also contains the relationship tables as well
"""
from django.db import models
from database.uploadFile import uploadFile
"""
"class name: key_phrases
"description: a table containing all the key phrases found by the 
"parsers, as well as their types. it also contains the fields for
"the many to many relationships is_within_nm and attended(see below)
"""
class key_phrases(models.Model):

	keyPhrase = models.CharField(max_length = 50, primary_key=True)
	phraseType = models.CharField(max_length = 25)
	isWithinNM = models.ManyToManyField('documents',through = 'is_within_nm')#a many to many relationship with documents
	attended = models.ManyToManyField('documents',related_name="attendedKeyPhrases",through = 'attended')# a many to many relationshpip with documents
	
	class Meta:
		db_table = "key_phrases"
"""
"class name: documents
"description: a table containing all the documents as they taken from
"the file management system. it contains the documents creation date,
"its name, wordcount and wether it is a minute(relevant for relationships
"and searching)
"""
class documents(models.Model):

	documentName = models.CharField(max_length = 50, primary_key=True)
	documentDate = models.DateTimeField()
	wordCount = models.IntegerField()
	isMinute = models.BooleanField(blank=False)#a document must have an option for wether it is a minute or not
	council = models.CharField(max_length = 50,null = True)
	
	
	class Meta:
		db_table = "documents"
"""
"class name: files
"description: a table containing all the files as they uploaded.
"it contains the public filename, they dattime it was uploaded and
"the string for its file location. the file location will be used
"by many other systems to get the files after they are uploaded
"""
class files(models.Model):
	virtualName = models.CharField(max_length = 50)
	fileName = models.CharField(max_length = 50, primary_key=True)
	uploadDateTime = models.DateTimeField()
	docFile = models.FileField(upload_to=uploadFile.fileUp)#creates and contains the file directory for the file as a string
	class Meta:
		db_table = "files"
"""
"class name: jobs
"description: a table containing all the jobs as they are created
"by the job scheduler. it contains all the details neccessary to the job
"and details about when it begins and finished. it also has a "composite
"key" of job creation time and job number. this means the primary key will
"be an id assigned by django and these two fields will treated as keys for
"other features. this is becuase django does not support composite keys.
"it also contains a foreign key for files, for the cases of jobs relating to files
"""
class jobs(models.Model):

	fileName = models.ForeignKey(files,on_delete=models.CASCADE,null = True)#a foreign key for files, it can be null as a job may not involve a file
	jobType = models.CharField(max_length = 50)
	jobStatus = models.CharField(max_length = 50)
	jobNumber = models.IntegerField()
	jobCreation = models.DateTimeField()
	startDateTime = models.DateTimeField()
	completionDateTime = models.DateTimeField()
	class Meta:
		db_table = "jobs"
		unique_together = ['jobCreation', 'jobNumber']#creation of the composite key effect, both fields as considered one unique entity together(no two options of the pair are the same)
		
"""
"class name: agenda_items
"description: a table containing all the agenda_items as they are found
"by the pasrsers. these agenda items have a composite key of the agendacode
"and the document name as a foreign key of documents. this is because agendas
"may have the same code in different minutes, but never in the same minute.
"it also contains the field for the many to many relationship is_within(see below)
"""
class agenda_items(models.Model):

	documentName = models.ForeignKey(documents,on_delete=models.CASCADE,max_length = 50)
	agendaCode = models.CharField(max_length = 200,unique=True)
	agendaName = models.CharField(max_length = 200)
	wordCount = models.IntegerField()
	isWithin = models.ManyToManyField(key_phrases,through = 'is_within')#a many to many relationship with key_phrases
	class Meta:
		db_table = "agenda_items"
		unique_together = ['documentName', 'agendaCode']#creation of the composite key effect, both fields as considered one unique entity together(no two options of the pair are the same)
"""
"class name: is_from
"description: a table of a one to one relationship between files and docuements
"using the keys from these two tables. this relationship represents the to root
"file a document is from. It is one to one in that each document has exactly one
"file it is from and only one document is derived from any given file
"""
class is_from(models.Model):
	documentName = models.OneToOneField('documents',on_delete=models.CASCADE)
	fileName = models.OneToOneField('files',on_delete=models.CASCADE)
	class Meta:
		db_table = "is_from"
		unique_together = ['documentName', 'fileName']
"""
"class name: found_in
"description: a table of a many to one relationship between agenda_items and docuements
"using the keys from these two tables. it is many to one as an agenda may only come from
"one document and a document can have many agendas
"""
class found_in(models.Model):
	documentName = models.ForeignKey(documents,on_delete=models.CASCADE)
	agendaCode = models.ForeignKey(agenda_items,on_delete=models.CASCADE)
	class Meta:
		db_table = "found_in"
		unique_together = ['documentName', 'agendaCode']
"""
"class name: completes_with
"description: a table of a many to one relationship between jobs and files using the keys
"from both tables. this table contains all the jobs that are currently using files. it is a
"many to one relationship because a file may have many jobs, but each job can only work on one
"file.
"""
class completes_with(models.Model):
	jobCreation = models.ForeignKey(jobs,on_delete=models.CASCADE,related_name='jobCreatio',related_query_name='jobsC')
	jobNumber = models.OneToOneField(jobs,on_delete=models.CASCADE,related_name='jobNumbe',related_query_name='jobN')
	fileName = models.ForeignKey(files,on_delete=models.CASCADE)
	class Meta:
		db_table = "completes_with"
		unique_together = ['fileName', 'jobNumber','jobCreation']
"""
"class name: is_within
"description: a table of a many to many relationship between agenda_items and key_phrases using the keys
"from both tables. this table contains all the key phrases found within agenda items. this is the primary
"tree being searched when searching through minute documents. the relationship is many to many as an agenda
"may have multiple key phrases and a key phrase may appear in many agendas
"""
class is_within(models.Model):
	agendaCode = models.ForeignKey(agenda_items, on_delete=models.CASCADE)
	keyPhrase = models.ForeignKey(key_phrases, on_delete=models.CASCADE)
	wordCount = models.IntegerField(default=0)#an extra field for the amount of times the phrase appears in a agenda
	class Meta:
		db_table = "is_within"
		unique_together = ['keyPhrase', 'agendaCode']
"""
"class name: attended
"description: a table of a many to many relationship between documents and key_phrases using the keys
"from both tables. this table contains the attendence of councillors at within certain minutes. this 
"relationship is many to many as a minute may have multiple councillors attending and a councillor can
"attend many meetings
"""
class attended(models.Model):
	keyPhrase = models.ForeignKey(key_phrases, on_delete=models.CASCADE,related_name="attendedKeyPhrases")
	documentName = models.ForeignKey(documents, on_delete=models.CASCADE)
	class Meta:
		db_table = "attended"
		unique_together = ['keyPhrase', 'documentName']
"""
"class name: is_within_nm
"description: a table of a many to many relationship between documents and key_phrases using the keys
"from both tables. this table contains the key phrases in non-minute documents. this reltionship is
"many to many as a key phrase may appear in many non-minute documents and a non-minute document may
"have multiple key phrases
"""
class is_within_nm(models.Model):
	documentName = models.ForeignKey(documents, on_delete=models.CASCADE)
	keyPhrase = models.ForeignKey(key_phrases, on_delete=models.CASCADE)
	wordCount = models.IntegerField(null = True)#an extra field for the amount of times the phrase appears in the document
	class Meta:
		db_table = "is_within_nm"
		unique_together = ['keyPhrase', 'documentName']