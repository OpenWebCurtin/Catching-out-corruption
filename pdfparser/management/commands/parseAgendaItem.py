from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
#from pdfparser.PDFParser import PDFParser
from pdfparser.AgendaItemExtractor import AgendaItemExtractor

class Command(BaseCommand):
    def handle(self, *args, **options):


        inXML = ("pdfparser/Perth_2005~Agenda.xml")
        # Parse the document.
        p = AgendaItemExtractor()
        p.parse(inXML)
