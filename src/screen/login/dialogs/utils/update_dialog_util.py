import threading

from src.screen.login.dialogs.utils.dots_timer import DotsTimer

def addDots(infoDialog):
    if('...' in infoDialog.text):
        infoDialog.text = infoDialog.text[:-3]
    else:
        infoDialog.text = infoDialog.text + '.'
            

def showDialog(function):
    def wrap(loginScreen, *args, **kwargs):
        loginScreen.infoDialog.auto_dismiss = False
        loginScreen.updateDone = False  
        loginScreen.bind(updateDone = loginScreen.infoDialog.dismiss)  
        loginScreen.infoDialog.open()
        thread = threading.Thread(target=function,
                                  args = [loginScreen,
                                          *args],
                                  kwargs=kwargs)  
        loginScreen.infoDialog.dotsTimer = \
                DotsTimer(0.5, lambda: addDots(loginScreen.infoDialog))
        loginScreen.infoDialog.dotsTimer.start()
        thread.start() 
        return thread

    return wrap
