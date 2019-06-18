import os
import subprocess
import matplotlib.pyplot as plt

max_N = 8

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



programs = list(range(2,max_N))
pbs = []
sbs = []
for ts in programs:
	df = ts
	SB = str(run_nidhugg("readerswriters.c","SB",-1, df))
	PB = str(run_nidhugg("readerswriters.c","PB",-1, df))
	pbs.append(PB)
	sbs.append(SB)

plt.figure()
plt.title("Number of traces for readerswriters")
x = list(range(2,max_N))
plt.plot(x,sbs, label='Source-DPOR')
plt.plot(x,pbs, label='DPOR')
plt.legend()
plt.draw()
plt.savefig('wNr.png')
		
		

