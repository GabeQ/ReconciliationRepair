#treeToNewickParser.py

#Created by Matt Dohlen, Chen Pekker, Gabriel Quiroz
#June 2016

#This file contains functions that are used in order to convert a .tree file into 
#a .newick file so that we could run cheeta. TreeToNewickParser reads through the
#.tree file, creates dictionaries of each parent and child node combination as well
#as dictionaries containing the names of node, and uses a networkx graph to construct
#the newick tree. It does this for both the host and parasite trees, and then parses 
#the phi connections.
import errno
import networkx as nx
import tempfile
from CheetaExceptions import *

def readTree(content, lineNum):
    entryDict = {}
    count = 0
    while True:
        if content[lineNum].isspace():
            break
        entry = content[lineNum].split()
        if len(entry) < 3:
            raise FileFormatError("The keyword null is required to identify tip edges in the .tree file format");
        if len(entry) > 3:
            raise FileFormatError("No polytomy allowed")
        name = entry[0]
        entryDict[name] = (entry[1], entry[2])
        count += 1
        lineNum += 1
    return entryDict, count
    
def readNames(content, lineNum):
    names = {}
    while True:
        if content[lineNum].isspace():
            break
        entry = content[lineNum].split()
        if len(entry) != 2:
            raise FileFormatError("Improperly formatted names section")
        names[entry[0]] = entry[1]
        lineNum += 1
    return names
    
def readPhi(content, lineNum):
    phi = []
    while True:
        if lineNum >= len(content) or content[lineNum].isspace():
            break
        entry = content[lineNum].split()
        if len(entry) != 2:
            raise FileFormatError("Improperly formatted phi")
        phi.append((entry[0], entry[1]))
        lineNum += 1
    return phi
        
def namePhi(phiList, hostNames, parasNames):
    phiStr = ""
    for phi in phiList:
        # Tree maps host to parasite, newick maps parasite to host
        phiStr = phiStr + parasNames[phi[1]] + ":" + hostNames[phi[0]] + "\n"
    return phiStr
        
def toNewick(graph, root):
    if graph.degree(root) == 1:
        return root
    else:
        outEdges = graph.out_edges(root)
        child1 = outEdges[0][1]
        child2 = outEdges[1][1]
        return "(" + toNewick(graph, child1) + "," + toNewick(graph, child2) + ")" + root
    
def createTree(treeDict, treeNames):
    treeGraph = nx.DiGraph()
    for key in treeDict.keys():
        if treeDict[key][0] != "null":
            root = treeNames[key]
            child1 = treeNames[treeDict[key][0]]
            child2 = treeNames[treeDict[key][1]]
            treeGraph.add_edge(root, child1)
            treeGraph.add_edge(root, child2)
            
    root = None
    for node in treeGraph:
        if treeGraph.degree(node) == 2:
            root = node
            break
    return toNewick(treeGraph, root)
    
def treeToNewickParser(treeFile):
    try:
        f = open(treeFile, 'r')
        content = f.readlines()
        f.close()
    except (OSError, IOError) as e:
        if e.errno == errno.ENOENT:
            raise CheetaError(CheetaErrorEnum.FileParse, [treeFile, "File access error - File does not exist"])
        elif e.errno == errno.EACCES:
            raise CheetaError(CheetaErrorEnum.FileParse, [treeFile, "File access error - Access denied"])
        else:
            raise CheetaError(CheetaErrorEnum.FileParse, [treeFile, "Could not access file"])

    try:
        index = 1

        # HOSTTREE
        hostDict, numHost = readTree(content, index)
        index = index + numHost + 2
        # HOSTNAME
        hostNames = readNames(content, index)
        index = index + numHost + 2

        hostTreeStr = createTree(hostDict, hostNames)

        # PARASITETREE
        parasDict, numParas = readTree(content, index)
        index = index + numParas + 2
        # PARASITENAMES
        parasNames = readNames(content, index)
        index = index + numParas + 2

        parasTreeStr = createTree(parasDict, parasNames)

        # PHI
        phiList = readPhi(content, index)
        phiStr = namePhi(phiList, hostNames, parasNames)

        fileStr = hostTreeStr + ";\n" + parasTreeStr + ";\n" + phiStr + "\n"

        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(fileStr)
        temp.close()
        return temp.name
    except FileFormatError as e:
        raise CheetaError(CheetaErrorEnum.FileParse, [treeFile, "File format error - " + e.message])
    except:
        raise CheetaError(CheetaErrorEnum.FileParse,
                             [treeFile, "Could not parse file - Check to see file formatting is correct"])