#cheeta.py

#Created by Matt Dohlen, Chen Pekker, Gabriel Quiroz
#June 2016

#This file is the master Cheeta program that will run in termimal. It takes
#as input a .tree or .newick file, the duplication cost, transfer cost, loss
#cost, population size, and the number of generations. It takes the file
#and stores it as both a .newick and .tree file (since Jane takesin .tree
#files and the DP and fixer take in .newick files). It runs both fixer.py 
#and Jane in order to compute the minimum cost to construct a reconciliation of
#a host and parasite tree (aka the most paresemonious solution). It then compares
#to tell the user whether Jane has the most parsemonious solution, whether there
#is a better solution, or whether there may be a better solution with larger
#input values for Jane.


import calcJaneCost as cjc
import DP
import execJane
import fixer
import Greedy
import makePlot
import MasterReconciliation
import newickFormatReader as nfr
import newickToTreeParser as ntp
import orderGraph
import ReconciliationGraph as rg
import sys
import os
                        
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
    
    #file converter (still waiting on treeToNewickParser)
    if '.tree' in fileName:
        treeFile = fileName
        newickFile = None
    elif '.newick' in fileName:
        newickFile = fileName
        treeFile = ntp.newickToTreeParser(fileName)
    else:
        print "The file must be in either '.tree' or '.newick' format"
        return
        
    #run the DP with .newick file
    DTL, numRecon, DPCost = DP.reconcile(newickFile, dVal, tVal, lVal)

    #test if the DP is temporally consistent
    recs, allRecs = MasterReconciliation.Reconcile(["", fileName, str(dVal), str(tVal), str(lVal), "unit", 0, 1, 0, 1])
    if len(recs) == 0: #no infeasible reconciliations found --> no need for fixer algorithm
        fixerCost = float('inf')
    else:
        fixerCost = fixer.fixer(newickFile, dVal, tVal, lVal) #run fixer.py with .newick file       

    #run fixer.py with .newick file
    fixerCost = fixer.fixer(newickFile, dVal, tVal, lVal)

    #run Jane with .tree file
    janeOut = execJane.runJane(treeFile, popSize, numGen, dVal, tVal, lVal)
    janeCost = cjc.janeCost(janeOut, dVal, tVal, lVal)

    #compare fixer score with Jane score
    if DPCost == janeCost: #Jane's solution is optimal
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Jane's Solution is Optimal"
        return
          
    elif fixerCost < janeCost: #fixer found a better solution than Jane
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Cheeta found a valid solution of " + str(fixerCost)
        print "You may wish to try running Jane again with larger values for the population and/or generation parameters"
        return
        
    else: #fixer was unable to find a better solution than Jane
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Cheeta was unable to find a valid solution better than Jane"
        print "You may wish to try running Jane again with larger values for the population and/or generation parameters"
        
if __name__ == '__main__':
    main()