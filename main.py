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

invoice = 'https://www.zet.hr/interno/UserDocsImages/tp%20dubrava/Slu%C5%BEbe%20za%20sve%20voza%C4%8De/tpd.pdf'
invoice_pdf = download_file(invoice)

pdf = pdfplumber.open(invoice_pdf)
page = pdf.pages[2]
text = page.extract_text()
#print(text)
    
def isFourDigit(x):
    #print(x, '\n')
    #if(not isinstance(x, int)):
    if(not x.isdigit()):
        return False
    #print(x)
    x = int(x)
    if(x>=1000 and x<=9999):
        return True
    return False
    
x = text.find("2621")
text = text[x:]
text = re.split('\s|\n', text)
y = (i for i,v in enumerate(text) if isFourDigit(v))
x1 = next(y)
x2 = next(y)
#print(text)
#x = text.find("02528")
sifre = text[:x2]
#text = text[5:]
#sifre = text.split(' ');
sifre.pop(0)

#print(sifre)

invoice = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20RD_internet%20od%2011.7.22..pdf'
invoice_pdf = download_file(invoice)

def isTwoOrThreeDigit(x):
    #print(x, '\n')
    #if(not isinstance(x, int)):
    if(not x.isdigit()):
        return False
    #print(x)
    x = int(x)
    if(x>=10 and x<=999):
        return True
    return False



vanjski = ""
dani = ['Ponedjeljak', 'Utorak', 'Srijeda',
        'Cetvrtak', 'Petak', 'Subota', 'Nedjelja']
sluzbe = []
pdf = pdfplumber.open(invoice_pdf)
for i in range(0, len(sifre), 1):
    if(sifre[i] == 'O' or sifre[i] == 'O\n'):
        #print(i)
        sluzbe.append('O')
        continue
    pocetak = 0
    stranica = 0
    while(True):
        page = pdf.pages[stranica]
        text = page.extract_text()
        pocetak = text.find(sifre[i])
        if(pocetak != -1):
            break
        stranica += 1
    
    text = text[pocetak:]
    text = re.split('\s|\n', text)
    #print(text)
    # l = ['707', '08.01', 'Draškovićeva', '', '17:24', '00:08', '7,90', '2,13', '4,60\nsmjer', 'Zapruđe', 'smjer', 'Mihaljevac\n108', '08.02', 'PTD', '04:11', '11:02', '8,02', '1,82', '408']
    y = (i for i,v in enumerate(text) if isTwoOrThreeDigit(v))
    x1 = next(y)
    x2 = next(y)
    #print(x1, x2)
    text = text[:x2]
    #vanjski += ''.join(text)
    #print(text)
    firstOccrSmjer = text.index('smjer')
    lastOccrSmjer = len(text) - 1 - text[::-1].index('smjer')
    del text[firstOccrSmjer:lastOccrSmjer]
    del text[3]
    del text[5:8]
    print(text)

    temp = text[0]
    text[0] = 'broj sluzbe: ' + text[0]
    text[1] = 'vozni red: ' + text[1]
    text[2] = text[3] + ', ' + text[2] + ' ' + text[5] + ' ' + ''.join(text[6:])
    text[3] = text[4]
    del text[4:]
    
    sluzbe.append(text)

    

    


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
            size: self.size
            pos: self.pos
''')

class Sluzbe(BoxLayout):
    def __init__(self,table='', **kwargs):
        super().__init__(**kwargs)

        data = {
            'Dan':{0:'Ponedjeljak',1:'Utorak',2:'Srijeda',3:'Cetvrtak',
                 4: 'Petak', 5:'Subota',6:'Nedjelja'},
            'Sluzba':{0:'\n'.join(sluzbe[0]),1:'\n'.join(sluzbe[1]),
                 2:'\n'.join(sluzbe[2]),3:'\n'.join(sluzbe[3]),
                 4:'\n'.join(sluzbe[4]),5:'\n'.join(sluzbe[5]),
                 6:'\n'.join(sluzbe[6])},
        } #data store

        column_titles = [x for x in data.keys()]
        rows_length = len(data[column_titles[0]])
        self.columns = len(column_titles)

        table_data = []
        for y in column_titles:
            table_data.append({'text':str(y),'size_hint_y':None,
                               'height':30,'bcolor':(.05,.30,.80,1)}) #append the data

        for z in range(rows_length):
            for y in column_titles:
                if(sluzbe[z]=='O'):
                    table_data.append({'text':str(data[y][z]),'size_hint_y':None,
                                   'height':100,'bcolor':(.10,.50,.150,1),
                                   'halign':'center', 'valign':'top'}) #append the data
                else:                   
                    table_data.append({'text':str(data[y][z]),'size_hint_y':None,
                                   'height':100,'bcolor':(.06,.25,.50,1),
                                   'halign':'center', 'valign':'top'}) #append the data

        self.ids.table_floor_layout.cols = self.columns #define value of cols to the value of self.columns
        self.ids.table_floor.data = table_data #add table_data to data value

class SluzbeApp(App):
    def build(self):
        return Sluzbe()

if __name__=='__main__':
    SluzbeApp().run()
