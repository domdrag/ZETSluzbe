import os
import requests
import pdfplumber
import re
import os.path
import ast
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta, FR
from bs4 import BeautifulSoup, SoupStrainer


holidays2022 = ['15.8.','1.12.','18.11.','25.12.','26.12.']

PDFFile = 'tpd.pdf'
pdf = pdfplumber.open(PDFFile)
page = pdf.pages[0]

rects = page.rects
chars = page.chars
saturdayColor = (0.56471, 0.93333, 0.56471)
sundayColor = (1, 0.71373, 0.75686)

for char in chars:
    if char['text'] in 'SN':
        charTop = char['top']
        charBottom = char['bottom']
        charLeft = char['x0']
        charRight = char['x1']
        for rect in rects:
            rectTop = rect['top']
            rectBottom = rect['bottom']
            rectLeft = rect['x0']
            rectRight = rect['x1']
            if(charTop > rectTop and charBottom < rectBottom and
               charLeft > rectLeft and charRight < rectRight):
                print(rect['non_stroking_color'])

'''
with pdfplumber.open(PDFFile) as PDF:
 
    # citamo sluzbe za ovaj tjedan
    #fileW = open('relevant/services.txt', 'w', encoding='utf-8')
    for page in PDF.pages:
        tables = page.dedupe_chars().find_tables()
        for tableId in tables:
            table = tableId.extract()
            print(table)
            for services in table:
                if(isinstance(services[0], str) and services[0].isnumeric()):
                    if(not services[0]):
                        continue
                    #fileW.write(f"{services[0:8]}\n")
                    if(not services[8]):
                        continue
                    #fileW.write(f"{services[8:]}\n")
    #fileW.close()
'''
