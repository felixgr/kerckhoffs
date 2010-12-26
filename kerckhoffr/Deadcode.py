


#
# deadcode, mainly for testing (cumu) or signature generation (const, chains)
#
#





# if mode == 'cumu':
#     parser.moduleFilter = [".exe", "beecrypt.dll", "LIBEAY32.dll"]
#     parser.run()
#     cumus[datafile] = ae.wangReformat_rtn()
# 
#     if mode == 'cumu':
#         logging.info("running ipython...")
#         IPython.Shell.IPShell(user_ns=locals()).mainloop()
# for key in cumus.keys():
#     fh = open(key+'.csv','w')
#     s = key+'\n'
#     for v in (cumus[key])[::len(cumus[key])/1000]:
#         s += (str(v)[0:5]).replace('.',',')+"\n"
#     fh.write(s)
#     fh.close()
# # fix
# cumus = {}
# # fix
# old = 0.0
# for index in range(len(cumu)):
#     c = cumu[index]
#     if c != None:
#         old = c
#     else:
#         cumu[index] = old
# 
# return cumu


# filenamePickle = self.filename + ".pkl"
# try:
#     fh = open(filenamePickle,'r')
#     self.targetPool = cPickle.load(fh)
#     self.targetPool.filling = False
#     fh.close()
#     logging.debug('parsing finished (.PKL) %s' % (self.targetPool))
# except IOError:

# # save pickle
# fh = open(filenamePickle,'w')
# cPickle.dump(self.targetPool, fh)
# fh.close()
# logging.debug('saved new .pkl')



# 
# 
# #
# # enumerate constants (TESTING)
# #
# if mode == 'consts':
#     parser.moduleFilter = [".exe", "beecrypt.dll", "LIBEAY32.dll", "EMPTY"]
#     # cProfile.run('parser.run()')
#     parser.run()
#     filenamePickle = datafile + ".consts.pkl"
#     const = {}
#     for i in pool:
#         c = i.disConst()
#         if c != 0 and i.isBitwiseArith():
#             const[(c,i.mnemonic())] = None
#     fh = open(filenamePickle,'w')
#     cPickle.dump(const.keys(), fh)
#     fh.close()
#     
# #
# # compare constants (TESTING)
# #
# if mode == 'constsCmp':
#     # compares pkl files
#     
#     fh = open(datafile,'r')
#     consts[datafile] = frozenset(cPickle.load(fh))
#     fh.close()
#     
#     if len(consts) == 1:
#         share = consts[datafile]
#     else:
#         share = share & consts[datafile]
#     
#     if len(consts) == len(datafiles):
#         
#         for f in consts.keys():
#             logging.info("%s\t%f" % (f,len(share)/float(len(consts[f]))))
#         
#         for s in share:
#             logging.info("%s\t%s" % (s[1],hex(s[0])))
#         
#         constants = {}
#         for key, value in constsCmpFiles.items():
#             for const,entry in value:
#                 if constants.has_key(const):
#                     constants[const] += 1
#                 else:
#                     constants[const] = 1
#         
#         def keyname(s):
#             return '"' + s.split('-')[2].split('.')[0].split('_')[0] + ' ' + s.split('-')[2].split('.')[0].split('_')[1] + '"'
#         def entryname(s):
#             return '"%s %x"' % (s[1],s[0])
#         
#         fh = open('constCmp.dot','w')
#         fh.write('graph { node [shape=rect];\n')
#         for key, value in constsCmpFiles.items():
#             for entry in value:
#                 # todo
#                 if constants[entry[0]] > 1 and entry[1] != 'cmp':
#                     fh.write("%s -- %s;\n" % (keyname(key),entryname(entry)))
#                     # fh.write("%s %s\n" % (keyname(key),entryname(entry)))
#         fh.write("\n}")
#         fh.close()
#         
#         logging.info("running ipython...")
#         ipshell = IPShellEmbed()
#         ipshell()




