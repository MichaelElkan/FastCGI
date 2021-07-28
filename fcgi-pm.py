#initial commit
#todo: 
# docker
# bind to port
# exit clean up
# variable logging verbosity

import argparse
import multiprocessing
import subprocess
import atexit
import signal
import os
import socket
import sys
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-s','--socket', help='Specify the socket.')
parser.add_argument('-q','--queue-size', help='Specify the queue size.')
parser.add_argument('-c', '--count', help='Specify the count.')
parser.add_argument('-e', '--executable', help='Specify the executable and any of its arguments.')
parser.add_argument('-v', '--verbose', action='store_true', help='Specify if you want verbose output.')
args = parser.parse_args()

SOCKET_ARG = args.socket
QUEUESIZE = int(args.queue_size)
COUNT = int(args.count)
EXECUTABLE = args.executable
VERBOSE = args.verbose
print(args)
PROCESS_LIST = []

def main():
    bindport()
    if VERBOSE:
        log("Starting Fcgi-pm at " + str(datetime.now()))
    pool = multiprocessing.Pool(processes=COUNT)
    tasks = range(QUEUESIZE)
    results = []
    r = pool.map_async(work, tasks, callback=results.append)
    r.wait()
    print(results)

def bindport():
    HOST = SOCKET_ARG.split(':')[0]
    PORT = int(SOCKET_ARG.split(':')[1])
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        SOCKET.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    print('Socket bind complete')

def work(value):
    process = subprocess.Popen(EXECUTABLE, shell=True, stdin=subprocess.PIPE)
  
    PROCESS_ID = process.pid
    if VERBOSE:
        log("Starting process " + str(PROCESS_ID) + " at " + str(datetime.now()))

    PROCESS_LIST.append(PROCESS_ID)
    process.communicate(bytes(SOCKET_ARG, encoding='utf-8'))
    process.wait()
   
    if VERBOSE:
        log("Ending process " + str(PROCESS_ID) + " at " + str(datetime.now()))

    PROCESS_LIST.remove(PROCESS_ID)
    return process


def cleanup():
    for pid in PROCESS_LIST:
        if pid != None:
            print("Killing: ", pid)
            os.kill(pid, signal.SIGTERM)

def log(text):
    try:
        FILE = open('logfile.txt', 'a')
        FILE.write(text + '\n')
        FILE.close()
    except IOError:
        FILE = open('logfile.txt', 'w+')
        FILE.write(text + '\n')
        FILE.close()
    
    

atexit.register(cleanup)
#signal.signal(signal.SIGTERM, cleanup)
#signal.signal(signal.SIGINT, cleanup)

main()
