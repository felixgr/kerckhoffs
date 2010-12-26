import logging, re
from InstructionTypes import ins2type, type2desc

class Instruction(object):
    """Atomic Tracepoint: Instruction with meta data"""
    def __init__(self, eip, module, symbol, offset, disasm, data):
        self.eip = eip
        self.module = module
        self.symbol = symbol
        self.offset = offset
        self.disasm = disasm
        self.data = data
        self.multiData = [data]
        self.cryptoResults = []
        
    def __str__(self):
        datas = ''
        for data in self.data:
            datas += " "+str(data)
        return "<Instruction %s %s+%s %r%s>" % (hex(self.eip), self.symbolicID(), hex(self.offset), self.disasm, datas)
    
    def __repr__(self):
        return "<%s>" % (self.disasm)
    
    def __cmp__(self, other):
        if other.__class__ == None.__class__:
            return -1
        return cmp(self.eip, other.eip)
    
    def __eq__(self, other):
        return self.eip == other.eip and self.disasm == other.disasm
    
    def instructionTypes(self):
        return ins2type(self.mnemonic())
    
    def mnemonic(self):
        return self.disasm.split(' ')[0]
    
    def modulefile(self):
        return self.module.split('\\')[-1]
    
    def symbolicID(self):
        return self.module + ":" + self.symbol
    
    disConstRegex = re.compile('0x([0-9a-f])*')
    
    def disConst(self):
        try:
            return int(Instruction.disConstRegex.search(self.disasm).group(0),16)
        except AttributeError:
            return 0
    
    def isBitwiseArith(self):
        for t in self.instructionTypes():
            if t in ['logical', 'shftrot', 'bit', 'binary', 'arith']:
                return True
        return False
    
    def isMov(self):
        return 'datamov' in self.instructionTypes()
    
    def isBranch(self):
        return 'branch' in self.instructionTypes()
    
    def addCryptoResult(self, result):
        self.cryptoResults.append(result)
    
    def hasResultAlgo(self, algo):
        for result in self.cryptoResults:
            if result.algorithm == algo:
                return True
        return False
    
    def mergeData(self, instruction):
        if self == instruction:
            self.multiData.append(instruction.data)
        else:
            logging.error("self != instruction")
