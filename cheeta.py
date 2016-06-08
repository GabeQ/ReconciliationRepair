#cheeta.py

#Created by Matt Dohlen, Chen Pekker, Gabriel Quiroz
#June 2016

#This file is the master Cheeta program that will run in termimal. It takes
#as input a .tree or .newick file, the duplication cost, transfer cost, loss
#cost, population size, and the number of generations. It runs both fixer.py 
# and Jane in order to compute the minimum cost to construct a reconciliation of
#a host and parasite tree (aka the most paresemonious solution). It then compares
#to tell the user whether Jane has the most parsemonious solution, whether there is
#a better solution, or whether there may be a better solution with larger input
#values for Jane.


import calcJaneCost as cjc
import DP
import execJane
import fixer
import Greedy
import makePlot
import MasterReconciliation
import newickFormatReader as nfr
import newickToTreeParser as ntp
import treeToNewickParser as ptn
import orderGraph
import ReconciliationGraph as rg
import sys
import os


def runJane(fileName, popSize, numGen, dVal, tVal, lVal):
    os.system("./Jane/jane-cli.sh -C -p " + str(popSize) + " -i " + str(numGen) + " -c 0 " + str(dVal) + " " + str(tVal) + " " + str(lVal) + " 0 " + str(fileName) + " > janeOut.txt") 
    return "janeOut.txt"
                        
def main():
    #arguments to be provided in the command line
    fileName = sys.argv[1]
    dVal = int(sys.argv[2])
    tVal = int(sys.argv[3])
    lVal = int(sys.argv[4])
    popSize = int(sys.argv[5])
    numGen = int(sys.argv[6])
    newickFile = None
    treeFile = None
    tempFileToRemove = None
    
    #file converter (still waiting on treeToNewickParser)
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
        return
    
    #run fixer.py with .newick file
    fixerCost = fixer.fixer(newickFile, dVal, tVal, lVal)
    
    #run Jane with .tree file
    janeOut = runJane(treeFile, popSize, numGen, dVal, tVal, lVal)
    janeCost = cjc.janeCost(janeOut, dVal, tVal, lVal)
    
    #compare fixer score with Jane score, print results to user
    if fixerCost == janeCost or janeCost < fixerCost:
        print "Jane's solution is optimal"
        print "Optimal Cost: " + janeCost
    elif fixerCost < janeCost:
        print "Jane's solution may or may not be optimal, try running Jane with a larger population size and more generations"
        print "Lower Bound Cost: " #returns the DP output
        print "Jane Cost: " + janeCost
        print "Fixer Cost: " + fixerCost
    
    os.remove(tempFileToRemove)
    return
    
if __name__ == '__main__':
    main()