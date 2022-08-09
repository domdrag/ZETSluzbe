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
#print(page.extract_text())



class MyApp(App):
    def build(self):
        return Label(text="Hello")

if __name__ == "__main__":
   MyApp().run()
