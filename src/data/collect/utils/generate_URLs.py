from src.data.manager.config_manager import ConfigManager
from src.share.trace import TRACE

def generateURLs():
    activatedTestPackNum = ConfigManager.getConfig('ACTIVATED_TEST_PACK_NUM')

    if (activatedTestPackNum):
        TRACE('TEST_PACK_NUM_ACTIVATED - generating test URLs')
        testDomain = ConfigManager.getConfig('TEST_DOMAIN')
        testPackURLPattern = testDomain + '/test_pack_' + str(activatedTestPackNum)
        mainPageURL = testPackURLPattern + '/zet.html'
        allServicesURL = testPackURLPattern + ConfigManager.getConfig('COMMON_ALL_SERVICES_URL_FULL_PATH')
    else:
        TRACE('GENERATING OFFICIAL ZET URLS')
        mainPageURL = ConfigManager.getConfig('ZET_MAIN_PAGE_URL')
        allServicesURL = (ConfigManager.getConfig('ZET_DOMAIN') +
                          ConfigManager.getConfig('COMMON_ALL_SERVICES_URL_FULL_PATH'))

    return {'mainPageURL': mainPageURL, 'allServicesURL': allServicesURL}