#include "pin.H"
#include "instlib.H"
#include "portability.H"
#include <vector>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <map>
#include <set>

using namespace INSTLIB;


/* Commandline Switches */

KNOB<std::string> KnobModuleWhitelist(KNOB_MODE_APPEND, "pintool",
  "mw", "", "whitelist a module for tracing");
KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE,         "pintool",
    "o", "kerck.out", "trace file");
KNOB<UINT64>   KnobStart(KNOB_MODE_WRITEONCE,                "pintool",
    "istart", "0", "after which number of instructions to start (default 0)");
KNOB<UINT64>   KnobStop(KNOB_MODE_WRITEONCE,                "pintool",
    "istop", "100000000", "after which number of instructions to stop (default 100 000 000)");
KNOB<THREADID>   KnobWatchThread(KNOB_MODE_WRITEONCE,                "pintool",
    "watch_thread", "-1", "thread to watch, -1 for all");
KNOB<BOOL>   KnobFlush(KNOB_MODE_WRITEONCE,                "pintool",
    "flush", "0", "Flush output after every instruction");
KNOB<BOOL>   KnobSymbols(KNOB_MODE_WRITEONCE,       "pintool",
    "symbols", "1", "Include symbol information");
KNOB<BOOL>   KnobLines(KNOB_MODE_WRITEONCE,       "pintool",
    "lines", "0", "Include line number information");
KNOB<BOOL>   KnobSilent(KNOB_MODE_WRITEONCE,       "pintool",
    "silent", "0", "Do everything but write file (for debugging).");




INT32 Usage()
{
    cerr <<
        "This pin tool collects an instruction trace for debugging\n"
        "\n";

    cerr << KNOB_BASE::StringKnobSummary();

    cerr << endl;

    return -1;
}


LOCALVAR UINT64 startStopEnabled = 1;


LOCALVAR std::ofstream out;

LOCALVAR INT32 enabled = 0;

LOCALFUN BOOL Emit(THREADID threadid)
{
    if (!enabled || 
        KnobSilent || 
        (KnobWatchThread != static_cast<THREADID>(-1) && KnobWatchThread != threadid))
        return false;
    return true;
}

LOCALFUN VOID Flush()
{
    if (KnobFlush)
        out << flush;
}




LOCALFUN VOID Handler(CONTROL_EVENT ev, VOID *, CONTEXT * ctxt, VOID *, THREADID)
{
    switch(ev)
    {
      case CONTROL_START:
        enabled = 1;
        PIN_RemoveInstrumentation();
    // So that the rest of the current trace is re-instrumented.
    if (ctxt) PIN_ExecuteAt (ctxt);
        break;

      case CONTROL_STOP:
        enabled = 0;
        PIN_RemoveInstrumentation();
    // So that the rest of the current trace is re-instrumented.
    if (ctxt) PIN_ExecuteAt (ctxt);
        break;

      default:
        ASSERTX(false);
    }
}




VOID EmitNoValues(THREADID threadid, string * str)
{
    if (!Emit(threadid))
        return;
    
    out
        << *str
        << '\n' << std::flush;

    Flush();
}

VOID Emit1Values(THREADID threadid, string * str, string * reg1str, ADDRINT reg1val)
{
    if (!Emit(threadid))
        return;
    
    out
        << *str << "|"
        << *reg1str << "=" << reg1val
        << '\n' << std::flush;

    Flush();
}

VOID Emit2Values(THREADID threadid, string * str, string * reg1str, ADDRINT reg1val, string * reg2str, ADDRINT reg2val)
{
    if (!Emit(threadid))
        return;
    
    out
        << *str << "|"
        << *reg1str << "=" << reg1val
        << "|" << *reg2str << "=" << reg2val
        << '\n' << std::flush;
    
    Flush();
}

