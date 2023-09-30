# assert keyword not working on Android for some reason
def ASSERT_THROW(statement, message):
    if (not statement):
        raise Exception(message)