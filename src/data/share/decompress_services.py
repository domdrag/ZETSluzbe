import zipfile
import shutil

from src.share.filenames import CENTRAL_DATA_DIR, COMPRESSED_SERVICES_PATH, COMPRESSED_SHIFTS_PATH

def decompressServicesFile(servicesFile):
    with zipfile.ZipFile(COMPRESSED_SERVICES_PATH, 'r', zipfile.ZIP_DEFLATED) as servicesZIP:
        servicesFiles = servicesZIP.namelist()
        if (servicesFile not in servicesFiles):
            return
        with servicesZIP.open(servicesFile) as compressedServices:
            with open(CENTRAL_DATA_DIR + servicesFile, 'wb') as services:
                shutil.copyfileobj(compressedServices, services)

def decompressShiftsFile(shiftsFile):
    with zipfile.ZipFile(COMPRESSED_SHIFTS_PATH, 'r', zipfile.ZIP_DEFLATED) as shiftsZIP:
        shiftsFiles = shiftsZIP.namelist()
        if (shiftsFile not in shiftsFiles):
            return
        with shiftsZIP.open(shiftsFile) as compressedShifts:
            with open(CENTRAL_DATA_DIR + shiftsFile, 'wb') as shifts:
                shutil.copyfileobj(compressedShifts, shifts)