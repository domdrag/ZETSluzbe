from src.share.trace import TRACE

def generateURLs(config):
    activatedTestPackNum = config['ACTIVATED_TEST_PACK_NUM']

    if (activatedTestPackNum):
        TRACE('TEST_PACK_NUM_ACTIVATED - generating test URLs')
        testDomain = config['TEST_DOMAIN']
        testPackURLPattern = testDomain + '/test_pack_' + str(activatedTestPackNum)
        mainPageURL = testPackURLPattern + '/zet.html'
        allServicesURL = testPackURLPattern + config['COMMON_ALL_SERVICES_URL_FULL_PATH']
    else:
        TRACE('GENERATING OFFICIAL ZET URLS')
        mainPageURL = config['ZET_MAIN_PAGE_URL']
        allServicesURL = config['ZET_DOMAIN'] + config['COMMON_ALL_SERVICES_URL_FULL_PATH']

    return {'mainPageURL': mainPageURL, 'allServicesURL': allServicesURL}