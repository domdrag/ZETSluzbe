import datetime

from dateutil.relativedelta import relativedelta, FR
from datetime import date

from src.data.retrieve.utils.get_service_date import getServiceDate

def getTodayDate():
    now = datetime.datetime.now()
    todayDate = date(now.year, now.month, now.day)
    return todayDate

def checkServiceDateValidity(weekService):
    todayDate = getTodayDate()
    serviceDate = getServiceDate(weekService)
    dateDiff = serviceDate - todayDate
    if(dateDiff.days >= 0):
        return True
    else:
        return False
