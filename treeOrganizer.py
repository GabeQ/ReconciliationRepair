#takes .tree files from various folders/directories and puts them into a an output folders
# Chen Pekker, June 2016

import shutil
import os


for folderName, subfolders, filenames in os.walk('/Users/cssummer16/GitHub/ReconciliationRepair/mediumDTL'): #need to change this for every directory
    for filename in filenames:
        stringName = str(filename)
        if ".newick" in stringName:
            os.chdir(folderName)
            shutil.copy(filename, "/Users/cssummer16/GitHub/ReconciliationRepair/mediumDTL/mediumNewickTrees") #need to change the output file
        print('File inside: ' + folderName + ' <- of that folder: '+ filename)

    print('')