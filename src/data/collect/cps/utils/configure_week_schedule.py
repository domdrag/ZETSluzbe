import pdfplumber

from datetime import date, timedelta

from src.data.retrieve.get_holidays import getHolidays
from src.data.manager.warning_messages_manager import WarningMessagesManager
from src.share.trace import TRACE
from src.share.asserts import ASSERT_NO_THROW

MAX_X_COORD_CHARS_GAP = 0.1

def getAllRectsInsideChar(char, rects):
    charTop = char['top']
    charBottom = char['bottom']
    charLeft = char['x0']
    charRight = char['x1']
    foundRects = []
    for rect in rects:
        rectTop = rect['top']
        rectBottom = rect['bottom']
        rectLeft = rect['x0']
        rectRight = rect['x1']
        if (charTop > rectTop and charBottom < rectBottom and
                charLeft > rectLeft and charRight < rectRight):
            foundRects.append(rect)
    return foundRects

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

def addHolidays(firstStageHolidayList):
    fileA = open('data/central_data/holidays.txt', 'a', encoding='utf-8')
    for holiday in firstStageHolidayList:
        year = holiday.year
        month = holiday.month
        day = holiday.day
        fileA.write(f"{[year, month, day]}\n")
    fileA.close()

def configureWeekSchedule(page, weekSchedule, mondayDate):
    # pdlplumber se gubi kada rect nije obojan u smislu
    # da izbacuje cudne atribute pozicija i velicina
    # program se pouzdava da se ne gubi kada je rect obojan
    weekScheduleDefault = True
    rects = page.rects
    chars = page.chars

    message0 = 'Uobicajen vozni red.'
    message1 = 'Neuobicajen vozni red. Sugerira se samostalna provjera sluzbi.'
    errorMessage = 'Greska! Pogledati logove!'
    plausibleErrorMessage = 'Moguca greska! Pogledati logove!'
    nonWorkingDays = dict()
    days = ['Ponedjeljak', 'Utorak', 'Srijeda', \
            'Cetvrtak', 'Petak', 'Subota', 'Nedjelja']
    errorOccured = False
    plausibleErrorOccured = False
    
    # check colors
    for idx in range(len(chars)):
        if charsRepresentDays(chars, idx):
            # days row check
            TRACE('----------------------------------------')
            for day in range(0,7):
                insideRects = getAllRectsInsideChar(chars[idx + day], rects)
                for insideRect in insideRects:
                    color = insideRect['non_stroking_color']
                    if color[1] >= 0.9 and color != (1, 1, 1):  # green
                        TRACE('Found ' + days[day] + ' as green cell on days-row.')
                        nonWorkingDays[days[day]] = 'Subota'
                        weekSchedule[day] = 'ST'
                        break
                    elif color[0] >= 0.9 and color != (1, 1, 1):  # red
                        TRACE('Found ' + days[day] + ' as red cell on days-row.')
                        nonWorkingDays[days[day]] = 'Nedjelja'
                        weekSchedule[day] = 'SN'
                        break

            # below days row check, skip table on the right first
            idx += 1 # chars no longer represent days
            while (not charsRepresentDays(chars, idx)):
                idx = idx + 1 # aiming for days row on table on the right
            idx += 7 # reach uncolored day-numbers on table on the left
            while (not (chars[idx]['text']).isalpha()):
                idx = idx + 1 # aiming for first service

            TRACE('----------------------------------------')
            for day in range(0, 7):
                insideRects = getAllRectsInsideChar(chars[idx + day], rects)
                for insideRect in insideRects:
                    color = insideRect['non_stroking_color']
                    unMatchingColorsMessage = 'COLORS MISMATCH BETWEEN DAYS-ROW AND FIRST-SERVICES-ROW FOR '
                    if color[1] >= 0.9 and color != (1, 1, 1):  # green
                        TRACE('Found ' + days[day] + ' as green cell on first-services-row.')
                        if (nonWorkingDays[days[day]] != 'Subota'):
                            plausibleErrorOccured = True
                            checkedDay = str(days[day])
                            TRACE('COLORS MISMATCH BETWEEN DAYS-ROW AND FIRST-SERVICES-ROW FOR ' + checkedDay)
                            nonWorkingDays[days[day]] = 'Subota'
                            weekSchedule[day] = 'ST'
                        break
                    elif color[0] >= 0.9 and color != (1, 1, 1):  # red
                        TRACE('Found ' + days[day] + ' as red cell on first-services-row.')
                        if (nonWorkingDays[days[day]] != 'Nedjelja'):
                            plausibleErrorOccured = True
                            checkedDay = str(days[day])
                            TRACE('COLORS MISMATCH BETWEEN DAYS-ROW AND FIRST-SERVICES-ROW FOR ' + checkedDay)
                            nonWorkingDays[days[day]] = 'Nedjelja'
                            weekSchedule[day] = 'SN'
                        break

                while (chars[idx + day]['x1'] + MAX_X_COORD_CHARS_GAP >= chars[idx + 1 + day]['x0']):
                    idx = idx + 1
            TRACE('----------------------------------------')

            if 'Subota' not in nonWorkingDays:
                # Saturday is not green nor red
                TRACE('Saturday not marked green nor red on days-row.')
                errorOccured = True 
            elif nonWorkingDays['Subota'] == 'Subota':
                del nonWorkingDays['Subota']

            if 'Nedjelja' not in nonWorkingDays or \
               nonWorkingDays['Nedjelja'] == 'Subota':
                # Sunday is not red
                TRACE('Sunday not marked red on days-row.')
                errorOccured = True
            else:
                del nonWorkingDays['Nedjelja']

            break

    nonDefaultDays = nonWorkingDays
    # All holidays should already be listed in holidays.txt so this
    # list should be empty after checking holidays.txt
    firstStageHolidayList = []
    for nonDefaultDay in list(nonDefaultDays.keys()):
        if nonDefaultDays[nonDefaultDay] == 'Nedjelja' and \
           nonDefaultDay in days:
            mondayDiff = days.index(nonDefaultDay)
            holidayDate = mondayDate + timedelta(days = mondayDiff)
            firstStageHolidayList.append(holidayDate)

    sundayDate = mondayDate + timedelta(days = 6)
    holidays = getHolidays()
    for holiday in holidays:
        year = holiday[0]
        if year == 0: # fixed holiday every year
            # only if it's New Year check the sunday year
            # Remark: only checking sunday year wouldn't work for Christmas
            # in case Christmas falls on monday
            if (holiday[1] == 1 and holiday[2] == 1):
                year = sundayDate.year
            else:
                year = mondayDate.year
            
        holidayDate = date(year, holiday[1], holiday[2])
        if (mondayDate <= holidayDate < sundayDate):
            if holidayDate in firstStageHolidayList:
                # Already found holiday by looking at colors -> expected
                firstStageHolidayList.remove(holidayDate)
                continue
            mondayDiff = (holidayDate - mondayDate).days
            dayToModify = days[mondayDiff]
            if (dayToModify in nonDefaultDays and
                nonDefaultDays[dayToModify] == 'Subota'):
                # Found day in holidays.txt, but remarked as green not red
                # If it had been red, it would been found in firstStage list
                TRACE('Found holiday (' + str(holidayDate) + ') in database, '
                      'but remarked as green on days-row.')
                errorOccured = True
                weekSchedule[mondayDiff] = 'ST'
            else:
                # Not found by colors, but present in holidays.txt
                TRACE('Found holiday (' + str(holidayDate) + ') in database, '
                      'but not remarked as red on days-row.')
                plausibleErrorOccured = True
                nonDefaultDays[dayToModify] = 'Nedjelja'
                weekSchedule[mondayDiff] = 'SN'

    if (firstStageHolidayList):
        TRACE('Found holidays/nonWorkingDays (' + str(firstStageHolidayList) + ') by colors on days-row, '
              'but not present in database.')
        plausibleErrorOccured = True
        # In case the program found a holiday by looking colors in pdf
        # and the same holiday hasn't been found in holidays.txt, we decided
        # to put the holiday in holidays.txt so the calendar can receive it.
        # Anyhow, the plausible error message will be shown on login screen
        ## and possible issue needs to be checked by the admin.
        addHolidays(firstStageHolidayList)

    # add saturday line of traffic
    # tuesday merge
    if ('Utorak' in nonDefaultDays and nonDefaultDays['Utorak'] == 'Nedjelja'):
        if ('Ponedjeljak' in nonDefaultDays):
                pass
        else:
            nonDefaultDays['Ponedjeljak'] = 'Subota'
            weekSchedule[0] = 'ST'
            
    # thursday merge
    if ('Cetvrtak' in nonDefaultDays and \
        nonDefaultDays['Cetvrtak'] == 'Nedjelja'):
        if ('Petak' in nonDefaultDays):
            pass
        else:
            nonDefaultDays['Petak'] = 'Subota'
            weekSchedule[4] = 'ST'

    if not nonDefaultDays:
        WarningMessagesManager.addWarningMessage(message0)
    else:
        if (errorOccured):
            message1 = errorMessage
        if (plausibleErrorOccured):
            message1 = message1 + '\n' + plausibleErrorMessage
        WarningMessagesManager.addWarningMessage(message1)

    for dayIndex in range(len(weekSchedule)):
        warningMessage = ''
        typeOfDay = weekSchedule[dayIndex]

        if dayIndex < 5 and typeOfDay != 'W':
            warningMessage = ('Za {0} se gleda se gleda vozni red za {1} ili poseban raspored.'.
                              format(days[dayIndex], 'Subotu' if typeOfDay == 'ST' else 'Nedjelju'))
        elif dayIndex == 5 and typeOfDay != 'ST':
            warningMessage = ('Za Subotu se gleda se gleda vozni red za {0} ili poseban raspored.'.
                              format('Nedjelju' if typeOfDay == 'SN' else 'Radni dan'))
        elif dayIndex == 6 and typeOfDay != 'SN':
            warningMessage = ('Za Nedjelju se gleda se gleda vozni red za {0} ili poseban raspored.'.
                              format('Subotu' if typeOfDay == 'ST' else 'Radni dan'))

        if (warningMessage):
            WarningMessagesManager.addWarningMessage(warningMessage)




    
