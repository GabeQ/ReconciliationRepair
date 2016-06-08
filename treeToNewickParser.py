#treeToNewickParser.py

#Created by Matt Dohlen, Chen Pekker, Gabriel Quiroz
#June 2016

from cStringIO import StringIO
import networkx as nx
import tempfile

def readTree(content, lineNum):
    entryDict = {}
    count = 0
    while True:
        if content[lineNum].isspace():
            break
        entry = content[lineNum].split()
        if len(entry) < 3:
            return
            #throw
            #throw new FileFormatException("The keyword null is required to identify tip edges in the .tree file format");
        if len(entry) > 3:
            return
            #throw
            #throw "No polytomy allowed"
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
            return
            #throw
            # 'Improperly formatted names'
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
            return
            #throw
            # 'Improperly formatted phi'
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
    f = open(treeFile, 'r')
    content = f.readlines()
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
    
    fileStr = hostTreeStr + ";\n" + parasTreeStr + ";\n" + phiStr
    
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(fileStr)
    temp.close()
    return temp.name