import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib.cm as cm

max_N = 6
max_B = 4

def count_total_traces(cmd):
	command = cmd
	output = subprocess.getoutput(command)
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
fig = plt.figure(figsize=(4,4))
# st = fig.suptitle("Impact of bound for various numbers N of readers.\n x: Number of readers, y: Number of traces", y=1.08)

for ts in programs:
    pbs = []
    sbs = []
    vans = []
    ax = fig.add_subplot(max_N-1,1,ts-1)
    df = ts
    for b in range(0,max_B):
        Van = str(run_nidhugg("readerswriters.c","S",b, df))
        SB = str(run_nidhugg("readerswriters.c","SB",b, df))
        PB = str(run_nidhugg("readerswriters.c","L",b, df))
        vans.append(Van)
        pbs.append(PB)
        sbs.append(SB)

    plt.subplot(220+ts-1)
    x = list(range(0,max_B))
    plt.title("N=%d"%ts)
    plt.plot(x,vans, label='Naive-BPOR')
    plt.plot(x,sbs, label='Nidhugg-BPOR')
    plt.plot(x,pbs, label='Lazy-BPOR')

fig.tight_layout()
# st.set_y(0.95)
# fig.subplots_adjust(top=0.85)
# plt.legend()

plt.legend(loc='upper center', bbox_to_anchor=(0.0, -0.3), ncol=5)
plt.savefig('wNrLB.png',bbox_inches='tight')

