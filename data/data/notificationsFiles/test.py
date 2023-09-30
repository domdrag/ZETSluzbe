import pdfplumber

PDF = pdfplumber.open('Obavijest.pdf')
page = PDF.pages[0]

image = page.to_image(resolution = 300)
text = 'UTF ENCODING ČČčč'
encodedText = text.encode('utf8')
image.save(encodedText + '.png')
