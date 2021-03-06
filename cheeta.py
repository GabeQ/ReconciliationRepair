# cheeta.py

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
import logging
import newickToTreeParser as ntp
import treeToNewickParser as ptn
from CheetaExceptions import CheetaError, CheetaErrorEnum
import datetime
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
    print "usage: cheeta.py [-help] [-v] [-l {limit}] [-c {dupCost, transCost, lossCost}] [-p {popSize, numGen}] file"
    sys.exit(1)

def help():
    print 'usage: python cheeta.py [-options] filename\n\n' + \
    'Where [-options] include:\n' + \
    '\t-help\t\tPrint this message\n' + \
    '\t-v\t\tTurns on verbose output\n' + \
    '\t-l\t\tPlaces a limit on the number of infeasible reconciliations that Cheeta looks at\n' + \
    '\t-c\t\tAllows user to input costs for duplications, transfers, and losses respectively\n' + \
    '\t-p\t\tAllows user to input parameters for population size and number of generations in Jane\n'
    sys.exit(0)

def readArgs():
    global fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit
    
    i = 1
    if len(sys.argv) == 1:
        usage()
    if sys.argv[i] == '-h' or sys.argv[i] == '-help' or sys.argv[i] == '--h' or sys.argv[i] == '--help' or sys.argv[i] == '-?':
        help()

    try:
        while i < len(sys.argv) - 1:
            if sys.argv[i] == '-v' or sys.argv[i] == '-V':
                verbose = True
                i += 1
            elif sys.argv[i] == '-l' or sys.argv[i] == '-L':
                limit = int(sys.argv[i+1])
                i += 2
            elif sys.argv[i] == '-c' or sys.argv[i] == '-C':
                dVal = int(sys.argv[i+1])
                tVal = int(sys.argv[i+2])
                lVal = int(sys.argv[i+3])
                i += 4
            elif sys.argv[i] == '-p' or sys.argv[i] == '-P':
                popSize = int(sys.argv[i+1])
                numGen = int(sys.argv[i+2])
                i += 3
            elif sys.argv[i].startswith('-'):
                print 'Unrecognized flag: ' + sys.argv[i]
                usage()
            else:
                print 'Command not recognized'
                usage()
    except:
        print 'Command not recognized'
        usage()

    if i == len(sys.argv) - 1:
        if sys.argv[i].endswith('.tree') or sys.argv[i].endswith('.newick') or sys.argv[i].endswith('.nwk'):
            fileName = sys.argv[i]
        else:
            print 'Last argument must be a tree or newick file'
            usage()
    else:
        usage()
    
                       

def cheeta(fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit):
    
    newickFile = None
    treeFile = None
    tempFileToRemove = None

    logging.basicConfig(filename='CheetaError.log', level=logging.ERROR)

    try:
        # file converter
        if fileName.endswith('.tree'):
            treeFile = fileName
            newickFile = ptn.treeToNewickParser(fileName)
            tempFileToRemove = newickFile
        elif fileName.endswith('.newick') or fileName.endswith('.nwk'):
            newickFile = fileName
            treeFile = ntp.newickToTreeParser(fileName)
            tempFileToRemove = treeFile
        else:
            raise CheetaError(CheetaErrorEnum.FileParseError, fileName, "The file must be in either tree or newick format")

        fixerCost, DPCost, fixerLog = fixer.fix(newickFile, dVal, tVal, lVal, verbose, limit) # run fixer.py with .newick file
        DPCost = int(DPCost)
        
        # run Jane with .tree file
        janeOut = JaneUtil.runJane(treeFile, popSize, numGen, dVal, tVal, lVal)
        janeCost = JaneUtil.janeCost(janeOut, dVal, tVal, lVal)
    except CheetaError as e:
        if e.hasInnerError:
            logging.exception("Cheeta error: {:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()))
        raise
    except:
        logging.exception("Cheeta error: {:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()))
        raise CheetaError(CheetaErrorEnum.Other), None, sys.exc_info()[2]

    try:
        os.remove(tempFileToRemove)
        os.remove(janeOut)
    except OSError:
        pass

    return fixerCost, fixerLog, DPCost, janeCost

    

if __name__ == '__main__':
    readArgs()
    try:
        fixerCost, fixerLog, DPCost, janeCost = cheeta(fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit)
    except CheetaError as e:
        print str(e)
        raise
    except:
        print "Unknown error has occurred. Check Error Log"
        raise
    
    # Print Fixer Log
    if verbose == True:
        print fixerLog
    
    # compare fixer score with Jane score
    if DPCost == janeCost:  # Jane's solution is optimal
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Jane's Solution is Optimal"

    elif fixerCost < janeCost:  # fixer found a better solution than Jane
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Cheeta found a valid solution of cost: " + str(fixerCost)
        print "You may wish to try running Jane again with larger values for the population and/or generation parameters"

    else:  # fixer was unable to find a better solution than Jane
        print "Jane Solution Cost: " + str(janeCost)
        print "Theoretical Lower Bound: " + str(DPCost)
        print "Cheeta was unable to find a valid solution better than Jane"
        print "You may wish to try running Jane again with larger values for the population and/or generation parameters"
        
