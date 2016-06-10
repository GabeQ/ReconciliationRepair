# makeSortedPlot.py
#
# modified from 'makePlot.py' by Chen Pekker
# June 2016
#
# This file plots costs of temporally consistent reconciliations found 
# by TemporalConsistencyFixer algorithm as well as those found by Jane 
# against file indices.
#
# Run with
#   python makePlot.py

import os
import os.path
from cStringIO import StringIO
import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np
import MasterReconciliation

# Global variables (can be customized in the future)
dVal = 2
tVal = 3
lVal = 1
num = 100

janeMemo = {}
optimalMemo = {}
fixerMemo = {}

def findGroups(fileNum):
    
        janeList = []
	fixerList = []
	optimalList = []
	
        optimal = [] #list of scores where the optimal score is better than Jane
        repair = [] #list of scores where the repair score is better than Jane
        tie = [] #list of scores where the repair score is the same as Jane's
        
        scores = []
	for i in fileNum:
	    
		index = str(i)
	#	print "index B4: " + index
		
		for j in xrange(4 - len(str(i + 1))):
			index = "0" + index
		
		f = "janeCosts/COG" + index + ".txt"

		if not os.path.isfile(f):
			continue

		janeFile = open(f, 'r')

		lines = janeFile.readlines()
		janeList.append(int(lines[-1]))
		janeScore = int(lines[-1])
		janeMemo[i] = janeScore
		print "Jane:", int(lines[-1])

		janeFile.close()

		f = "fixerOut/COG" + index + ".txt"

		fixerFile = open(f, 'r')

		for line in fixerFile:
			if line.startswith("min total:"):
				if line.startswith("min total: None"):
					fileName = "real-100taxa/COG" + index + ".newick"
					recs, allRecs = MasterReconciliation.Reconcile(["", fileName, str(dVal), str(tVal), str(lVal), "unit", "0", "1", "0", "1"])
					T = allRecs[0]

					d, s, t, l = 0, 0, 0, 0
					for key in T.keys():
						if T[key][0] == 'D':
							d += 1
						elif T[key][0] == 'S':
							s += 1
						elif T[key][0] == 'T':
							t += 1
						elif T[key][0] == 'L':
							l += 1

					score = d * dVal + t * tVal + l * lVal

					optimalList.append(score)
					print "Optimal:", score
					optimalScore = score
					optimalMemo[i] = optimalScore
					fixerScore = None
					#fixerMemo[i] = fixerScore
				else:
					fixerList.append(int(line[11:]))
					print "Fixer:", int(line[11:])
					fixerScore = int(line[11:])
					fixerMemo[i] = fixerScore
					optimalScore = None
					#optimalMemo[i] = optimalScore
		fixerFile.close()
		print "Done ", index
		scores.append((i, janeScore, optimalScore, fixerScore))
		
	print scores
	for i in range(len(scores)):
	    if scores[i][2] != None: #if there is an optimal score and a 'None' for the fixer score
	        if scores[i][2] < scores[i][1]: #if the optimal score is less than the Jane score
	            optimal.append(scores[i][0])  #append the sample number to the list of 'optimals'
	    elif scores[i][3] != None: #if there is an fixer score and a 'None' for the optimal score
	        if scores[i][3] < scores[i][1]: 
	            repair.append(scores[i][0])
	        if scores[i][3] == scores[i][2]:
	            tie.append(scores[i][0])
	           
	print optimal, repair, tie
        return optimal, repair, tie


def janeSort(list):
        """ takes in a list with the index numbers of samples, 
        returns a list of the sample numbers ranked in order of 
        increasing jane scores for those samples"""
    
        optimal = [2,23,26,27,29,33,34,41,52,58,62,67,69,72,86,92]
        repair = [1,16,24,30,51,55,61,75,85,96,98]
        tie = [95]
        allElse = []
        for x in range(1,101):
            if x not in optimal:
                if x not in repair:
                    if x not in tie:
                        allElse.append(x)
        fileNum = list
            
        scores = []
	for i in fileNum:
	    
		index = str(i)		
		for j in xrange(4 - len(str(i + 1))):
			index = "0" + index
		
		f = "janeCosts/COG" + index + ".txt"

		if not os.path.isfile(f):
			continue

		janeFile = open(f, 'r')

		lines = janeFile.readlines()
		janeScore = int(lines[-1])
		scores.append((janeScore, i)) #list of tuples

		janeFile.close()
	
	sortedScores = sorted(scores) #sorted list of tuples
	janeIncreasing = []
	for i in range(len(sortedScores)):
	    janeIncreasing.append(sortedScores[i][1]) #get the sample numbers (second element in the tuples) from sortedScores
	    
	return janeIncreasing


