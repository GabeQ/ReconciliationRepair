import shutil
import os


for folderName, subfolders, filenames in os.walk('/Users/cssummer16/GitHub/ReconciliationRepair/mediumDTL'): #need to change this for every directory
    for filename in filenames:
        stringName = str(filename)
        if ".tree" in stringName:
            print "YESSSS"
            os.chdir(folderName)
            shutil.copy(filename, "/Users/cssummer16/GitHub/ReconciliationRepair/mediumDTL/mediumOrganizedTrees") #need to change the output file
        print('File inside: ' + folderName + ' <- of that folder: '+ filename)

    print('')