import xml.etree.ElementTree as ET
import re
import time

class InfoLocation:
    def __init__(self, page, textBox, textLine, textBBox):
        self.page = page
        self.textBox = textBox
        self.textLine = textLine
        self.textBBox = textBBox


class Agenda:
    def __init__(self, id, start, end, code):
        self.id = id
        self.start = start
        self.end = end
        self.code = code


'#returns the file as a string'
class agendaExtractor(object):
    def getXMLString(self, xmlfile):
        f = open(xmlfile, "r")
        contents = f.read()
        return contents

    def get_symbol_string(self, council, year, sfile):
        f = open(sfile, "r")

        contents = f.read()
        linelist = contents.split('\n')
        for i in linelist:
            commalist = i.split(',')
            if(commalist[0].upper() == council.upper()):
                if(year >= commalist[1] and year <= commalist[2]):
                    print('Matched with council: ' + council + ' and Year: ' + year)
                    return str(commalist[3]) + ',' + str(commalist[4])
        return None
                
    '#searches through xml document, while creating a buffer of buffersize lines to see if there is any combination of buffersize characters that matches agenda pattern'
    def searchxml(self, buffersize, symbollist, root, charArray, elementArray, infoLocationArray, agendaList, fontsize):

        linenum = 0
        agendaCount = 0
        lastagenda = None

        for page in root:
            for textbox in page:
                for textline in textbox:
                    for text in textline:

                        '#record a buffer of last buffersize character values'
                        '#record a buffer of last buffersize elements'
                        '#records a buffer of all hierachal information from last buffersize lines'
                        for i in range(buffersize):
                            charArray[i] = charArray[i+1]
                            elementArray[i] = elementArray[i+1]
                            infoLocationArray[i] = infoLocationArray[i+1]

                        charArray[buffersize] = text.text
                        elementArray[buffersize] = text

                        '#stops program trying to take attribute bbox from text where there is no bbox value'
                        if(text.attrib and text.tag == 'text'):
                            infoLocationArray[buffersize] = InfoLocation(page, textbox, textline, str(text.attrib['bbox']))
                            temp = infoLocationArray[buffersize].textLine.attrib["bbox"]
                        else:
                            infoLocationArray[buffersize] = None


                        validSplit,agendaCode = self.symbolString(symbollist,charArray)


                        #infoLocationArray[buffersize]

                        #str(agenda.end.textLine.attrib["bbox"])


                        if(validSplit and temp != lastagenda):
                            if(self.isFontSize(elementArray, fontsize)):
                                print()
                                print()
                                print('Match')
                                print(agendaCode)
                                lastagenda = infoLocationArray[len(agendaCode)-1].textLine.attrib["bbox"]



                            if(self.isFontSize(elementArray, fontsize)):

                                agendaCount += 1

                                agendaCode.append('_')
                                agendaCode.append(str(agendaCount))

                                '#creates all information required to split agenda, stores in an agendaList'
                                agendaList.append(Agenda(str(agendaCount), infoLocationArray[1], infoLocationArray[len(agendaCode)-3],agendaCode))




    #General Section________________________________________________________________________________________________

    # each cluster should be seperated with a space


    #singular characters represented with themselves delimited by spaces e.g. 1 / 3 6 D

    # 0* represents any number
    # A* represents any capital letter 
    # a* represents any letter
    # -- represents a space

    #repetitions represented by format 'x'^1,3 where 1 and 3 can be any numbers representing the upper and lower bounds of the repetitions 'x' represents any symbol, with quotes excluded in actual string

    #example string for perth 2005:   '-- 0* 0* 0* / 0* 0*'
    #this means a space any 3 numbers, a forward slash then any 2 numbers and a space at the end

    def symbolString(self, slist, bufferarray):
        count = 0
        validsplit = True

        loop = 0
        for i in slist:
            if(len(i) == 1):
                if(bufferarray[count] == i):
                    count += 1
                else:
                    validsplit = False
            elif(len(i) == 2):
                if(i == '--'):
                    if(re.search('\s', str(bufferarray[count]))):
                        count += 1
                    else:
                        validsplit = False
                elif(i == '0*'):
                    if(self.isNumber(bufferarray[count])):        
                        count += 1
                    else:
                        validsplit = False

                elif(i == 'A*'):
                    if(isCapital(bufferarray[count])):
                        count += 1
                    else:
                        validsplit = False

                elif(i == 'a*'):
                    if(isLetter(bufferarray[count])):
                        count += 1
                    else:
                        validsplit = False
                else:
                    raise Exception('cluster is not recognized as an option')

            elif(len(i) == 5 and '^' in i):
                s = i.split('^')
                char = s[0]
                s = s[1].split('-')
                copycount = count
                lowrange = int(s[0])
                highrange = int(s[1])
                loopcount = 0
                for x in range(highrange):
                    #if problems occur try and equal to or greater than
                    if(x <= lowrange):
                        #might need to add an equal to or greater than here if exceptions happen
                        if(count+x > len(bufferarray)):
                            validsplit = False
                            break
                        elif(not bufferarray[count+x] == char):
                            validsplit = False
                            break
                    else:
                        if(count+x > len(bufferarray)):
                            break
                        elif(bufferarray[count+x] == char):
                            loopcount +=1
                        else:
                            break
                    
                    count = copycount + lowrange + loopcount
                        
                        
                

            elif(len(i) == 6 and '^' in i):
                s = i.split('^')
                char = s[0]
                s = s[1].split('-')
                copycount = count
                lowrange = int(s[0])
                highrange = int(s[1])
                loopcount = 0
                for x in range(highrange):
                    if(x < lowrange):
                        if(count+x > len(bufferarray)):
                            validsplit = False
                            break
                        elif(char == '--'):
                            if(not re.search('\s', str(bufferarray[count + x]))):
                                validsplit = False
                                break
                        elif(char == '0*'):
                            if(not self.isNumber(bufferarray[count + x])):
                                validsplit = False
                                break
                        elif(char == 'A*'):
                            if(not isCapital(bufferarray[count+x])):
                                validsplit = False
                                break
                        elif(char == 'a*'):
                            if(not isLetter(bufferarray[count+x])):
                                validsplit = False
                                break
                        else:
                            raise Exception('cluster is not recognized as an option')
                    else:
                        if(count+x >= len(bufferarray)):
                            break
                        elif(char == '--'):
                            if(re.search('\s', str(bufferarray[count + x]))):
                                loopcount += 1
                            else:
                                break
                        elif(char == '0*'):

                            if(self.isNumber(bufferarray[count + x])):
                                loopcount += 1

                            else:      
                                break
                        elif(char == 'A*'):
                            if(isCapital(bufferarray[count+x])):
                                loopcount += 1
                            else:
                                break
                        elif(char == 'a*'):
                            if(isLetter(bufferarray[count+x])):
                                loopcount += 1
                            else:
                                break
                    
                count = copycount + lowrange + loopcount

            else:
                raise Exception('cluster in string is not of length 1,2,5 or 6')




            if(validsplit):
                loop += 1
            else:
                break
        return validsplit, bufferarray[0:count]




    '#checks if an inputed character is a number'
    def isNumber(self, character):
        result = re.search('[0-9]', str(character))
        if result:
            return True
        else:
            return False

    def isCapital(character):
        result = re.search('[A-Z]', str(character))
        if result:
            return True
        else:
            return False

    def isLetter(character):
        result = re.search('[a-zA-Z]', str(character))
        if result:
            return True
        else:
            return False

    '#checks to see if matched pattern also matches agenda split font size'
    def isFontSize(self, array, font):
        valid = True;
        fontcount = 0

        for element in array:
            if(element.attrib):
                if(font == element.attrib['size']):

                    fontcount +=1
        if(fontcount/len(array) <0.5):

            valid = False
            
        return valid


    '#______________________________________________________________________________________________________________________________________________'
    '#splits agendas out of xml document'

    def splitxml(self, contents, agendaList, councilname):
        filecount = 1
        notFirst = False

        filenames = []
        agendanames = []
        agendasize = []

        line1 = ''
        line2 = ''
        line3 = ''

        totalsize = len(contents)

        print('AgendaLocations:\n')

        for agenda in agendaList:


            print(agenda.code)

            agLocation = str(agenda.end.textLine.attrib["bbox"])
            pgLocation = str(agenda.end.page.attrib["bbox"])
            pg = str(agenda.end.page.attrib["id"])

            for i in range(3):
                pgLocation = pgLocation[pgLocation[0:].find(',')+1:]

            for i in range(3):
                agLocation = agLocation[agLocation[0:].find(',')+1:]

            locationString = agLocation+','+pgLocation+','+pg
            print(locationString)
            print('\n')

            parse = str(agenda.end.textBBox)
            split1 = contents[0:].find(parse)

            split2 = contents[split1:].find('</text>')  
            combine = split1 + split2

            split3 = contents[combine+1:].find('<text>')
            combine = combine + split3

            split4 = contents[combine+2:].find('</text>')
            combine = combine + split4

            split5 = contents[combine+2:].find('\n')
            combine = combine + split5

            split = contents[0:combine+2]
            contents = contents[combine+2:]
            
            agendasize.append(combine+2)

            filenames.append(councilname+"agenda"+str(filecount)+".xml")
            agendanames.append(agenda.code)

            f = open('pdfparser/minute_store/' +councilname+"agenda" + str(filecount) + ".xml", "w+")

            '#this loop adds the formatting for the beggining of an xml document, begins after first loop'
            if(notFirst):
                '#line1 & 2, contains <pages> declaration and <page> declaration'
                f.write('<pages>\n')
                line1 = '<page id="' + str(agenda.start.page.attrib["id"])
                line1 += '" bbox="' + str(agenda.start.page.attrib["bbox"])
                line1 += '" rotate="' + str(agenda.start.page.attrib["rotate"]) + '">\n'
                f.write(line1)

                '#line3, contains <textbox> declaration'
                line2 = '<textbox id="' + str(agenda.start.textBox.attrib["id"])
                line2 += '" bbox="' + str(agenda.start.textBox.attrib["bbox"]) + '">\n'
                f.write(line2)

                '#lin4, contains <textline> declaration'
                line3 = '<textline bbox="' + str(agenda.start.textLine.attrib["bbox"]) + '">'
                f.write(line3)

            '#writes first split agenda to file'
            f.write(split)
            f.write('\n</textline>\n</textbox>\n</page>\n</pages>\n')
            notFirst = True
            filecount += 1


        '# writes last agenda to file'
        filenames.append(councilname+"agenda"+str(filecount)+".xml")
        f = open('pdfparser/minute_store/'+councilname+"agenda" + str(filecount) + ".xml", "w+")
        f.write('<pages>\n')
        f.write(line1 + line2 + line3)
        f.write(contents)

        agendasize.append(contents)

        print(filenames)

        return totalsize, agendasize, agendanames, filenames


    #mainsection____________________________________________________________


    def run(self, councilname,meetingdate):
        xml = 'pdfparser/minute_store/minutes.xml'
        symbolfile = 'pdfparser/sfile.txt'
        tree = ET.parse(xml)
        root = tree.getroot()

        #takes in year, not entire date
        meetingdate = meetingdate[0:4]


        sstring = self.get_symbol_string(councilname,meetingdate,symbolfile)

        if(sstring == None):
            raise Exception('Council and Date combination listed not found')

        sstring = sstring.split(',')
        fontsize = sstring[1]
        sstring = sstring[0]

        slist = sstring.split()

        buff = len(slist)


        if('^' in sstring):
            s = sstring.split('^')
            for i in range(len(s)):
                #loops on odd numbers to avoid bad side of split
                if(i != 0):
                    x = s[i].split(' ')
                    x = x[0].split('-')
                    x = x[1]
                    buff += int(x) -1
                

        charArray = [None] * buff
        elementArray = [None] * buff
        infoLocationArray = [None] * buff

        agendaList = []

        self.searchxml(buff-1, slist, root, charArray, elementArray, infoLocationArray, agendaList, fontsize)

        if(len(agendaList) > 3):
            t,ags,a,f = self.splitxml(self.getXMLString(xml), agendaList, councilname)
        else:
            t,ags,a,f = None

        return t,ags,a,f

