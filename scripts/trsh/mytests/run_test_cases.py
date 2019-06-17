import os
import subprocess
import matplotlib.pyplot as plt

max_N = 7
max_B = 4


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


print("\\begin{center}")
print("\\begin{tabular}{ |c|c|c| }")
print("\\hline")
print("Test case & Traces for Source-DPOR & Traces for Classic-DPOR \\\\")
print("\\hline \\hline")

programs = [("account.c",), ("lazy.c",),("micro.c",), ("lastzero.c",5), ("lastzeromod.ll",), ("indexer0.c",12), ("indexermod.c",5)]

for ts in programs:
	df = -1
	if len(ts)>1 :
		df = ts[1]
	SB = str(run_nidhugg(ts[0],"SB",-1, df))
	PB = str(run_nidhugg(ts[0],"PB",-1, df))
	print(ts[0] + " & " + SB + " & " + PB + "\\\\")	
	print("\\hline")

print("\\end{tabular}")
print("\\end{center}")

