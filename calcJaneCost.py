# calcJaneCost.py
#
# Weiyun Ma
# May 2016
#
# This file calculates the total cost of the reconciliation for 
# each file in the janeOut folder. It writes the results
# into corresponding .txt files in the janeCosts folder.
#
# Run with
#   python calcJaneCost.py

import os
import os.path
from cStringIO import StringIO

# Global variables (can be customized in the future)
dVal = 2
tVal = 3
lVal = 1

def main():

	if not os.path.exists("janeCosts"):
		os.mkdir("janeCosts")

	for i in xrange(6000):

		index = str(i + 1)

		for j in xrange(4 - len(str(i + 1))):
			index = "0" + index

		f = "janeOut/COG" + index + ".txt"

		if not os.path.isfile(f):
			continue

		inFile = open(f, 'r')

		ans = 0

		for line in inFile:
			if line.startswith("Duplication: "):
				num = int(line[13:])
				ans += num * dVal
				print num
			elif line.startswith("Host Switch: "):
				num = int(line[12:])
				ans += num * tVal
				print num
			elif line.startswith("Loss: "):
				num = int(line[6:])
				ans += num * lVal
				print num

		print ans

		inFile.close()
		
		f = "janeCosts/COG" + index + ".txt"
		outFile = open(f, 'w')
		outFile.write(str(ans))
		outFile.close()

		print "Done ", index



if __name__ == "__main__": 
	main()