# makePlot.py
#
# Weiyun Ma, Dima Smirnov
# May 2016
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
import numpy as np
import MasterReconciliation

# Global variables (can be customized in the future)
dVal = 2
tVal = 3
lVal = 1
fileNum = 100

def main():

	janeX = []
	fixerX = []
	janeList = []
	fixerList = []
	optimalX = []
	optimalList = []

	for i in xrange(fileNum):

		index = str(i + 1)

		for j in xrange(4 - len(str(i + 1))):
			index = "0" + index

		f = "janeCosts/COG" + index + ".txt"

		if not os.path.isfile(f):
			continue

		janeX.append(i + 1)

		janeFile = open(f, 'r')

		lines = janeFile.readlines()
		janeList.append(int(lines[-1]))
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

					optimalX.append(i + 1)
					optimalList.append(score)
					print "Optimal:", score
				else:
					fixerX.append(i + 1)
					fixerList.append(int(line[11:]))
					print "Fixer:", int(line[11:])

		fixerFile.close()

		print "Done ", index

	plt.plot(janeX, janeList, 'ro', label='Jane')
	plt.plot(fixerX, fixerList, 'b*', label='Fixer Alg')
	plt.plot(optimalX, optimalList, 'y*', label='Optimal (No Fixing Needed)')
	plt.xlabel('File Index')
	plt.ylabel('Cost')
	plt.legend()
	plt.grid()
	plt.xticks(np.arange(0, fileNum, 1))
	plt.show()


if __name__ == "__main__":
	main()