# chains = {}
# if mode == 'chains':
#         parser.moduleFilter = [".exe", "beecrypt.dll", "LIBEAY32.dll", "EMPTY"]
#         parser.run()
#         executedBBLs = pool.BBLs()
#         cfg = pool.CFG(executedBBLs)
#         uniqueBBLs = cfg.keys()
#         
#         # log-small/kerck-cryptopp_rc4.out
#         fid = datafile.replace('log-small/kerck-','').replace('.out','')
#         
#         for b in uniqueBBLs:
#             if not chains.has_key(fid):
#                 chains[fid] = set()
#             
#             chains[fid].add(mnenomicChain(b))
# fh = open('out.pkl','w')
# cPickle.dump(chains, fh)
# fh.close()






# 
# 
# 
# import cPickle, pprint
# fh = open('kerckhoffr/tests/signatures/chainsForImplementation.pkl')
# chainsForImplementation = cPickle.load(fh)
# fh.close()
# 
# newchainsForImplementation = {}
# for impl, chain in chainsForImplementation.items():
#     if not ('xor' in impl or 'debug' in impl):
#         newchainsForImplementation[impl] = chain
# 
# chainsForImplementation = newchainsForImplementation
# 
# chainsForAlgorithm = {}
# chainsForAlgorithmUnique = {}
# chainsForImplementationUnique = {}
# 
# for impl, chain in chainsForImplementation.items():
#     # print impl
#     if not chainsForImplementationUnique.has_key(impl):
#         chainsForImplementationUnique[impl] = chainsForImplementation[impl]
#         
#     for impl2, chain2 in chainsForImplementation.items():
#         if impl2 != impl:
#             chainsForImplementationUnique[impl] = chainsForImplementationUnique[impl] - chain2
# 
# 
# for impl, chain in chainsForImplementation.items():
#     # print impl
#     algo = impl.split('_')[1]
#     if not chainsForAlgorithm.has_key(algo):
#         chainsForAlgorithm[algo] = set()
#     chainsForAlgorithm[algo] = chainsForAlgorithm[algo] | chain
# 
# 
# for algo, chain in chainsForAlgorithm.items():
#     # print algo
#     if not chainsForAlgorithmUnique.has_key(algo):
#         chainsForAlgorithmUnique[algo] = chainsForAlgorithm[algo]
#         
#     for algo2, chain2 in chainsForAlgorithm.items():
#         if algo2 != algo:
#             chainsForAlgorithmUnique[algo] = chainsForAlgorithmUnique[algo] - chain2
# 
# # 
# # print
# # for i,v in chainsForImplementation.items(): print i, len(v)
# # print
# # for i,v in chainsForImplementationUnique.items(): print i, len(v)
# # print
# # for i,v in chainsForAlgorithm.items(): print i, len(v)
# # print
# # for i,v in chainsForAlgorithmUnique.items(): print i, len(v)
# 
# pprint.pprint(chainsForImplementation)
# pprint.pprint(chainsForImplementationUnique)
# pprint.pprint(chainsForAlgorithm)
# pprint.pprint(chainsForAlgorithmUnique)


