
from __future__ import (unicode_literals, division, print_function,
                        absolute_import)

import totut
import time
import argparse
import psutil


def get_percent(process):
    
    try:
        #print(process.cpu_percent(duration = 0.1)/psutil.cpu_count())
        return process.cpu_percent(interval = 0.1)/psutil.cpu_count()
    except AttributeError:
        return process.get_cpu_percent(interval = 0.1)/psutil.cpu_count()


def get_memory(process):
    try:
        return process.memory_info()
    except AttributeError:
        return process.get_memory_info()



def main():

    parser = argparse.ArgumentParser(
        description='Record CPU and memory usage for a process')

    parser.add_argument('process_id_or_command', type=str,
                        help='the process id or command')

    parser.add_argument('--log', type=str,
                        help='output the statistics to a file')

    parser.add_argument('--plot', type=str,
                        help='output the statistics to a plot')

    parser.add_argument('--duration', type=float,
                        help='how long to record for (in seconds). If not '
                             'specified, the recording is continuous until '
                             'the job exits.')

    parser.add_argument('--interval', type=float,
                        help='how long to wait between each sample (in '
                             'seconds). By default the process is sampled '
                             'as often as possible.')

    parser.add_argument('--include-children',
                        help='include sub-processes in statistics (results '
                             'in a slower maximum sampling rate).',
                        action='store_true')

    args = parser.parse_args()

    # Attach to process
##    try:
##        pid = int(args.process_id_or_command)
##        print("Attaching to process {0}".format(pid))
##        sprocess = None
##    except Exception:
##        import subprocess
##        command = args.process_id_or_command
##        print("Starting up command '{0}' and attaching to process"
##              .format(command))
##        sprocess = subprocess.Popen(command, shell=True)
##        pid = sprocess.pid
##
##    monitor(pid, logfile=args.log, plot=args.plot, duration=args.duration,
##            interval=args.interval, include_children=args.include_children)
##
##    if sprocess is not None:
##        sprocess.kill()


def monitor(pid, logfile=None, plot=None, duration=None, interval=None,
            include_children=False):

    import psutil
    totut.calc(duration = duration)
    pr = psutil.Process(pid)
    #print(pr.cpu_percent(interval = 0.1)/psutil.cpu_count())

    start_time = time.time()

    log = {}
    log['times'] = []
    log['cpu'] = []
    log['mem_real'] = []
    log['mem_virtual'] = []
    try:

        while True:

            current_time = time.time()

            try:
                pr_status = pr.status()
            except TypeError:  
                pr_status = pr.status
            except psutil.NoSuchProcess:  # pragma: no cover
                break

            if pr_status in [psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD]:
                print("Process finished ({0:.2f} seconds)".format(current_time - start_time))
                break
            
            if duration is not None and current_time - start_time > duration:
                break
            try:
                current_cpu = get_percent(pr)
                current_mem = get_memory(pr)
            except Exception:
                break
            current_mem_real = current_mem.rss / 1024. ** 2
            current_mem_virtual = current_mem.vms / 1024. ** 2


            if plot:
                log['times'].append(current_time - start_time)
                log['cpu'].append(current_cpu)
                log['mem_real'].append(current_mem_real)
                log['mem_virtual'].append(current_mem_virtual)

    
    except KeyboardInterrupt:  # pragma: no cover
        pass

##    if logfile:
##        f.close()

    
    if plot:
        import matplotlib.pyplot as plt
        with plt.rc_context({'backend': 'Agg'}):

            fig = plt.figure(figsize = (20,20))
            ax = fig.add_subplot(3, 1, 1)
    

            ax.plot(log['times'], log['cpu'], '-', lw=1, color='r')

            ax.set_ylabel('CPU (%)', color='r')
            ax.set_ylim(0., max(log['cpu']) * 1.2)

            #plt.subplot(1,1,1)

            #ax2 = ax.twinx()
            ax2 = fig.add_subplot(3, 1, 2)
            ax2.plot(log['times'], log['mem_real'], '-', lw=1, color='b')
            ax2.set_ylim(0., max(log['mem_real']) * 1.2)

            ax2.set_ylabel('Real Memory (MB)', color='b')            
            #plt.subplot(1,1,2)

            #ax3 = ax.twinx()
            ax3 = fig.add_subplot(3, 1, 3)
            ax3.plot(log['times'], log['mem_virtual'], '-', lw=1, color='g')
            ax3.set_ylim(0., max(log['mem_virtual']) * 1.2)

            ax3.set_ylabel('Virtual Memory (MB)', color='g')
            ax3.set_xlabel('time (s)')
            
            #plt.subplot(1,1,3)
            ax.grid()
            ax2.grid()
            ax3.grid()

            fig.savefig(plot)
            plt.show(fig)
