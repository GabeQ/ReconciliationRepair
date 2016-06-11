class FileFormatError(Exception):
    def __init__(self, message):
        self.message

    def __str__(self):
        return self.message


class FileParseError(Exception):
    def __init__(self, fileName, reason):
        self.fileName = fileName
        self.fileExt = "." + fileName.split('.')[1]
        self.reason = reason

    def __str__(self):
        return "Could not parse " + self.fileExt + " file\n\tFileName: " + self.fileName + "\n\tReason: " + self.reason

class AlgorithmError(Exception):
    def __init__(self, algName, innerError):
        self.algName = algName
        self.innerError = innerError