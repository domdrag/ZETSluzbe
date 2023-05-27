from datetime import date, timedelta

def setHolidays(mondayDate, weekSchedule):
    fileW = open('data/data/holidays.txt', 'a', encoding='utf-8')
    fileW.write(f"{[mondayDate.year, mondayDate.month, mondayDate.day]}\n")
    for dayIndex in range(6):
        if (weekSchedule[dayIndex] == 'St'):
            holidayDate = mondayDate + timedelta(days=dayIndex)
            year = holidayDate.year
            month = holidayDate.month
            day = holidayDate.day
            
            fileW.write(f"{[year, month, day]}\n")
    fileW.close()
