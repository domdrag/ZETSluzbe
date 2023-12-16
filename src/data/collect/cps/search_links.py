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

                    if ('RD' in linkURL or 'Radni dan' in linkName):
                        workDayLinks.append({'URL': linkURL, 'name': linkName})
                        TRACE('Rules link found: ' + linkName + ' Treated as workDay link.')
                    elif ('SUB' in linkURL or 'S_internet' in linkURL or 'Subota' in linkName):
                        saturdayLinks.append({'URL': linkURL, 'name': linkName})
                        TRACE('Rules link found: ' + linkName + ' Treated as saturday link.')
                    elif ('NED' in linkURL or 'N_internet' in linkURL or 'Nedjelja' in linkName):
                        sundayLinks.append({'URL': linkURL, 'name': linkName})
                        TRACE('Rules link found: ' + linkName + ' Treated as sunday link.')
                    else:
                        specialDayLinks.append({'URL': linkURL, 'name': linkName})
                        TRACE('Rules link found: ' + linkName + ' Treated as specialDay link.')

            searchComplete = True
        except Exception as e:
            TRACE(e)

    ASSERT_THROW(len(saturdayLinks) < 2, "Found multiple saturday links.")
    ASSERT_THROW(len(sundayLinks) < 2, "Found multiple sunday links.")

    # we tolerate no links because we may use old resources
    ASSERT_NO_THROW(len(workDayLinks) < 2, "Found multiple workDay's links.")
    ASSERT_NO_THROW(len(workDayLinks) > 0, 'No workDay link found.')
    ASSERT_NO_THROW(len(saturdayLinks) == 1, 'No saturday link found.')
    ASSERT_NO_THROW(len(sundayLinks) == 1, 'No sunday link found.')

    return {'workDay': workDayLinks,
            'saturday': saturdayLinks,
            'sunday': sundayLinks,
            'specialDay': specialDayLinks,
            'notificationsLinks': notificationsLinks}
