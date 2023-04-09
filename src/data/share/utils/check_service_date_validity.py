from dateutil.relativedelta import relativedelta, FR

from src.data.share.utils.get_today_date import getTodayDate
from src.data.share.utils.get_service_date import getServiceDate

def checkServiceDateValidity(weekService):
    todayDate = getTodayDate()
    serviceDate = getServiceDate(weekService)
    dateDiff = serviceDate - todayDate
    if(dateDiff.days >= 0):
        return True
    else:
        return False
