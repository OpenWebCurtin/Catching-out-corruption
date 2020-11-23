from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from pdfparser.PDFParser import PDFParser

class Command(BaseCommand):
    def handle(self, *args, **options):


        inPDF = ("pdfparser/minutes.pdf")
        # Parse the document.
        p = PDFParser()
        p.parse(inPDF)
