import logging
from threading import Thread
import itertools, struct

import time

from Math import hammingOnePercentage, calcEntropy, calcEntropyLutz, numUniqueBytes, numDifferentBytes

from CryptoResult import CryptoResult
from CryptoReport import CryptoReport

from verifier.xor import xorVerify
from verifier.des import check_p_box, check_s_box, desBool
from verifier.aes import aesBool, aesResult
from verifier.rc4 import rc4Bool
from verifier.md5 import md5Bool

from signatures.api import signaturesymbols
from signatures.mnenomicchains import chainsForImplementationUnique, chainsForAlgorithmUnique, chainsForAlgorithm, chainsForImplementation
from signatures.memory import DES_all, RawDES_Spbox
from signatures.memory import Rijndael_Te0, Rijndael_Te1,Rijndael_Te2,Rijndael_Te3,Rijndael_Te4, Rijndael_Td0,Rijndael_Td1, Rijndael_Td2,Rijndael_Td3, Rijndael_Td4
from signatures.memory import PKCS_DigestDecoration_MD5, MD5MAC_T, MD5
from signatures.mnenomicconst import unique, intersect, implementation

class Analysis(Thread):
    """Analysis of Traces"""
    def __init__(self, target):
        super(Analysis, self).__init__()
        self.target = target
    
    def run(self):
        while not self.target.finishedFilling:
            if self.target.stopFilling:
                self.analyze()
                self.target.stopFilling = False # re-enable parsing
        self.analyze()
    
    def analyze(self):
        
        # # adjusted
        # if self.target.inserted < 10904120:
        #     self.target.list = []
        #     logging.debug("skipping analysis")
        #     return
        
        logging.debug("running analysis on %s" % (self.target))
        
        self.caballero()
        self.wang()
        self.lutz()
        
        
        self.chains()
        self.constmemory()
        self.constmnenomic()
        self.sigAPI()
        
        self.xorNotNullAndMov()
        self.loopDiffer()
        self.symmetricCipherDataTester()
        
        # self.target.list = [] # adjusted
        
        # self.md5sequencetest()
        
        # # self.rsaDataTester()
        
        # logging.debug("report:")
        # CryptoReport(self.target).printText()
        # logging.debug("report finished.")
    
    def md5sequencetest(self):
        for bbl in self.target.getUniqueBBLs():
            if 'rol add mov xor and xor' in bbl.mnenomicChain():
                print 'FOUND'
                print bbl
        
        
    
    def caballero(self, minIns = 20, threshold = 0.55):
        for structuredInstructions in (self.target.getRTNs().bodies(), self.target.getUniqueBBLs()):
            for instructions in structuredInstructions:
                if len(instructions) >= minIns and instructions.isBitwiseArithPercentage() >= threshold:
                    logging.info("caballero module = %s, caballero symbol = %s, caballero types = %r  %f, instructions %r" % (instructions[0].modulefile(), instructions[0].symbol, instructions.instructionTypes(), instructions.isBitwiseArithPercentage(), instructions))
    
    def chains(self):
        chains = set()
        for bbl in self.target.getUniqueBBLs():
            chains.add(bbl.mnenomicChain())
            
        for impl, signatureChains in chainsForImplementation.items():
            match = float(len(chains & signatureChains))/len(signatureChains)
            logging.debug('chainsForImplementation %s %f' % (impl, match))
            
        for impl, signatureChains in chainsForImplementationUnique.items():
            match = float(len(chains & signatureChains))/len(signatureChains)
            logging.debug('chainsForImplementationUnique %s %f' % (impl, match))
            
        for impl, signatureChains in chainsForAlgorithm.items():
            match = float(len(chains & signatureChains))/len(signatureChains)
            logging.debug('chainsForAlgorithm %s %f' % (impl, match))
            
        for impl, signatureChains in chainsForAlgorithmUnique.items():
            match = float(len(chains & signatureChains))/len(signatureChains)
            logging.debug('chainsForAlgorithmUnique %s %f' % (impl, match))
            
    
    def constmemory(self):
        logging.debug('a')
        a = self.target.getBitwiseInstructions()
        logging.debug('b')
        b = a.dataReadsWithoutWrites()
        logging.debug('c')
        c = b.dataMemoryRaw()
        logging.debug('d')
        check = set(c)
        
        s = ''
        for i in check:
            s += '%x ' % (i)
        # logging.debug("%s" % (s))
        for sig in Rijndael_Te0, Rijndael_Te1,Rijndael_Te2,Rijndael_Te3,Rijndael_Te4, Rijndael_Td0,Rijndael_Td1, Rijndael_Td2,Rijndael_Td3, Rijndael_Td4:
            logging.debug("aes %f (%d)" % (float(len(set(sig) & check)) / len(set(sig)), len(set(sig))))
        for sig in PKCS_DigestDecoration_MD5, MD5MAC_T, MD5:
            logging.debug("md5 %f (%d)" % (float(len(set(sig) & check)) / len(set(sig)), len(set(sig))))
        logging.debug("DES_all %f (%d)" % (float(len(set(DES_all) & check)) / len(set(DES_all)), len(set(DES_all))))
        logging.debug("RawDES_Spbox %f (%d)" % (float(len(set(RawDES_Spbox) & check)) / len(set(RawDES_Spbox)), len(set(RawDES_Spbox))))
    
    
    def constmnenomic(self, globalThreshold = 0.70):
        tocheck = set()
        
        for i in self.target.getBitwiseInstructions():
            c = i.disConst()
            if c != 0:
                tocheck.add((c,i.mnemonic()))
        
        for algo in unique.keys():
            p = unique[algo].intersection(tocheck)
            percent = len(p) / float(len(unique[algo]))
            logging.debug('unique %s %f' % (algo, percent))
            
        for algo in intersect.keys():
            p = intersect[algo].intersection(tocheck)
            percent = len(p) / float(len(intersect[algo]))
            logging.debug('intersect %s %f' % (algo, percent))
            
        for algo in implementation.keys():
            for impl in implementation[algo]:
                p = implementation[algo][impl].intersection(tocheck)
                percent = len(p) / float(len(implementation[algo][impl]))
                logging.debug('implementation %s %s %f' % (algo, impl, percent))
    
    def lutz(self, changeThreshold = 0.15):
        # The detection algorithm searches for loops that decrease
        # entropy for any of the three entropy measures by more
        # than 15% and contain xor and arithmetic operations in their loop body.
        
        uniqueBBLs = self.target.getUniqueBBLs()
        loops = self.target.getLoops().stats
        loopExecutions = self.target.getLoops().execs
        
        
        for startEIP, endEIP, execs, minIter, avgIter, maxIter, totalIter in loops:
            executions = loopExecutions[startEIP]
            
            for execution in executions:
                for iteration in execution:
                    intlistWrites = []
                    intlistReads = []
                    datas = []
                    
                    
                    for instruction in iteration:
                        for data in instruction.data:
                            if data.mode != None:
                                datas.append(data)
                    inputAddr = []
                    outputAddr = []
                    for data in datas:
                        if data.mode == data.modeRead and data.addr not in inputAddr:
                            inputAddr.append(data.addr)
                            for i in data.data2int8list():
                                intlistReads.append(i)
                    datas.reverse()
                    for data in datas:
                        if data.mode == data.modeWrite and data.addr not in outputAddr:
                            outputAddr.append(data.addr)
                            for i in data.data2int8list():
                                intlistWrites.append(i)
                                
                    
                    if not (len(intlistWrites) > 1 and len(intlistReads) > 1):
                        # logging.debug("\tmissing in or output (> 1)")
                        continue
                    
                    uniqueIn = numUniqueBytes(intlistReads)/float(len(intlistReads))
                    differentIn = numDifferentBytes(intlistReads)/float(len(intlistReads))
                    entropyIn = calcEntropyLutz(intlistReads)
                    
                    uniqueOut = numUniqueBytes(intlistWrites)/float(len(intlistWrites))
                    differentOut = numDifferentBytes(intlistWrites)/float(len(intlistWrites))
                    entropyOut = calcEntropyLutz(intlistWrites)
                    
                    if min(abs(uniqueIn-uniqueOut), abs(entropyIn-entropyOut), abs(differentIn-differentOut)) > changeThreshold:
                        logging.info("entropy hit: bbl %s of %s:%s, bitwise = %f, writes %d reads %d" % (hex(iteration[0].eip), iteration[0].modulefile(), iteration[0].symbol, iteration.isBitwiseArithPercentage(), len(intlistWrites), len(intlistReads)))
                        logging.debug("%r - %r\texes %d\tmin %d\tavg %d\tmax %d\ttotal %d" % (startEIP, endEIP, execs, minIter, avgIter, maxIter, totalIter))
                        logging.debug(" input: %f / %f / %f" % (uniqueIn, entropyIn, differentIn))
                        logging.debug("output: %f / %f / %f" % (uniqueOut, entropyOut, differentOut))
                        logging.debug("deltas: %f / %f / %f" % (abs(uniqueIn-uniqueOut), abs(entropyIn-entropyOut), abs(differentIn-differentOut)))
                        logging.debug(" indata: %r" % intlistReads)
                        logging.debug("outdata: %r" % intlistWrites)
                        
                        # result = Result('lutz')
                        # result.getLocationFromInstruction(iteration[0])
                        # result.plaintext = intlistReads
                        # result.ciphertext = intlistWrites
                        # result.cryptoConfidence = iteration.isBitwiseArithPercentage()
                        
    
    def sigAPI(self):
        codesymbols = set()
        
        for instruction in self.target:
            codesymbols.add(instruction.symbol)
            
            for signature in signaturesymbols.keys():
                if signature.lower() in instruction.symbol.lower():
                    instruction.addCryptoResult(CryptoResult(\
                    implementation = "unknown implementation, function %s" % (instruction.symbol), \
                    algorithm = signature, \
                    correspondingTest = "sigAPI", \
                    infoText = signaturesymbols[signature]\
                    ))
        
        
        for symbol in codesymbols:
            for signature in signaturesymbols.keys():
                if signature.lower() in symbol.lower():
                    logging.debug('sigAPI: hit %r signature %r description %r' % (symbol, signature, signaturesymbols[signature]))
    
    def wang(self, threshold = 0.50):
        trace = self.target
        
        # first cummulative phase
        total = 0.0
        bitwise = 0.0
        for i in trace:
            if i.isMov():
                i.cumulative = None
                continue
            if i.isBitwiseArith():
                bitwise += 1
            total += 1
            i.cumulative = bitwise/total
        cumu = map(lambda x : x.cumulative, trace)
        cumuMax = cumu.index(max(cumu)) # this is an index
        
        # find min != None
        cumuMin = cumu[cumuMax]
        for value in cumu[cumuMax:]:
            if value < cumuMin and value != None:
                cumuMin = value
        cumuMin = cumuMax + cumu[cumuMax:].index(cumuMin) # this is an index
        
        longestLeafRTN = max(map(lambda x : len(x), trace.getLeafRTNs()))
        for index in range(longestLeafRTN):
            if cumuMax-index >= 0:
                break
            if trace[cumuMax].symbolicID() != trace[cumuMax-index].symbolicID():
                break
        cumuMax = cumuMax - index + 1
        # logging.info("index %d" % (index))
        for index in range(longestLeafRTN):
            if cumuMin+index < len(trace):
                break
            if trace[cumuMin].symbolicID() != trace[cumuMin+index].symbolicID():
                break
        cumuMin = cumuMin + index - 1
        # logging.info("index %d" % (index))
        
        # logging.debug("cumuMax %s cumuMin %s" % (trace[cumuMax+0].symbol, trace[cumuMin+0].symbol))
        
        # leaf phase
        transition = None
        for leaf in trace[cumuMax:cumuMin].getLeafRTNs():
            # logging.debug("%f %s" % (isBitwiseArithPercentage(leaf), leaf[0].symbol))
            if leaf.isBitwiseArithPercentage() > threshold:
                transition = leaf
        if transition != None:
            logging.info("wang reformat transistion function (%f) %s %r" % (transition.isBitwiseArithPercentage(), transition[1].symbol, transition))
        else:
            pass
            # logging.debug("wang reformat no results")
    
    
    
    def xorNotNullAndMov(self, minXorInstructions = 16, maxXorEqualsZero = 0.4, preLenMov = 5, postLenMov = 5):
        trace = self.target
        uniqueBBLs = self.target.getUniqueBBLs()
        loops = self.target.getLoops().stats
        loopExecutions = self.target.getLoops().execs
        
        # based on:
        # xor result != 0
        # xor near mov
        # xor verifier
        
        # check for xor results != 0
        targets = []
        for bbl in uniqueBBLs:
            for ins in bbl:
                if ins.mnemonic() == 'xor' and len(ins.multiData) >= minXorInstructions:
                    dataEqualsZero = 0.0
                    for datas in ins.multiData:
                        for data in datas:
                            if data.addr != 'eflags' and data.data == '0':
                                dataEqualsZero += 1.0
                    if dataEqualsZero/len(ins.multiData) <= maxXorEqualsZero:
                        # logging.debug('appending %s %f' % (ins,dataEqualsZero/len(ins.multiData)))
                        targets.append(ins)
        
        # mov heuristic is not always true
        # heuristic: xor: 2x mov!?
        targets2 = []
        for target in targets:
            for index in range(len(trace)):
                i = trace[index]
                if i == target:
                    if 'mov' in map(lambda x : x.mnemonic(), trace[index-preLenMov:index]) and 'mov' in map(lambda x : x.mnemonic(), trace[index+1:index+1+postLenMov]):
                        targets2.append(i)
        for target in targets:
            if target not in targets2:
                targets.remove(target)
        
        uniqueResults = set()
        
        for target in targets:
            for startEIP, endEIP, execs, minIter, avgIter, maxIter, totalIter in loops:
                # logging.debug("loop start %x end %x target %s" % (startEIP, endEIP, target))
                for execution in loopExecutions[startEIP]:
                    # loop execution = data block
                    # iteration = single xor encryption
                    for iteration in execution:
                        # check that the target is inside the loop body
                        # startEIP < target.eip < endEIP does not work b/c of nested loop bodies
                        inside = False
                        for instruction in iteration:
                            if instruction == target:
                                inside = True
                        if inside:
                            # logging.debug("xorNotNullAndMov %r " % (iteration))
                            
                            # todo: determine input / output by data.mode?
                            int32set = set(iteration.dataMemoryRegisterRaw())
                            
                            for combo in itertools.combinations(int32set, 3):
                                if xorVerify(combo[0],combo[1],combo[2]):
                                    # logging.debug('found xor relation %d ^ %d == %d' % combo)
                                    uniqueResults.add(combo)
                            
        for combo in uniqueResults:
            logging.debug('found xor relation %d ^ %d == %d' % combo)
                # iteration.addCryptoResult(CryptoResult(\
                # implementation = "unknown implementation", \
                # algorithm = "xor", \
                # key = a, \
                # plaintext = b, \
                # ciphertext = c, \
                # verified = True, \
                # cryptoConfidence = 1.0, \
                # implementationConfidence = 0.0, \
                # algorithmConfidence = 1.0, \
                # correspondingTest = "xorNotNullAndMov", \
                # infoText = "todo loop info?"\
                # ))

    
    def loopDiffer(self):
        def sp(dataList, minimumDataFields = 2, hammingThreshold = 0.2):
            if len(dataList) < minimumDataFields:
                return
            
            data = set()
            for item in dataList:
                data.add(item.data2int())
        
            for combo in itertools.combinations(data, 2):
                if check_p_box(combo[0], combo[1]):
                    # include hamming weight of combo into decision making
                    if hammingOnePercentage(combo[0]) > hammingThreshold or hammingOnePercentage(combo[1]) > hammingThreshold:
                        logging.debug('compilant pbox:  %d == p(%d) (hamming:%f,%f)' % (combo[0],combo[1],hammingOnePercentage(combo[0]),hammingOnePercentage(combo[1])))
                    
                # if check_s_box(combo[0], combo[1]):
                #     logging.debug('compilant pbox:  %d == p(%d)' % combo)
        
        def counterSearch(listOfData, minimumDataFields = 5):
            if len(listOfData) < minimumDataFields:
                return
            
            length = len(listOfData)
            first = listOfData[0].data2int()
            last = listOfData[-1].data2int()
            firstLastFit = (float(max(first, last) - min(first, last)) / length)
            
            deltas = []
            for index, data in enumerate(listOfData):
                value = data.data2int()
                if index == 0:
                    lastValue = value
                    continue
                deltas.append(abs(value-lastValue))
                lastValue = value
            
            oneDeltaPercentage = deltas.count(1)/float(len(deltas))
            
            if round(oneDeltaPercentage) > 0.9 and round(firstLastFit) == 1:
                if first > last:
                    logging.debug('downward counter from %d to %d, distance %d' % (first, last, abs(first-last)))
                else:
                    logging.debug('  upward counter from %d to %d, distance %d' % (first, last, abs(first-last)))
        
        def xorSearch(dataList, minimumDataFields = 5):
            if len(dataList) < minimumDataFields:
                return
            
            data = set()
            for item in dataList:
                data.add(item.data2int())
            
            for combo in itertools.combinations(data, 3):
                # todo use verifier or otherwise generate results
                if combo[0] ^ combo[1] == combo[2]:
                    logging.debug('found xor relation %d ^ %d == %d' % combo)
                    # todo: verfify manually
                    # print dataList
        
        def entropyCheck(dataList, changeThreshold = 0.15):
            reads, writes = readsWrites(dataList)
            
            if len(reads) > 1 and len(writes) > 1:
                uniqueIn = numUniqueBytes(reads)/float(len(reads))
                differentIn = numDifferentBytes(reads)/float(len(reads))
                entropyIn = calcEntropyLutz(reads)
                
                uniqueOut = numUniqueBytes(writes)/float(len(writes))
                differentOut = numDifferentBytes(writes)/float(len(writes))
                entropyOut = calcEntropyLutz(writes)
                
                if min(abs(uniqueIn-uniqueOut), abs(entropyIn-entropyOut), abs(differentIn-differentOut)) > changeThreshold:
                    logging.debug("\tentropy hit")
                    logging.debug("\t input: %f / %f / %f" % (uniqueIn, entropyIn, differentIn))
                    logging.debug("\toutput: %f / %f / %f" % (uniqueOut, entropyOut, differentOut))
                    logging.debug("\tdeltas: %f / %f / %f" % (abs(uniqueIn-uniqueOut), abs(entropyIn-entropyOut), abs(differentIn-differentOut)))
                    logging.debug("\t indata: %r" % reads)
                    logging.debug("\toutdata: %r" % writes)
        
        def readsWrites(dataList):
            reads = []
            writes = []
            for data in dataList:
                if data.mode == data.modeRead:
                    for value in data.data2int8list():
                        reads.append(value)
                if data.mode == data.modeWrite:
                    for value in data.data2int8list():
                        writes.append(value)
            return reads, writes
        
        def runChecks(dataList):
            counterSearch(dataList)
            # xorSearch(dataList) # XXX disabled
            # entropyCheck(dataList) # XXX disable
            # sp(dataList)
            
        
        loops = self.target.getLoops().stats
        loopExecutions = self.target.getLoops().execs
        
        for loopstart, executions in loopExecutions.items():
            # debug info
            for loop in loops:
                if loop[0] == loopstart:
                    logging.debug("loop %r - %r\texes %d\tmin %d\tavg %d\tmax %d\ttotal %d" % loop)
            
            # prepare matrix
            
            traceExecutions = []
            for execution in executions:
                traceIterations = []
                for iteration in execution:
                    traceInstructions = []
                    for instruction in iteration:
                        for data in instruction.data:
                            if data.addr != 'eflags':
                                traceInstructions.append(data)
                    traceIterations.append(traceInstructions)
                traceExecutions.append(traceIterations)
            
            # fix every dimension in matrix to have equal length # todo?
            
            tupelsExecution = set()
            tupelsIteration = set()
            tupelsData = set()
            
            for indexExecution, currentExecution in enumerate(traceExecutions):
                for indexIteration, currentIteration in enumerate(currentExecution):
                    for indexData, currentData in enumerate(currentIteration):
                        # logging.debug("matrix position %d / %d / %d" % (indexExecution, indexIteration, indexData))
                        
                        axisExecution = []
                        if (indexIteration,indexData) not in tupelsExecution:
                            for i in xrange(0, len(traceExecutions)):
                                try:
                                    axisExecution.append(traceExecutions[i][indexIteration][indexData])
                                    tupelsExecution.add((indexIteration,indexData))
                                except IndexError:
                                    pass
                                    # logging.debug("IndexError axisExecution")
                        
                        axisIteration = []
                        if (indexExecution,indexData) not in tupelsIteration:
                            for i in xrange(0, len(currentExecution)):
                                try:
                                    axisIteration.append(traceExecutions[indexExecution][i][indexData])
                                    tupelsIteration.add((indexExecution,indexData))
                                except IndexError:
                                    pass
                                    # logging.debug("IndexError axisIteration")
                            
                        
                        axisData = []
                        if (indexExecution,indexIteration) not in tupelsData:
                            for i in xrange(0, len(currentIteration)):
                                try:
                                    axisData.append(traceExecutions[indexExecution][indexIteration][i])
                                    tupelsData.add((indexExecution,indexIteration))
                                except IndexError:
                                    pass
                                    # logging.debug("IndexError axisData")
                        
                        # todo: santiy check for axis data alignment?
                        
                        runChecks(axisExecution)
                        runChecks(axisIteration)
                        runChecks(axisData)
                        
                logging.debug('end of iteration')
            logging.debug('end of execution')
    
    def symmetricCipherDataTester(self):
        # # rc4
        # plainData = self.target.getNearbyBlocks(True, 1024)
        # keyData = plainData
        # outData = self.target.getNearbyBlocks(False, 1024)
        # 
        # logging.debug('testing a set of %d rc4 keys'    % (len(keyData)))
        # logging.debug('testing a set of %d rc4 inputs'  % (len(plainData)))
        # logging.debug('testing a set of %d rc4 outputs' % (len(outData)))
        # 
        # print 'rc4 cryptopp/openssl k', 'u\xa6\xd1^\x1b\x19\xaa\xc6I\xbek,\x80\xd4\xf4\x9e\x89?\x9e\xa5[f\x1f\xd4S\xa8]\xf1@Q\x16)\x12\xec}\x0f\xa8\x99\xbe_\x90$1\xbe3|$\x92\x07\xc0q\xb8\xbd\x8f]\x90\xaa\xc12\xc61\x87\x8c)\xb7}\x00(\xeb!\xdeM\r\x00S)=\xe9\xda\x1a\x15\x81]\x86\xae\x95\xc0\xe7_\x7f>B%\x81\xcfF\xcd|$\xad\xd0\x87.6\x7f\xfb\xbe\xfeT\xda\xecbO\\8\xc6\xad\x92\xc8\xfan\xf8\x144\x9fBp9' in keyData
        # print 'rc4 cryptopp/openssl p', 'DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333DDDD3333' in plainData
        # print 'rc4 cryptopp/openssl c', '\xf5\xb6\x97\xb5\xe4\xdd\xb3nm\xbd\x861\xdc\xbf\xb4l\x99|\xfdSh`\xfac\xf5<:\xe3\xd1\xad\xfd\xf3W\x11&\xba}\xe7\x93p&\x16\x1c\xacs\x86\x81\xcc\x19lP\xb3\x07[\rk\x8d\xe9_,o"\xfb\x03\xaf\xa3\x8a\xb7\xc31F\xea\x88\xf36\x98\x86\xe8\xdb\xb9n;\xb9-\x8b_\xf1F\xcf/\xe4\xe7?Pds\xdb:V\xae\xb1\xe5\xa9\x9c\x13S\xf0\\Xr\xb8;k\t\xb4k\xa6\xd24\xab\xb3\x14r\xc7\xb7\x9e\xc7\x92' in outData
        
        # aes
        # plainData = self.target.hasResultAlgo('aes').getNearbyBlocks(True, 128)
        # keyData = self.target.hasResultAlgo('aes').getNearbyBlocks(True, 128)
        # outData = self.target.hasResultAlgo('aes').getNearbyBlocks(False, 128)
        
        plainData = self.target.getNearbyBlocks(True, 128)
        keyData = plainData # also 128 bit
        outData = self.target.getNearbyBlocks(False, 128)
        
        logging.debug('testing a set of %d aes keys'    % (len(keyData)))
        logging.debug('testing a set of %d aes inputs'  % (len(plainData)))
        logging.debug('testing a set of %d aes outputs' % (len(outData)))
        
        
        # print 'data='+repr((plainData, keyData, outData))
        # return
        
        
        # print 'beecrypt p', 'DDDD3333DDDD3333' in plainData
        # print 'beecrypt k', "'M\t\xcb\x10\xec\xca\xad\xa9A\x92P\xce\xc9\xe4\x1b" in keyData
        # print 'beecrypt c', '\xa7;p\xfc\xb0\x9d\xea\xc1\xb7]^\xb4\x83\x9c\x1c\n' in outData
        # print 'openssl  p',  "47\xcc\xfd\x13z\xb4\x01'M\t\xcb\x10\xec\xca\xad" in plainData
        # print 'openssl  k',  "'M\t\xcb\x10\xec\xca\xad\xa9A\x92P\xce\xc9\xe4\x1bR\xa4i-\x02\x8a\x0c\xc3\xfb\x83\xea\x88X\x1b\xa8#" in keyData
        # print 'openssl  c',  'k7,\x92\xc8*\xdd8\x9e\xddS\xc0\xb7\xa7\xf6\xd3' in outData
        # print 'gladman  p',  't\x8a\x8cj\xfbS\xc2\x15\x91\xfb\xeccw\x9cn\xc8' in plainData
        # print 'gladman  k',  '\xdd\xdd33\xdd\xdd33\xdd\xdd33\xdd\xdd33' in keyData
        # print 'gladman  c',  '\x90\xf3\xe0\xed\x12\x7d\xc5\xe6\x85\x44\x5f\xdf\xea\xe9\x4f\xc6' in outData
        # print 'cryptopp p', '47\xcc\xfd\x13z\xb4\x01\x00\x00\x00\x00\x00\x00\x00\x00' in plainData
        # print 'cryptopp k', "'M\t\xcb\x10\xec\xca\xad\xa9A\x92P\xce\xc9\xe4\x1b" in keyData
        # print 'cryptopp c', 's\xd8\x8b-\xe4\x91\xe4\x1d\rN\x91\x93\xabf\xbc=' in outData
        # 
        # # des
        # plainData = self.target.getNearbyBlocks(True, 64)
        # keyData = plainData
        # outData = self.target.getNearbyBlocks(False, 64)
        # 
        # logging.debug('testing a set of %d des keys'    % (len(keyData)))
        # logging.debug('testing a set of %d des inputs'  % (len(plainData)))
        # logging.debug('testing a set of %d des outputs' % (len(outData)))
        # 
        # print 'des openssl k', '\x34\x37\xcc\xfd\x13\x7a\xb4\x01' in keyData
        # print 'des openssl p', 'DDDD3333' in plainData
        # print 'des openssl c', '\xf1\xd0\xd7\x06\x52\x49\x6b\xfe' in outData
        # print 'des cryptopp k', '\x34\x37\xcc\xfd\x13\x7a\xb4\x01' in keyData
        # print 'des cryptopp p', '\x34\x37\xcc\xfd\x13\x7a\xb4\x01' in plainData
        # print 'des cryptopp c', 'UW\xc7\x9a\xb4{\xdc\xf7' in outData
        # 
        count = 0
        total = len(keyData)*len(plainData)
        starttime = time.time()
        
        # todo check that search space is small enough!
        
        for key in keyData:
            for plain in plainData:
                out = aesResult(plain, key)
                if out in outData:
                    logging.debug('found aes %r %r %r' % (plain, key, out))
                # if desBool(plain, key, out):
                #     logging.debug('found des %r %r %r' % (plain, key, out))                    
                count += 1
                if count % 10000000 == 0:
                    logging.debug('tried %d %% of all combinations with %.3f combination per second' % ((count/float(total))*100, count/float(time.time()-starttime) ))
        
    def rsaDataTester(self):
        # # openssl rsa -in io/o/cryptopp_rsa_key.pem -text
        # Private-Key: (1024 bit)
        # modulus:
        #     00:b2:99:18:2c:e1:0a:8e:69:42:79:83:c4:5c:56:
        #     be:9f:da:6c:02:08:4e:2e:44:66:24:d0:e6:85:3c:
        #     19:e5:1b:08:d0:13:06:62:ab:36:02:2e:78:bc:a2:
        #     9b:57:88:36:9e:a0:54:c6:fc:e0:82:dc:0b:8d:ec:
        #     2a:69:c1:63:f1:2d:04:d3:e7:0c:f8:12:9c:dd:99:
        #     c5:e4:2e:f4:fc:48:04:ef:ed:87:23:84:1e:22:75:
        #     3f:0a:2f:8d:87:03:bb:db:2f:7c:5e:bc:28:d6:9c:
        #     25:1a:0b:81:e4:e5:9b:54:ab:f5:8e:1d:06:cf:0a:
        #     2f:fa:d1:33:35:47:98:4c:0b
        # publicExponent: 17 (0x11)
        # privateExponent:
        #     0f:c2:36:d6:c8:8f:fd:81:c2:19:c7:dc:9e:bc:5c:
        #     1d:29:dc:5a:88:43:22:33:36:30:6c:c9:0b:c1:89:
        #     d0:73:53:99:e3:8f:9f:4b:57:96:c7:dd:7a:0e:59:
        #     00:31:aa:77:68:7f:f3:70:aa:65:e6:3d:41:3a:7c:
        #     36:82:01:49:d6:40:11:73:ff:f7:95:4c:7b:03:ca:
        #     b8:cc:02:2c:f2:c3:20:af:35:ad:f8:98:f8:d7:de:
        #     79:10:43:83:4f:e2:92:37:a8:bf:56:85:a2:9b:3a:
        #     03:61:3e:82:7a:b5:62:f1:69:ec:2e:33:f7:fb:14:
        #     a9:5a:97:ba:21:15:17:4d
        # prime1:
        #     00:f9:de:61:c0:ba:20:6e:84:9b:8e:a2:79:c3:f6:
        #     9d:7f:e7:0f:c3:a0:89:d8:bd:07:c8:13:b4:33:f9:
        #     50:7c:62:a9:66:b7:30:62:a9:c2:24:e8:4b:f5:26:
        #     29:4a:42:8c:82:05:a3:09:3a:2a:58:a3:88:36:a3:
        #     b2:31:b1:db:fd
        # prime2:
        #     00:b6:fb:01:ae:53:37:08:0a:cf:e0:29:e6:b8:3b:
        #     0c:08:cf:c3:12:db:90:a9:f0:c1:1e:a7:4f:43:41:
        #     bb:a8:a6:b8:a7:4c:b5:da:3f:36:ed:55:fd:1d:97:
        #     4a:2c:a6:66:cf:3f:76:5d:7f:aa:3e:a2:48:97:d7:
        #     f0:49:a2:12:a7
        # exponent1:
        #     00:cd:c6:32:62:7b:29:c4:6d:34:cf:d1:18:fb:bc:
        #     09:3c:27:b2:a1:1a:cb:df:aa:bb:1d:3d:67:39:dc:
        #     60:66:6f:5e:54:96:dc:8d:7c:be:00:46:d5:24:3d:
        #     8b:6a:54:ec:2e:d7:77:34:c6:7d:39:f0:15:d2:a4:
        #     ed:19:dd:c4:39
        # exponent2:
        #     60:df:3d:20:0d:ef:f5:32:e6:85:bb:d4:7f:a6:ca:
        #     22:c8:58:37:28:f2:3b:d9:cf:a6:d1:0b:d8:4f:f9:
        #     ef:df:cb:2b:64:d8:be:d6:2c:23:4b:a4:1e:b9:81:
        #     9f:2a:eb:22:6c:e4:4f:9d:f0:b7:bf:53:9b:ae:8e:
        #     45:19:91:67
        # coefficient:
        #     00:cf:4d:f6:f5:74:71:a1:8d:df:1f:ff:58:f3:81:
        #     4d:e0:20:e1:8d:c3:d4:11:5a:6b:4b:b4:60:ea:8c:
        #     6a:6f:d2:78:78:eb:9f:9b:cb:db:c3:83:0f:f8:43:
        #     ec:5e:00:cc:15:0f:16:cd:cf:f0:36:68:d0:75:1e:
        #     2b:88:d5:00:56
        # # openssl rsa -in io/o/openssl_rsa_private.key -text
        # Private-Key: (512 bit)
        # modulus:
        #     00:ad:f2:52:86:dd:f0:0d:15:dc:32:b3:57:6f:51:
        #     df:58:f7:3d:ce:e4:a7:bb:e0:b4:77:4f:39:f6:bb:
        #     d4:a0:14:8a:3b:2a:b1:5e:25:f8:cd:69:c6:17:1b:
        #     51:8d:2d:2b:8b:e5:9b:b1:20:75:70:94:ad:2d:ee:
        #     37:3f:2a:10:cf
        # publicExponent: 65537 (0x10001)
        # privateExponent:
        #     07:3e:44:f3:7a:c0:69:3b:14:cd:43:ac:8b:65:24:
        #     60:c7:02:da:df:a8:a0:69:2d:fa:9d:e0:f3:06:45:
        #     47:59:21:fd:07:d3:25:ce:39:ee:92:f6:0f:05:81:
        #     66:1b:db:ad:8d:60:8f:7b:e7:59:4f:11:ef:4e:13:
        #     be:c0:04:09
        # prime1:
        #     00:e3:3e:8f:e6:a2:d8:fc:43:73:42:61:0e:24:86:
        #     b3:bd:f4:68:e1:44:cd:b2:55:67:8f:1b:94:b6:9b:
        #     d7:8a:63
        # prime2:
        #     00:c3:f5:36:1e:b9:4b:b2:a3:35:06:4a:de:e3:b4:
        #     46:6a:bd:31:4b:ee:63:f1:cd:5e:e8:00:e6:7d:76:
        #     f9:55:a5
        # exponent1:
        #     32:46:2e:09:e5:6f:41:e8:1e:40:ca:3e:19:c0:9f:
        #     55:60:14:2f:fa:4b:d3:af:67:58:d6:ce:40:d4:1b:
        #     8c:67
        # exponent2:
        #     00:84:8e:a3:1e:a3:80:16:86:9a:fe:f7:b4:d1:5a:
        #     08:ec:79:b1:18:49:5a:28:9f:21:9d:55:c6:95:86:
        #     de:e1:d5
        # coefficient:
        #     20:15:52:ff:67:45:60:0c:5c:3c:45:30:f2:00:90:
        #     86:15:c5:53:f3:f2:3d:1a:94:be:22:6e:16:25:e0:
        #     c1:1e
        
        reads512 = self.target.getNearbyBlocks(True, 512)
        reads1024 = self.target.getNearbyBlocks(True, 1024)
        
        privcryptopp = '\x0f\xc2\x36\xd6\xc8\x8f\xfd\x81\xc2\x19\xc7\xdc\x9e\xbc\x5c\x1d\x29\xdc\x5a\x88\x43\x22\x33\x36\x30\x6c\xc9\x0b\xc1\x89\xd0\x73\x53\x99\xe3\x8f\x9f\x4b\x57\x96\xc7\xdd\x7a\x0e\x59\x00\x31\xaa\x77\x68\x7f\xf3\x70\xaa\x65\xe6\x3d\x41\x3a\x7c\x36\x82\x01\x49\xd6\x40\x11\x73\xff\xf7\x95\x4c\x7b\x03\xca\xb8\xcc\x02\x2c\xf2\xc3\x20\xaf\x35\xad\xf8\x98\xf8\xd7\xde\x79\x10\x43\x83\x4f\xe2\x92\x37\xa8\xbf\x56\x85\xa2\x9b\x3a\x03\x61\x3e\x82\x7a\xb5\x62\xf1\x69\xec\x2e\x33\xf7\xfb\x14\xa9\x5a\x97\xba\x21\x15\x17\x4d'
        
        privopenssl = '\x07\x3e\x44\xf3\x7a\xc0\x69\x3b\x14\xcd\x43\xac\x8b\x65\x24\x60\xc7\x02\xda\xdf\xa8\xa0\x69\x2d\xfa\x9d\xe0\xf3\x06\x45\x47\x59\x21\xfd\x07\xd3\x25\xce\x39\xee\x92\xf6\x0f\x05\x81\x66\x1b\xdb\xad\x8d\x60\x8f\x7b\xe7\x59\x4f\x11\xef\x4e\x13\xbe\xc0\x04\x09'
        
        
        if privopenssl in reads512:
            logging.debug('found privopenssl')
        if privcryptopp in reads1024:
            logging.debug('found privcryptopp')