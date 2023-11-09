import warnings

import requests
import re
import warnings
from bs4 import BeautifulSoup, SoupStrainer, GuessedAtParserWarning

warnings.filterwarnings('ignore', category=GuessedAtParserWarning)

from src.data.collect.cps.utils.regex_definitions import RegexDefinitions
from src.data.manager.config_manager import getConfig
from src.share.asserts import ASSERT_THROW, ASSERT_NO_THROW
from src.share.trace import TRACE

def isValidRulesLink(linkName, linkURL):
    dateMatch = re.search(RegexDefinitions.dateRegex, linkName)
    return (bool(dateMatch) and
            ('rada/' in linkURL or '/Oglasne'  in linkURL))


def searchLinks():
    workDayLinks = []
    saturdayLinks = []
    sundayLinks = []
    specialDayLinks = []

    payload = {
        'pojam': 'zetovci'
    }

    searchComplete = False
    while not searchComplete:
        try:
            config = getConfig()
            if (config['TEST_CONFIGURATION_ACTIVATED']):
                TRACE('TEST_CONFIGURATION_ACTIVATED - searching links on custom html file')
                with open('zet.html', 'r',encoding = 'utf-8') as fileR:
                    content = fileR.read()
            else:
                with requests.Session() as s:
                    p = s.post('https://www.zet.hr/interno/default.aspx?a=login',
                               data=payload)
                    r = s.get('https://www.zet.hr/interno/default.aspx?id=1041')
                    content = r.content

            notificationsLinks = []
            for line in BeautifulSoup(content,
                                      parse_only=SoupStrainer('a')):
                if hasattr(line, "href"):
                    linkURL = line['href']
                    linkName = line.text

                    # notifications
                    if ('dubrava/' in linkURL):
                        notificationsLinks.append({'URL': linkURL, 'name': linkName})
                        continue

                    if (not isValidRulesLink(linkName, linkURL)):
                        continue

                    TRACE('Rules link found: ' + linkName)

                    if ('RD' in linkURL):
                        workDayLinks.append({'URL': linkURL, 'name': linkName})
                    elif ('SUB' in linkURL or 'S_internet' in linkURL):
                        saturdayLinks.append({'URL': linkURL, 'name': linkName})
                    elif ('NED' in linkURL or 'N_internet' in linkURL):
                        sundayLinks.append({'URL': linkURL, 'name': linkName})
                    else:
                        specialDayLinks.append({'URL': linkURL, 'name': linkName})

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
            'specialDay': specialDayLinks,
            'notificationsLinks': notificationsLinks}
