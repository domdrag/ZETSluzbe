import dropbox

ACCESS_TOKEN = 'sl.BXTD1ZxuUvz_F0pVw5AE4dsoBr1HeV-sXxWq-gLgoVOZkUBgUqnFEgQ7Bg-gLg7D9m9A360VOGPAVoCAiK2ttaliiJcP24lykURZ1am1uaxEvKHxopW-lsjcXEGXiEoBxA7HrAMt'

def updateNeeded():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    dbx.files_download_to_file('data/dropbox/temp/last_record_date.txt',
                               '/last_record_date.txt')
    fileR = open('data/dropbox/temp/last_record_date.txt', 'r')
    currentDate = fileR.read()
    fileR.close()
    fileR = open('data/dropbox/last_record_date.txt', 'r')
    oldDate = fileR.read()
    fileR.close()

    if currentDate == oldDate:
        return False
    return True

def downloadDataFromDropbox():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    dbx.files_download_to_file('data/dropbox/data.zip',
                               '/data.zip')
    dbx.files_download_to_file('data/dropbox/last_record_date.txt',
                               '/last_record_date.txt')
                               
def uploadDataFromDropbox():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    with open('data/data.zip', 'rb') as f:
            dbx.files_upload(f.read(), '/data.zip')

