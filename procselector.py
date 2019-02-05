import os
import ps
import psutil
import totut

index = 1
pids = []
pnames = []


for pdet in psutil.process_iter():
    pdict = pdet.as_dict(attrs = ['pid','name','threads'])
##    pt = str(pdict['threads']).split()
##    for i in pt:
##        if 'id=' in i:
##            #print(i)
##            print(int(i[i.index('=')+1:-2]))
    pids.append(pdict['pid'])
    pnames.append(pdict['name'])
    print(index,'. ',pdict['name'],' '*(30-len(str(pdict['name']))), pdict['pid'])
    index+=1
##    if index == 10:
##        break

while True:
    spid = int(input('Select the index of any process: '))
    print('\nSelected process: ',pnames[spid-1])

    duration = int(input('Enter duration of performance measurement: '))

##    tot = 0
##    pt = str(psutil.Process(pids[spid-1]).threads()).split()
##    for i in pt:
##        if 'id=' in i:
##            pid1 = int(i[i.index('=')+1:-2])
##            print(pid1)
##            pr = psutil.Process(pid1)
##            print(pr)
##            x = process.cpu_percent(pr)
##            print(x)
##            tot+=x
##
##    print(tot)
##    test_list = []
##
##    for i in range(10):
##        p = psutil.Process(pids[spid-1])
##        p_cpu = p.cpu_percent(interval = 0.1)
##        test_list.append(p_cpu)
##
##    print(float(sum(test_list))/len(test_list))
    ps.monitor(pids[spid-1], plot="perf.png", duration = duration)
    #totut.calc(duration = duration)
    