def main():
    
	janeX = []
	fixerX = []
	janeList = []
	fixerList = []
	optimalX = []
	optimalList = []
	
	fileNum = range(1, num+1)
	optimal, repair, tie = findGroups(fileNum)
	
        remaining = []
        for x in range(1, num+1): 
            if x not in optimal:
                if x not in repair:
                    if x not in tie:
                        remaining.append(x)
                        
        optimal = janeSort(optimal)
        print optimal
        repair = janeSort(repair)
        print repair
        tie = janeSort(tie)
        print tie
        allElse = janeSort(remaining)
        print allElse
                        
        realFileNum = []
        for i in optimal:
            realFileNum.append(i)
        for i in repair:
            realFileNum.append(i)
        for i in tie:
            realFileNum.append(i)
        for i in allElse:
            realFileNum.append(i)
            
        print "realFileNum:"
        print realFileNum
            
        count = 0
        
	for i in realFileNum:
	        count +=1
	        janeX.append(count)

		index = str(i)
		print "index B4: " + index
		
		for j in xrange(4 - len(str(i + 1))):
			index = "0" + index
		
		f = "janeCosts/COG" + index + ".txt"

		if not os.path.isfile(f):
			continue

		if i in janeMemo:
		    janeList.append(janeMemo[i])
		    
		else:
		        print "NEEDED TO GO IN THE 'ELSE CASE' FOR JANE"
		        janeFile = open(f, 'r')

          		lines = janeFile.readlines()
          		janeList.append(int(lines[-1]))
          		print "Jane:", int(lines[-1])
            
          		janeFile.close()
          		
                if i in fixerMemo:
                    fixerX.append(count)
		    fixerList.append(fixerMemo[i])
		
		elif i in optimalMemo:
		    optimalList.append(optimalMemo[i])
		    optimalX.append(count)
		else:
		        print "NEEDED TO GO IN THE 'ELSE CASE' FOR FIXER/OPTIMAL"
		        f = "fixerOut/COG" + index + ".txt"

          		fixerFile = open(f, 'r')
            
          		for line in fixerFile:
         			if line.startswith("min total:"):
            				if line.startswith("min total: None"):
           					fileName = "real-100taxa/COG" + index + ".newick"
           					recs, allRecs = MasterReconciliation.Reconcile(["", fileName, str(dVal), str(tVal), str(lVal), "unit", "0", "1", "0", "1"])
           					T = allRecs[0]
            
           					d, s, t, l = 0, 0, 0, 0
           					for key in T.keys():
          						if T[key][0] == 'D':
         							d += 1
          						elif T[key][0] == 'S':
         							s += 1
          						elif T[key][0] == 'T':
         							t += 1
          						elif T[key][0] == 'L':
         							l += 1
            
           					score = d * dVal + t * tVal + l * lVal
            
           					optimalList.append(score)
           					optimalX.append(count)
           					print "Optimal:", score
           					print "NEEDED TO GO IN for OPTIMAL"
            				else:
           					fixerList.append(int(line[11:]))
           					fixerX.append(count)
           					print "Fixer:", int(line[11:])
           					print "NEEDED TO GO IN for FIXER"
          		fixerFile.close()
          		print "Done ", index
        
     
      	print "janeX:"
        print janeX
        print janeList
      	print "fixerX:"
        print fixerX
        print fixerList
        print "optimalX:"
        print optimalX
        print optimalList
        	     		    
        fig, ax = plt.subplots()
        ax.set_xticks([16, 27, 100]) #ticks for the x axis
	ax.plot(janeX, janeList, 'ro', label='Jane')
	ax.plot(fixerX, fixerList, 'b*', label='Repair')
	ax.plot(optimalX, optimalList, 'y^', label='No Repair')
	plt.xlabel('COG File', fontsize=21)
	plt.ylabel('Cost', fontsize=21)
	plt.legend()
	plt.grid()
	#plt.xticks(np.arange(0, count, 100))
	legend = ax.legend(loc='upper right', numpoints = 1)
	
	# Set the fontsize
        for label in legend.get_texts():
            label.set_fontsize('xx-large')
            
        plt.show()


if __name__ == "__main__":
	main()
