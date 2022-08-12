#import kivy
#from kivy.app import App
#from kivy.uix.label import Label
#from kivy.uix.gridlayout import GridLayout

import os
import requests
import pdfplumber
import re
import os.path
import ast

def download_file(url):
    local_filename = url.split('/')[-1]
    
    with requests.get(url) as r:
        assert r.status_code == 200, f'error, status code is {r.status_code}'
        with open(local_filename, 'wb') as f:
            f.write(r.content)
        
    return local_filename

def isFourDigit(x):
    if(not x.isdigit()):
        return False
    x = int(x)
    if(x>=1000 and x<=9999):
        return True
    return False

def isTwoOrThreeDigit(x):
    if(not x.isdigit()):
        return False
    x = int(x)
    if(x>=10 and x<=999):
        return True
    return False

def isAlphaWithSpaces(x):
    if(x == ''):
        return False
    y = re.split('\n|\.| ',x)
    for el in y:
        if(el == ''):
            continue
        if(not el.isalpha()):
            return False
    return True


# Pitaj medu za url-ove
firstURL = 'https://www.zet.hr/interno/UserDocsImages/tp%20dubrava/Slu%C5%BEbe%20za%20sve%20voza%C4%8De/tpd.pdf'
offNum = '2545'

################################################################

filePath = 'firstPDF.txt'
if(os.path.exists(filePath) and os.stat(filePath).st_size):
    fileR = open(filePath, 'r', encoding='utf-8')
    textFirstPDF = fileR.read()
    indexOffNum = textFirstPDF.find(offNum)
    fileR.close()
else:
    PDFFile = download_file(firstURL)
    PDF = pdfplumber.open(PDFFile)
    for pageNum in range(len(PDF.pages)):
        page = PDF.pages[pageNum]
        textFirstPDF = page.extract_text()
        indexOffNum = textFirstPDF.find(offNum)
        if(indexOffNum != -1):
            break
    fileW = open(filePath, 'w', encoding='utf-8')
    fileW.writelines(textFirstPDF)
    fileW.close()
    
############################################################## 

textCutLeft = textFirstPDF[indexOffNum:]
listCutLeft = re.split(' |\n', textCutLeft)
nextOffNumGenerator = (i for i,v in enumerate(listCutLeft) if isFourDigit(v))
tempThrow = next(nextOffNumGenerator)
nextOffNum = next(nextOffNumGenerator)
serviceNumbers = listCutLeft[1:nextOffNum]

#############################################

workDayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20RD_internet%20od%2011.7.22..pdf'
saturdayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20SUB_internet%20od%2016.7.22..pdf'
sundayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20NED_internet%20od%2026.6.22..pdf'

services = []

