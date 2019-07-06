#!/usr/bin/python3


import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from matplotlib.legend_handler import HandlerLine2D
from matplotlib import ticker



def plot(test, N, B):
    fl1 = test + '_' + N + '_' + B + '_source.txt'
    fl2 = test + '_' + N + '_' + B + '_optimal.txt'
    name = test + ' ' + N
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
    
    schedulers2 = []
    times2 = []
    speedup2 = []

    with open(fl2) as f:
        for line in f:
            lin = line.split()
            print(lin)
            schedulers2.append(int(lin[0]))
            times2.append(float(lin[1]))
            speedup2.append(times2[0]/float(lin[1]))

    # TIME
    f, axs = plt.subplots(1,2,figsize=(12,5))
    plt.subplot(1,2,1)

    plt.xlabel('Schedulers')
    plt.ylabel('Time (sec)')
    # plt.title(name + ' ' + N + ', Budget = ' + B)
    #plt.title('$\lambda$ = ' + str(l) + ' clients/sec, k = ' + str(k) + ' clients/sec')
    # plt.plot(np.array(schedulers), np.array(times), 'b')
    plt.plot(np.array(schedulers), np.array(times), 'bx')
    plt.xticks(np.arange(0, 33, 4))
    line1, = plt.plot(np.array(schedulers), np.array(times), label='Source-DPOR')
    # plt.plot(np.array(schedulers2), np.array(times2), 'red')
    plt.plot(np.array(schedulers2), np.array(times2), 'gx')
    line2, = plt.plot(np.array(schedulers2), np.array(times2), label='Optimal-DPOR')

    # plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)}, loc=1)
    # plt.savefig(test + '_' + N + '_' + B + '_combo_time.png')
    plt.grid(True) 
    # plt.show()
    # plt.close()
    # exit()
    # Speedup
    plt.subplot(1,2,2)

    plt.xlabel('Schedulers')
    plt.ylabel('Speedup')
    #plt.title('$\lambda$ = ' + str(l) + ' clients/sec, k = ' + str(k) + ' clients/sec')
    # plt.plot(np.array(schedulers), np.array(speedup), 'b')
    plt.plot(np.array(schedulers), np.array(speedup), 'bx')
    plt.plot(np.array(schedulers2), np.array(speedup2), 'gx')
    line3, = plt.plot(np.array(schedulers), np.array(speedup), label='Source-DPOR')
    line4, = plt.plot(np.array(schedulers2), np.array(speedup2), label='Optimal-DPOR')
    f.legend([line1,line2,line3,line4], ['Source-DPOR', 'Optimal-DPOR'], loc = 'center right', borderaxespad=0.1 )
    # ax1.legend(loc='upper left')
    plt.subplots_adjust(right=0.80)
    plt.xticks(np.arange(0, 33, 4))
    # plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)}, loc=2)
    # plt.savefig(name + '_speedup.png')
    # plt.close()
    plt.grid(True) 
    # plt.savefig(test + '_' + N + '_' + B + '_combo_time.png')
    plt.show()
    plt.close()
    # exit()
    # Speedup
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

def stackplots(name):
    fl1 = name + '_' + 'source_claims' +'.txt'


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
    ax.stackplot(schedulers, be, oc, done, labels=['Budget Exceeded', 'Disputed Entry Found', 'Finished'], colors=['darkblue','orange','g'])
    ax.legend(loc='upper left')
    plt.xlabel('Schedulers')
    plt.ylabel('Reports to Controller')
    # plt.xticks(schedulers)
    plt.savefig(name + '_' + 'source' +'_stack.png')
    plt.close()

    fl2 = name + '_' + 'optimal_claims' +'.txt'


    schedulers2 = []
    be2 = []
    oc2 = []
    done2 = []

    with open(fl2) as f:
        for line in f:
            lin = line.split()
            print(lin)
            schedulers2.append(int(lin[0]))
            be2.append(int(lin[1]))
            oc2.append(int(lin[2]))
            done2.append(int(lin[3]))

    # plt.show()
    # fig, ax = plt.subplots()
    # ax.stackplot(x, y)
    # plt.show()
    fig, ax = plt.subplots()
    ax.stackplot(schedulers2, be2, oc2, done2, labels=['Budget Exceeded', 'Disputed Entry Found', 'Finished'], colors=['darkblue','orange','g'])
    ax.legend(loc='upper left')
    plt.xlabel('Schedulers')
    plt.ylabel('Reports to Controller')
    # plt.xticks(schedulers)
    plt.savefig(name + '_' + 'optimal' +'_stack.png')
    plt.close()

    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12,5))
    l4,l5,l6 = ax2.stackplot(schedulers2, be2, oc2, done2, labels=['Budget Exceeded', 'Disputed Entry Found', 'Finished'], colors=['darkblue','orange','g'])
    # ax2.legend(loc='upper left')
    l1,l2,l3 = ax1.stackplot(schedulers, be, oc, done, labels=['Budget Exceeded', 'Disputed Entry Found', 'Finished'], colors=['darkblue','orange','g'])
    fig.legend([l1,l2,l3,l4,l5,l6], ['Budget Exceeded', 'Disputed Entry Found', 'Finished'], loc = 'center right', borderaxespad=0.1 )
    # ax1.legend(loc='upper left')
    plt.subplots_adjust(right=0.75)
    ax1.set_title('Source-DPOR')
    ax2.set_title('Optimal-DPOR')
    # ax1.set_ylim([0,2500])
    # ax2.set_ylim([0,2500])
    ax1.set_xlim([2,32])
    ax2.set_xlim([2,32])
    ax1.set(xlabel='Schedulers')
    ax2.set(xlabel='Schedulers')
    # plt.xlabel('Schedulers')
    # plt.xlabel('Schedulers')
    # plt.ylabel('Reports to Controller')
    # plt.xticks(schedulers)
    # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
        #    ncol=3, mode="expand", borderaxespad=0.)
    ax1.xaxis.set_ticks(np.arange(0, 33, 4))
    ax2.xaxis.set_ticks(np.arange(0, 33, 4))
    plt.savefig(name + '_' + 'combined' +'_stack.png')
    # plt.show()
    plt.close()

if __name__ == "__main__":
    stackplots('readers1510000')
    stackplots('readers1530000')
    plot('readers','15','10000')
    plot('readers','15','30000')
    # plot('indexer15')
    # plot('readers15')
    # plot('lastzero11')
    # plots(['indexer15', 'readers15', 'lastzero11'])
    # plot('readers10')



