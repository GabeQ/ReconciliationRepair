import os
import tempfile

def runJane(fileName, popSize, numGen, dVal, tVal, lVal):
    '''runs Jane in the command line, saves the output in a file, and returns the file name'''
    tempOut = tempfile.NamedTemporaryFile(delete=False)
    tempOut.close()
    os.system("./Jane/jane-cli.sh -C -p " + str(popSize) + " -i " + str(numGen) +
              " -c 0 " + str(dVal) + " " + str(tVal) + " " + str(lVal) + " 0 " +
              str(fileName) + " >> " + tempOut.name) 
    return tempOut.name

def janeCost(janeOutFile, dVal, tVal, lVal):
    File = open(janeOutFile, 'r')
    ans = 0

    for line in File:
        if line.startswith("Duplication: "):
            num = int(line[13:])
            ans += num * dVal
        elif line.startswith("Host Switch: "):
            num = int(line[12:])
            ans += num * tVal
        elif line.startswith("Loss: "):
            num = int(line[6:])
            ans += num * lVal
    return ans