# source:
# http://ref.x86asm.net/#column_grp1_grp2_grp3
mnem2type = {
 'adc': ['arith', 'binary'], # gen
 'add': ['arith', 'binary'], # gen
 'addpd': ['pcksclr', 'arith'],
 'addps': ['simdfp', 'arith'],
 'addsd': ['pcksclr', 'arith'],
 'addss': ['simdfp', 'arith'],
 'addsubpd': ['simdfp', 'arith'],
 'addsubps': ['simdfp', 'arith'],
 'and': ['logical'], # gen
 'andnpd': ['pcksclr', 'logical'],
 'andnps': ['simdfp', 'logical'],
 'andpd': ['pcksclr', 'logical'],
 'andps': ['simdfp', 'logical'],
 'bsf': ['bit'], # gen
 'bsr': ['bit'], # gen
 'bswap': ['datamov'], # gen
 'bt': ['bit'], # gen
 'btc': ['bit'], # gen
 'btr': ['bit'], # gen
 'bts': ['bit'], # gen
 'call': ['branch', 'stack'], # gen
 'callf': ['branch', 'stack'], # gen
 'cbw': ['conver'], # gen
 'cdq': ['conver'], # gen
 'cdqe': ['conver'], # gen
 'clc': ['flgctrl'], # gen
 'cld': ['flgctrl'], # gen
 'clflush': ['cachect'],
 'cli': ['flgctrl'], # gen
 'clts': ['system'],
 'cmc': ['flgctrl'], # gen
 'cmova': ['datamov'], # gen
 'cmovae': ['datamov'], # gen
 'cmovb': ['datamov'], # gen
 'cmovbe': ['datamov'], # gen
 'cmovc': ['datamov'], # gen
 'cmove': ['datamov'], # gen
 'cmovg': ['datamov'], # gen
 'cmovge': ['datamov'], # gen
 'cmovl': ['datamov'], # gen
 'cmovle': ['datamov'], # gen
 'cmovna': ['datamov'], # gen
 'cmovnae': ['datamov'], # gen
 'cmovnb': ['datamov'], # gen
 'cmovnbe': ['datamov'], # gen
 'cmovnc': ['datamov'], # gen
 'cmovne': ['datamov'], # gen
 'cmovng': ['datamov'], # gen
 'cmovnge': ['datamov'], # gen
 'cmovnl': ['datamov'], # gen
 'cmovnle': ['datamov'], # gen
 'cmovno': ['datamov'], # gen
 'cmovnp': ['datamov'], # gen
 'cmovns': ['datamov'], # gen
 'cmovnz': ['datamov'], # gen
 'cmovo': ['datamov'], # gen
 'cmovp': ['datamov'], # gen
 'cmovpe': ['datamov'], # gen
 'cmovpo': ['datamov'], # gen
 'cmovs': ['datamov'], # gen
 'cmovz': ['datamov'], # gen
 'cmp': ['arith', 'binary'], # gen
 'cmppd': ['pcksclr', 'compar'],
 'cmpps': ['simdfp', 'compar'],
 'cmps': ['arith', 'string', 'binary'], # gen
 'cmpsb': ['arith', 'string', 'binary'], # gen
 'cmpsd': ['pcksclr', 'compar'],
 'cmpsq': ['arith', 'string', 'binary'], # gen
 'cmpss': ['simdfp', 'compar'],
 'cmpsw': ['arith', 'string', 'binary'], # gen
 'cmpxchg': ['datamov', 'arith', 'binary'], # gen
 'cmpxchg16b': ['datamov', 'arith', 'binary'], # gen
 'cmpxchg8b': ['datamov', 'arith', 'binary'], # gen
 'comisd': ['pcksclr', 'compar'],
 'comiss': ['simdfp', 'compar'],
 'cpuid': ['control'], # gen
 'cqo': ['conver'], # gen
 'cvtdq2pd': ['pcksclr', 'conver'],
 'cvtdq2ps': ['pcksp'],
 'cvtpd2dq': ['pcksclr', 'conver'],
 'cvtpd2pi': ['pcksclr', 'conver'],
 'cvtpd2ps': ['pcksclr', 'conver'],
 'cvtpi2pd': ['pcksclr', 'conver'],
 'cvtpi2ps': ['conver'],
 'cvtps2dq': ['pcksp'],
 'cvtps2pd': ['pcksclr', 'conver'],
 'cvtps2pi': ['conver'],
 'cvtsd2si': ['pcksclr', 'conver'],
 'cvtsd2ss': ['pcksclr', 'conver'],
 'cvtsi2sd': ['pcksclr', 'conver'],
 'cvtsi2ss': ['conver'],
 'cvtss2sd': ['pcksclr', 'conver'],
 'cvtss2si': ['conver'],
 'cvttpd2dq': ['pcksclr', 'conver'],
 'cvttpd2pi': ['pcksclr', 'conver'],
 'cvttps2dq': ['pcksp'],
 'cvttps2pi': ['conver'],
 'cvttsd2si': ['pcksclr', 'conver'],
 'cvttss2si': ['conver'],
 'cwd': ['conver'], # gen
 'cwde': ['conver'], # gen
 'dec': ['arith', 'binary'], # gen
 'div': ['arith', 'binary'], # gen
 'divpd': ['pcksclr', 'arith'],
 'divps': ['simdfp', 'arith'],
 'divsd': ['pcksclr', 'arith'],
 'divss': ['simdfp', 'arith'],
 'emms': ['x87fpu', 'control'],
 'enter': ['stack'], # gen
 'f2xm1': ['x87fpu'],
 'fabs': ['x87fpu', 'arith'],
 'fadd': ['x87fpu', 'arith'],
 'faddp': ['x87fpu', 'arith'],
 'fbld': ['x87fpu', 'datamov'],
 'fbstp': ['x87fpu', 'datamov'],
 'fchs': ['x87fpu', 'arith'],
 'fclex': ['x87fpu', 'control'],
 'fcmovb': ['x87fpu', 'datamov'],
 'fcmovbe': ['x87fpu', 'datamov'],
 'fcmove': ['x87fpu', 'datamov'],
 'fcmovnb': ['x87fpu', 'datamov'],
 'fcmovnbe': ['x87fpu', 'datamov'],
 'fcmovne': ['x87fpu', 'datamov'],
 'fcmovnu': ['x87fpu', 'datamov'],
 'fcmovu': ['x87fpu', 'datamov'],
 'fcom': ['x87fpu', 'compar'],
 'fcom2alias': ['x87fpu', 'compar'],
 'fcomi': ['x87fpu', 'compar'],
 'fcomip': ['x87fpu', 'compar'],
 'fcomp': ['x87fpu', 'compar'],
 'fcomp3alias': ['x87fpu', 'compar'],
 'fcomp5alias': ['x87fpu', 'compar'],
 'fcompp': ['x87fpu', 'compar'],
 'fcos': ['x87fpu'],
 'fdecstp': ['x87fpu', 'control'],
 'fdiv': ['x87fpu', 'arith'],
 'fdivp': ['x87fpu', 'arith'],
 'fdivr': ['x87fpu', 'arith'],
 'fdivrp': ['x87fpu', 'arith'],
 'ffree': ['x87fpu', 'control'],
 'ffreep': ['x87fpu', 'control'],
 'fiadd': ['x87fpu', 'arith'],
 'ficom': ['x87fpu', 'compar'],
 'ficomp': ['x87fpu', 'compar'],
 'fidiv': ['x87fpu', 'arith'],
 'fidivr': ['x87fpu', 'arith'],
 'fild': ['x87fpu', 'datamov'],
 'fimul': ['x87fpu', 'arith'],
 'fincstp': ['x87fpu', 'control'],
 'finit': ['x87fpu', 'control'],
 'fist': ['x87fpu', 'datamov'],
 'fistp': ['x87fpu', 'datamov'],
 'fisttp': ['x87fpu', 'conver'],
 'fisub': ['x87fpu', 'arith'],
 'fisubr': ['x87fpu', 'arith'],
 'fld': ['x87fpu', 'datamov'],
 'fld1': ['x87fpu', 'ldconst'],
 'fldcw': ['x87fpu', 'control'],
 'fldenv': ['x87fpu', 'control'],
 'fldl2e': ['x87fpu', 'ldconst'],
 'fldl2t': ['x87fpu', 'ldconst'],
 'fldlg2': ['x87fpu', 'ldconst'],
 'fldln2': ['x87fpu', 'ldconst'],
 'fldpi': ['x87fpu', 'ldconst'],
 'fldz': ['x87fpu', 'ldconst'],
 'fmul': ['x87fpu', 'arith'],
 'fmulp': ['x87fpu', 'arith'],
 'fnclex': ['x87fpu', 'control'],
 'fndisinop': ['obsol', 'control'],
 'fneninop': ['obsol', 'control'],
 'fninit': ['x87fpu', 'control'],
 'fnop': ['x87fpu', 'control'],
 'fnsave': ['x87fpu', 'control'],
 'fnsetpmnop': ['obsol', 'control'],
 'fnstcw': ['x87fpu', 'control'],
 'fnstenv': ['x87fpu', 'control'],
 'fnstsw': ['x87fpu', 'control'],
 'fpatan': ['x87fpu'],
 'fprem': ['x87fpu', 'arith'],
 'fprem1': ['x87fpu', 'arith'],
 'fptan': ['x87fpu'],
 'frndint': ['x87fpu', 'arith'],
 'frstor': ['x87fpu', 'control'],
 'fs': ['prefix', 'segreg'],
 'fsave': ['x87fpu', 'control'],
 'fscale': ['x87fpu', 'arith'],
 'fsin': ['x87fpu'],
 'fsincos': ['x87fpu'],
 'fsqrt': ['x87fpu', 'arith'],
 'fst': ['x87fpu', 'datamov'],
 'fstcw': ['x87fpu', 'control'],
 'fstenv': ['x87fpu', 'control'],
 'fstp': ['x87fpu', 'datamov'],
 'fstp1partalias': ['x87fpu', 'datamov'],
 'fstp8alias': ['x87fpu', 'datamov'],
 'fstp9alias': ['x87fpu', 'datamov'],
 'fstsw': ['x87fpu', 'control'],
 'fsub': ['x87fpu', 'arith'],
 'fsubp': ['x87fpu', 'arith'],
 'fsubr': ['x87fpu', 'arith'],
 'fsubrp': ['x87fpu', 'arith'],
 'ftst': ['x87fpu', 'compar'],
 'fucom': ['x87fpu', 'compar'],
 'fucomi': ['x87fpu', 'compar'],
 'fucomip': ['x87fpu', 'compar'],
 'fucomp': ['x87fpu', 'compar'],
 'fucompp': ['x87fpu', 'compar'],
 'fwait': ['x87fpu', 'control'],
 'fxam': ['x87fpu'],
 'fxch': ['x87fpu', 'datamov'],
 'fxch4alias': ['x87fpu', 'datamov'],
 'fxch7alias': ['x87fpu', 'datamov'],
 'fxrstor': ['sm'],
 'fxsave': ['sm'],
 'fxtract': ['x87fpu', 'arith'],
 'fyl2x': ['x87fpu'],
 'fyl2xp1': ['x87fpu'],
 'gs': ['prefix', 'segreg'],
 'haddpd': ['simdfp', 'arith'],
 'haddps': ['simdfp', 'arith'],
 'hlt': ['system'],
 'hsubpd': ['simdfp', 'arith'],
 'hsubps': ['simdfp', 'arith'],
 'icebppartalias7': ['break', 'stack'], # gen
 'idiv': ['arith', 'binary'], # gen
 'imul': ['arith', 'binary'], # gen
 'in': ['inout'], # gen
 'inc': ['arith', 'binary'], # gen
 'ins': ['inout', 'string'], # gen
 'insb': ['inout', 'string'], # gen
 'insd': ['inout', 'string'], # gen
 'insw': ['inout', 'string'], # gen
 'int': ['break', 'stack'], # gen
 'int1partalias7': ['break', 'stack'], # gen
 'into': ['break', 'stack'], # gen
 'invd': ['system'],
 'invlpg': ['system'],
 'iret': ['break', 'stack'], # gen
 'iretd': ['break', 'stack'], # gen
 'iretq': ['break', 'stack'], # gen
 'ja': ['branch', 'cond'], # gen
 'jae': ['branch', 'cond'], # gen
 'jb': ['branch', 'cond'], # gen
 'jbe': ['branch', 'cond'], # gen
 'jc': ['branch', 'cond'], # gen
 'je': ['branch', 'cond'], # gen
 'jecxz': ['branch', 'cond'], # gen
 'jg': ['branch', 'cond'], # gen
 'jge': ['branch', 'cond'], # gen
 'jl': ['branch', 'cond'], # gen
 'jle': ['branch', 'cond'], # gen
 'jmp': ['branch'], # gen
 'jmpe': ['system', 'branch'],
 'jmpf': ['branch'], # gen
 'jna': ['branch', 'cond'], # gen
 'jnae': ['branch', 'cond'], # gen
 'jnb': ['branch', 'cond'], # gen
 'jnbe': ['branch', 'cond'], # gen
 'jnc': ['branch', 'cond'], # gen
 'jne': ['branch', 'cond'], # gen
 'jng': ['branch', 'cond'], # gen
 'jnge': ['branch', 'cond'], # gen
 'jnl': ['branch', 'cond'], # gen
 'jnle': ['branch', 'cond'], # gen
 'jno': ['branch', 'cond'], # gen
 'jnp': ['branch', 'cond'], # gen
 'jns': ['branch', 'cond'], # gen
 'jnz': ['branch', 'cond'], # gen
 'jo': ['branch', 'cond'], # gen
 'jp': ['branch', 'cond'], # gen
 'jpe': ['branch', 'cond'], # gen
 'jpo': ['branch', 'cond'], # gen
 'jrcxz': ['branch', 'cond'], # gen
 'js': ['branch', 'cond'], # gen
 'jz': ['branch', 'cond'], # gen
 'lahf': ['datamov', 'flgctrl'], # gen
 'lar': ['system'],
 'lddqu': ['cachect'],
 'ldmxcsr': ['mxcsrsm'],
 'lea': ['datamov'], # gen
 'leave': ['stack'], # gen
 'lfence': ['order'],
 'lfs': ['datamov', 'segreg'], # gen
 'lgdt': ['system'],
 'lgs': ['datamov', 'segreg'], # gen
 'lidt': ['system'],
 'lldt': ['system'],
 'lmsw': ['system'],
 'lock': ['prefix'],
 'lods': ['datamov', 'string'], # gen
 'lodsb': ['datamov', 'string'], # gen
 'lodsd': ['datamov', 'string'], # gen
 'lodsq': ['datamov', 'string'], # gen
 'lodsw': ['datamov', 'string'], # gen
 'loop': ['branch', 'cond'], # gen
 'loope': ['branch', 'cond'], # gen
 'loopne': ['branch', 'cond'], # gen
 'loopnz': ['branch', 'cond'], # gen
 'loopz': ['branch', 'cond'], # gen
 'lsl': ['system'],
 'lss': ['datamov', 'segreg'], # gen
 'ltr': ['system'],
 'maskmovdqu': ['cachect'],
 'maskmovq': ['cachect'],
 'maxpd': ['pcksclr', 'arith'],
 'maxps': ['simdfp', 'arith'],
 'maxsd': ['pcksclr', 'arith'],
 'maxss': ['simdfp', 'arith'],
 'mfence': ['order'],
 'minpd': ['pcksclr', 'arith'],
 'minps': ['simdfp', 'arith'],
 'minsd': ['pcksclr', 'arith'],
 'minss': ['simdfp', 'arith'],
 'monitor': ['sync'],
 'mov': ['datamov'], # system
 'movapd': ['pcksclr', 'datamov'],
 'movaps': ['simdfp', 'datamov'],
 'movd': ['datamov'],
 'movddup': ['simdfp', 'datamov'],
 'movdq2q': ['simdint', 'datamov'],
 'movdqa': ['simdint', 'datamov'],
 'movdqu': ['simdint', 'datamov'],
 'movhlps': ['simdfp', 'datamov'],
 'movhpd': ['pcksclr', 'datamov'],
 'movhps': ['simdfp', 'datamov'],
 'movlhps': ['simdfp', 'datamov'],
 'movlpd': ['pcksclr', 'datamov'],
 'movlps': ['simdfp', 'datamov'],
 'movmskpd': ['pcksclr', 'datamov'],
 'movmskps': ['simdfp', 'datamov'],
 'movntdq': ['cachect'],
 'movnti': ['cachect'],
 'movntpd': ['cachect'],
 'movntps': ['cachect'],
 'movntq': ['cachect'],
 'movq': ['datamov'],
 'movq2dq': ['simdint', 'datamov'],
 'movs': ['datamov', 'string'], # gen
 'movsb': ['datamov', 'string'], # gen
 'movsd': ['pcksclr', 'datamov'],
 'movshdup': ['simdfp', 'datamov'],
 'movsldup': ['simdfp', 'datamov'],
 'movsq': ['datamov', 'string'], # gen
 'movss': ['simdfp', 'datamov'],
 'movsw': ['datamov', 'string'], # gen
 'movsx': ['conver'], # gen
 'movsxd': ['conver'], # gen
 'movupd': ['pcksclr', 'datamov'],
 'movups': ['simdfp', 'datamov'],
 'movzx': ['conver'], # gen
 'mul': ['arith', 'binary'], # gen
 'mulpd': ['pcksclr', 'arith'],
 'mulps': ['simdfp', 'arith'],
 'mulsd': ['pcksclr', 'arith'],
 'mulss': ['simdfp', 'arith'],
 'mwait': ['sync'],
 'neg': ['arith', 'binary'], # gen
 'nop': ['control'], # gen
 'not': ['logical'], # gen
 'or': ['logical'], # gen
 'orpd': ['pcksclr', 'logical'],
 'orps': ['simdfp', 'logical'],
 'out': ['inout'], # gen
 'outs': ['inout', 'string'], # gen
 'outsb': ['inout', 'string'], # gen
 'outsd': ['inout', 'string'], # gen
 'outsw': ['inout', 'string'], # gen
 'pabsb': ['simdint'],
 'pabsd': ['simdint'],
 'pabsw': ['simdint'],
 'packssdw': ['conver'],
 'packsswb': ['conver'],
 'packuswb': ['conver'],
 'paddb': ['arith'],
 'paddd': ['arith'],
 'paddq': ['simdint', 'arith'],
 'paddsb': ['arith'],
 'paddsw': ['arith'],
 'paddusb': ['arith'],
 'paddusw': ['arith'],
 'paddw': ['arith'],
 'palignr': ['simdint'],
 'pand': ['logical'],
 'pandn': ['logical'],
 'pause': ['cachect'],
 'pavgb': ['simdint'],
 'pavgw': ['simdint'],
 'pcmpeqb': ['compar'],
 'pcmpeqd': ['compar'],
 'pcmpeqw': ['compar'],
 'pcmpgtb': ['compar'],
 'pcmpgtd': ['compar'],
 'pcmpgtw': ['compar'],
 'pextrw': ['simdint', 'word'],
 'phaddd': ['simdint'],
 'phaddsw': ['simdint'],
 'phaddw': ['simdint'],
 'phsubd': ['simdint'],
 'phsubsw': ['simdint'],
 'phsubw': ['simdint'],
 'pinsrw': ['simdint', 'word'],
 'pmaddubsw': ['simdint'],
 'pmaddwd': ['arith'],
 'pmaxsw': ['simdint'],
 'pmaxub': ['simdint'],
 'pminsw': ['simdint'],
 'pminub': ['simdint'],
 'pmovmskb': ['simdint'],
 'pmulhrsw': ['simdint'],
 'pmulhuw': ['simdint'],
 'pmulhw': ['arith'],
 'pmullw': ['arith'],
 'pmuludq': ['simdint', 'arith'],
 'pop': ['stack', 'segreg'], # gen
 'popf': ['stack', 'flgctrl'], # gen
 'popfq': ['stack', 'flgctrl'], # gen
 'por': ['logical'],
 'prefetchnta': ['fetch'],
 'prefetcht0': ['fetch'],
 'prefetcht1': ['fetch'],
 'prefetcht2': ['fetch'],
 'psadbw': ['simdint'],
 'pshufb': ['simdint'],
 'pshufd': ['simdint', 'shunpck'],
 'pshufhw': ['simdint', 'shunpck'],
 'pshuflw': ['simdint', 'shunpck'],
 'pshufw': ['simdint'],
 'psignb': ['simdint'],
 'psignd': ['simdint'],
 'psignw': ['simdint'],
 'pslld': ['shift'],
 'pslldq': ['simdint', 'shift'],
 'psllq': ['shift'],
 'psllw': ['shift'],
 'psrad': ['shift'],
 'psraw': ['shift'],
 'psrld': ['shift'],
 'psrldq': ['simdint', 'shift'],
 'psrlq': ['shift'],
 'psrlw': ['shift'],
 'psubb': ['arith'],
 'psubd': ['arith'],
 'psubq': ['simdint', 'arith'],
 'psubsb': ['arith'],
 'psubsw': ['arith'],
 'psubusb': ['arith'],
 'psubusw': ['arith'],
 'psubw': ['arith'],
 'punpckhbw': ['unpack'],
 'punpckhdq': ['unpack'],
 'punpckhqdq': ['simdint', 'shunpck'],
 'punpckhwd': ['unpack'],
 'punpcklbw': ['unpack'],
 'punpckldq': ['unpack'],
 'punpcklqdq': ['simdint', 'shunpck'],
 'punpcklwd': ['unpack'],
 'push': ['stack', 'segreg'], # gen
 'pushf': ['stack', 'flgctrl'], # gen
 'pushfq': ['stack', 'flgctrl'], # gen
 'pxor': ['logical'],
 'rcl': ['shftrot'], # gen
 'rcpps': ['simdfp', 'arith'],
 'rcpss': ['simdfp', 'arith'],
 'rcr': ['shftrot'], # gen
 'rdmsr': ['system'],
 'rdpmc': ['system'],
 'rdtsc': ['system'],
 'rep': ['prefix', 'string'],
 'repe': ['prefix', 'string'],
 'repne': ['prefix', 'string'],
 'repnz': ['prefix', 'string'],
 'repz': ['prefix', 'string'],
 'retf': ['branch', 'stack'], # gen
 'retn': ['branch', 'stack'], # gen
 'ret': ['branch', 'stack'], # MANUAL
 'rex': ['prefix'],
 'rex.b': ['prefix'],
 'rex.r': ['prefix'],
 'rex.rb': ['prefix'],
 'rex.rx': ['prefix'],
 'rex.rxb': ['prefix'],
 'rex.w': ['prefix'],
 'rex.wb': ['prefix'],
 'rex.wr': ['prefix'],
 'rex.wrb': ['prefix'],
 'rex.wrx': ['prefix'],
 'rex.wrxb': ['prefix'],
 'rex.wx': ['prefix'],
 'rex.wxb': ['prefix'],
 'rex.x': ['prefix'],
 'rex.xb': ['prefix'],
 'rol': ['shftrot'], # gen
 'ror': ['shftrot'], # gen
 'rsm': ['system', 'branch'],
 'rsqrtps': ['simdfp', 'arith'],
 'rsqrtss': ['simdfp', 'arith'],
 'sahf': ['datamov', 'flgctrl'], # gen
 'sal': ['shftrot'], # gen
 'salalias': ['shftrot'], # gen
 'sar': ['shftrot'], # gen
 'sbb': ['arith', 'binary'], # gen
 'scas': ['arith', 'string', 'binary'], # gen
 'scasb': ['arith', 'string', 'binary'], # gen
 'scasd': ['arith', 'string', 'binary'], # gen
 'scasq': ['arith', 'string', 'binary'], # gen
 'scasw': ['arith', 'string', 'binary'], # gen
 'seta': ['datamov'], # gen
 'setae': ['datamov'], # gen
 'setb': ['datamov'], # gen
 'setbe': ['datamov'], # gen
 'setc': ['datamov'], # gen
 'sete': ['datamov'], # gen
 'setg': ['datamov'], # gen
 'setge': ['datamov'], # gen
 'setl': ['datamov'], # gen
 'setle': ['datamov'], # gen
 'setna': ['datamov'], # gen
 'setnae': ['datamov'], # gen
 'setnb': ['datamov'], # gen
 'setnbe': ['datamov'], # gen
 'setnc': ['datamov'], # gen
 'setne': ['datamov'], # gen
 'setng': ['datamov'], # gen
 'setnge': ['datamov'], # gen
 'setnl': ['datamov'], # gen
 'setnle': ['datamov'], # gen
 'setno': ['datamov'], # gen
 'setnp': ['datamov'], # gen
 'setns': ['datamov'], # gen
 'setnz': ['datamov'], # gen
 'seto': ['datamov'], # gen
 'setp': ['datamov'], # gen
 'setpe': ['datamov'], # gen
 'setpo': ['datamov'], # gen
 'sets': ['datamov'], # gen
 'setz': ['datamov'], # gen
 'sfence': ['order'],
 'sgdt': ['system'],
 'shl': ['shftrot'], # gen
 'shlalias': ['shftrot'], # gen
 'shld': ['shftrot'], # gen
 'shr': ['shftrot'], # gen
 'shrd': ['shftrot'], # gen
 'shufpd': ['pcksclr', 'shunpck'],
 'shufps': ['simdfp', 'shunpck'],
 'sidt': ['system'],
 'sldt': ['system'],
 'smsw': ['system'],
 'sqrtpd': ['pcksclr', 'arith'],
 'sqrtps': ['simdfp', 'arith'],
 'sqrtsd': ['pcksclr', 'arith'],
 'sqrtss': ['simdfp', 'arith'],
 'stc': ['flgctrl'], # gen
 'std': ['flgctrl'], # gen
 'sti': ['flgctrl'], # gen
 'stmxcsr': ['mxcsrsm'],
 'stos': ['datamov', 'string'], # gen
 'stosb': ['datamov', 'string'], # gen
 'stosd': ['datamov', 'string'], # gen
 'stosq': ['datamov', 'string'], # gen
 'stosw': ['datamov', 'string'], # gen
 'str': ['system'],
 'sub': ['arith', 'binary'], # gen
 'subpd': ['pcksclr', 'arith'],
 'subps': ['simdfp', 'arith'],
 'subsd': ['pcksclr', 'arith'],
 'subss': ['simdfp', 'arith'],
 'swapgs': ['system'],
 'syscall': ['system', 'branch'],
 'sysenter': ['system', 'branch'],
 'sysexit': ['system', 'branch'],
 'sysret': ['system', 'branch'],
 'test': ['logical'], # gen
 'testalias': ['logical'], # gen
 'ucomisd': ['pcksclr', 'compar'],
 'ucomiss': ['simdfp', 'compar'],
 'ud': ['control'], # gen
 'ud2': ['control'], # gen
 'unpckhpd': ['pcksclr', 'shunpck'],
 'unpckhps': ['simdfp', 'shunpck'],
 'unpcklpd': ['pcksclr', 'shunpck'],
 'unpcklps': ['simdfp', 'shunpck'],
 'verr': ['system'],
 'verw': ['system'],
 'wait': ['x87fpu', 'control'],
 'wbinvd': ['system'],
 'wrmsr': ['system'],
 'xadd': ['datamov', 'arith', 'binary'], # gen
 'xchg': ['datamov'], # gen
 'xlat': ['datamov'], # gen
 'xlatb': ['datamov'], # gen
 'xor': ['logical'], # gen
 'xorpd': ['pcksclr', 'logical'],
 'xorps': ['simdfp', 'logical']
}

