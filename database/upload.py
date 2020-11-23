class uploadFile:
	def fileUp(instance, filename):
		extension = filename.split('.')[-1]
		if instance.pk:
			return '{}.{}'.format(instance.pk, ext)
		