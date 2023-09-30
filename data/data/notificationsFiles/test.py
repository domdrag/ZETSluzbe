import pdfplumber

PDF = pdfplumber.open('Obavijest.pdf')
page = PDF.pages[0]

image = page.to_image(resolution = 300)
image.save('UTF ENCODING ČsČčč.png', encoding = 'utf-8')
