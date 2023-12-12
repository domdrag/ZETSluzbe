from src.data.manager.logs_manager import LogsManager
from src.data.manager.config_manager import loadConfig
from src.data.manager.design_manager import loadDesign
from src.app.utils.environment_setup import environmentSetup

LogsManager.beginLogging()
loadConfig()
environmentSetup()
loadDesign()
print('yoka')

if __name__ == '__main__':
    from src.app.zet_app import ZETApp
    ZETApp().run()