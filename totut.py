import os
import ps
import psutil
import matplotlib.pyplot as plt
import time

def calc(duration):
    core1 = []
    core2 = []
    core3 = []
    core4 = []
    timer = []
    start_time = time.time()
    while True:
        c1, c2, c3, c4 = psutil.cpu_percent(interval = 0.1, percpu = True)
        core1.append(c1)
        core2.append(c2)
        core3.append(c3)
        core4.append(c4)
        current_time = time.time()
        timer.append(current_time - start_time)

        if current_time - start_time > duration:
            break

    fig = plt.figure(figsize = (20,20))
    ax = fig.add_subplot(2, 2, 1)
    ax.plot(timer, core1, '-', lw=1, color='r')
    ax.set_ylim(0., max(core1) * 1.2)
    ax.set_ylabel('CPU 1 (%)', color='r')

    ax1 = fig.add_subplot(2, 2, 2)
    ax1.plot(timer, core2, '-', lw=1, color='g')
    ax1.set_ylim(0., max(core2) * 1.2)
    ax1.set_ylabel('CPU 2 (%)', color='g')

    ax2 = fig.add_subplot(2, 2, 3)
    ax2.plot(timer, core3, '-', lw=1, color='b')
    ax2.set_ylim(0., max(core3) * 1.2)
    ax2.set_ylabel('CPU 3 (%)', color='b')

    ax3 = fig.add_subplot(2, 2, 4)
    ax3.plot(timer, core4, '-', lw=1, color='m')
    ax3.set_ylim(0., max(core4) * 1.2)
    ax3.set_ylabel('CPU 4 (%)', color='m')
    ax3.set_xlabel('time (s)')

    ax.grid()
    ax1.grid()
    ax2.grid()
    ax3.grid()
    plt.show(fig)
    

    

    
