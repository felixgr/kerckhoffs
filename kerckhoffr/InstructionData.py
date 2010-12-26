import struct

class InstructionData(object):
    """Referenced Data in a Instruction"""
    
    modeRead = 'R'
    modeWrite = 'W'
    
    def __init__(self, addr, data, size = None, mode = None):
        self.addr = addr
        self.data = data
        self.size = size
        self.mode = mode
        self.nearbydata = []
        self.used = False # used for recursive blocksearch
    
    def __str__(self):
        if self.mode == None:
            return "<Register %s=%s>" % (self.addr, self.data)
        else:
            if self.mode == self.modeRead:
                mode = 'Read'
            if self.mode == self.modeWrite:
                mode = 'Write'
            return "<%s (%d) %s=%s>" % (mode, self.size, hex(self.addr), self.data)
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __repr__(self):
        return str(self)
    
    def isMemory(self):
        return self.mode != None
    
    def isMemoryRead(self):
        return self.mode == self.modeRead
    
    def isMemoryWrite(self):
        return self.mode == self.modeWrite
    
    def data2int(self):
        if self.size <= 64:
            return int(self.data, 16)
        else:
            s = 0
            for index, value in enumerate(self.data2int32list()):
                s += value << (32*index)
            return s
    
    def data2int32list(self):
        # todo: endianess!?
        intlist = []
        s = self.data.replace('0x','')
        for d in s.split('_'):
            intlist.append(int(d, 16))
        return intlist
    
    def data2int8list(self):
        # todo: endianess!?
        intlist = []
        if self.data.count('0x') > 0:
            v = int(self.data,16)
            for ls in range(0, self.size, 8):
                intlist.append((v >> ls) & 0xFF)
        if self.data.count('_') > 0:
            for d in self.data.split('_'):
                v = int(d, 16)
                for ls in range(0,32/(8/len(d)),8):
                    intlist.append((v >> ls) & 0xFF)
        # todo: fix!!
        if intlist == []:
            return [0]
        return intlist
    
    def data2bytes(self):
        bytes = ''
        
        intlist = self.data2int32list()
        
        if self.size > 64:
            intlist.reverse()
            for integer in intlist:
                bytes += struct.pack('<I',integer)
        else:
            integer = intlist[0]
            if self.size == 64:
                bytes += struct.pack('<Q',integer)
            if self.size == 32:
                bytes += struct.pack('<I',integer)
            if self.size == 16:
                bytes += struct.pack('<H',integer)
            if self.size == 8:
                bytes += struct.pack('<B',integer)
        
        return bytes
            