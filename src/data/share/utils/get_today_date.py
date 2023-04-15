# FILE ALSO USED IN:
## data/user/update_required_date_check.py but that file is curr. obsolete

from datetime import date
import datetime

def getTodayDate():
    now = datetime.datetime.now()
    todayDate = date(now.year, now.month, now.day)
    return todayDate
