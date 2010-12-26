from Crypto.Cipher import ARC4

def rc4Bool(indata, key, outdata):
    # tested
    return outdata == ARC4.new(key).encrypt(indata)
