import os

class FileSystemManager:
    STATUS_OK = 0
    STATUS_FILE_NO_EXIST = 1

    def add_file(self, filename, file):
        # TODO implement
        pass

    def file_exists(self, filename):
        # Just a stub.
        # TODO implement
        if filename == "File_Exists":
            return True
        return False

    def delete_upload(self, upload_file):
        status = self.STATUS_OK
        path = 'uploads/%s' % (str(upload_file))

        exists = os.path.exists(path)

        if (exists):
            os.remove(path)
        else:
            status = STATUS_FILE_NO_EXIST
            #status = self.STATUS_OK

        return status