# 
# 
# # print 'rand.0032 key (beecrypt, 1sthalf)', '\x27\x4d\x09\xcb\x10\xec\xca\xad\xa9\x41\x92\x50\xce\xc9\xe4\x1b' in inData
# # print 'rand.0032 key (beecrypt, 2ndhalf)', '\x52\xa4\x69\x2d\x02\x8a\x0c\xc3\xfb\x83\xea\x88\x58\x1b\xa8\x23' in inData
# # print 'rand.0032 key (256ish)  ', '\x27\x4d\x09\xcb\x10\xec\xca\xad\xa9\x41\x92\x50\xce\xc9\xe4\x1b\x52\xa4\x69\x2d\x02\x8a\x0c\xc3\xfb\x83\xea\x88\x58\x1b\xa8\x23' in inData
# # print 'rand.0008               ', '\x34\x37\xcc\xfd\x13\x7a\xb4\x01' in inData
# # print 'rand.0008 left pad      ', '\x00\x00\x00\x00\x00\x00\x00\x00\x34\x37\xcc\xfd\x13\x7a\xb4\x01' in inData
# # print 'rand.0008 right pad     ', '\x34\x37\xcc\xfd\x13\x7a\xb4\x01\x00\x00\x00\x00\x00\x00\x00\x00' in inData
# # print 'rand.0008 256ish        ', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x34\x37\xcc\xfd\x13\x7a\xb4\x01' in inData
# # print 'vectorized openssl key  ', "47\xcc\xfd\x13z\xb4\x01'M\t\xcb\x10\xec\xca\xad" in inData
# # print 'plain.0032 key (gladman)', 'DDDD3333DDDD3333DDDD3333DDDD3333' in inData
# 
# print 'beecrypt p', 'DDDD3333DDDD3333' in plainData
# print 'beecrypt k', "'M\t\xcb\x10\xec\xca\xad\xa9A\x92P\xce\xc9\xe4\x1b" in keyData
# print 'beecrypt c', '\xa7;p\xfc\xb0\x9d\xea\xc1\xb7]^\xb4\x83\x9c\x1c\n' in outData
# 
# print 'openssl  p',  "47\xcc\xfd\x13z\xb4\x01'M\t\xcb\x10\xec\xca\xad" in plainData
# print 'openssl  k',  "'M\t\xcb\x10\xec\xca\xad\xa9A\x92P\xce\xc9\xe4\x1bR\xa4i-\x02\x8a\x0c\xc3\xfb\x83\xea\x88X\x1b\xa8#" in keyData
# print 'openssl  c',  'k7,\x92\xc8*\xdd8\x9e\xddS\xc0\xb7\xa7\xf6\xd3' in outData
# 
# print 'gladman  p',  't\x8a\x8cj\xfbS\xc2\x15\x91\xfb\xeccw\x9cn\xc8' in plainData
# print 'gladman  k',  '\xdd\xdd33\xdd\xdd33\xdd\xdd33\xdd\xdd33' in keyData
# print 'gladman  c',  '\x90\xf3\xe0\xed\x12\x7d\xc5\xe6\x85\x44\x5f\xdf\xea\xe9\x4f\xc6' in outData
# 
# print 'cryptopp p', '47\xcc\xfd\x13z\xb4\x01\x00\x00\x00\x00\x00\x00\x00\x00' in plainData
# print 'cryptopp k', "'M\t\xcb\x10\xec\xca\xad\xa9A\x92P\xce\xc9\xe4\x1b" in keyData
# print 'cryptopp c', 's\xd8\x8b-\xe4\x91\xe4\x1d\rN\x91\x93\xabf\xbc=' in outData
# # print 'cryptopp c (file)', '\x37\x9c\xcf\x69\xd7\xa2\xd7\x2e\x49\x0a\xd5\xd7\x98\x55\x8f\x0e' in outData

# print 'openssl k', '\x34\x37\xcc\xfd\x13\x7a\xb4\x01' in keyData
# print 'openssl p', 'DDDD3333' in plainData
# print 'openssl c', '\xf1\xd0\xd7\x06\x52\x49\x6b\xfe' in outData
# 
# print 'cryptopp k', '\x34\x37\xcc\xfd\x13\x7a\xb4\x01' in keyData
# print 'cryptopp p', '\x34\x37\xcc\xfd\x13\x7a\xb4\x01' in plainData
# print 'cryptopp c', 'UW\xc7\x9a\xb4{\xdc\xf7' in outData


# for out in outData:
#     for outComb in itertools.permutations(out,4): # check combinations, product
#         outComb = "".join(outComb)
#         # logging.debug('outComb %d %r' % (len(outComb), outComb))
#         
#         # following the inData, which is consectutive
#         for blockKey in inData:
#             keyData = "".join(blockKey)
#             keyDataPtr = 0
#             while keyDataPtr <= len(keyData)-16:
#                 keyComb = keyData[keyDataPtr:keyDataPtr+16]
#                 # logging.debug('keyComb %d %r' % (len(keyComb), keyComb))
#                 
#                 for blockInput in inData:
#                     inputData = "".join(blockInput)
#                     inputDataPtr = 0
#                     while inputDataPtr <= len(inputData)-16:
#                         inputComb = inputData[inputDataPtr:inputDataPtr+16]
#                         # logging.debug('inputComb %d %r' % (len(inputComb), inputComb))
#                         
#                         if aesBool(inputComb, keyComb, outComb):
#                             logging.debug('found aes %r %r %r' % (keyComb, outComb, inputComb))
#                             return
#                         inputDataPtr += 4
#                 keyDataPtr += 4
#                 # return

