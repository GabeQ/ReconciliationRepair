import os
import tempfile
from CheetaExceptions import CheetaError
from CheetaExceptions import CheetaErrorEnum

def runJane(fileName, popSize, numGen, dVal, tVal, lVal):
    '''runs Jane in the command line, saves the output in a file, and returns the file name'''
    try:
        tempOut = tempfile.NamedTemporaryFile(delete=False)
        tempOut.close()
    except Exception as e:
        raise CheetaError(CheetaErrorEnum.Other, [e.message])
    returnVal = os.system("./Jane/jane-cli.sh -C -p " + str(popSize) + " -i " + str(numGen) +
              " -c 0 " + str(dVal) + " " + str(tVal) + " " + str(lVal) + " 0 " +
              str(fileName) + " >> " + tempOut.name)
    if returnVal != 0:
        raise CheetaError(CheetaErrorEnum.JaneCLI)
    return tempOut.name


def janeCost(janeOutFile, dVal, tVal, lVal):
    try:
        f = open(janeOutFile, 'r')
        ans = 0

        for line in f:
            if line.startswith("Duplication: "):
                num = int(line[13:])
                ans += num * dVal
            elif line.startswith("Host Switch: "):
                num = int(line[12:])
                ans += num * tVal
            elif line.startswith("Loss: "):
                num = int(line[6:])
                ans += num * lVal

        f.close()
        return ans
    except Exception as e:
        raise CheetaError(CheetaErrorEnum.Other, [e.message])
