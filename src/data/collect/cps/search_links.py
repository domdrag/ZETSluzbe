import requests
from bs4 import BeautifulSoup, SoupStrainer

from src.share.asserts import ASSERT_THROW, ASSERT_NO_THROW

def searchLinks():
    workDayURL = ''
    workDayLinks = []
    saturdayURL = ''
    saturdayLinks = []
    sundayURL = ''
    sundayLinks = []

    payload = {
        'pojam': 'zetovci'
    }

    searchComplete = False
    while not searchComplete:
        try:
            with requests.Session() as s:
                p = s.post('https://www.zet.hr/interno/default.aspx?a=login',
                           data=payload)
                r = s.get('https://www.zet.hr/interno/default.aspx?id=1041')
                content = r.content

                notificationsLinks = []
                for line in BeautifulSoup(content,
                                          parse_only=SoupStrainer('a')):
                    if hasattr(line, "href"):
                        link = line['href']
                        # notifications
                        if ('dubrava/' in link):
                            notificationsLinks.append({'URL': link, 'name': line.text})

                        if('RD' in link):
                            workDayLinks.append({'URL': link, 'name': line.text})
                            #workDayURL = link
                        if('SUB' in link or 'S_internet' in link):
                            saturdayLinks.append({'URL': link, 'name': line.text})
                            #saturdayURL = link
                        if('NED' in link or 'N_internet' in link):
                            sundayLinks.append({'URL': link, 'name': line.text})
                            #sundayURL = link
            searchComplete = True
        except Exception as e:
            TRACE(e)

    ASSERT_THROW(len(saturdayLinks) < 2,  'Nadjeno vise linkova subotnjih rasporeda.')
    ASSERT_THROW(len(sundayLinks) < 2, 'Nadjeno vise linkova nedeljnih rasporeda.')

    # we tolerate no links because we may use old resources
    ASSERT_NO_THROW(len(workDayLinks) < 2, 'Nadjeno vise linkova za raspored za radni dan.')
    ASSERT_NO_THROW(len(workDayLinks) > 0, 'Nije nadjen link za raspored za radni dan.')
    ASSERT_NO_THROW(len(saturdayLinks) == 1, 'Nije nadjen link za subotnji raspored.')
    ASSERT_NO_THROW(len(sundayLinks) == 1, 'Nije nadjen link za nedeljni raspored.')

    return {'workDay': workDayLinks,
            'saturday': saturdayLinks,
            'sunday': sundayLinks,
            'notificationsLinks': notificationsLinks}
