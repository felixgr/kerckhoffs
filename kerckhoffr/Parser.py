import logging, os, sys

from threading import Thread

from Instruction import Instruction
from InstructionData import InstructionData


class Parser(Thread):
    """Parser for kerck.dll generated Traces"""
    def __init__(self, datafile, destinationBuffer, moduleFilter = (".exe", "beecrypt.dll", "LIBEAY32.dll", "EMPTY", "libeay32.dll", "libssl32.dll", "libcurl.dll")):
        super(Parser, self).__init__()
        
        # for parsing
        self.datafile = datafile
        self.parsed = 0
        self.symbolLookuptable = {}
        self.moduleLookuptable = {}
        self.moduleFilter = moduleFilter
        
        self.destinationBuffer = destinationBuffer
        self.step = self.destinationBuffer.size * 0.75 # warning watch out for overlapping stuff
        self.currentThreshold = self.destinationBuffer.size - 1
        
        if 'kerck-' in self.datafile:
            logging.info('assuming old syntax')
            self.oldSyntax = True
        else:
            logging.info('assuming new syntax')
            self.oldSyntax = False
        
        # manually set syntax
        # self.oldSyntax = False
        
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "<Parser parsed %d lines of file %s, module filtering = %r>" % (self.parsed, self.datafile, self.moduleFilter)
    
    def checkBufferSize(self):
        # eventually pause the filling of destinationBuffer, called on each inserted instruction
        if self.destinationBuffer.inserted > self.currentThreshold:
            self.destinationBuffer.stopFilling = True
            self.currentThreshold += self.step
    
    def run(self):
        def pauseParsing():
            # eventually pause filling
            while self.destinationBuffer.stopFilling:
                pass
        
        try:
            fh = open(self.datafile,'r')
        except IOError:
            logging.error("could not open filename %r" % (self.datafile))
            return
        
        pre = ''  # R
        pre2 = '' # R2
        ins = ''  # 0x Instruction
        post = '' # W
        
        # statistics
        bytesCount = 0
        totalBytes = os.path.getsize(self.datafile)
        intervalBytes = totalBytes / 11
        
        
        for line in fh:
            # statistics
            bytesCount += len(line)
            if self.parsed != 0 and self.parsed % 10000 == 0:
                logging.info("%d %% %s" % (100*bytesCount/float(totalBytes), self.destinationBuffer))
            
            self.parsed += 1
            line = line.replace('\r\n','')
            if len(ins) != 0 and line[0] != 'W':
                # fill fifo
                pauseParsing()
                self.generateInstruction(pre, pre2, ins, post)
                pre, pre2, ins, post = '', '', '', ''
            if line[0] == 'R':
                if pre == '':
                    pre = line
                else:
                    if pre2 != '':
                        logging.debug('triple read at %s / %d' % (pre2, bytesCount))
                    pre2 = line
            if line[0] == '0':
                assert(ins == '')
                ins = line
            if line[0] == 'W':
                if post != '':
                    logging.debug('double write at %s / %d' % (post, bytesCount))
                post = line
        # insert last instruction
        pauseParsing()
        self.generateInstruction(pre, pre2, ins, post)
        
        # finish up
        logging.debug('parsing finished (EOF).')
        self.destinationBuffer.finishedFilling = True
        fh.close()
    
    def generateInstruction(self, pre, pre2, ins, post):
        if self.oldSyntax:
            eip, module, symbol, offset, disasm = ins.split('|')[0:5]
        else:
            eip, module, symbol, offset, threadid, disasm = ins.split('|')[0:6]
        
        
        
        eip = int(eip,16)
        try:
            offset = int(offset,16)
            emptySym = False
        except ValueError:
            # logging.warn('empty symbol information %s:%s+%s' % (module,symbol,offset))
            offset = 0
            emptySym = True
            if module == '' and symbol == '':
                module = 'EMPTY' # todo?
                symbol = 'EMPTY' # todo?
                
        if not emptySym:
            module = self.lookup(self.moduleLookuptable, module)
            symbol = self.lookup(self.symbolLookuptable, symbol)
            
        if len(self.moduleFilter) > 0:
            inside = False
            for m in self.moduleFilter:
                if module.lower().count(m.lower()) > 0:
                    inside = True
            if inside == False:
                return
                
        data = []
        
        if self.oldSyntax:
            registers = ins.split('|')[5:]
        else:
            registers = ins.split('|')[6:]
        
        for register in registers:
            addr, value = register.split('=')
            
            if addr not in ['eax','ebx','ecx','edx','ebp','esp','edi','esi','eflags']:
                logging.warning("exotic register %s" % (addr))
                
            # fixup [abcd][xhl] (like ah, bl, etc)
            # (esi/edi -> si/di not logged by pin)
            if addr in ['eax','ebx','ecx','edx']:
                if addr not in disasm:
                    # logging.debug('not inside %s => %s' % (addr, disasm))
                    letter = addr[1]
                    newreg = ''
                    
                    for part in ['x','h','l']:
                        if letter+part in disasm:
                            # logging.debug('found %s' % (letter+part))
                            newreg = letter+part
                            
                    if newreg != '':
                        # we assert a space before the al/ax/ah register
                        if disasm[disasm.find(newreg)-1] != ' ':
                            logging.warning('NOT A REG? addr %s newreg %s disasm %s' % (addr, newreg, disasm))
                        else:
                            # logging.debug('addr %s newreg %s disasm %s' % (addr, newreg, disasm))
                            addr = newreg
                            # logging.debug('data before %s' % (value))
                            if newreg[1] == 'l':
                                value = hex(int(value,16) & 0x000000FF)
                            if newreg[1] == 'h':
                                value = hex((int(value,16) & 0x0000FF00) >> 8)
                            if newreg[1] == 'x':
                                value = hex(int(value,16) & 0x0000FFFF)
                            # stupid fixup for hex()
                            if value == '0x0':
                                value = '0'
                            # logging.debug('data after %s' % (value))
            # addr fixup done
            
            data.append(InstructionData(addr,value))
            
        for mem in pre, pre2, post:
            if mem != '':
                assert(mem[0] == 'R' or mem[0] == 'W')
                if mem[1:] != '|0':
                    size, assign = mem.split('|')[1:]
                    addr, value = assign.split('=')
                    addr = int(addr,16)
                    size = int(size)
                    data.append(InstructionData(addr, value, size, mem[0]))
        
        # insert the instruction into the fifo
        self.destinationBuffer.insertInstruction(Instruction(eip, module, symbol, offset, disasm, data))
        
        self.checkBufferSize()
    
    def lookup(self, table, string):
        # string is either '@2@somefunction' or '@2'
        if string.count('@') == 1:
            number = string.split('@')[1]
            return table[number]
        else:
            number = string.split('@')[1]
            name = '@'.join(string.split('@')[2:])
            table[number] = name
            return name
    
