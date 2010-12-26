import logging, os

CONFIG_DOTEXEC = "/opt/local/bin/dot"
# CONFIG_BUFFERSIZE = 750000
# CONFIG_BUFFERSIZE = 100000
# CONFIG_BUFFERSIZE = 250000
# CONFIG_BUFFERSIZE = 600000
CONFIG_BUFFERSIZE = 500000

class Instructions(object):
    """Uberclass for a FIFO of Instruction created from file or memory"""
    
    def __init__(self, l = []):
        # for buffering
        self.size = CONFIG_BUFFERSIZE
        self.list = []
        self.inserted = 0
        
        # for parsing
        self.stopFilling = False
        self.finishedFilling = False
        
        # buffered meta types
        self.snapshot = None # todo single snapshot sufficient?
        self.bufferedBBLs = None
        self.bufferedCFG = None
        self.bufferedRTNs = None
        self.bufferedLeafRTNs = None
        self.bufferedLoops = None
        
        if len(l) > 0:
            self.importInstructionList(l)
    
    def __len__(self):
        return self.list.__len__()
    
    def __iter__(self):
        return self.list.__iter__()
    
    def __getitem__(self, item):
        return self.list[item]
    
    def __getslice__(self, i, j):
        return Instructions(self.list.__getslice__(i, j))
    
    def identifier(self):
        if len(self) > 0:
            return hash(self[0].symbol+self[0].disasm+self[-1].disasm+str(self[0].eip)+str(len(self)))
        else:
            return "<Instructions with no elements>"
    
    def __eq__(self, other):
        return self.identifier() == other.identifier()
    
    def __str__(self):
        if len(self) > 1000:
            return "<Instructions with %d elements, %d total, maxsize %d>" % (len(self), self.inserted, self.size)
        else:
            return "<Instructions with %d elements>" % (len(self))
    
    def __repr__(self):
        if len(self) == 0:
            return "<Instructions with no elements>"
        s = ''
        for i in self:
            s += repr(i) + " "
        return "<Instructions %s %s (%d): %s>" % (hex(self[0].eip), self[0].symbol, len(self), s)
    
    def addCryptoResult(self, result):
        """append a result to a set of Instructions"""
        for i in self:
            i.addCryptoResult(result)
    
    # used for CFG uniqueBBLs
    def mergeData(self, other):
        for i in xrange(len(other)):
            self[i].mergeData(other[i])
    
    # instruction mass analysis
    
    def instructionDiversity(self):
        iMnemomics = {}
        for i in self:
            mnemonic = i.mnemonic()
            try:
                iMnemomics[mnemonic] += 1
            except KeyError:
                iMnemomics[mnemonic] = 1
        for mnemonic in iMnemomics.keys():
            iMnemomics[mnemonic] = iMnemomics[mnemonic] / float(len(self))
        return iMnemomics
    
    def instructionTypes(self):
        rTypes = {}
        rTotal = 0
        for i in self:
            types = i.instructionTypes()
            for type in types:
                try:
                    rTypes[type] += 1/float(len(types))
                except KeyError:
                    rTypes[type] = 1/float(len(types))
                rTotal += 1/float(len(types))
        for type in rTypes.keys():
            rTypes[type] = float(rTypes[type]) / float(rTotal)
        return rTypes
    
    def isBitwiseArithPercentage(self, skipMov = True):
        ba = 0.0
        total = 0.0
        for i in self:
            if skipMov and 'datamov' in i.instructionTypes():
                continue
            if i.isBitwiseArith():
                ba+=1
            total+=1
        if total == 0:
            return 0
        else:
            return ba/total
    
    def mnenomicChain(self):
        chain = ''
        for i in self:
            chain += i.mnemonic()+' '
        return chain
    
    def dataReadsWithoutWrites(self):
        # does not respect size of written data,
        # thus a written block might overlap to a
        # read block
        
        writes = set()
        reads = []
        
        for i in self:
            for data in i.data:
                if data.mode == data.modeRead:
                    if data.addr not in writes:
                        reads.append(i)
                if data.mode == data.modeWrite:
                    writes.add(data.addr)
        return Instructions(reads)
    
    def dataWrites(self):
        writes = []
        for i in self:
            for data in i.data:
                if data.mode == data.modeWrite:
                    writes.append(i)
        return Instructions(writes)
    
    def dataReads(self):
        reads = []
        for i in self:
            for data in i.data:
                if data.mode == data.modeRead:
                    reads.append(i)
        return Instructions(reads)
    
    def dataReadsBlocks(self):
        blocks = []
        currentBlocks = {}
        
        for instruction in self:
            for data in instruction.data:
                if data.mode == data.modeRead:
                    pass
                if data.mode == data.modeWrite:
                    pass
    
    def dataReadsBlocks2(self, addrThreshold = 16):
        lastAddr = 0
        lastInstruction = None
        
        blocks = []
        currentBlock = []
        
        for i in self:
            datas = []
            for data in i.data:
                if data.mode == data.modeRead:
                    datas.append(data)
            if len(datas) == 1:
                data = datas[0]
                
                if abs(lastAddr-data.addr) <= addrThreshold:
                    if len(currentBlock) == 0 and lastInstruction != None:
                        currentBlock.append(lastInstruction)
                    currentBlock.append(i)
                elif len(currentBlock) == 0:
                    blocks.append([lastInstruction])
                else:
                    blocks.append(currentBlock)
                    currentBlock = []
                lastAddr = data.addr
                lastInstruction = i
                
            if len(datas) == 2:
                pass
                # todo
            if len(datas) > 2:
                logging.warn('ouch len(datas) > 2')
        return blocks
    
    def dataWritesBlocks(self, addrThreshold = 16):
        lastAddr = 0
        lastInstruction = None
        
        blocks = []
        currentBlock = []
        
        for i in self:
            for data in i.data:
                if data.mode == data.modeWrite:
                    if abs(lastAddr-data.addr) <= addrThreshold:
                        if len(currentBlock) == 0 and lastInstruction != None:
                            currentBlock.append(lastInstruction)
                        currentBlock.append(i)
                    elif len(currentBlock) > 0:
                        blocks.append(currentBlock)
                        currentBlock = []
                    lastAddr = data.addr
                    lastInstruction = i
        return blocks
    
    def dataMemoryRaw(self):
        raw = []
        for i in self:
            for data in i.data:
                if data.mode == data.modeRead or data.mode == data.modeWrite:
                    raw = raw + data.data2int32list()
        return raw
    
    def dataMemoryRegisterRaw(self):
        raw = []
        for i in self:
            for data in i.data:
                if data.addr != 'eflags':
                    raw = raw + data.data2int32list()
        return raw
    
    
    def getNearbyBlocks(self, readFlag, blockSize):
        
        # prepare nearby usage based view
        backlog = []
        
        for instruction in self:
            for data in instruction.data:
                if (data.mode == data.modeRead and readFlag) or (data.mode == data.modeWrite and not readFlag):
                    for backdata in backlog:
                        # save nearbydata for later use
                        backdata.nearbydata.append(data)
                        data.nearbydata.append(backdata)
                    
                    # append to backlog FIFO
                    backlog.append(data)
                    if len(backlog) > 6: # todo parameterize # min is 6 for beecrypt_aes to work
                        backlog.pop(0)
        
        # now generate an address based view
        dataByAddress = {}
        
        for instruction in self:
            for data in instruction.data:
                if (data.mode == data.modeRead and readFlag) or (data.mode == data.modeWrite and not readFlag):
                    if dataByAddress.has_key(data.addr):
                        if not data in dataByAddress[data.addr]:
                            dataByAddress[data.addr].append(data)
                    else:
                        dataByAddress[data.addr] = [data]
                        
        
        def dataIdent(listOfData):
            s = '['
            for data in listOfData:
                s += '%d/' % data.size
            return s+']'
        
        def recursiveBlockSearch(block, level, address, index):
            level += 1
            # get current data
            currentData = dataByAddress[address][index]
            # append current data to block
            if not currentData.used:
                block.append(currentData)
            # data was used already, we are on a dead end
            else:
                return
            # mark current data as used
            currentData.used = True
            
            nextAddress = (currentData.size/8) + address
            
            if dataByAddress.has_key(nextAddress):
                # determine whether some of next data was used nearby of current data
                nearbyUsedData = set(currentData.nearbydata) & set(dataByAddress[nextAddress])
                
                if len(nearbyUsedData) > 1:
                    for nextData in nearbyUsedData:
                        nextIndex = dataByAddress[nextAddress].index(nextData)
                        # copy old block to use in new recursion branch
                        newblock = block[:]
                        blocks.append(newblock)
                        recursiveBlockSearch(newblock, level, nextAddress, nextIndex)
                elif len(nearbyUsedData) == 1:
                    nextData = nearbyUsedData.pop()
                    nextIndex = dataByAddress[nextAddress].index(nextData)
                    recursiveBlockSearch(block, level, nextAddress, nextIndex)
                elif len(nearbyUsedData) == 0:
                    # check whether the data set at the next address has the same structure
                    if dataIdent(dataByAddress[address]) == dataIdent(dataByAddress[nextAddress]):
                        recursiveBlockSearch(block, level, nextAddress, index)
            
            
        
        # apply recursive function to all addresses
        keys = dataByAddress.keys()
        keys.sort()
        allBlocks = []
        
        for address in keys:
            for index, data in enumerate(dataByAddress[address]):
                # print "%.8x %s" % (data.addr, data.data)
                
                block = []
                blocks = [block]
                level = 0
                try:
                    recursiveBlockSearch(block, level, address, index)
                    for blockToAppend in blocks:
                        allBlocks.append(blockToAppend)
                except RuntimeError:
                    logging.warning('RuntimeError: maximum recursion depth exceeded in searching for blocks')
                    for blockToAppend in blocks:
                        allBlocks.append(blockToAppend)
        
        # filter some blocks, which are less blockSize bits
        sizeReduced = []
        for block in allBlocks:
            size = 0
            for data in block:
                size += data.size
            if size >= blockSize:
                sizeReduced.append(block)
        
        # generate the candidate chunks
        candidates = set()
        
        for block in sizeReduced:
            bytes = ""
            for data in block:
                bytes += data.data2bytes()
            
            index = 0
            total = blockSize/8
            step = 32/8
            while index <= (len(bytes) - total):
                candidates.add(bytes[index:(index+total)])
                index += step
        
        # clear used flag
        self.clearUsedFlag()
        
        return candidates
    
    def clearUsedFlag(self):
        for instruction in self:
            for data in instruction.data:
                data.used = False
    
    # meta types
    
    def hasResultAlgo(self, algo):
        hasResultAlgo = []
        for i in self:
            if i.hasResultAlgo(algo):
                hasResultAlgo.append(i)
        return Instructions(hasResultAlgo)
        
    
    def getBitwiseInstructions(self):
        bitwise = []
        for i in self:
            if i.isBitwiseArith():
                bitwise.append(i)
        return Instructions(bitwise)
    
    # meta type buffering
    
    def getBBLs(self):
        if self.snapshot == self.inserted and self.bufferedBBLs != None:
            return self.bufferedBBLs
        else:
            self.bufferedBBLs = BBLs(self)
            self.snapshot = self.inserted
            return self.bufferedBBLs
    
    def getCFG(self):
        if self.snapshot == self.inserted and self.bufferedCFG != None:
            return self.bufferedCFG
        else:
            self.bufferedCFG = CFG(self.getBBLs())
            self.snapshot = self.inserted
            return self.bufferedCFG
    
    def getUniqueBBLs(self):
        if self.snapshot == self.inserted and self.bufferedCFG != None:
            return self.bufferedCFG
        else:
            self.bufferedCFG = CFG(self.getBBLs())
            self.snapshot = self.inserted
            return self.bufferedCFG.getUniqueBBLs()
    
    def getRTNs(self):
        if self.snapshot == self.inserted and self.bufferedRTNs != None:
            return self.bufferedRTNs
        else:
            self.bufferedRTNs = RTNs(self.getCFG())
            self.snapshot = self.inserted
            return self.bufferedRTNs
    
    def getLeafRTNs(self):
        if self.snapshot == self.inserted and self.bufferedLeafRTNs != None:
            return self.bufferedLeafRTNs
        else:
            self.bufferedLeafRTNs = leafRTNs(self)
            self.snapshot = self.inserted
            return self.bufferedLeafRTNs
    
    def getLoops(self):
        if self.snapshot == self.inserted and self.bufferedLoops != None:
            return self.bufferedLoops
        else:
            self.bufferedLoops = Loops(self.getCFG(), self)
            self.snapshot = self.inserted
            return self.bufferedLoops
    
    # buffer functions
    
    def insertInstruction(self, e):
        self.list.append(e)
        self.inserted += 1
        # implements the FIFO
        if len(self) > self.size:
            self.list.pop(0)
    
    def importInstructionList(self, l):
        # fill buffer from an external list l
        assert(len(self) == 0)
        self.list = l
        self.inserted = len(self)




