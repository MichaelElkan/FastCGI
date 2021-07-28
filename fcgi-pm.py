#initial commit
#todo: mandatory arguments

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

def work(value):
    #return value
    return subprocess.Popen('bash /home/melkan/work/FastCGI/testexe.sh', shell=True,)

pool = multiprocessing.Pool(processes=COUNT)
tasks = range(QUEUESIZE)
results = []
r = pool.map_async(work, tasks, callback=results.append)
r.wait()
print(results)