for i in range(0, len(serviceNumbers), 1):
    if(serviceNumbers[i] == 'O' or serviceNumbers[i] == 'O\n'):
        services.append('O')
        continue
    
    if(i == 5):
        URL = saturdayURL
        fileStart = 'saturdayPage'
    elif(i == 6):
        URL = sundayURL
        fileStart = 'sundayPage'
    else:
        URL = workDayURL
        fileStart = 'workDayPage'
    
    mPage = 0
    while(True):
        filePath = fileStart+str(mPage)+'PDF.txt'
        if(os.path.exists(filePath) and os.stat(filePath).st_size):
            fileR = open(filePath, 'r', encoding='utf-8')
            mTextSecondPDF = fileR.read()
            mStart = mTextSecondPDF.find(serviceNumbers[i])
            if(mStart != -1):
                fileR.close()
                break
            fileR.close()
        else:
            PDFFile = download_file(URL)
            PDF = pdfplumber.open(PDFFile)
            page = PDF.pages[mPage]
            mTextSecondPDF = page.extract_text()
            mStart = mTextSecondPDF.find(serviceNumbers[i])
            fileW = open(filePath, 'w', encoding='utf-8')
            fileW.writelines(mTextSecondPDF)
            fileW.close()
            if(mStart != -1):
                break
        mPage = mPage + 1

    mTable = 0
    while(True):
        filePath = fileStart+str(mPage)+'Table'+str(mTable)+'PDF.txt'
        # postoji opasnost da file nestane nakon cekiranja, pripazi !!
        if(os.path.exists(filePath) and os.stat(filePath).st_size):
            fileR = open(filePath, 'r', encoding='utf-8')
            lines = fileR.readlines()
            fileR.close()
            lines = [line.rstrip() for line in lines]
            found = False
            for line in lines:
                line = ast.literal_eval(line)
                #print(line)
                if(serviceNumbers[i] in line):
                    found = True
                    serviceLine = line
                    break
            if(found):
                break
            
        else:
            page = PDF.pages[mPage]
            tables = page.find_tables()
            table = tables[mTable].extract()
            fileW = open(filePath, 'w', encoding='utf-8')
            for mList in table:
                fileW.write(f"{mList}\n")
            fileW.close()
            found = False
            for serviceLine in table:
                if(serviceNumbers[i] in serviceLine):
                    found = True
                    break
            if(found):
                break
            
        mTable = mTable + 1
        
    '''
    PDFFile = download_file(URL)
    PDF = pdfplumber.open(PDFFile)
    for pageNum in range(len(PDF.pages)):
        page = PDF.pages[pageNum]
        textSecondPDF = page.extract_text()
        start = textSecondPDF.find(serviceNumbers[i])
        if(start != -1):
            break

    tables = page.find_tables()
    for tableId in tables:
        found = False
        table = tableId.extract()
        for serviceLine in table:
            if(serviceNumbers[i] in serviceLine):
                found = True
                break
        if(found):
            break'''
    #print(serviceLine)
    #print(serviceNumbers[i])
    serviceStartIndex = serviceLine.index(serviceNumbers[i])
    #print(serviceStartIndex)
    serviceNumber = serviceLine[serviceStartIndex]
    #print(serviceNumber)
    driveOrder = serviceLine[serviceStartIndex+1]
    receptionPoint = serviceLine[serviceStartIndex+2].replace('\n','')
    receptionTime = serviceLine[serviceStartIndex+3]
    
    if(receptionPoint == 'PTD' or receptionPoint == 'PTT'):
        driveOrder = 'PRIČUVA'
        releasePoint = receptionPoint
    else:
        releasePoint = 'PTD'
        for element in serviceLine[serviceStartIndex+3:]:
            if(isAlphaWithSpaces(element)):
                releasePoint = element.replace('\n','')
            
    releaseTime = serviceLine[serviceStartIndex+4]
        
    
    # slaganje za layout
    serviceLayout = []
    serviceLayout.append('broj sluzbe: ' + serviceNumber)
    serviceLayout.append('vozni red: ' + driveOrder)
    serviceLayout.append(receptionTime + ', ' + receptionPoint)
    serviceLayout.append(releaseTime + ', ' + releasePoint)
    
    services.append(serviceLayout)


print(services)


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

#kv codes
Builder.load_string('''
<Sluzbe>:
    id: main_win
    RecycleView:
        viewclass: 'CustomLabel'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None,250)
            default_size_hint: (1,None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
<CustomLabel@Label>:
    bcolor: (1,1,1,1)
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: root.size
            pos: self.pos
''')

class Sluzbe(BoxLayout):
    def __init__(self,table='', **kwargs):
        super().__init__(**kwargs)

        data = {
            'Dan':{0:'Ponedjeljak',1:'Utorak',2:'Srijeda',3:'Cetvrtak',
                 4: 'Petak', 5:'Subota',6:'Nedjelja'},
            'Sluzba':{0:'\n'.join(services[0]),1:'\n'.join(services[1]),
                 2:'\n'.join(services[2]),3:'\n'.join(services[3]),
                 4:'\n'.join(services[4]),5:'\n'.join(services[5]),
                 6:'\n'.join(services[6])},
        } #data store

        #column_titles = [x for x in data.keys()]
        #rows_length = len(data[column_titles[0]])
        #self.columns = len(column_titles)

        column_titles = ['Dan/Sluzba']
        rows_length = 7*2
        self.columns = 1

        table_data = []
        #for y in column_titles:
          #  table_data.append({'text':str(y),'size_hint_y':None,
         #                      'height':30,'bcolor':(.05,.30,.80,1)}) #append the data

        for z in range(7):    
            if(services[z]=='O'):
                table_data.append({'text':str(data['Dan'][z]),'size_hint_y':None,
                                   'height':100,'bcolor':(.05,.30,.80,1),
                                   'halign':'center', 'valign':'top'}) #append the data
                table_data.append({'text':str(data['Sluzba'][z]),'size_hint_y':None,
                                   'height':300,'bcolor':(.10,.50,.150,1),
                                   'halign':'center', 'valign':'top'}) #append the data 
                
            else:
                table_data.append({'text':str(data['Dan'][z]),'size_hint_y':None,
                                   'height':100,'bcolor':(.05,.30,.80,1),
                                   'halign':'center', 'valign':'top'}) #append the data
                table_data.append({'text':str(data['Sluzba'][z]),'size_hint_y':None,
                                   'height':300,'bcolor':(.06,.25,.50,1),
                                   'halign':'center', 'valign':'top'}) #append the data 

        self.ids.table_floor_layout.cols = self.columns #define value of cols to the value of self.columns
        self.ids.table_floor.data = table_data #add table_data to data value

class SluzbeApp(App):
    def build(self):
        return Sluzbe()

if __name__=='__main__':
    SluzbeApp().run()

