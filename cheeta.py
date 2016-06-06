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


import calcJaneCost
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

    
def main():
    #arguments
    fileName = sys.argv[1]
    dupCost = sys.argv[2]
    transCost = sys.argv[3]
    lossCost = sys.argv[4]
    popSize = sys.argv[5]
    numGen = sys.argv[6]
    newickFile = None
    treeFile = None
    
    #file converter
    if fileName.contains('.tree'):
        treeFile = fileName
        newickFile = None
    elif fileName.contains('.newick'):
        newickFile = fileName
        treeFile = ntp.newickToTreeParser(fileName)
    else:
        print 'The file must be of .tree or .newick format'
        return
    
    #run fixer.py with .newick file
    fixerCost = fixer(newickFile, dupCost, transCost, lossCost)
    
    #run Jane with .tree file
    janeCost = 
        
    #compare fixer score with jane score    
    
    return

if __name__ == '__main__':
    main()