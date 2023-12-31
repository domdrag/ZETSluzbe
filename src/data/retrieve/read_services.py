import ast

from src.data.manager.design_manager import DesignManager

from src.data.retrieve.utils.get_services import getServices
from src.data.retrieve.utils.check_service_date_validity import (
    checkServiceDateValidity
    )

from src.share.trace import TRACE

def readServices(offNum):
    weekServices = ''
    try:
        weekServices = getServices(offNum)
    except Exception as e:
        TRACE(e)
        return None
    
    weekServicesData = []
    for weekServiceRawString in weekServices:
        weekService = ast.literal_eval(weekServiceRawString)
        if(not checkServiceDateValidity(weekService)):
            continue
        if(len(weekService) == 2):
            bgColor = DesignManager.getFreeDayColor()
            if(weekService[1] == 'empty' or
               weekService[1] == '' or # za svaki slucaj case-vi
               weekService[1] == ' '):
                bgColor = DesignManager.getErrorColor()
            weekServicesData.append({'day': weekService[0],
                                     'service': '\n'.join(weekService[1:]),
                                     'bg_color': bgColor})
        else:
            weekServicesData.append({'day': weekService[0],
                                     'service': '\n'.join(weekService[1:]),
                                     'bg_color': DesignManager.getServiceColor()})
    return weekServicesData