class BBLs(object):
    """list of BBLs, each BBL is a Instructions Object"""
    def __init__(self, instructionList):
        self.list = []
        
        logging.debug("creating BBLs step 1")
        lastWasBranch = True
        starter = {}
        for i in instructionList:
            if lastWasBranch == True:
                i.startsBBL = True
                starter[i.eip] = 1
            else:
                i.startsBBL = False
                
            if i.isBranch():
                i.endsBBL = True
                lastWasBranch = True
            else:
                i.endsBBL = False
                lastWasBranch = False
                
        logging.debug("creating BBLs step 2")
        cur = []
        for i in instructionList:
            # check if there is another bbl which punches a hole into cur
            if not i.startsBBL and len(cur) > 0:
                try:
                    if starter[i.eip] == 1:
                        self.list.append(Instructions(cur))
                        cur = []
                except KeyError:
                    pass
            cur.append(i)
            if i.endsBBL:
                self.list.append(Instructions(cur))
                cur = []
                
        logging.debug("creating BBLs finished %s" % (self))
    
    def __len__(self):
        return self.list.__len__()
    
    def __iter__(self):
        return self.list.__iter__()
    
    def __getitem__(self, item):
        return self.list[item]
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "<%d BBLs (executed) first starting with instruction %s>" % (len(self), self[0][0])


