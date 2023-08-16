import json

def getLinks():
    with open('data/links.json', 'r', encoding='utf-8') as linksFile:
        LINKS = json.load(linksFile)

    return LINKS

def readLinks():
    links = getLinks()
    linksData = []

    for linkText, linkURL in links.items():
        linksData.append({'linkText': linkText,
                          'linkURL': linkURL['URL']})
    return linksData

