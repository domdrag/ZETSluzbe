import zipfile
import shutil

CENTRAL_DATA_DIR = 'data/central_data/'
COMPRESSED_SERVICES_PATH = CENTRAL_DATA_DIR + 'services.zip'
COMPRESSED_SHIFTS_PATH = CENTRAL_DATA_DIR + 'shifts.zip'

def decompressServicesFile(servicesFile):
    with zipfile.ZipFile(COMPRESSED_SERVICES_PATH, 'r', zipfile.ZIP_DEFLATED) as servicesZIP:
        servicesFiles = servicesZIP.namelist()
        if (servicesFile not in servicesFiles):
            # new colleague detected when adding services
            return
        with servicesZIP.open(servicesFile) as compressedServices:
            with open(CENTRAL_DATA_DIR + servicesFile, 'wb') as services:
                shutil.copyfileobj(compressedServices, services)

def decompressShiftsFile(shiftsFile):
    with zipfile.ZipFile(COMPRESSED_SHIFTS_PATH, 'r', zipfile.ZIP_DEFLATED) as shiftsZIP:
        shiftsFiles = shiftsZIP.namelist()
        if (shiftsFile not in shiftsFiles):
            # new colleague detected
            return
        with shiftsZIP.open(shiftsFile) as compressedShifts:
            with open(CENTRAL_DATA_DIR + shiftsFile, 'wb') as shifts:
                shutil.copyfileobj(compressedShifts, shifts)