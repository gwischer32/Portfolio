# run on linux as: python3 vecAdd.property
import threading  # for thread
import time       # for time.sleep(sec)

def vecAddThread(aa, bb, cc, start, stop):
    print(str(start) + " " + str(stop))
    for x in range(start, stop):
        cc[x] = aa[x] + bb[x]

        
a = [x for x in range(100)]
b = [x for x in range(100)]
c = [0 for x in range(100)]

numThreads = 4
threads = [None]*numThreads #empty list of 4 elements

for i in range(numThreads):
    start = (100//numThreads)*i
    stop = (100//numThreads)*(i+1)
    threads[i] = threading.Thread(target=vecAddThread, args=(a, b, c, start, stop))
    threads[i].start()

for i in range(numThreads):
    threads[i].join()

print(c)
