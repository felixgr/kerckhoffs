import hashlib

def md5Bool(indata, outdata):
    # tested
    return outdata == hashlib.md5(indata).digest()