VOID Emit3Values(THREADID threadid, string * str, string * reg1str, ADDRINT reg1val, string * reg2str, ADDRINT reg2val, string * reg3str, ADDRINT reg3val)
{
    if (!Emit(threadid))
        return;
    
    out
        << *str << "|"
        << *reg1str << "=" << reg1val
        << "|" << *reg2str << "=" << reg2val
        << "|" << *reg3str << "=" << reg3val
        << '\n' << std::flush;
    
    Flush();
}


VOID Emit4Values(THREADID threadid, string * str, string * reg1str, ADDRINT reg1val, string * reg2str, ADDRINT reg2val, string * reg3str, ADDRINT reg3val, string * reg4str, ADDRINT reg4val)
{
    if (!Emit(threadid))
        return;
    
    out
        << *str << "|"
        << *reg1str << "=" << reg1val
        << "|" << *reg2str << "=" << reg2val
        << "|" << *reg3str << "=" << reg3val
        << "|" << *reg4str << "=" << reg4val
        << '\n' << std::flush;
    
    Flush();
}


const UINT32 MaxEmitArgs = 4;

AFUNPTR emitFuns[] = 
{
    AFUNPTR(EmitNoValues), AFUNPTR(Emit1Values), AFUNPTR(Emit2Values), AFUNPTR(Emit3Values), AFUNPTR(Emit4Values)
};

VOID EmitXMM(THREADID threadid, UINT32 regno, PIN_REGISTER* xmm)
{
    if (!Emit(threadid))
        return;
    out << "\t\t\tXMM" << dec << regno << " := " << setfill('0') << hex;
    out.unsetf(ios::showbase);
    for(int i=0;i<16;i++) {
        if (i==4 || i==8 || i==12)
            out << "_";
        out << setw(2) << (int)xmm->byte[15-i]; // msb on the left as in registers
    }
    out  << setfill(' ') << '\n' << std::flush;
    out.setf(ios::showbase);
    Flush();
}

VOID AddXMMEmit(INS ins, IPOINT point, REG xmm_dst) 
{
    INS_InsertCall(ins, point, AFUNPTR(EmitXMM), IARG_THREAD_ID,
                   IARG_UINT32, xmm_dst - REG_XMM0,
                   IARG_REG_CONST_REFERENCE, xmm_dst,
                   IARG_END);
}

VOID AddEmit(INS ins, IPOINT point, string & traceString, UINT32 regCount, REG regs[])
{
    if (regCount > MaxEmitArgs)
        regCount = MaxEmitArgs;
    
    IARGLIST args = IARGLIST_Alloc();
    for (UINT32 i = 0; i < regCount; i++)
    {
        IARGLIST_AddArguments(args, IARG_PTR, new string(REG_StringShort(regs[i])), IARG_REG_VALUE, regs[i], IARG_END);
    }

    INS_InsertCall(ins, point, emitFuns[regCount], IARG_THREAD_ID,
                   IARG_PTR, new string(traceString),
                   IARG_IARGLIST, args,
                   IARG_END);
    IARGLIST_Free(args);
}

LOCALVAR VOID *WriteEa[PIN_MAX_THREADS];

VOID CaptureWriteEa(THREADID threadid, VOID * addr)
{
    WriteEa[threadid] = addr;
}

VOID ShowN(UINT32 n, VOID *ea)
{
    out.unsetf(ios::showbase);
    // Print out the bytes in "big endian even though they are in memory little endian.
    // This is most natural for 8B and 16B quantities that show up most frequently.
    // The address pointed to 
    out << std::setfill('0');
    UINT8 b[512];
    UINT8* x;
    if (n > 512)
        x = new UINT8[n];
    else
        x = b;
    PIN_SafeCopy(x,static_cast<UINT8*>(ea),n);    
    for (UINT32 i = 0; i < n; i++)
    {
        out << std::setw(2) <<  static_cast<UINT32>(x[n-i-1]);
        if (((reinterpret_cast<ADDRINT>(ea)+n-i-1)&0x3)==0 && i<n-1)
            out << "_";
    }
    out << std::setfill(' ');
    out.setf(ios::showbase);
    if (n>512)
        delete [] x;
}


