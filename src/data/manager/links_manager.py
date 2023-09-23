import json

def getLinks():
    with open('data/links.json', 'r', encoding='utf-8') as linksFile:
        LINKS = json.load(linksFile)

    return LINKS