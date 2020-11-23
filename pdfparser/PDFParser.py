import os
from os import path

from pdfparser.DependPDFParser import DependPDFParser
from pdfparser.agendaExtractor import agendaExtractor
from pdfparser.nameGenerator import nameGenerator
from pdfparser.AgendaItemExtractor import AgendaItemExtractor
from pdfparser.pdf2xml import pdf2xml
from pdfparser.pdf2text import pdf2text
from database.insert import insert

#Main function, imports other programs within file to run their methods

class PDFParser(DependPDFParser):



    def parse(self,inPDF):

        validfile = 0

        #Converts pdf document named minutes.pdf to a text document named minutes.txt
        try:
            pdf2text.run(inPDF)
        except Exception as e:
            validfile = 1
            print("failed pdf to text")
            raise

        #Converts pdf document named minutes.pdf to an xml document named minutes.xml
        if validfile == 0:
            try:
                pdf2xml.run(inPDF)
            except Exception as e:
                validfile = 2
                print("failed pdf to xml")

        #Parses through the minutes.txt document to retrieve council name and council date, returns both of these and filename generated from them
        if validfile == 0:
            gen = nameGenerator()
            try:

                genName,date,councilName  = gen.run()
            except Exception as e:
                validfile = 3
                print("failed to generate council name or date")
                raise

        #insertKeyPhrase


        #insertAttended(inPhrase,inDocumentName) 




        #Run with name and council date from above program, this parses through the xml document and splits apart the agendas

        if validfile == 0:
            age = agendaExtractor()
            try:
                minutesize, agendasizes, agendanames, filelist = age.run(councilName,date)
                if(agendanames == None):
                    validfile = 4
            except Exception as e:
                print("failed extracting the agenda, possibly due to unsupported format")
                validfile = 4
                raise

#  insertDocument(inDocumentName,inDate,inWordcount,inIsMinute,inCouncil)
#   documentname (string)
#   date (timestamp)
#   wordcountdoc (int)
#   isminute (boolean)   =   always true in this section
#   incouncil (string)

        if validfile == 0:
            try:
                print(date)
                insert.insertDocument(genName,date,minutesize,True,councilName)
            except Exception as e:
                validfile = 5
                print("failed inserting document to the database")
                raise

#  insertAgendaItem(inAgendaCode, inDocumentName, inWordCount)
#  agenda code (string)
#  document name (string)
#  wordcount (int)

        if validfile == 0:
            try:   
                for i in range(len(agendanames)):
                    insert.insertAgendaItem(''.join(agendanames[i]),genName,agendasizes[i])
            except Exception as e:
                validfile = 5
                print("failed inserting agenda to the database, possibly due to not being unique")
    
        if validfile == 0:
            try:

                agendaParser = AgendaItemExtractor()
                ii = 0
                agendanames.append('Lastone')
                for i in filelist:
                    agen = agendanames[ii]
                    agendaParser.parse(i,genName,agen)
                    ii = ii + 1
            except Exception as e:
                validfile = 6
                print("Error in AgendaItemExtractor or Spacy")
                raise

        d_path = 'pdfparser/minute_store/'


        print("EOF")
        filelist = [ f for f in os.listdir(d_path)]
        for f in filelist:
           os.remove(os.path.join(d_path, f))
           f = open(d_path + "nothing" + ".txt", "w+")
           f.write('nothing')

        return validfile
    
