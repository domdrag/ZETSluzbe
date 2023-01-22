import dropbox
import ast

ACCESS_TOKEN = 'sl.BXa8uiO6hF3pNBfPuqn4zcgn2WUJiOmE2cRmEF956nq1R5LpCfw7N6h0VuxGYccQrgI1SVsaHz1a54TLwblHC6jJ_6xJJ_6XniabMBbSbEf9YtqYzwjxsmzEdp2-l1eetzwpKGxu'

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

