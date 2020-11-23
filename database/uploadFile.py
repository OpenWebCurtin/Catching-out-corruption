from database import models 
class uploadFile:
	def fileUp(instance, filename):
		if instance.pk:
			return instance.pk
	def getHighestFileNum():
		fileList = models.files.objects.all()
		num = 1
		for file in fileList:
			name = file.fileName
			nameSplit = name.split('.')
			nameInt = int(nameSplit[0])
			if(nameInt > num):
				num = nameInt
		return num