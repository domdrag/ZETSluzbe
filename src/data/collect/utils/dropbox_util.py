import dropbox
import ast

ACCESS_TOKEN = 'sl.BXWP8aIKlGTrj-Fmbr6UpBPOxVc-Rr6jIeYOiGihISZLUlBNhQZQDD0UBtJ1okejwk1piyZs1R2UJjI00yYc3ipMJIHLHTT4gG3oLEbPhTOswbNQzZPMG15wQDdf6UIKQC0ifp95'

def updateNeeded():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    dbx.files_download_to_file('data/dropbox/last_record_date.txt',
                               '/last_record_date.txt')
    fileR = open('data/data/last_record_date.txt', 'r')
    currentDate = fileR.read()
    currentDate = ast.literal_eval(currentDate)
    fileR.close()
    fileR = open('data/dropbox/last_record_date.txt', 'r')
    oldDate = fileR.read()
    oldDate = ast.literal_eval(oldDate)
    fileR.close()
    
    if currentDate == oldDate:
        return False
    return True

def downloadData():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    dbx.files_download_to_file('data/dropbox/data.zip',
                               '/data.zip')
                               
def uploadData():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    with open('data/dropbox/data.zip', 'rb') as f:
            dbx.files_upload(f.read(),
                             '/data.zip',
                             mode = dropbox.files.WriteMode.overwrite)
    with open('data/data/last_record_date.txt', 'rb') as f:
            dbx.files_upload(f.read(),
                             '/last_record_date.txt',
                             mode = dropbox.files.WriteMode.overwrite)

