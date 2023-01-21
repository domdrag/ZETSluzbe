import dropbox
import ast

ACCESS_TOKEN = 'sl.BXVcSMrbkSPrs8i8CwyspJPJVpathdAAccBj9Y3E2OQdoI1ZnqeSTiIwHWyZ1G4bC4wK9cYvDdJSRd_qzlZv3pvyPaegwitScs54KtqaIXxPE_PwMl89xEtwmxsdEe9zpT1wLnHh'

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

