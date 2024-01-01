import json

from src.share.filenames import MONTHLY_HOURS_FUND_PATH

def getMonthlyHoursFund(month):
    with open(MONTHLY_HOURS_FUND_PATH, 'r', encoding='utf-8') as monthlyHoursFundFile:
        MONTHLY_HOURS_FUND = json.load(monthlyHoursFundFile)

    if month in MONTHLY_HOURS_FUND:
        return MONTHLY_HOURS_FUND[month]
    else:
        return dict()