type2descr = {
 'arith' : 'arithmetic', #!!
 'binary' : 'binary arithmetic', #!!
 'bit' : 'bit manipulation', #!!
 'branch' : 'branch',
 'break' : 'interrupt',
 'cachect' : 'cacheability control',
 'compar' : 'comparison',
 'cond' : 'conditional',
 'control' : 'control',
 'conver' : 'type conversion instructions',
 'datamov' : 'data movement',
 'fetch' : 'prefetch',
 'flgctrl' : 'flag control',
 'gen' : 'general',
 'inout' : 'I/O',
 'ldconst' : 'load constant',
 'logical' : 'logical', #!!
 'mxcsrsm' : 'MXCSR state management', # sse1
 'order' : 'instruction ordering',
 'pcksclr' : 'packed and scalar double-precision floating-point', # sse2
 'pcksp' : 'packed single-precision floating-point', # sse2
 'prefix' : 'prefix',
 'segreg' : 'segment register manipulation',
 'shftrot' : 'shift&rotate', #!!
 'shift' : 'shifting', # mmx/sse2
 'stack' : 'stack instruction',
 'string' : 'string instruction',
 'sync' : 'agent synchronization', # sse3
 'unpack' : 'unpacking', # mmx/sse1/sse2
 'word' : 'WORD operation', # sse1
 'shunpck' : 'shuffle&unpacking', # sse1/2
 'simdfp' : 'SIMD single-precision floating-point (SIMD packed)', # sse1/sse3
 'simdint' : '64/128-bit SIMD integer', # ssse3 only
 'sm' : 'x87 FPU and SIMD state management', # x87fpu only
 'system' : 'system-related instruction',
 'x87fpu' : 'x87 FPU'
}

