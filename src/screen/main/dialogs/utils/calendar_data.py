###########################################################
# KivyCalendar (X11/MIT License)
# Calendar & Date picker widgets for Kivy (http://kivy.org)
# https://bitbucket.org/xxblx/kivycalendar
# 
# Oleg Kozlov (xxblx), 2015
# https://xxblx.bitbucket.org/
###########################################################

from calendar import Calendar, monthrange
from datetime import datetime
from locale import getdefaultlocale
import locale as _locale

class TimeEncoding:
    def __init__(self, locale):
        self.locale = locale

    def __enter__(self):
        self.oldlocale = _locale.setlocale(_locale.LC_TIME, self.locale)
        return _locale.getlocale(_locale.LC_TIME)[1]

    def __exit__(self, *args):
        _locale.setlocale(_locale.LC_TIME, self.oldlocale)

def get_month_names():
    return get_month_names_eng()
        
def get_month_names_eng():
    result = ['Sijecanj', 'Veljaca', 'Ozujak', 'Travanj', 'Svibanj', 'Lipanj',
              'Srpanj', 'Kolovoz', 'Rujan', 'Listopad', 'Studeni', 'Prosinac']
        
    return result

def get_days_abbrs():
    result = ['Pon', 'Uto', 'Sri', 'Cet', 'Pet', 'Sub', 'Ned']    
    return result

def calc_quarter(y, m):
    """ Calculate previous and next month """
    
    # Previous / Next month's year number and month number
    prev_y = y
    prev_m = m - 1
    next_y = y
    next_m = m + 1    
    
    if m == 1:
        prev_m = 12
        prev_y = y - 1
    elif m == 12:
        next_m = 1
        next_y = y + 1
        
    return [(prev_y, prev_m), (y, m), (next_y, next_m)]

def get_month(y, m):
    """ 
    Return list of month's weeks, which day 
    is a turple (<month day number>, <weekday number>) 
    """
    
    cal = Calendar()
    month = cal.monthdays2calendar(y, m)
    
    # Add additional num to every day which mark from 
    # this or from other day that day numer
    for week in range(len(month)):
        for day in range(len(month[week])):
            _day = month[week][day]
            if _day[0] == 0:
                this = 0
            else: 
                this = 1
            _day = (_day[0], _day[1], this)
            month[week][day] = _day
    
    # Days numbers of days from preious and next monthes
    # marked as 0 (zero), replace it with correct numbers
    # If month include 4 weeks it hasn't any zero
    if len(month) == 4:
        return month        
    
    quater = calc_quarter(y, m)
    
    # Zeros in first week    
    fcount = 0
    for i in month[0]:
        if i[0] == 0:
            fcount += 1
    
    # Zeros in last week
    lcount = 0
    for i in month[-1]:
        if i[0] == 0:
            lcount += 1
            
    if fcount:
        # Last day of prev month
        n = monthrange(quater[0][0], quater[0][1])[1]
        
        for i in range(fcount):
            month[0][i] = (n - (fcount - 1 - i), i, 0)
            
    if lcount:
        # First day of next month
        n = 1
        
        for i in range(lcount):
            month[-1][-lcount + i] = (n + i, 7 - lcount + i, 0)
            
    return month

def get_quarter(y, m):
    """ Get quarter where m is a middle month """
    
    result = []
    quarter = calc_quarter(y, m)
    for i in quarter:
        result.append(get_month(i[0], i[1]))
        
    return result

def today_date_list():
    """ Return list with today date """
    
    return [datetime.now().day, datetime.now().month, datetime.now().year]
    
def today_date():
    """ Return today date dd.mm.yyyy like 28.02.2015 """

    return datetime.now().strftime("%d.%m.%Y")
