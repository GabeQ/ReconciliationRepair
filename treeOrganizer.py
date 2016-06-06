#takes tree from various files and puts them into a new directory
# modified by Chen Pekker

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