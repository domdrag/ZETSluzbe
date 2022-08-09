import kivy
from kivy.app import App
from kivy.uix.label import Label

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





class MyApp(App):
    def build(self):
        return Label(text="Hello World")

if __name__ == "__main__":
   MyApp().run()
