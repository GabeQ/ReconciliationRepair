# execJane.py
#
# Weiyun Ma
# May 2016
#
# This file executes Jane on the first 100 .tree files in the 
# treeFiles folder and writes outputs into corresponding .txt 
# files in the janeOut folder.
#
# Run with
#   python execJane.py

import os
import os.path
from cStringIO import StringIO

# Global variables (can be customized in the future)
dVal = 2
tVal = 3
lVal = 1
fileNum = 100
initPopulationSize = 30
numOfGenerations = 30

def runJane(fileName, popSize, numGen, dVal, tVal, lVal):
    '''runs Jane in the command line, saves the output in a file, and returns the file name'''
    os.system("./Jane/jane-cli.sh -C -p " + str(popSize) + " -i " + str(numGen) + " -c 0 " + str(dVal) + " " + str(tVal) + " " + str(lVal) + " 0 " + str(fileName) + " > janeOut.txt") 
    return "janeOut.txt"

def main():

	if not os.path.exists("janeOut"):
		os.mkdir("janeOut")

	for i in xrange(fileNum):

		index = str(i + 1)

		for j in xrange(4 - len(str(i + 1))):
			index = "0" + index

		inFile = "real-100taxa/COG" + index + ".newick"

		if not os.path.isfile(inFile):
			continue
		os.system("./Jane/jane-cli.sh -C -p {0} -i {1} -c 0 {2} {3} {4} 0 treeFiles/COG".format(initPopulationSize, numOfGenerations, dVal, tVal, lVal) 
			+ index + ".tree > janeOut/COG" + index + ".txt")

#if __name__ == "__main__": 
#	main()