from src.data.manager.links_manager import getLinks

def readLinks():
    links = getLinks()
    linksData = []

    for linkText, linkURL in links.items():
        linksData.append({'linkText': linkText,
                          'linkURL': linkURL['URL']})
    return linksData

