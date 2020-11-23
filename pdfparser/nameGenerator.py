#!/usr/bin/python

import io 
import re
class nameGenerator(object):
    #Name of textfile
    def getString(self, pdf): 
        f = open(pdf, "rt") 
        contents = f.read() 
        return contents

    def returnCouncil(self, minutes, cList):

        cList = cList.split(",")

        countList = [0] * len(cList) 

        minutes = minutes.upper()

        for idx, i in enumerate(cList):
            i = "".join(i.split())
            if(i != ''):
                countList[idx] = minutes.count('OF ' + str(i.upper()))
            else:
                countList[idx] = 0

        total = 0
        for i in countList:
            total += i

        if(total):
            max = 0
            for i in countList:
                if (i > max and i):
                    max = i
            index = countList.index(max)
            name = cList[index]
        else:
            name = 'Not Found'

        return name

    def returnDate(self, minutes, cList):

        date = re.search("\d", minutes)
        if date:
            day = minutes[date.start():].find(" ")
            month = minutes[date.start()+day+1:].find(" ") +1
            year = minutes[date.start()+day+month+1:].find(" ") +1
        
            dateString = minutes[date.start():date.start()+day+month+year]

        return dateString

    def dateValidate(self, date):
        user = ''
        user = input("We found the date of this document was: " + date + " - If this is incorrect, enter the correct date, otherwise press enter:\n")

        if user:
            date = user

        return date    
        
    def councilValidate(self, council):
        user = ''
        user = input("We found the council name of this document was: " + council + " - If this is incorrect, enter the correct name, otherwise press enter:\n")

        if user:
            council = user

        return council  


    def sendToDatabase(nameList):
        print(nameList)

    def run(self):

            text = "pdfparser/minute_store/minutes.txt"
            councilPath = "pdfparser/councilList.txt"

            minutes = self.getString(text)
            councilList = self.getString(councilPath)  

            date = self.returnDate(minutes, councilList)
            council = self.returnCouncil(minutes,councilList)
            
            #date = self.dateValidate(date)
            #cleanDate
            date = date.replace(" ","")

            date = date.upper()
            date = date.replace('JANUARY','-01-')
            date = date.replace('FEBRUARY','-02-')
            date = date.replace('MARCH','-03-')
            date = date.replace('APRIL','-04-')
            date = date.replace('MAY','-05-')
            date = date.replace('JUNE','-06-')
            date = date.replace('JULY','-07-')
            date = date.replace('AUGUST','-08-')
            date = date.replace('SEPTEMBER','-09-')
            date = date.replace('OCTOBER','-10-')
            date = date.replace('NOVEMBER','-11-')
            date = date.replace('DECEMBER','-12-')
            t_date = date.split('-')
            newdate = t_date[2]
            newdate += '-' + t_date[1]
            newdate += '-' + t_date[0]
            date = newdate

            
            generatedName = council+date+".pdf"
            
            #check with the database to see if generated name already exists and therefore is a duplicate

            print("File: " + generatedName + " , has been generated")

            return generatedName, date, council

