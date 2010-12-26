class CryptoReport(object):
    """CryptoReport unique'ifies Results and prints them in a specified format"""
    def __init__(self, trace):
        self.trace = trace
    
    def printText(self):
        uniqueText = set()
        for instruction in self.trace:
            for result in instruction.cryptoResults:
                uniqueText.add(result.formatText())
        for result in uniqueText:
            print result
        