class Loops(object):
    """meta type object for Loops"""
    def __init__(self, cfg, trace):
        def reverseIndex(l, e):
            l.reverse()
            i = len(l) - l.index(e) - 1
            l.reverse()
            return i
        
        def newLoop(t,pc):
            CLS.append([t,pc,1])
        
        def iterateLoop(t,b):
            i = reverseIndex(map(lambda x : x[0], CLS), t)
            CLS[i][2] += 1
        
        def finishLoop(t,b):
            i = reverseIndex(map(lambda x : x[0], CLS), t)
            finishedLoops.append((CLS[i][0].eip, CLS[i][1].eip, CLS[i][2]))
        
        self.CFG = cfg
        
        CLS = []
        standardBranches = {}
        finishedLoops = []
        
        logging.debug('creating loops: preparing branch list')
        
        # enumerate all cfg branches
        cfgBranches = []
        for bbl in cfg.getUniqueBBLs():
            # get amount of unique edges from bbl
            s = {}
            for e in cfg[bbl]:
                s[repr(e)] = 0
            if len(s.keys()) > 1:
                # if edges > 1, add to branch list
                cfgBranches.append(bbl[-1])
        
        logging.debug('creating loops: walking through execution')
        
        # walk through execution
        for index in range(len(trace)):
            # skip last instruction
            if index == len(trace) - 1:
                continue
                
            # current instruction
            pc = trace[index]
            # next instruction
            t = trace[index+1]
            
            if pc in cfgBranches:
                CLSt = map(lambda x : x[0], CLS)
                CLSb = map(lambda x : x[1], CLS)
                
                # logging.info(' ')
                # logging.info(' pc %s' % hex(pc.eip))
                # logging.info('  t %s' % hex(t.eip))
                # for clsvar in CLS:
                #     logging.info('CLS t %s b %s c %d' % (hex(clsvar[0].eip), hex(clsvar[1].eip), clsvar[2]))
                
                # Absatz 1
                # Whenever a backward branch or jump instruction
                # to target T is executed, the CLS is searched.
                if t not in CLSt:
                    # logging.info('CASE-A')
                    # If there is not any entry with target address
                    # T and the branch is taken, it means that a new
                    # loop execution is started. In this case, loop
                    # (T,PC) is pushed onto the CLS. If the branch is
                    # not taken, no action is performed. It means
                    # that a loop with only one iteration has been
                    # executed.
                    newLoop(t,pc)
                    standardBranches[pc.eip] = t
                else:
                    # If loop T is found in the entry i of the CLS
                    i = reverseIndex(CLSt, t)
                    # and the branch is taken,
                    
                    try:
                        taken = (standardBranches[pc.eip] == t)
                    except KeyError:
                        taken = True
                        
                    if taken:
                        # logging.info('CASE-B1')
                        # an iteration of loop T has finished and consequently,
                        # a new iteration of the same loop execution is started.
                        iterateLoop(t,pc)
                        
                        # The CLS entries in the range [top,i+1] are popped out.
                        CLS = CLS[:i + 1]
                        
                        # If PC is higher than the value of field B, this field is updated.
                        if pc > CLS[i][1]:
                            CLS[i][1] = pc
                            standardBranches[pc.eip] = t
                    else:
                        # If the branch is not taken and the value of field B is
                        # lower than or equal to PC, it means that both the
                        # iteration and the execution of loop T have finished.
                        
                        try:
                            i = reverseIndex(CLSt, standardBranches[pc.eip])
                            if pc >= CLS[i][1]:
                                # logging.info('CASE-B2')
                                iterateLoop(CLS[i][0],CLS[i][1])
                                finishLoop(CLS[i][0],CLS[i][1])
                                # The CLS entries in the range [top,i] are popped out.
                                CLS = CLS[:i]
                        except ValueError:
                            pass
                            
                # Absatz 2
                # Whenever the address of a jump or a taken branch belongs to a
                # loop in the CLS, it is checked whether the target address is
                # outside the loop body.
                newCLS = []
                for entry in CLS:
                    remove = False
                    
                    if pc >= entry[0] and pc <= entry[1]:
                        if t < entry[0] or t > entry[1]:
                            # All loops that meet this condition are
                            # removed from the CLS (i.e., it is considered that their
                            # executions have finished).
                            # logging.info('CASE-C1')
                            iterateLoop(entry[0],entry[1])
                            remove = True
                    # Finally, for any executed return
                    # instruction, all loops in the CLS whose body comprise such
                    # instruction are also popped out.
                    if pc.mnemonic().count('ret') > 0:
                        if pc >= entry[0] and pc <= entry[1]:
                            # logging.info('CASE-C2')
                            remove = True
                            
                    if remove:
                        # iterateLoop(entry[0],entry[1]) # not needed?
                        finishLoop(entry[0],entry[1])
                    else:
                        newCLS.append(entry)
                CLS = newCLS
                
            # end of 'if pc in cfgBranches'
            
            
            
        # finish up the rest on the stack
        CLS.reverse()
        for entry in CLS:
            finishLoop(entry[0],entry[1])
            
        # analysis, generate stats table
        analysis = {}
        for r in finishedLoops:
            # logging.info("%s %s %d" % (r)) # example: 4198704 4198725 128
            try:
                analysis[r[0],r[1]].append(r[2])
            except KeyError:
                analysis[r[0],r[1]] = [r[2]]
                
        def total(seq):
            s = 0
            for e in seq:
                s += e
            return s
        
        def avg(seq):
            return total(seq)/float(len(seq))
        
        self.stats = []
        for r in analysis.keys():
            s = analysis[r]
            if(total(s) > 1):
                # we only record loop bodies with more than one execution
                self.stats.append((r[0], r[1], len(s), min(s), avg(s), max(s), total(s)))
                
        # do a second walk through the execution to determine the loop bodies
        self.execs = {}
        for loopInfo in self.stats:
            self.execs[loopInfo[0]] = [[Instructions()]]
        # self.execs = exec->iter->ins
        
        # prepare iteration decrementer
        loopIterations = []
        for iteration in finishedLoops:
            # filter / more than one iteration
            if iteration[2] > 1:
                loopIterations.append([iteration[0], iteration[2]])
                # logging.debug("%r %r" % (iteration[0], iteration[2]))
                
        currentLoop = []
        inLoop = False
        
        for ins in trace:
            eip = ins.eip
            
            startsLoop = eip in map(lambda x : x[0], self.stats)
            endsLoop = eip in map(lambda x : x[1], self.stats)
            
            # assert(not (startsLoop and endsLoop)) # fails in crytpopp des # todo
            
            # start new loop
            if startsLoop:
                currentLoop.append(eip)
                
            # are we inside a loop?
            try:
                currentBody = currentLoop[-1]
                inLoop = True
            except IndexError:
                currentBody = None
                inLoop = False
                
            # save instruction
            if inLoop:
                self.execs[currentBody][-1][-1].insertInstruction(ins) # last Iteration For Current Body
                
            # do we end a loop iteration?
            if endsLoop and inLoop:
                self.execs[currentBody][-1].append(Instructions()) # next iteration
                currentLoop.pop()
                
                # logging.debug('eo iter')
                
                # do we end a loop exection?
                for execution in loopIterations:
                    if currentBody == execution[0] and execution[1] > 0:
                        execution[1] = execution[1] - 1
                        if execution[1] == 0:
                            self.execs[currentBody].append([Instructions()]) # next execution
                            # logging.debug('eo exec')
                        break
                        
        # remove last empty list
        for key in self.execs.keys():
            for execution in self.execs[key]:
                for iteration in execution:
                    if len(iteration) == 0:
                        execution.remove(iteration)
                if execution == []:
                    self.execs[key].remove([])
        
        logging.debug('creating loops finished %s' % (self))
        
        # end of loop detection
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        s = ''
        for stat in self.stats:
            s += ' %d|%d' % (stat[2], stat[6])
        return "<Loops %d bodies, executions|total iterations =%s>" % (len(self.stats), s)
    
    def loggingOutputStats(self):
        for stat in self.stats:
            logging.info("%r - %r\texes %d\tmin %d\tavg %d\tmax %d\ttotal %d" % stat)
    



