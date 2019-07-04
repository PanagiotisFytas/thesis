#!/usr/bin/python3


import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from matplotlib.legend_handler import HandlerLine2D



def plot(name):
    fl1 = name + '.txt'

    schedulers = []
    times = []
    speedup = []

    with open(fl1) as f:
        for line in f:
            lin = line.split()
            print(lin)
            schedulers.append(int(lin[0]))
            times.append(float(lin[1]))
            speedup.append(times[0]/float(lin[1]))
            

    # TIME

    plt.xlabel('Schedulers')
    plt.ylabel('Time (sec)')
    #plt.title('$\lambda$ = ' + str(l) + ' clients/sec, k = ' + str(k) + ' clients/sec')
    plt.plot(np.array(schedulers), np.array(times), 'b')
    plt.plot(np.array(schedulers), np.array(times), 'bx')
    line1, = plt.plot(np.array(schedulers), np.array(times), label=name)
    plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)}, loc=1)
    plt.savefig(name + '_time.png')
    plt.close()

    # Speedup

    plt.xlabel('Schedulers')
    plt.ylabel('Speedup')
    #plt.title('$\lambda$ = ' + str(l) + ' clients/sec, k = ' + str(k) + ' clients/sec')
    plt.plot(np.array(schedulers), np.array(speedup), 'b')
    plt.plot(np.array(schedulers), np.array(speedup), 'bx')
    line1, = plt.plot(np.array(schedulers), np.array(speedup), label=name)
    plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)}, loc=2)
    plt.savefig(name + '_speedup.png')
    plt.close()
    return

def plots(fls):
    i = 0
    schedulers = [[], [], []]
    times = [[], [], []]
    speedup = [[], [], []]
    for fl in fls:
        flt = fl + '.txt'

        with open(flt) as f:
            for line in f:
                lin = line.split()
                print(lin)
                schedulers[i].append(int(lin[0]))
                times[i].append(float(lin[1]))
                speedup[i].append(times[i][0]/float(lin[1]))
        i += 1
 # Speedup

    plt.xlabel('Schedulers')
    plt.ylabel('Speedup')
    #plt.title('$\lambda$ = ' + str(l) + ' clients/sec, k = ' + str(k) + ' clients/sec')
    plt.plot(np.array(schedulers[0]), np.array(speedup[0]), 'bx')
    plt.plot(np.array(schedulers[1]), np.array(speedup[1]), 'gx')
    plt.plot(np.array(schedulers[2]), np.array(speedup[2]), 'rx')
    line1, = plt.plot(np.array(schedulers[0]), np.array(speedup[0]), label=fls[0])
    line2, = plt.plot(np.array(schedulers[1]), np.array(speedup[1]), label=fls[1])
    line3, = plt.plot(np.array(schedulers[2]), np.array(speedup[2]), label=fls[2])
    plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)}, loc=2)
    plt.tight_layout()
    plt.savefig('allspeedup.png')
    plt.close()
    return

def stackplots(name, algo):
    fl1 = name + '_' + algo +'.txt'


    schedulers = []
    be = []
    oc = []
    done = []

    with open(fl1) as f:
        for line in f:
            lin = line.split()
            print(lin)
            schedulers.append(int(lin[0]))
            be.append(int(lin[1]))
            oc.append(int(lin[2]))
            done.append(int(lin[3]))

    print (len(schedulers), len(be), len(oc) ,len(done))
    y = np.vstack([be, oc, done])

    fig, ax = plt.subplots()
    ax.stackplot(schedulers, be, oc, done, labels=['Budget Exceeded', 'Disputed Entry Found', 'Finished'], colors=['darkblue','r','g'])
    ax.legend(loc='upper left')
    plt.xlabel('Schedulers')
    plt.savefig(name + '_' + algo + '_stack.png')
    
    plt.show()
    # fig, ax = plt.subplots()
    # ax.stackplot(x, y)
    # plt.show()
    plt.close()

if __name__ == "__main__":
        plot('indexer15')
        plot('readers15')
        plot('lastzero11')
        plots(['indexer15', 'readers15', 'lastzero11'])
        plot('readers10')