VOID EmitWrite(THREADID threadid, UINT32 size)
{
    if (!Emit(threadid))
        return;
    
    out << "W|";
    
    VOID * ea = WriteEa[threadid];
    
    switch(size)
    {
      case 0:
        out << "0" << '\n' << std::flush; // zero repeat count
        break;
        
      case 1:
        {
            UINT8 x;
            PIN_SafeCopy(&x, static_cast<UINT8*>(ea), 1);
            out << "8|" << ea << "=" << static_cast<UINT32>(x) << '\n' << std::flush;
        }
        break;
        
      case 2:
        {
            UINT16 x;
            PIN_SafeCopy(&x, static_cast<UINT16*>(ea), 2);
            out << "16|" << ea << "=" << x << '\n' << std::flush;
        }
        break;
        
      case 4:
        {
            UINT32 x;
            PIN_SafeCopy(&x, static_cast<UINT32*>(ea), 4);
            out << "32|" << ea << "=" << x << '\n' << std::flush;
        }
        break;
        
      case 8:
        {
            UINT64 x;
            PIN_SafeCopy(&x, static_cast<UINT64*>(ea), 8);
            out << "64|" << ea << "=" << x << '\n' << std::flush;
        }
        break;
        
      default:
        out << "" << dec << size * 8 << hex << "|" << ea << "=";
        ShowN(size,ea);
        out << '\n' << std::flush;
        break;
    }

    Flush();
}

VOID EmitRead(THREADID threadid, VOID * ea, UINT32 size)
{
    if (!Emit(threadid))
        return;
    
    out << "R|";

    switch(size)
    {
      case 0:
        out << "0" << '\n' << std::flush; // zero repeat count
        break;
        
      case 1:
        {
            UINT8 x;
            PIN_SafeCopy(&x,static_cast<UINT8*>(ea),1);
            out << "8|" << ea << "=" << static_cast<UINT32>(x) <<  '\n' << std::flush;
        }
        break;
        
      case 2:
        {
            UINT16 x;
            PIN_SafeCopy(&x,static_cast<UINT16*>(ea),2);
            out << "16|" << ea << "=" << x << '\n' << std::flush;
        }
        break;
        
      case 4:
        {
            UINT32 x;
            PIN_SafeCopy(&x,static_cast<UINT32*>(ea),4);
            out << "32|" << ea << "=" << x << '\n' << std::flush;
        }
        break;
        
      case 8:
        {
            UINT64 x;
            PIN_SafeCopy(&x,static_cast<UINT64*>(ea),8);
            out << "64|" << ea << "=" << x << '\n' << std::flush;
        }
        break;
        
      default:
        
		out << dec << size * 8 << hex << "|" << ea << "=";
		ShowN(size,ea);
		out << '\n' << std::flush;
        break;
    }

    Flush();
}

map<string, UINT32> compressedDLLs;
UINT32 countDLLs = 1;

map<string, UINT32> compressedRTNs;
UINT32 countRTNs = 1;

string FormatAddress(ADDRINT address, RTN rtn)
{
    string s = StringFromAddrint(address);
    
    if (KnobSymbols && RTN_Valid(rtn))
    {
		// dll file
		string filename = IMG_Valid(IMG_FindByAddress(address)) ? IMG_Name(IMG_FindByAddress(address)).c_str() : "";
		string show = "";
		if (compressedDLLs.find(filename) == compressedDLLs.end()) // not yet compressed
		{
			compressedDLLs[filename] = countDLLs;
			show = "@" + decstr(countDLLs) + "@" + filename;
			countDLLs++;
		}
		else
		{
			show = "@";
			show = show + decstr(compressedDLLs[filename]);
		}
		s += "|" + show;
		
		string routine = RTN_Name(rtn);
		show = "";
		if (compressedRTNs.find(routine) == compressedRTNs.end()) // not yet compressed
		{
			compressedRTNs[routine] = countRTNs;
			show = "@" + decstr(countRTNs) + "@" + routine;
			countRTNs++;
		}
		else
		{
			show = "@";
			show = show + decstr(compressedRTNs[routine]);
		}
		s += "|" + show;

        ADDRINT delta = address - RTN_Address(rtn);
        s += "|" + hexstr(delta, 4);
    }
	else
	{
		s += "|||";
	}
    return s;
}



