
def countPreviouslyAddedServices(oldMissingServices):
    return sum(int(service == 0) for service in oldMissingServices)