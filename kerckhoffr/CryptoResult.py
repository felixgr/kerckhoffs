class CryptoResult(object):
    """Analysis Result for a Test"""
    def __init__(self, \
                 implementation = "unknown implementation", \
                 algorithm = "unknown algorithm", \
                 key = None, \
                 plaintext = None, \
                 ciphertext = None, \
                 verified = False, \
                 cryptoConfidence = 0.0, \
                 implementationConfidence = 0.0, \
                 algorithmConfidence = 0.0, \
                 correspondingTest = "unspecified test", \
                 infoText = ""\
                 ):
        
        self.implementation = implementation
        self.algorithm = algorithm
        
        self.key = key
        self.plaintext = plaintext
        self.ciphertext = ciphertext
        self.verified = verified
        
        self.cryptoConfidence = cryptoConfidence
        self.implementationConfidence = implementationConfidence
        self.algorithmConfidence = algorithmConfidence
        
        self.correspondingTest = correspondingTest
        self.infoText = infoText
    
    def __str__(self):
        return formatText(self)
    
    def formatText(self):
        if self.verified:
            verified = 'verified'
        else:
            verified = 'not verified'
        
        if self.algorithm == 'xor':
            return "<CryptoResult from %s isCrypto[%.2f] %s[%.2f] %s[%.2f] with %s parameters key=0x%x plaintext=0x%x ciphertext=0x%x and infoText=%r>" % (self.correspondingTest, self.cryptoConfidence, self.implementation, self.implementationConfidence, self.algorithm, self.algorithmConfidence, verified, self.key, self.plaintext, self.ciphertext, self.infoText)
        else:
            return "<CryptoResult from %s isCrypto[%.2f] %s[%.2f] %s[%.2f] with %s parameters key=%r plaintext=%r ciphertext=%r and infoText=%r>" % (self.correspondingTest, self.cryptoConfidence, self.implementation, self.implementationConfidence, self.algorithm, self.algorithmConfidence, verified, self.key, self.plaintext, self.ciphertext, self.infoText)
        
        
        
