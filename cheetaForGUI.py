# cheetaForGUI.py
#
# Created by Matt Dohlen, Chen Pekker, Gabriel Quiroz
# June 2016

# This file is the master Cheeta program that will run in termimal. It takes
# as input a .tree or .newick file, the duplication cost, transfer cost, loss
# cost, population size, and the number of generations. It takes the file
# and stores it as both a .newick and .tree file (since Jane takes in .tree
# files and the DP and fixer take in .newick files). It runs both fixer.py
# and Jane in order to compute the minimum cost to construct a reconciliation of
# a host and parasite tree (aka the most parsemonious solution). It then compares 
# the two and uses the scores to tell the user whether Jane has the most parsemonious 
# solution (optimal score and Jane score are the same), whether there could be a better 
# solution, or whether there may be a better solution with larger input values for Jane.

import fixer
import JaneUtil
import newickToTreeParser as ntp
import treeToNewickParser as ptn
from CheetaExceptions import CheetaError
import sys
import os

def usage():
    print "usage: cheeta.py [-help] [-v] [-l {limit}] [-c {dupCost, transCost, lossCost}] [-p {popSize, numGen}] file"
    return "usage: cheeta.py [-help] [-v] [-l {limit}] [-c {dupCost, transCost, lossCost}] [-p {popSize, numGen}] file"
 #   sys.exit(1)

def help():
    print 'usage: python cheeta.py [-options] filename\n\n' + \
    'Where [-options] include:\n' + \
    '\t-help\t\tPrint this message\n' + \
    '\t-v\t\tTurns on verbose output\n' + \
    '\t-l\t\tPlaces a limit on the number of infeasible reconciliations that Cheeta looks at\n' + \
    '\t-c\t\tAllows user to input costs for duplications, transfers, and losses respectively\n' + \
    '\t-p\t\tAllows user to input parameters for population size and number of generations in Jane\n'
    return 'usage: python cheeta.py [-options] filename\n\n' + \
    'Where [-options] include:\n' + \
    '\t-help\t\tPrint this message\n' + \
    '\t-v\t\tTurns on verbose output\n' + \
    '\t-l\t\tPlaces a limit on the number of infeasible reconciliations that Cheeta looks at\n' + \
    '\t-c\t\tAllows user to input costs for duplications, transfers, and losses respectively\n' + \
    '\t-p\t\tAllows user to input parameters for population size and number of generations in Jane\n'
 #   sys.exit(0)
                       
def cheeta(fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit):
    newickFile = None
    treeFile = None
    tempFileToRemove = None

    print "In cheetaForGUI"
    try:
        # file converter
        if fileName == None:
            print "The file must be in either '.tree' or '.newick' format"
            return "The file must be in either '.tree' or '.newick' format"
        elif fileName.endswith('.tree'):
            treeFile = fileName
            newickFile = ptn.treeToNewickParser(fileName)
            tempFileToRemove = newickFile
        elif fileName.endswith('.newick') or fileName.endswith('.nwk'):
            newickFile = fileName
            treeFile = ntp.newickToTreeParser(fileName)
            tempFileToRemove = treeFile
        else:
            print "The file must be in either '.tree' or '.newick' format"
            return "The file must be in either '.tree' or '.newick' format"
         #   sys.exit(1)

        fixerCost, DPCost = fixer.fix(newickFile, dVal, tVal, lVal, verbose, limit) # run fixer.py with .newick file

        # run Jane with .tree file
        janeOut = JaneUtil.runJane(treeFile, popSize, numGen, dVal, tVal, lVal)
        janeCost = JaneUtil.janeCost(janeOut, dVal, tVal, lVal)
    except CheetaError as e:
        print str(e)
        if e.hasInnerError:
            print >> sys.stderr, e.innerError
        return str(e)
     #   sys.exit(1)
    except Exception as e:
        print "Unknown error has occurred"
        print >> sys.stderr, e.message
        return "Unknown error has occurred"
      #  sys.exit(1)

    # compare fixer score with Jane score
    if DPCost == janeCost:  # Jane's solution is optimal
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Jane's Solution is Optimal"
        answer = "Jane Solution Cost: " + str(janeCost) + ", Theoretical Lower Bound: " + str(DPCost) + ", Jane's Solution is Optimal"

    elif fixerCost < janeCost:  # fixer found a better solution than Jane
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Cheeta found a valid solution of cost: " + str(fixerCost)
        print "You may wish to try running Jane again with larger values for the population and/or generation parameters"
        answer = "Jane Solution Cost: " + str(janeCost) + ", Theoretical Lower Bound: " + str(DPCost) + ", You may wish to try running Jane again with larger values for the population and/or generation parameters"
    
    else:  # fixer was unable to find a better solution than Jane
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Cheeta was unable to find a valid solution better than Jane"
        print "You may wish to try running Jane again with larger values for the population and/or generation parameters"
        answer = "Jane Solution Cost: " + str(janeCost) + ", Theoretical Lower Bound: " + str(DPCost) + ", Cheeta was unable to find a valid solution better than Jane" + " You may wish to try running Jane again with larger values for the population and/or generation parameters"

    try:
        os.remove(tempFileToRemove)
        os.remove(janeOut)
    except OSError:
        pass
    return answer
  #  sys.exit(0)


