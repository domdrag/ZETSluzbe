# FILE ALSO USED IN:
## data/user/update_required_date_check.py

from datetime import date
import datetime

def getTodayDate():
    now = datetime.datetime.now()
    todayDate = date(now.year, now.month, now.day)
    return todayDate