class RTNs(object):
    """meta type object for routines"""
    def __init__(self, cfg):
        # does not always work properly
        self.sym = {}
        for bbl in cfg.getUniqueBBLs():
            for i in bbl:
                try:
                    self.sym[i.symbolicID()].insertInstruction(i)
                except KeyError:
                    self.sym[i.symbolicID()] = Instructions()
                    self.sym[i.symbolicID()].insertInstruction(i)
    
    def __len__(self):
        return self.sym.__len__()
    
    def __iter__(self):
        return self.sym.__iter__()
    
    def __getitem__(self, item):
        return self.sym[item]
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "<%d RTNs (executed)>" % (len(self))
    
    def bodies(self):
        return self.sym.values()

class leafRTNs(object):
    """meta type for wang et. al. leaf routines"""
    def __init__(self, trace):
        self.sym = []
        cur = Instructions()
        curRTN = ''
        for i in trace:
            if curRTN != i.symbolicID() and len(cur) > 0:
                self.sym.append(cur)
                cur = Instructions()
            curRTN = i.symbolicID()
            cur.insertInstruction(i)
    
    def __len__(self):
        return self.sym.__len__()
    
    def __iter__(self):
        return self.sym.__iter__()
    
    def __getitem__(self, item):
        return self.sym[item]
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "<%d leafRTNs (executed)>" % (len(self))


