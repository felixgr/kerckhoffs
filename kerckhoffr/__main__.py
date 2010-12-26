import sys, os, logging
# import cPickle, cProfile
from IPython.Shell import IPShellEmbed

from Instructions import Instructions
from Parser import Parser
from Analysis import Analysis


# configuration options

logging.basicConfig(level=logging.DEBUG, format='\033[0;32m%(asctime)s \033[0;36m%(filename)s:%(funcName)s@%(lineno)d \033[1;33m[%(levelname)s] \033[0;37m%(message)s')
# also see Instructions.py


if len(sys.argv) < 3:
    print "Usage: python %s <single|full|debug|cfg|parse> <inputfile1> <inputfile2> .. <inputfileN>" % (sys.argv[0])
else:
    mode = sys.argv[1]
    datafiles = sys.argv[2:]
    
    if 'full' in mode:
        sys.setrecursionlimit(500) # watch out!
    if 'single' in mode:
        sys.setrecursionlimit(2000) # watch out!
    
    
    try:
        for datafile in datafiles:
            
            instructions = Instructions()
            parser = Parser(datafile, instructions)
            analysis = Analysis(instructions)
            
            if mode == 'debugnofilter':
                logging.info("running debug mode with ipython on file %s..." % (datafile))
                
                parser = Parser(datafile, instructions, [])
                
                parser.run()
                ipshell = IPShellEmbed()
                ipshell()
            
            if mode == 'debug':
                logging.info("running debug mode with ipython on file %s..." % (datafile))
                
                parser.run()
                ipshell = IPShellEmbed()
                ipshell()
            
            if mode == 'singlenofilter':
                logging.info("running single (non-threaded) mode on file %s..." % (datafile))
                parser = Parser(datafile, instructions, [])
                parser.run()
                analysis.run()
            
            if mode == 'single':
                logging.info("running single (non-threaded) mode on file %s..." % (datafile))
                
                parser.run()
                analysis.run()
            
            if mode == 'full':
                logging.info("running full mode on file %s..." % (datafile))
                
                parser.start()
                analysis.start()
                parser.name = 'Parser'
                analysis.name = 'Analysis'
                
                for thread in [analysis, parser]:
                    thread.join()
                    # logging.debug("thread %s joined." % (thread))
            
            if mode == 'fullnofilter':
                logging.info("running debug mode with ipython on file %s..." % (datafile))
                
                parser = Parser(datafile, instructions, [])
                
                parser.start()
                analysis.start()
                parser.name = 'Parser'
                analysis.name = 'Analysis'
                
                for thread in [analysis, parser]:
                    thread.join()
                    # logging.debug("thread %s joined." % (thread))
            
            if mode == 'parse':
                logging.info("running parse test, no analysis on file %s..." % (datafile))
                parser.run()
            
            if mode == 'cfg':
                logging.info("generate control flow graph pdf using dot on file %s..." % (datafile))
                parser.run()
                cfg = instructions.getCFG()
                cfg.writeDOTnPDF(datafile+"-graph")
            
    except KeyboardInterrupt:
        logging.info("aborting...")
    
    logging.info("finished. exiting...")
