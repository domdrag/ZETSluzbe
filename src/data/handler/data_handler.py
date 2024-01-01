from src.data.collect.data_collector import DataCollector, STARTING_OUTPUT_MESSAGE
from src.data.manager.config_manager import ConfigManager

from src.data.share.synchronization_util import gatherRemoteCentralData
from src.data.handler.utils.load_data import loadBasicData, loadCentralData

from src.share.trace import TRACE

def loadDataAtStartup():
    loadBasicData()
    if (ConfigManager.dataCorrupted()):
        TRACE('ERROR IN LAST UPDATE - REPAIRING CENTRAL DATA')
        recoverData()
    loadCentralData()
    TRACE('DATA LOADED')

def updateData(outputStream):
    outputStream.message = STARTING_OUTPUT_MESSAGE
    dataCollector = DataCollector()
    updateResult = {'finished': False}
    while not updateResult['finished']:
        updateResult = dataCollector.keepCollectingData()
        finished = updateResult['finished']
        outputStream.message = updateResult['message']

    if (updateResult['error']):
        recoverData()
    else:
        TRACE('DATA UPDATE FINISHED SUCCESSFULLY')

    loadCentralData()
    return updateResult

def recoverData():
    TRACE('RECOVERING CENTRAL DATA')
    try:
        ConfigManager.initiateDataRecovery()
        gatherRemoteCentralData()
        ConfigManager.completeDataRecovery()
    except Exception as e:
        TRACE(e)
        raise Exception('Recovering data failed')
    TRACE('CENTRAL DATA RECOVERED')

