import ast

from src.data.share.utils.check_service_date_validity import (
    checkServiceDateValidity
    )
from src.data.share.design_manager import (getPrimaryColor,
                                          getServiceColor,
                                          getFreeDayColor,
                                          getErrorColor)


def readServices(offNum):
    filePath = 'data/data/all_services_by_driver_decrypted/' + offNum + '.txt'
    weekServices = ''
    
    try:
        fileR = open(filePath, 'r', encoding='utf-8')
        weekServices = fileR.readlines()
        fileR.close()
    except:
        return None
    
    weekServicesData = []
    for weekServiceRawString in weekServices:
        weekService = ast.literal_eval(weekServiceRawString)
        if(not checkServiceDateValidity(weekService)):
            continue
        if(len(weekService) == 2):
            bgColor = getFreeDayColor()
            if(weekService[1] == 'empty' or
               weekService[1] == '' or # za svaki slucaj case-vi
               weekService[1] == ' '):
                bgColor = getErrorColor()
            weekServicesData.append({'day': weekService[0],
                                     'service': '\n'.join(weekService[1:]),
                                     'bg_color': bgColor})
        else:
            weekServicesData.append({'day': weekService[0],
                                     'service': '\n'.join(weekService[1:]),
                                     'bg_color': getServiceColor()})
    return weekServicesData