# def xor(a,b):
#     c = ""
#     assert(len(a)==len(b))
#     for i in xrange(len(a)):
#         c += chr(ord(a[i])^ord(b[i]))
#     return c

# 
# def getNearbyBlocks_old(self, readFlag, blockSize):
#     
#     # prepare nearby usage
#     backlog = []
#     
#     for instruction in self:
#         for data in instruction.data:
#             if (data.mode == data.modeRead and readFlag) or (data.mode == data.modeWrite and not readFlag):
#                 for backdata in backlog:
#                     # if abs(data.addr - backdata.addr) == (backdata.size/8):
#                     # save nearbydata for later use
#                     backdata.nearbydata.append(data)
#                     data.nearbydata.append(backdata)
#                 
#                 # append to backlog FIFO
#                 backlog.append(data)
#                 if len(backlog) > 6: # todo parameterize # min is 6 for beecrypt_aes to work
#                     backlog.pop(0)
#     
#     # debug print
#     # for instruction in self:
#     #     for data in instruction.data:
#     #         if (data.mode == data.modeRead and readFlag) or (data.mode == data.modeWrite and not readFlag):
#     #             if len(data.nearbydata) > 0:
#     #                 print data, data.nearbydata
#     #             else:
#     #                 print data
#     
#     
#     # now generate an address based view
#     nearbyData = {}
#     nearbyDataDebug = {}
#     
#     for instruction in self:
#         for data in instruction.data:
#             if (data.mode == data.modeRead and readFlag) or (data.mode == data.modeWrite and not readFlag):
#                 
#                 if nearbyData.has_key(data.addr):
#                     if not data in nearbyData[data.addr]:
#                         # print 'attaching data %r to nearbyData[data.addr] = %r' % (data, nearbyData[data.addr])
#                         nearbyData[data.addr].append(data)
#                         nearbyDataDebug[data.addr].append(data)
#                 else:
#                     nearbyData[data.addr] = [data]
#                     nearbyDataDebug[data.addr] = [data]
#                     
#     keys = nearbyData.keys()
#     keys.sort()
#     blocks = []
#     
#     for address in keys:
#         # debug info
#         s = 'fict %.8x (%d) ' % (address, len(nearbyDataDebug[address]))
#         for data in nearbyDataDebug[address]:
#             s += data.data + " "
#         print s
#         
#         # debug info
#         s = 'real %.8x (%d) ' % (address, len(nearbyData[address]))
#         for data in nearbyData[address]:
#             s += data.data + " "
#         print s
#         
#         
#         def dataIdent(listOfData):
#             s = ''
#             for data in listOfData:
#                 s += '%d ' % data.size
#             return s
#         
#         def recursiveBlockSearch(origIndex, address, ident, block, nextIndex = None):
#             if nextIndex == None:
#                 try:
#                     currentData = nearbyData[address][origIndex]
#                 except IndexError:
#                     print 'data has been used before: returning, address = %.8x origIndex = %d ' % (address, origIndex)
#                     currentData = iteratelist[origIndex]
#                     # return block
#             else:
#                 currentData = nearbyData[address][nextIndex]
#             
#             block.append(currentData)
#             
#             try:
#                 nearbyData[address].remove(currentData)
#             except ValueError:
#                 pass
#             
#             nextAddr = (currentData.size/8) + address
#             
#             if nearbyData.has_key(nextAddr):
#                 # check whether the data set at the next address has the same structure
#                 sameDataRowStructure = ident == dataIdent(nearbyData[nextAddr])
#                 
#                 # determine index dynamically based upon the nearby usage of values
#                 nearbyUsageData = set(currentData.nearbydata) & set(nearbyData[nextAddr])
#                 print "%r ===> %r" % (currentData, nearbyUsageData)
#                 
#                 if len(nearbyUsageData) > 1:
#                     print '(0) len(nearbyUsageData) > 1'
#                     d = []
#                     for nextData in nearbyUsageData:
#                         d = d + recursiveBlockSearch(origIndex, nextAddr, ident, block, nearbyData[nextAddr].index(nextData))
#                     return d
#                 elif len(nearbyUsageData) == 1:
#                     nextData = nearbyUsageData.pop()
#                 elif len(nearbyUsageData) == 0:
#                     nextData = None
#                 
#                 
#                 if sameDataRowStructure and nextData == None:
#                     print '(1) sameDataRowStructure and nextData == None: recursing from %.8x to %.8x' % (address, nextAddr)
#                     return recursiveBlockSearch(origIndex, nextAddr, ident, block)
#                 if sameDataRowStructure and nextData != None:
#                     print '(2) sameDataRowStructure and nextData != None'
#                     return recursiveBlockSearch(origIndex, nextAddr, ident, block)
#                 
#                 if not sameDataRowStructure and nextData != None:
#                     print '(3) not sameDataRowStructure and nextData != None'
#                     nextIndex = nearbyData[nextAddr].index(nextData)
#                     return recursiveBlockSearch(origIndex, nextAddr, ident, block, nextIndex)
#                 if not sameDataRowStructure and nextData == None:
#                     print '(4) not sameDataRowStructure and nextData == None: returning'
#                     return block
#             else:
#                 # nextAddr has nothing for us, thus we return
#                 return block
#         
#         
#         # print "LENGTH", len(nearbyData[address])
#         # copy list to iterate over, because we want to remove elements from the original
#         iteratelist = nearbyData[address][:]
#         for index, data in enumerate(iteratelist):
#             ident = dataIdent(nearbyData[address])
#             block = []
#             try:
#                 print
#                 print 'recursing', data, 'index', index, 'ident', ident
#                 blocks.append(recursiveBlockSearch(index, address, ident, block))
#                 print
#             except RuntimeError:
#                 logging.warning('RuntimeError: maximum recursion depth exceeded in searching for blocks')
#                 blocks.append(block)
#     
#     
#     # debug print
#     # for block in blocks:
#     #     s = "%.8x " % block[0].addr
#     #     for i in block:
#     #         s += "%.8x:%s " % (i.addr, i.data)
#     #     print s
#     #     print
#     
#     # filter some blocks, which are less 128 bits
#     readBlocks = []
#     for block in blocks:
#         size = 0
#         for data in block:
#             size += data.size
#         if size >= blockSize:
#             readBlocks.append(block)
#     
#     # debug print
#     # print '-----------------------------'
#     # for block in readBlocks:
#     #     s = "size reduced %.8x " % block[0].addr
#     #     for i in block:
#     #         s += "%.8x:%s " % (i.addr, i.data)
#     #     print s
#     #     print
#     
#     
#     candidates = set()
#     
#     for block in readBlocks:
#         bytes = ""
#         for data in block:
#             bytes += data.data2bytes()
#         
#         # s = ''
#         # for byte in bytes:
#         #     s += "%.2x" % (ord(byte))
#         # print "byte="+s
#         
#         index = 0
#         total = blockSize/8
#         step = 32/8
#         while index <= (len(bytes) - total):
#             # s = ''
#             # for byte in bytes[index:(index+total)]:
#             #     s += "%.2x" % (ord(byte))
#             # print " add="+s
#             
#             candidates.add(bytes[index:(index+total)])
#             index += step
#     
#     # for i in candidates:
#     #     s = ''
#     #     for byte in i:
#     #         s += "%.2x" % (ord(byte))
#     #     print "cand="+s
#     # print "len+"+str(len(candidates))
#     
#     return candidates