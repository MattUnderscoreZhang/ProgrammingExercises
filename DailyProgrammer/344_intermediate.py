import pandas as pd
import subprocess
import sys
from operator import add

# Create a program that will solve the banker's algorithm. This algorithm stops deadlocks from happening by not allowing processes to start if they don't have access to the resources necessary to finish. A process is allocated certain resources from the start, and there are other available resources. In order for the process to end, it has to have the required amount of resources in each slot.

initial_resources = []
available_resources = []
needed_resources = []
process_number = []

def read_file(file_name):

    global initial_resources, available_resources, needed_resources, process_number

    processes = pd.read_csv(file_name, header=None, delimiter="\t", engine="python", skipfooter=1)
    initial = processes[0]
    needed = processes[1]
    last_line = subprocess.check_output(['tail', '-1', file_name])[:-1]
    initial_resources = [i.split(" ") for i in initial]
    needed_resources = [i.split(" ") for i in needed]
    available_resources = last_line.split(" ")
    initial_resources = [[int(i) for i in process] for process in initial_resources]
    needed_resources = [[int(i) for i in process] for process in needed_resources]
    available_resources = [int(i) for i in available_resources]
    process_number = range(len(initial_resources))

def find_runnable_process():

    global initial_resources, available_resources, needed_resources

    for process, initial in enumerate(initial_resources):
        total_available = map(add, initial, available_resources)
        if all([i>=j for i,j in zip(total_available, needed_resources[process])]):
            return process
    return -1

if __name__ == "__main__":

    file_name = "344_intermediate.csv"
    read_file(file_name)
    
    process_order = []

    while len(initial_resources) > 0: # processes remaining in list
        next_process = find_runnable_process()
        if next_process == -1:
            print "Algorithm is not completable"
            sys.exit(0)
        available_resources = map(add, available_resources, initial_resources[next_process])
        process_order.append(process_number[next_process])
        initial_resources.pop(next_process)
        needed_resources.pop(next_process)
        process_number.pop(next_process)

    print process_order
