#initial commit
#todo: 
# docker
# bind to port
# exit clean up
# variable logging verbosity

import argparse
import multiprocessing
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-s','--socket', help='Specify the socket.')
parser.add_argument('-q','--queue-size', help='Specify the queue size.')
parser.add_argument('-c', '--count', help='Specify the count')
parser.add_argument('-e', '--executable', help='Specify the executable and any of its arguments')
args = parser.parse_args()

SOCKET = args.socket
QUEUESIZE = int(args.queue_size)
COUNT = int(args.count)
EXECUTABLE = args.executable
print(SOCKET)

def work(value):
    process = subprocess.Popen(EXECUTABLE, shell=True,stdin=subprocess.PIPE)
    process.communicate(bytes(SOCKET, encoding='utf-8'))
    process.wait()
    return process


pool = multiprocessing.Pool(processes=COUNT)
tasks = range(QUEUESIZE)
results = []
r = pool.map_async(work, tasks, callback=results.append)
r.wait()
print(results)


