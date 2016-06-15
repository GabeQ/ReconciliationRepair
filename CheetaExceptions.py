from enum import Enum

class CheetaErrorEnum(Enum):
    JaneCLI = 0
    FileParse = 1
    Alg = 2
    Other = 10


class CheetaError(Exception):
    def __init__(self, errNum, *args):
        self.errNum = errNum
        self.hasInnerError = False

        # no args
        if errNum == CheetaErrorEnum.JaneCLI:
            self.message = "Not able to execute Jane from the command line. Make sure that Jane is " + \
                           "located in the parent directory"
        # args: fileName, message
        elif errNum == CheetaErrorEnum.FileParse:
            fileName = args[0]
            fileExt = "." + fileName.split('.')[1]
            self.message = "Could not parse " + fileExt + " file\n\tFileName: " + fileName + \
                           "\n\tReason: " + args[1]
        # args: algName, inner error
        elif errNum == CheetaErrorEnum.Alg:
            self.hasInnerError = True
            self.message = "Failure in one of the underlying algorithms. See error logs for more info"
        # unknown or system errors
        # args: inner error
        else:
            self.hasInnerError = True
            self.message = "Failure to run Cheeta. See error logs for more info"

    def __str__(self):
        return self.message


class FileFormatError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
