# assert keyword not working on Android for some reason
from src.share.trace import TRACE

def ASSERT_THROW(statement, message):
    if (not statement):
        raise Exception(message)

def ASSERT_NO_THROW(statement, message):
    if (not statement):
        TRACE(message)