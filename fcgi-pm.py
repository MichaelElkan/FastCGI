# Michael Elkan
# 7/28/2021

# standard library imports
import argparse
import multiprocessing
import subprocess
import atexit
import signal
import os
import socket
import sys
from datetime import datetime

# command line argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-s','--socket', help='Specify the socket.')
parser.add_argument('-q','--queue-size', help='Specify the queue size.')
parser.add_argument('-c', '--count', help='Specify the count.')
parser.add_argument('-e', '--executable', help='Specify the executable and any of its arguments.')
parser.add_argument('-v', '--verbose', action='store_true', help='Specify if you want verbose output.')
args = parser.parse_args()

# command line arguments
SOCKET_ARG = args.socket
QUEUESIZE = int(args.queue_size)
COUNT = int(args.count)
EXECUTABLE = args.executable
VERBOSE = args.verbose
# Process list for clean up
PROCESS_LIST = []


def main():
    SOCKET = bindport() 
    if VERBOSE:
        log("Starting Fcgi-pm at " + str(datetime.now()))
    pool = multiprocessing.Pool(processes=COUNT)
    tasks = range(QUEUESIZE)
    results = []
    r = pool.map_async(work, tasks, callback=results.append)
    r.wait()
    print(results)

# binds socket and waits for connection
def bindport():
    # get host and port variables from command line argument
    HOST = SOCKET_ARG.split(':')[0]
    PORT = int(SOCKET_ARG.split(':')[1])
    
    # initialize and bind socket
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        SOCKET.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    if VERBOSE:
        log("Socket succesfully bound: " + str(SOCKET) + " at " + str(datetime.now()) )
    # waits for connection to be made
    SOCKET.listen(5)
    cli, addr = SOCKET.accept()

# main driver of fcgi executables
def work(value):
    # spawns a child subprocess 
    process = subprocess.Popen(EXECUTABLE, shell=True, stdin=subprocess.PIPE)
    
    # saves the process ID to use for clean up if needed
    PROCESS_ID = process.pid
    PROCESS_LIST.append(PROCESS_ID)
    # logging if desired
    if VERBOSE:
        log("Starting process " + str(PROCESS_ID) + " at " + str(datetime.now()))

    # passes socket to fcgi executable through stdin
    process.communicate(bytes(SOCKET_ARG, encoding='utf-8'))
    process.wait()
   
    if VERBOSE:
        log("Ending process " + str(PROCESS_ID) + " at " + str(datetime.now()))

    PROCESS_LIST.remove(PROCESS_ID)
    return process

# clean up if any process are still running at program exit
def cleanup():
    for pid in PROCESS_LIST:
        if pid != None:
            print("Killing: ", pid)
            os.kill(pid, signal.SIGTERM)

# logging function
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

main()