class CFG(object):
    """meta type class for CFGs"""
    def __init__(self, executedBBLs):
        bblsUnique = {}
        bblsEdges = {}
        lastBBL = None
        self.CFG = {}
        
        logging.debug("creating CFG step 1: unique bbls, instruction data array")
        for bbl in executedBBLs:
            try:
                bblsUnique[bbl.identifier()].mergeData(bbl)
            except KeyError:
                bblsUnique[bbl.identifier()] = bbl
            
            try:
                bblsEdges[lastBBL].append(bbl)
            except KeyError:
                bblsEdges[lastBBL] = [bbl]
            
            lastBBL = bbl.identifier()
        
        logging.debug("creating CFG step 2: create edges")
        
        for bbl in bblsUnique.values():
            try:
                self.CFG[bbl] = bblsEdges[bbl.identifier()]
            except KeyError:
                self.CFG[bbl] = [] # has no edges going away from the bb
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        e = 0
        for i in self.CFG.values():
            e += len(i)
        return "<CFG with %d nodes, %d edges>" % (len(self.CFG.keys()), e)
    
    def __getitem__(self, item):
        return self.CFG[item]
    
    def __iter__(self):
        return self.CFG.__iter__()
    
    def getUniqueBBLs(self):
        return self.CFG.keys()
    
    def writeDOTnPDF(self, filename):
        def printer(s):
            s = repr(s)
            s = s.replace(": <",":\\n<")
            s = s.replace("> <",">\\n<")
            s = s.replace("<Instructions ","").replace("<","").replace(">","")
            return '"%s"' % (s)
        dotEvil = 'digraph { bgcolor=black; edge[fontcolor=white, color=green]; node [shape=rect, color=green, fontcolor=white];\n'
        dotDefault = 'digraph { node [shape=rect];\n'
        dot = dotDefault
        for bbl in self.CFG.keys():
            targets = []
            for target in self.CFG[bbl]:
                if target not in targets:
                    targets.append(target)
                else:
                    continue
                if self.CFG[bbl].count(target) > 1:
                    # label = "[color=green,fontcolor=white,label=\"%d\"]" % self.CFG[bbl].count(target)
                    label = "[label=%d]" % self.CFG[bbl].count(target)
                else:
                    label = ""
                try:
                    dot += "%s -> %s %s;\n" % (printer(bbl), printer(target), label)
                except KeyError:
                    pass
                    # logging.error("keyerr %s -> %s" % (bbl, target))
        dot += "\n}"
        fh = open(filename+'.dot','w')
        fh.write(dot)
        fh.close()
        
        logging.info("wrote CFG to %s.dot" % filename)
        
        cmd = "%s -Tpdf -O %s" % (CONFIG_DOTEXEC, filename+'.dot')
        if os.system(cmd) != 0:
            logging.warning("problem while running graphviz!")
        logging.info("wrote CFG to %s.dot.pdf" % filename)
