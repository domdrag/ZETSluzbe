import dropbox
import ast

RFRSH_TOKEN = 'wIxEqmHW0_IAAAAAAAAAAXS9N4JdzmOIt8rV90Y-uOVCdhhvC23S7qYHSSDSd53a'

def updateNeeded():
    dbx = dropbox.Dropbox(app_key = '9x72f19ngmg8mqo',
                          app_secret = 'msb8pniq2h76ym3',
                          oauth2_refresh_token = RFRSH_TOKEN)
    
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
    dbx = dropbox.Dropbox(app_key = '9x72f19ngmg8mqo',
                          app_secret = 'msb8pniq2h76ym3',
                          oauth2_refresh_token = RFRSH_TOKEN)
    dbx.files_download_to_file('data/dropbox/data.zip',
                               '/data.zip')
                               
def uploadData():
    dbx = dropbox.Dropbox(app_key = '9x72f19ngmg8mqo',
                          app_secret = 'msb8pniq2h76ym3',
                          oauth2_refresh_token = RFRSH_TOKEN)
    with open('data/dropbox/data.zip', 'rb') as f:
            dbx.files_upload(f.read(),
                             '/data.zip',
                             mode = dropbox.files.WriteMode.overwrite)
    with open('data/data/last_record_date.txt', 'rb') as f:
            dbx.files_upload(f.read(),
                             '/last_record_date.txt',
                             mode = dropbox.files.WriteMode.overwrite)

