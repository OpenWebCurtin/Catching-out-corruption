from fsm.fsm import FileSystemManager
from website.jobs import JobScheduler
from website.search import SearchEngine
from pdfparser.PDFParser import PDFParser

class Components():
    @staticmethod
    def get_file_manager():
        return FileSystemManager()

    @staticmethod
    def get_job_scheduler():
        return JobScheduler()

    @staticmethod
    def get_search_engine():
        return SearchEngine()

    @staticmethod
    def get_pdf_parser():
        return PDFParser()
