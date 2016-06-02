# MasterReconciliation.py
# Juliet Forman, Srinidhi Srinivasan, Annalise Schweickart, and Carter Slocum
# July 2015
#
# Modified by Weiyun Ma
# May 2016
#
# This file contains functions for computing maximum parsimony 
# DTL reconciliations using the edge-based DP algorithm.  The main # # function in this file is called Reconcile and the remaining 
# functions are helper functions that are used by Reconcile.

import DP
import Greedy
import newickFormatReader
from sys import argv
import ReconciliationGraph
import copy
# import calcCostscapeScore
import os
import orderGraph

def Reconcile(argList):
	"""Takes command-line arguments of a .newick file, duplication, transfer, 
	and loss costs, the type of scoring desired and possible switch and loss 
	ranges. Creates Files for the host, parasite, and reconciliations"""
	fileName = argList[1] #.newick file
	D = float(argList[2]) # Duplication cost
	T = float(argList[3]) # Transfer cost
	L = float(argList[4]) # Loss cost
	freqType = argList[5] # Frequency type
	# Optional inputs if freqType == xscape
	switchLo = float(argList[6]) # Switch lower boundary
	switchHi = float(argList[7]) # Switch upper boundary
	lossLo = float(argList[8]) # Loss lower boundary
	lossHi = float(argList[9]) # Loss upper boundary

	host, paras, phi = newickFormatReader.getInput(fileName)
	hostRoot = ReconciliationGraph.findRoot(host)
	# Default scoring function (if freqtype== Frequency scoring)
	DTLReconGraph, numRecon = DP.DP(host, paras, phi, D, T, L)
	#uses xScape scoring function
	# if freqType == "xscape":
	# 	DTLReconGraph = calcCostscapeScore.newScoreWrapper(fileName, switchLo, \
	# 		switchHi, lossLo, lossHi, D, T, L)
	#uses Unit scoring function
	if freqType == "unit":
		DTLReconGraph = unitScoreDTL(host, paras, phi, D, T, L)

	DTLGraph = copy.deepcopy(DTLReconGraph)
	scoresList, recs = Greedy.Greedy(DTLGraph, paras)

	infeasible_recs = []
	for rec in recs:
		if orderGraph.date(ReconciliationGraph.buildReconciliation(host, paras, rec)) == False:
			infeasible_recs.append(rec)

	return infeasible_recs, recs


def unitScoreDTL(hostTree, parasiteTree, phi, D, T, L):
	""" Takes a hostTree, parasiteTree, tip mapping function phi, and 
	duplication cost (D), transfer cost (T), and loss cost (L) and returns the
	DTL graph in the form of a dictionary, with event scores set to 1. 
	Cospeciation is assumed to cost 0. """
	DTLReconGraph, numRecon = DP.DP(hostTree, parasiteTree, phi, D, T, L)
	newDTL = {}
	for vertex in DTLReconGraph:
		newDTL[vertex] = []
		for event in DTLReconGraph[vertex][:-1]:
			newEvent = event[:-1] + [1.0]
			newDTL[vertex].append(newEvent)
		newDTL[vertex].append(DTLReconGraph[vertex][-1])
	return newDTL

def main():
	Reconcile(argv)

if __name__ == "__main__": main()