VOID InstructionTrace(TRACE trace, INS ins)
{
	// if(startStopEnabled == 0) return;
	
    ADDRINT addr = INS_Address(ins);
    ASSERTX(addr);
            
    // Format the string at instrumentation time
    string traceString = FormatAddress(INS_Address(ins), TRACE_Rtn(trace)) + "|";
	traceString += decstr(PIN_ThreadId()) + "|" + INS_Disassemble(ins);

    INT32 regCount = 0;
    REG regs[20];
    REG xmm_dst = REG_INVALID();
      
    for (UINT32 i = 0; i < INS_MaxNumWRegs(ins); i++)
    {
        REG x = REG_FullRegName(INS_RegW(ins, i));
        
        if (REG_is_gr(x) || x == REG_EFLAGS)
        {
            regs[regCount] = x;
            regCount++;
        }
    }

    if (INS_HasFallThrough(ins))
    {
        AddEmit(ins, IPOINT_AFTER, traceString, regCount, regs);
    }
    if (INS_IsBranchOrCall(ins))
    {
        AddEmit(ins, IPOINT_TAKEN_BRANCH, traceString, regCount, regs);
    }
    if (xmm_dst != REG_INVALID()) 
    {
        if (INS_HasFallThrough(ins))
            AddXMMEmit(ins, IPOINT_AFTER, xmm_dst);
        if (INS_IsBranchOrCall(ins))
            AddXMMEmit(ins, IPOINT_TAKEN_BRANCH, xmm_dst);
    }
}

VOID MemoryTrace(INS ins)
{
	// if(startStopEnabled == 0) return;
	
    if (INS_IsMemoryWrite(ins))
    {
        INS_InsertCall(ins, IPOINT_BEFORE, AFUNPTR(CaptureWriteEa), IARG_THREAD_ID, IARG_MEMORYWRITE_EA, IARG_END);

        if (INS_HasFallThrough(ins))
        {
            INS_InsertPredicatedCall(ins, IPOINT_AFTER, AFUNPTR(EmitWrite), IARG_THREAD_ID, IARG_MEMORYWRITE_SIZE, IARG_END);
        }
        if (INS_IsBranchOrCall(ins))
        {
            INS_InsertPredicatedCall(ins, IPOINT_TAKEN_BRANCH, AFUNPTR(EmitWrite), IARG_THREAD_ID, IARG_MEMORYWRITE_SIZE, IARG_END);
        }
    }

    if (INS_HasMemoryRead2(ins))
    {
        INS_InsertPredicatedCall(ins, IPOINT_BEFORE, AFUNPTR(EmitRead), IARG_THREAD_ID, IARG_MEMORYREAD2_EA, IARG_MEMORYREAD_SIZE, IARG_END);
    }

    if (INS_IsMemoryRead(ins) && !INS_IsPrefetch(ins))
    {
        INS_InsertPredicatedCall(ins, IPOINT_BEFORE, AFUNPTR(EmitRead), IARG_THREAD_ID, IARG_MEMORYREAD_EA, IARG_MEMORYREAD_SIZE, IARG_END);
    }
}


typedef std::set<std::string> ImageWhitelist;
ImageWhitelist whitelist;

// static UINT64 icount = 0;
// VOID PIN_FAST_ANALYSIS_CALL docount(ADDRINT c) { icount += c; }
					// BBL_InsertCall(bbl, IPOINT_ANYWHERE, AFUNPTR(docount), IARG_FAST_ANALYSIS_CALL, IARG_UINT32, BBL_NumIns(bbl), IARG_END);



