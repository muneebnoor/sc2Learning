import sc2reader
import time
import threading
import os
from multiprocessing.dummy import Pool
from multiprocessing import Process

path = "D:\\thesis\\replays500"
replays = sc2reader.load_replays(path, load_level=4, debug=True)
replayFiles = [path + '\\' + x for x in os.listdir(path)]

def add_path(fileName):
    fileName = path + '\\' + fileName

def read_replay(filePath):
    replay = sc2reader.load_replay(filePath, load_level=4, debug=True)
    process_replay(replay)

def read_replays(replaysPaths):
    for filePath in replaysPaths:
        replay = sc2reader.load_replay(filePath, load_level=4, debug=True)
        process_replay(replay)
        print("Processed: %s" % filePath )

def process_replay(replay):
    gameEvents = replay.events

def without_threads():
    for rf in replayFiles:
        read_replay(rf)

def threaded_process_replay(noOfThreads):
    pool = Pool(noOfThreads)
    pool.map(read_replay, replayFiles)
    pool.close()
    pool.join()

def multithreaded_process(noOfThreads):
    jobsPerThread = int(len(replayFiles)/noOfThreads)
    allocatedFiles = 0
    for i in range(noOfThreads):
        replaySet = replayFiles[allocatedFiles:jobsPerThread * (i + 1)]
        t = threading.Thread(target=read_replays, args=(replaySet,))
        allocatedFiles += jobsPerThread
        t.start()

def multiprocess_replay_parse(noOfProcesses):
    jobsPerProcess = int(len(replayFiles) / noOfProcesses)
    allocatedFiles = 0
    processes = []
    for i in range(noOfProcesses):
        replaySet = replayFiles[allocatedFiles:jobsPerProcess * (i + 1)]
        p = Process(target=read_replays, args=(replaySet,))
        allocatedFiles += jobsPerProcess
        p.start()
        processes.append(p)
    for proc in processes:
        proc.join()

startTime = time.time()
multiprocess_replay_parse(2)
print("--- Execution time without threads :%s ---" % (time.time() - startTime))


'''
    for r in replayFiles:
        t = threading.Thread(target=read_replay, args=(r,))
        t.start()



startTime = time.time()
without_threads()
print("--- Execution time without threads :%s ---" % (time.time() - startTime))


startTime = time.time()
multithreaded_process()
print("--- Execution time with threads :%s ---" % (time.time() - startTime))


startTime = time.time()
threaded_process_replay(4)
print("--- Execution time with 4 threads :%s ---" % (time.time() - startTime))

startTime = time.time()
threaded_process_replay(3)
print("--- Execution time with 8 threads :%s ---" % (time.time() - startTime))


startTime = time.time()
threaded_process_replay(16)
print("--- Execution time with 16 threads :%s ---" % (time.time() - startTime))

startTime = time.time()
threaded_process_replay(24)
print("--- Execution time with 24 threads :%s ---" % (time.time() - startTime))

startTime = time.time()
threaded_process_replay(50)
print("--- Execution time with 50 threads :%s ---" % (time.time() - startTime))

startTime = time.time()
threaded_process_replay(100)
print("--- Execution time with 100 threads :%s ---" % (time.time() - startTime))
'''