# These columns are present only in geek's editions.
# They classifies the instruction among groups.
# These groups don't match the instruction groups given by the Intel manual
# (I found them too loose). One instruction may fit into more groups.
# 
#    1. prefix
#          1. segreg segment register
#          2. branch
#                1. cond conditional
#          3. x87fpu
#                1. control (only WAIT)
#    2. obsol obsolete
#          1. control
#    3. gen general
#          1. datamov data movement
#          2. stack
#          3. conver type conversion
#          4. arith arithmetic
#                1. binary
#                2. decimal
#          5. logical
#          6. shftrot shift&rotate
#          7. bit bit manipulation
#          8. branch
#                1. cond conditional
#          9. break interrupt
#         10. string
#         11. inout I/O
#         12. flgctrl flag control
#         13. segreg segment register manipulation
#         14. control
#    4. system
#          1. branch
#                1. trans transitional (implies sensitivity to operand-size attribute)
#    5. x87fpu x87 FPU
#          1. datamov data movement
#          2. arith basic arithmetic
#          3. compar comparison
#          4. trans transcendental
#          5. ldconst load constant
#          6. control
#          7. conv conversion
#    6. sm x87 FPU and SIMD state management
# 
# MMX instruction extensions technology groups
# 
#    1. datamov data movement
#    2. arith packed arithmetic
#    3. compar comparison
#    4. conver conversion
#    5. logical
#    6. shift
#    7. unpack unpacking
# 
# SSE1 instruction extensions groups
# 
#    1. simdfp SIMD single-precision floating-point
#          1. datamov data movement
#          2. arith packed arithmetic
#          3. compar comparison
#          4. logical
#          5. shunpck shuffle&unpacking
#    2. conver conversion instructions
#    3. simdint 64-bit SIMD integer
#          1. word WORD operation
#    4. mxcsrsm MXCSR state management
#    5. cachect cacheability control
#    6. fetch prefetch
#    7. order instruction ordering
# 
# SSE2 instruction extensions groups:
# 
#    1. pcksclr packed and scalar double-precision floating-point
#          1. datamov data movement
#          2. conver conversion
#          3. arith packed arithmetic
#          4. compar comparison
#          5. logical
#          6. shunpck shuffle&unpacking
#    2. pcksp packed single-precision floating-point
#    3. simdint 128-bit SIMD integer
#          1. datamov data movement
#          2. arith packed arithmetic
#          3. shunpck shuffle&unpacking
#          4. shift
#    4. cachect cacheability control
#    5. order instruction ordering
# 
# SSE3 instruction extensions groups:
# 
#    1. simdfp SIMD single-precision floating-point (SIMD packed)
#          1. datamov data movement
#          2. arith packed arithmetic
#    2. cachect cacheability control
#    3. sync agent synchronization
# 
# SSSE3 instruction extensions group:
# 
#    1. simdint SIMD integer

def ins2type(mnemonic):
    try:
        return mnem2type[mnemonic]
    except KeyError:
        return ['unknown']
def type2desc(type):
    try:
        return type2desc[type]
    except KeyError:
        return 'unknown type'
    