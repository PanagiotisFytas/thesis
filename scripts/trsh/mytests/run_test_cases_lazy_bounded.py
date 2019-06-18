import os
import subprocess
import matplotlib.pyplot as plt

max_N = 7
max_B = 3


def count_total_traces(cmd):
	command = cmd 
	output = subprocess.getoutput(command)
	#print(output)
	output = output.split()
	index = output.index("count:") + 1
	count = int(output[index])
	sleep_set_blocked = int(output[index+2])
	total = count+ sleep_set_blocked
	#print(cmd)
	#print(total)
	return total

def run_nidhugg(program,mode,bound,define=-1):
	#print(program)
	df = ""
	nidhugg = "nidhuggc"
	if define >= 0:
		df = ("-DN=%d -- " % define)
	if ".ll" in program:
		nidhugg = "nidhugg"

	return count_total_traces(nidhugg + " " + df + " --sc --preemption-bounding=%s --bound=%d " %(mode,bound) + program )

begin_tabular = "\\begin{tabular}{ |c|" + 3*max_B*"c|" + "}"

print("\\begin{center}")
print(begin_tabular)
print("\\hline")
#print("Test case & Vanilla-BPOR & BPOR & Source-BPOR \\\\")
multicol = "\\multicolumn{1}{|c|}{Technique:} & \\multicolumn{" + str(max_B) + "}{c|}{Vanilla-BPOR} & \\multicolumn{" + str(max_B) + "}{c|}{Lazy-BPOR} & \\multicolumn{"+ str(max_B) + "}{c|}{BPOR} \\\\"
print(multicol)
print("\\hline")
bound_line = (" & ").join(3*[str(i) for i in range(0,max_B)])
print("Bound: & " + bound_line + " \\\\")
print("\\hline \\hline")

programs = [("account.c",), ("lazy.c",),("micro.c",), ("lastzero.c",5), ("lastzeromod.ll",), ("indexer0.c",12), ("indexermod.c",5)]
#programs = [("account.c",),("lazy.c",)]

for ts in programs:
	df = -1
	if len(ts)>1 :
		df = ts[1]
	print(ts[0],end='')
	for b in range(0,max_B):
		Van = str(run_nidhugg(ts[0],"S",b,df))
		print(' & ' + Van, end='')
	for b in range(0,max_B):
		SB = str(run_nidhugg(ts[0],"L",b, df))
		print(' & ' + SB, end='')
	for b in range(0,max_B):
		PB = str(run_nidhugg(ts[0],"PB",b, df))
		print(' & ' + PB, end='')
	print(" \\\\")	
		
	print("\\hline")

print("\\end{tabular}")
print("\\end{center}")		
		
		

