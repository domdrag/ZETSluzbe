import threading

from src.screen.login.dialogs.utils.dots_timer import DotsTimer

def addDots(updateDialog):
    if('...' in updateDialog.text):
        updateDialog.text = updateDialog.text[:-3]
    else:
        updateDialog.text = updateDialog.text + '.'
            

def showDialog(function):
    def wrap(loginScreen, *args, **kwargs):
        loginScreen.updateDialog.auto_dismiss = False
        loginScreen.updateDone = False  
        loginScreen.bind(updateDone = loginScreen.updateDialog.dismiss)  
        loginScreen.updateDialog.open()
        thread = threading.Thread(target=function,
                                  args = [loginScreen,
                                          *args],
                                  kwargs=kwargs)  
        loginScreen.updateDialog.dotsTimer = \
                DotsTimer(0.5, lambda: addDots(loginScreen.updateDialog))
        loginScreen.updateDialog.dotsTimer.start()
        thread.start() 
        return thread

    return wrap
