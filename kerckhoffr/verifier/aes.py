from Crypto.Cipher import AES

def aesBool(indata, key, outdata):
    # todo check sizes
    # tested
    return outdata == AES.new(key).encrypt(indata)

def aesResult(indata, key):
    return AES.new(key).encrypt(indata)
