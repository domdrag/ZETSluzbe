import threading
import multiprocessing

from src.screen.login.dialogs.utils.dots_timer import DotsTimer

def addDots(statusInfoDialog):
    if('...' in statusInfoDialog.text):
        statusInfoDialog.text = statusInfoDialog.text[:-3]
    else:
        statusInfoDialog.text = statusInfoDialog.text + '.'
            

def dataCollectionThreadWrapper(function):
    def wrap(loginScreen, *args, **kwargs):
        loginScreen.statusInfoDialog.auto_dismiss = False
        loginScreen.updateDone = False
        loginScreen.bind(updateDone = loginScreen.statusInfoDialog.dismiss)
        #loginScreen.statusInfoDialog.open()
        thread = threading.Thread(target=function,
                                  args = [loginScreen,
                                          *args],
                                  kwargs=kwargs)
        loginScreen.statusInfoDialog.dotsTimer = \
                DotsTimer(0.5, lambda: addDots(loginScreen.statusInfoDialog))
        loginScreen.statusInfoDialog.dotsTimer.start()
        thread.start() 
        return thread

    return wrap
