#import kivy
#from kivy.app import App
#from kivy.uix.label import Label
#from kivy.uix.gridlayout import GridLayout

import os
import requests
import pdfplumber
import re

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

# Pitaj medu za url-ove
firstURL = 'https://www.zet.hr/interno/UserDocsImages/tp%20dubrava/Slu%C5%BEbe%20za%20sve%20voza%C4%8De/tpd.pdf'
PDFFile = download_file(firstURL)
PDF = pdfplumber.open(PDFFile)
offNum = '2621'

for pageNum in range(len(PDF.pages)):
    page = PDF.pages[pageNum]
    textFirstPDF = page.extract_text()
    indexOffNum = textFirstPDF.find(offNum)
    if(indexOffNum != -1):
        break
    
textCutLeft = textFirstPDF[indexOffNum:]
listCutLeft = re.split('\s|\n', textCutLeft)
nextOffNumGenerator = (i for i,v in enumerate(listCutLeft) if isFourDigit(v))
tempThrow = next(nextOffNumGenerator)
nextOffNum = next(nextOffNumGenerator)
serviceNumbers = listCutLeft[1:nextOffNum]

#############################################

workDayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20RD_internet%20od%2011.7.22..pdf'
saturdayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20RD_internet%20od%2011.7.22..pdf'
sundayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20RD_internet%20od%2011.7.22..pdf'

URL = workDayURL
PDFFile = download_file(URL)
PDF = pdfplumber.open(PDFFile)
services = []
for i in range(0, len(serviceNumbers), 1):
    if(serviceNumbers[i] == 'O' or serviceNumbers[i] == 'O\n'):
        services.append('O')
        continue
    
    if(i == 5):
        URL = saturdayURL
        PDFFile = download_file(URL)
        PDF = pdfplumber.open(PDFFile)
    if(i == 6):
        URL = sundayURL
        PDFFile = download_file(URL)
        PDF = pdfplumber.open(PDFFile)

    
    for pageNum in range(len(PDF.pages)):
        page = PDF.pages[pageNum]
        textSecondPDF = page.extract_text()
        start = textSecondPDF.find(serviceNumbers[i])
        if(start != -1):
            break
    
    textCutLeft = textSecondPDF[start:]
    listCutLeft = re.split('\s|\n', textCutLeft)
    nextServiceGenerator = (i for i,v in enumerate(listCutLeft) if isTwoOrThreeDigit(v))
    tempThrow = next(nextServiceGenerator)
    nextService = next(nextServiceGenerator)
    if(not 'smjer' in listCutLeft[:nextService]): # rana ili srednja
        nextNextService = next(nextServiceGenerator)
        temp = listCutLeft[:nextNextService]
        tempFirstOccrSmjer = temp.index('smjer')
        tempLastOccrSmjer = len(temp) - 1 - temp[::-1].index('smjer')
        tempEmptySignIndex = nextService + temp[nextService:].index('')
        service = listCutLeft[:nextService]
        service = service + temp[tempFirstOccrSmjer:tempLastOccrSmjer]
        
        serviceNumber = service[0]
        driveOrder = service[1]

        emptySignIndex = service.index('')
        occrSmjer = service.index('smjer')
        
        receptionPoint = []
        receptionPoint = receptionPoint + service[2:emptySignIndex] + service[occrSmjer:]
        receptionTime = service[emptySignIndex+1]

        releasePoint = []
        releasePoint = releasePoint + temp[nextService+2:tempEmptySignIndex] + temp[tempLastOccrSmjer:]
        releaseTime = service[emptySignIndex+2]
    else:                                         # kasna
        temp = listCutLeft[:nextService]
        firstOccrSmjer = temp.index('smjer')
        lastOccrSmjer = len(temp) - 1 - temp[::-1].index('smjer')
        del temp[firstOccrSmjer:lastOccrSmjer]
        service = temp

        serviceNumber = service[0]
        driveOrder = service[1]

        emptySignIndex = service.index('')
        occrSmjer = service.index('smjer')
        
        receptionPoint = []
        receptionPoint = receptionPoint + service[2:emptySignIndex] + service[occrSmjer:]
        receptionTime = service[emptySignIndex+1]

        releasePoint = ['PTD']
        releaseTime = service[emptySignIndex+2]
        

    #print(serviceReception)
    # slaganje za layout
    serviceLayout = []
    serviceLayout.append('broj sluzbe: ' + serviceNumber)
    serviceLayout.append('vozni red: ' + driveOrder)
    serviceLayout.append(receptionTime + ', ' + ' '.join(receptionPoint))
    serviceLayout.append(releaseTime + ', ' + ' '.join(releasePoint))
    
    services.append(serviceLayout)


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
        for y in column_titles:
            table_data.append({'text':str(y),'size_hint_y':None,
                               'height':30,'bcolor':(.05,.30,.80,1)}) #append the data

        for z in range(7):    
            if(services[z]=='O'):
                table_data.append({'text':str(data['Dan'][z]),'size_hint_y':None,
                                   'height':20,'bcolor':(.05,.30,.80,1),
                                   'halign':'center', 'valign':'top'}) #append the data
                table_data.append({'text':str(data['Sluzba'][z]),'size_hint_y':None,
                                   'height':500,'bcolor':(.10,.50,.150,1),
                                   'halign':'center', 'valign':'top'}) #append the data 
                
            else:
                table_data.append({'text':str(data['Dan'][z]),'size_hint_y':None,
                                   'height':20,'bcolor':(.05,.30,.80,1),
                                   'halign':'center', 'valign':'top'}) #append the data
                table_data.append({'text':str(data['Sluzba'][z]),'size_hint_y':None,
                                   'height':500,'bcolor':(.06,.25,.50,1),
                                   'halign':'center', 'valign':'top'}) #append the data 

        self.ids.table_floor_layout.cols = self.columns #define value of cols to the value of self.columns
        self.ids.table_floor.data = table_data #add table_data to data value

class SluzbeApp(App):
    def build(self):
        return Sluzbe()

if __name__=='__main__':
    SluzbeApp().run()
