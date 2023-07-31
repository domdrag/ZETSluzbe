import dropbox

RFRSH_TOKEN = 'wIxEqmHW0_IAAAAAAAAAAXS9N4JdzmOIt8rV90Y-uOVCdhhvC23S7qYHSSDSd53a'
                               
def uploadData():
    dbx = dropbox.Dropbox(app_key = '9x72f19ngmg8mqo',
                          app_secret = 'msb8pniq2h76ym3',
                          oauth2_refresh_token = RFRSH_TOKEN)
    # WORKAROUND - connection fails on PC during uploads for some reason
    dataSent = False
    while not dataSent:
        try:
            with open('./data/dropbox/data.zip', 'rb') as f:
                dbx.files_upload(f.read(),
                                 '/data.zip',
                                 mode = dropbox.files.WriteMode.overwrite)
            dataSent = True
        except:
            pass

    configSent = False
    while not configSent:
        try:
            with open('./data/dropbox/config.json', 'rb') as f:
                dbx.files_upload(f.read(),
                                 '/config.json',
                                 mode = dropbox.files.WriteMode.overwrite)
            configSent = True
        except:
            pass
