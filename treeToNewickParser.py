#treeToNewickParser.py

#Created by Matt Dohlen, Chen Pekker, Gabriel Quiroz
#June 2016

from cStringIO import StringIO
import os.path
import os

def readTree(content, lineNum):
    entryToName = {}
    count = 0
    while True:
        if content[lineNum] == "":
            break
        entry = content[lineNum].split()
        if len(entry) < 3:
            throw
            #throw new FileFormatException("The keyword null is required to identify tip edges in the .tree file format");
        if len(entry) > 3:
            throw
            #throw "No polytomy allowed"
        name = entry[0]
        entryToName[name] = (entry[1], entry[2])
        count += 1
        lineNum += 1
    return entryToName, count
    
def readNames(content, lineNum):
    names = {}
    while True:
        if content[lineNum] == "":
            break
        entry = content[lineNum].split()
        if len(entry) != 2:
            throw
            # 'Improperly formatted names'
        names[entry[0]] = entry[1]
        lineNum += 1
    return names
    
def readPhi(content, lineNum):
    phi = {}
    count = 0
    while True:
        if content[lineNum] == "":
            break
        entry = content[lineNum].split()
        if len(entry) != 2:
            throw
            # 'Improperly formatted phi'
        phi[entry[0]] = entry[1]
        count += 1
        lineNum += 1

def treeToNewickParser(treeFile):
    f = open(treeFile, 'r')
    content = f.readlines()
    index = 1
    
    # HOSTTREE
    hostToName, numHost = readTree(content, index)
    index = index + numHost + 2
    # HOSTNAME
    hostNames = readNames(content, index)
    index = index + numHost + 2
    
    hostTree = createTree(hostToName, hostNames, numHost)
    
    # PARASITETREE
    parasToName, numParas = readTree(content, index)
    index = index + numParas + 2
    # PARASITENAMES
    parasNames = readNames(content, index)
    index = index + numParas + 2
    
    parasTree = createTree(parasToName, parasNames, numParas)
    
    # PHI
    tipMap, numPhi = readPhi(content, index)
    index = index + numPhi + 1
    
    if "HOSTRANKS" not in content[index]:
        throw
        # 'Must supply ranks for timing info'
    
    # HOSTRANKS
    
    if "PARASITERANKS" not in content[index]:
        throw
        # 'Must supply ranks for timing info'
    
    # PARASITERANKS
    
    return