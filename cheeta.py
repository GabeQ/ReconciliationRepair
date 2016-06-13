# cheeta.py

# Created by Matt Dohlen, Chen Pekker, Gabriel Quiroz
# June 2016

# This file is the master Cheeta program that will run in termimal. It takes
# as input a .tree or .newick file, the duplication cost, transfer cost, loss
# cost, population size, and the number of generations. It takes the file
# and stores it as both a .newick and .tree file (since Jane takesin .tree
# files and the DP and fixer take in .newick files). It runs both fixer.py
# and Jane in order to compute the minimum cost to construct a reconciliation of
# a host and parasite tree (aka the most paresemonious solution). It then compares
# to tell the user whether Jane has the most parsemonious solution, whether there
# is a better solution, or whether there may be a better solution with larger
# input values for Jane.

import fixer
import JaneUtil
import MasterReconciliation
import newickToTreeParser as ntp
import treeToNewickParser as ptn
import exceptions as ex
import sys
import os

fileName = None
dVal = 2
tVal = 3
lVal = 1
popSize = 30
numGen = 30
verbose = False
limit = None

def usage():
    print "usage: cheeta.py [-v] [-l {limit}] [-c {dupCost, transCost, lossCost}] [-p {popSize, numGen}] file"
    exit(1)


def readArgs():
    global fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit
    
    i = 1
    if len(sys.argv) > 2:
        while i < len(sys.argv) - 1:
            
            if sys.argv[i] == '-v':
                verbose = True
                i += 1
            elif sys.argv[i] == '-l':
                try:
                    limit = sys.argv[i+1]
                    i += 2
                except:
                    usage()
            elif sys.argv[i] == '-c':
                try:
                    dVal = int(sys.argv[i+1])
                    tVal = int(sys.argv[i+2])
                    lVal = int(sys.argv[i+3])
                    i += 4
                except:
                    usage()
            elif sys.argv[i] == '-p':
                try:
                    popSize = int(sys.argv[i+1])
                    numGen = int(sys.argv[i+2])
                    i += 3
                except:
                    usage()
            else:
                print 'Command not recognized'
                usage()
    print i
    print sys.argv[i]
    if '.tree' not in sys.argv[i] or '.newick' not in sys.argv[i]:
        print 'No filename ending in .tree or .newick provided'
        usage()
    else:
        fileName = sys.argv[i]
            
                
        
    
                       
def main():
    
    readArgs()
    # arguments to be provided in the command line
    fileName = sys.argv[1]
    dVal = int(sys.argv[2])
    tVal = int(sys.argv[3])
    lVal = int(sys.argv[4])
    popSize = int(sys.argv[5])
    numGen = int(sys.argv[6])
    newickFile = None
    treeFile = None
    tempFileToRemove = None
    
    # file converter
    if '.tree' in fileName:
        treeFile = fileName
        newickFile = ptn.treeToNewickParser(fileName)
        tempFileToRemove = newickFile
    elif '.newick' in fileName or '.nwk' in fileName:
        newickFile = fileName
        treeFile = ntp.newickToTreeParser(fileName)
        tempFileToRemove = treeFile
    else:
        print "The file must be in either '.tree' or '.newick' format"
        exit(1)

    # test if the DP is temporally consistent and get DP Cost
    recs, allRecs, DPCost = MasterReconciliation.Reconcile(["", newickFile, dVal, tVal, lVal, "unit", 0, 1, 0, 1])
    
    if len(recs) == 0:  # no infeasible reconciliations found --> no need for fixer algorithm
        fixerCost = float('inf')
    else:
        fixerCost = fixer.fix(newickFile, dVal, tVal, lVal) # run fixer.py with .newick file

    # run Jane with .tree file
    janeOut = JaneUtil.runJane(treeFile, popSize, numGen, dVal, tVal, lVal)
    janeCost = JaneUtil.janeCost(janeOut, dVal, tVal, lVal)

    # compare fixer score with Jane score
    if DPCost == janeCost:  # Jane's solution is optimal
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Jane's Solution is Optimal"
        return

    elif fixerCost < janeCost:  # fixer found a better solution than Jane
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Cheeta found a valid solution of cost: " + str(fixerCost)
        print "You may wish to try running Jane again with larger values for the population and/or generation parameters"
        return

    else:  # fixer was unable to find a better solution than Jane
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Cheeta was unable to find a valid solution better than Jane"
        print "You may wish to try running Jane again with larger values for the population and/or generation parameters"

    try:
        os.remove(tempFileToRemove)
        os.remove(janeOut)
    except OSError:
        pass

    return

    
if __name__ == '__main__':
    main()
