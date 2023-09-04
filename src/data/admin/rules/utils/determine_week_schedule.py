import pdfplumber

from datetime import date, timedelta

from src.data.share.get_holidays import getHolidays

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
    fileA = open('data/data/holidays.txt', 'a', encoding='utf-8')
    for holiday in firstStageHolidayList:
        year = holiday.year
        month = holiday.month
        day = holiday.day
        fileA.write(f"{[year, month, day]}\n")
    fileA.close()

def determineWeekSchedule(page, weekSchedule, mondayDate):
    # pdlplumber se gubi kada rect nije obojan u smislu
    # da izbacuje cudne atribute pozicija i velicina
    # program se pouzdava da se ne gubi kada je rect obojan
    weekScheduleDefault = True
    rects = page.rects
    chars = page.chars
    # Special message formatting (0=STANDARD, 1=NON-STANDARD, 2=ERROR).
    ### Check file: src/data/share/get_warning_message.py
    message0 = '0$Uobicajen vozni red.\n'
    message1 = '1$Neuobicajen vozni red. Sugerira se samostalna' \
               ' provjera sluzbi.\n'
    errorMessage = '2$Greska! Provjeriti sluzbe rucno!\n'
    plausibleErrorMessage = 'Moguca greska! Upozoriti admina!\n'
    nonWorkingDays = dict()
    days = ['Ponedjeljak', 'Utorak', 'Srijeda', \
            'Cetvrtak', 'Petak', 'Subota', 'Nedjelja']
    errorOccured = False
    plausibleErrorOccured = False
    
    # check colors
    for idx in range(len(chars)):
        if charsRepresentDays(chars, idx):
            for day in range(0,7):
                charTop = chars[idx + day]['top']
                charBottom = chars[idx + day]['bottom']
                charLeft = chars[idx + day]['x0']
                charRight = chars[idx + day]['x1']
                for rect in rects:
                    rectTop = rect['top']
                    rectBottom = rect['bottom']
                    rectLeft = rect['x0']
                    rectRight = rect['x1']
                    if(charTop > rectTop and charBottom < rectBottom and
                       charLeft > rectLeft and charRight < rectRight):
                        color = rect['non_stroking_color']
                        if color[1] >= 0.9 and color != (1,1,1): # green
                            nonWorkingDays[days[day]] = 'Subota'
                            weekSchedule[day] = 'St'
                            break
                        elif color[0] >= 0.9 and color != (1,1,1): # red
                            nonWorkingDays[days[day]] = 'Nedjelja'
                            weekSchedule[day] = 'Sn'
                            break
                        
            if 'Subota' not in nonWorkingDays:
                # Saturday is not green nor red
                errorOccured = True 
            elif nonWorkingDays['Subota'] == 'Subota':
                del nonWorkingDays['Subota']

            if 'Nedjelja' not in nonWorkingDays or \
               nonWorkingDays['Nedjelja'] == 'Subota':
                # Sunday is not red
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
                # Found day in holidays.txt, but remaked as green not red
                # If it had been red, it would been found in firstStage list
                errorOccured = True
            else:
                # Not found by colors, but present in holidays.txt
                plausibleErrorOccured = True
            nonDefaultDays[days[mondayDiff]] = 'Nedjelja'
            weekSchedule[mondayDiff] = 'Sn'

    if (firstStageHolidayList):
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
            weekSchedule[0] = 'St'
            
    # thursday merge
    if ('Cetvrtak' in nonDefaultDays and \
        nonDefaultDays['Cetvrtak'] == 'Nedjelja'):
        if ('Petak' in nonDefaultDays):
            pass
        else:
            nonDefaultDays['Petak'] = 'Subota'
            weekSchedule[4] = 'St'

    fileW = open('data/data/warnings.txt', 'w', encoding='utf-8')
    if not nonDefaultDays:
        fileW.write(message0)
    else:
        if (errorOccured):
            message1 = errorMessage
        if (plausibleErrorOccured):
            message1 = message1 + plausibleErrorMessage
        fileW.write(message1)

    messageAddOn = 'ni'
    for key,value in nonDefaultDays.items():
        if (value == 'Subota'):
            messageAddOn = 'nji'
        fileW.write('Za {0} se gleda {1}{2} vozni red.\n'.\
                    format(key.lower(), (value[:-1]).lower(), messageAddOn))
    fileW.close()




    
