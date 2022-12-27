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
curves = page.curves
saturdayColor = (0.56471, 0.93333, 0.56471)
sundayColor = (1, 0.71373, 0.75686)

im = page.to_image(resolution=150)
im.reset().debug_tablefinder()
im.save('./pic.jpg')

def charsRepresentDays(chars, idx):
    if(chars[idx]['text'] == 'P' and \
       chars[idx + 1]['text'] == 'U' and \
       chars[idx + 2]['text'] == 'S' and \
       chars[idx + 3]['text'] == 'Č' and \
       chars[idx + 4]['text'] == 'P' and \
       chars[idx + 5]['text'] == 'S' and \
       chars[idx + 6]['text'] == 'N'):
        return True
    else:
        return False
    
for idx in range(len(chars)):
        if charsRepresentDays(chars, idx):
            for day in range(0,7):
                charTop = chars[idx + day]['top']
                charBottom = chars[idx + day]['bottom']
                charLeft = chars[idx + day]['x0']
                charRight = chars[idx + day]['x1']
                for rect in rects:
                    rectTop = rect['top']
                    rectBottom = rect['bottom']
                    rectLeft = rect['x0']
                    rectRight = rect['x1']
                    if(charTop > rectTop and charBottom < rectBottom and
                       charLeft > rectLeft and charRight < rectRight):

                        if rect['non_stroking_color'][1] >= 0.9: # green
                            print(rect['non_stroking_color'])
                            break
                        elif rect['non_stroking_color'][0] >= 0.9: # red
                            print(rect['non_stroking_color'])
                            break


'''
for idx in range(len(chars)):
    if charsRepresentDays(chars, idx):
        print('sexy')

for idx in range(len(chars)):
        if charsRepresentDays(chars, idx):
            for day in range(0,7):
                charTop = chars[idx + day]['top']
                charBottom = chars[idx + day]['bottom']
                charLeft = chars[idx + day]['x0']
                charRight = chars[idx + day]['x1']
                print(day)
                print(charTop, charBottom, charLeft, charRight)
                print('\n')
                for rect in rects:
                    rectTop = rect['top']
                    rectBottom = rect['bottom']
                    rectLeft = rect['x0']
                    rectRight = rect['x1']
                    rectBottom1 = rect['y0']
                    rectTop1 = rect['y1']
                    height = rect['height']
                    width = rect['width']
                    color = rect['non_stroking_color']
                    print('HEIGHT: ', height, ' WIDTH :', width, ' COLOR: ', color)
                    #if(charLeft > rectLeft and charRight < rectRight):
                     #   print(rectTop, rectBottom, rectLeft, rectRight, height, sep = '\n')
                     #   print('\n')
    
                break
'''
'''
for rect in rects:
    if rect['non_stroking_color'] == saturdayColor or \
       rect['non_stroking_color'] == sundayColor:
        rectTop = rect['top']
        rectBottom = rect['bottom']
        rectLeft = rect['x0']
        rectRight = rect['x1']
        for char in chars:
            charTop = char['top']
            charBottom = char['bottom']
            charLeft = char['x0']
            charRight = char['x1']
            if(charTop > rectTop and charBottom < rectBottom and
               charLeft > rectLeft and charRight < rectRight):
                print(char['text'])
'''

'''
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
                print(rect['non_stroking_color'])'''

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
