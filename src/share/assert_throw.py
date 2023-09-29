
def ASSERT_THROW(statement, message):
    if (not statement):
        raise Exception(message)