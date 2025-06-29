import os
import subprocess
import sys

from test_utils.custom_print import customPrint

preferredTestPackNum = None
tracesEnabled = '1'
for argNameId in range(1, len(sys.argv), 2):
    argValueId = argNameId + 1
    if (sys.argv[argNameId] == '--testpack'):
        assert int(sys.argv[argValueId]) 
        preferredTestPackNum = sys.argv[argValueId]
    elif (sys.argv[argNameId] == '--traces'):
        assert sys.argv[argValueId].isdigit()
        argValue = int(sys.argv[argValueId])
        assert argValue == 0 or argValue == 1
        tracesEnabled = sys.argv[argValueId]
    elif (sys.argv[argNameId] == '--help'):
        print('py verify.py [--testpack <NUM>] [--traces <0/1>]')
        sys.exit()
    else:
        print('Invalid command')
        sys.exit()

# Running existing scripts on each test pack
'''
TEST_PACKS_DIR = 'test_packs/'
testPacksDirs = os.listdir(TEST_PACKS_DIR)
for testPackDir in testPacksDirs:
    testFileName = 'verify_' + testPackDir + '.py'
    subprocess.run(['python', testFileName],
                   cwd = TEST_PACKS_DIR + testPackDir)
'''

# Running one script for each test pack
TEST_PACKS_DIR = 'test_packs/'
TEST_VERIFICATION_SCRIPT_PATH = 'test_utils/verify_test_pack.py'
testPacksDirs = os.listdir(TEST_PACKS_DIR)
        
for testPackDir in testPacksDirs:
    if (preferredTestPackNum and testPackDir[-1] != preferredTestPackNum):
        continue

    verifScriptDestDir = TEST_PACKS_DIR + testPackDir
    customPrint('VERIFIYING ' + testPackDir.upper() + ' ...')
    subprocess.run(['python', os.path.relpath(TEST_VERIFICATION_SCRIPT_PATH,
                                              verifScriptDestDir),
                    tracesEnabled],
                   cwd = verifScriptDestDir)

customPrint('TEST RESULTS')
for testPackDir in testPacksDirs:
    verifScriptDestDir = TEST_PACKS_DIR + testPackDir
    fileR = open(verifScriptDestDir + '/out.txt', 'r')
    testResult = fileR.read()
    fileR.close()

    if testResult == '1':
        print(testPackDir.upper() + ': SUCCESSFUL')
    elif testResult == '0':
        print(testPackDir.upper() + ': FAILED DUE TO DATA COLLECTION COMPARISON')
    else:
        print(testPackDir.upper() + ': FAILED DUE TO COMPILATION ERROR')
customPrint('TEST END')