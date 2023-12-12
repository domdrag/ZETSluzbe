from src.data.collect.data_collector import DataCollector

def tryout2(queue):
    dataCollector = DataCollector(queue)
    finished = False
    while not finished:
        updateResult = dataCollector.keepCollectingData()
        finished = updateResult['finished']