VOID Trace(TRACE trace, VOID *v)
{
    if (enabled && startStopEnabled)
    {
        for (BBL bbl = TRACE_BblHead(trace); BBL_Valid(bbl); bbl = BBL_Next(bbl))
        {
			string path = IMG_Valid(IMG_FindByAddress(BBL_Address(bbl))) ? IMG_Name(IMG_FindByAddress(BBL_Address(bbl))).c_str() : "";
			std::string::size_type last_slash = path.rfind('\\');
			std::string name;
			if (last_slash == std::string::npos) {
		    	// should not happend
				name = path;
			} else {
				name = path.substr(last_slash + 1);
			}
		  
            // out << "|img|" << name << "|\n" << std::flush;

			if (whitelist.find(name) != whitelist.end() || KnobModuleWhitelist.NumberOfValues() == 0 || name.empty()) {
	            for (INS ins = BBL_InsHead(bbl); INS_Valid(ins); ins = INS_Next(ins))
	            {
					
	                InstructionTrace(trace, ins);
	                MemoryTrace(ins);
					
	            }
			}
        }
    }
}



// LOCALFUN VOID Fini(int, VOID * v);

LOCALFUN VOID Fini(int, VOID * v)
{
	// out << "fini " << decstr(startStopEnabled);
    out.close();
}



LOCALVAR CONTROL control;



INSTLIB::ALARM_ICOUNT ialarmStart;

VOID HandlerStart(VOID * val, CONTEXT * ctxt, VOID * ip, THREADID tid)
{
	startStopEnabled = 1;
	// out << "started " << decstr(startStopEnabled);
}

INSTLIB::ALARM_ICOUNT ialarmStop;

VOID HandlerStop(VOID * val, CONTEXT * ctxt, VOID * ip, THREADID tid)
{
	startStopEnabled = 0;
	// out << "stopped " << decstr(startStopEnabled);
	PIN_Detach();
	// Fini(0, ip);
    // INSTLIB::ALARM_ICOUNT * al = static_cast<INSTLIB::ALARM_ICOUNT *>(val);
    // 
    // std::cout << "Alarm fired, resetting" << endl;
    // al->SetAlarm(50000, Handler, al);
}


int main(int argc, CHAR *argv[])
{
    PIN_InitSymbols();

    if( PIN_Init(argc,argv) )
    {
        return Usage();
    }

    string filename =  KnobOutputFile.Value();

    // Do this before we activate controllers
    out.open(filename.c_str());
    out << hex << right;
    out.setf(ios::showbase);
    
	for (UINT32 i = 0; i < KnobModuleWhitelist.NumberOfValues(); ++i) {
		whitelist.insert(KnobModuleWhitelist.Value(i));
	}
	
	UINT64 kstart = KnobStart.Value();
	UINT64 kstop = KnobStop.Value();
	
	if(kstart > 0) {
		// out << "setting start " << decstr(kstart);
		startStopEnabled = 0;
		ialarmStart.Activate();
	    ialarmStart.SetAlarm(kstart, HandlerStart, &ialarmStart);
	}

	if(kstop != 100000000) {
		// out << "setting stop " << decstr(kstop);
		ialarmStop.Activate();
		ialarmStop.SetAlarm(kstop, HandlerStop, &ialarmStop);
	}

	// out << "kstart " << decstr(kstart);
	// out << "\n";
	// out << "kstop " << decstr(kstop);
	// out << "\n";
	// out << "en " << decstr(startStopEnabled);
	// out << "\n";
	// out << std::flush;

    control.CheckKnobs(Handler, 0);
    
    TRACE_AddInstrumentFunction(Trace, 0);

    PIN_AddFiniFunction(Fini, 0);

    PIN_StartProgram();
    
    return 0;
}
