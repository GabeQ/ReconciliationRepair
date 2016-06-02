# newickToTreeParser.py
#
# Modified by Weiyun Ma
# May 2016
#
# This files converts all .newick files in the real-100taxa folder into
# corresponding .tree files (that are later used as Jane's inputs) 
# in the treeFiles folder.
#
# Run with
#   python newickToTreeParser.py
#
#
# A tree file must consist of a series of blocks: 
# HOSTTREE, HOSTNAMES, PARASITETREE, PARASITENAMES, PHI, HOSTNAMES, 
# and optionally HOSTRANKS, PARASITERANKS, HOSTREGIONS and REGIONCOSTS, 
# in that order.

# HOSTTREE and PARASITETREE should consist of a series of entries, 
# one line for each node of each tree, of the form: 
# node	child1	child2
# for internal nodes, or 
# node	null	null
# for tips. Every node here needs to be represented by a number.

# HOSTNAMES and PARASITENAMES should be a series of lines listing the parasite/host's number, 
# a tab, then a human-readable name for the host/parasite.

# PHI should be a series of lines listing a host number, a tab, and then a list of parasite 
# tips that infect that particular host. A host may appear at the start of multiple lines. 
# Only the tips of the host and parasite tree should be used in this section (no internal 
# node numbers should appear).

# python libraries
from cStringIO import StringIO
import os.path
import os

import newickFormatReader
from ReconciliationGraph import treeFormat


def main():

	if not os.path.exists("treeFiles"):
		os.mkdir("treeFiles")	
	
	for i in xrange(6000):

		index = str(i + 1)

		for j in xrange(4 - len(str(i + 1))):
			index = "0" + index

		inFile = "real-100taxa/COG" + index + ".newick"

		if not os.path.isfile(inFile):
			continue

		outFile = open("treeFiles/COG" + index + ".tree", 'w')

		host, parasite, phi = newickFormatReader.getInput(inFile)
		H = treeFormat(host)
		P = treeFormat(parasite)

		H_dict = {}   # name:index
		P_dict = {}   # name:index

		count = 0
		for key in H:
			count += 1
			H_dict[key] = count

		for key in P:
			count += 1
			P_dict[key] = count

		outFile.write("HOSTTREE\n")
		for key in H:
			outFile.write(str(H_dict[key]) + "\t")
			if H[key] == [None, None]:
				outFile.write("null\tnull\n")
			else:
				outFile.write(str(H_dict[H[key][0]]) + "\t" + str(H_dict[H[key][1]]) + "\n")

		outFile.write("\nHOSTNAMES\n")
		for key in H:
			outFile.write(str(H_dict[key]) + "\t" + key + "\n")

		outFile.write("\nPARASITETREE\n")	
		for key in P:
			outFile.write(str(P_dict[key]) + "\t")
			if P[key] == [None, None]:
				outFile.write("null\tnull\n")
			else:
				outFile.write(str(P_dict[P[key][0]]) + "\t" + str(P_dict[P[key][1]]) + "\n")

		outFile.write("\nPARASITENAMES\n")
		for key in P:
			outFile.write(str(P_dict[key]) + "\t" + key + "\n")

		outFile.write("\nPHI\n")
		for key in phi:
			outFile.write(str(H_dict[phi[key]]) + "\t" + str(P_dict[key]) + "\n")

		outFile.close()


if __name__ == "__main__": 
	main()