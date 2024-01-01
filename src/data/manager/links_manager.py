import json

from src.share.filenames import LINKS_PATH

def getLinks():
    with open(LINKS_PATH, 'r', encoding='utf-8') as linksFile:
        LINKS = json.load(linksFile)

    return LINKS