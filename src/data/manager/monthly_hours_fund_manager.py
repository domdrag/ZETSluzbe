import json

def getMonthlyHoursFund(month):
    with open('data/monthly_hours_fund.json', 'r', encoding='utf-8') as monthlyHoursFundFile:
        MONTHLY_HOURS_FUND = json.load(monthlyHoursFundFile)

    return MONTHLY_HOURS_FUND[month]