import math

def hammingOnePercentage(x, assumeBitLength = 32):
    """returns the percentage of binary-ones in a value"""
    b = bin(x).replace('0b','')
    return b.count('1')/float(assumeBitLength)

def calcEntropy(buf):
    s = 0.0
    n = float(len(buf))
    
    assert(n > 1)
    
    for i in range(256):
        div = buf.count(i)/n
        if div != 0:
            s += div*math.log(div,2)
    return -s/math.log(n,2)

def calcEntropyLutz(buf):
    s = 0.0
    n = float(len(buf))
    
    assert(n > 1)
    for i in buf:
        assert(i <= 255 and i >= 0)
        
    for i in range(256):
        div = buf.count(i)/n
        if div != 0:
            s += div*math.log(div,2)
    return -s/math.log(min([n, 256]), 2)


def numUniqueBytes(buf):
    """returns number of bytes in array which only occur once"""
    d = {}
    for c in buf:
        if d.has_key(c):
            d[c] += 1
        else:
            d[c] = 1
    return d.values().count(1)

def numDifferentBytes(buf):
    """returns number of different bytes in array"""
    return len(set(buf))