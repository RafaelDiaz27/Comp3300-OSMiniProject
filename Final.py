# Mini Project: CPU Scheduling Algos
# Implements FIFO, SJF, Round Robin, and Priority Scheduling
# Team members: Maria Kandikova, John Rafael Diaz Cabangon, Claudia Dinatale

import json
import sys
from collections import deque

# helpers for sorting stuff
def by_arrival_then_pid(job):
    # sort by arrival first, then use pid to break ties
    return (job['arrival'], job['pid'])

def by_pid(job):
    # alphabetical tie breaker rule from the pdf
    return job['pid']

def by_prio_then_pid(job):
    # prio first, then pid
    return (job['priority'], job['pid'])

def calculate_metrics(policy_name, completed, arrival_times, burst_times, gantt):
    # calc turnaround and waiting time for the final output
    turnaround = {}
    waiting = {}
    
    for comp in completed:
        pid = comp['pid']
        ta = comp['completion'] - arrival_times[pid]
        turnaround[pid] = ta
        waiting[pid] = ta - burst_times[pid] # wait is turnaround minus the actual burst

    # needs to be exactly 2 decimal places for the autograder
    avg_turnaround = round(sum(turnaround.values()) / len(turnaround), 2)
    avg_waiting = round(sum(waiting.values()) / len(waiting), 2)

    return {
        "policy": policy_name,
        "gantt": gantt,
        "metrics": {
            "turnaround": turnaround,
            "waiting": waiting,
            "avg_turnaround": avg_turnaround,
            "avg_waiting": avg_waiting
        }
    }

def fifo_scheduler(jobs):
    # basic first in first out. just sort by arrival time and pid
    jobs.sort(key=lambda x: (x["arrival"], x["pid"]))

    current_time = 0
    gantt = []
    turnaround = {}
    waiting = {}

    for job in jobs:
        pid = job["pid"]
        arrival = job["arrival"]
        burst = job["burst"]

        # handle if cpu is just sitting there doing nothing
        if current_time < arrival:
            current_time = arrival

        start = current_time
        end = start + burst

        gantt.append({
            "pid": pid,
            "start": start,
            "end": end
        })

        turnaround[pid] = end - arrival
        waiting[pid] = turnaround[pid] - burst
        current_time = end

    # avg calculations
    avg_turnaround = sum(turnaround.values()) / len(jobs)
    avg_waiting = sum(waiting.values()) / len(jobs)

    return {
        "policy": "FIFO",
        "gantt": gantt,
        "metrics": {
            "turnaround": turnaround,
            "waiting": waiting,
            "avg_turnaround": round(avg_turnaround, 2),
            "avg_waiting": round(avg_waiting, 2)
        }
    }

def sjf_scheduler(jobs):
    # shortest job first (non preemptive)
    # add some flags so we know whats done and whats not
    for job in jobs:
        job["done"] = False
        job["finish_time"] = 0

    current_time = 0
    gantt = []
    total_jobs = len(jobs)
    completed = 0

    while completed < total_jobs:

        # grab everything that arrived and is waiting in queue
        ready = []
        for job in jobs:
            if not job["done"] and job["arrival"] <= current_time:
                ready.append(job)

        # if queue is empty, fast forward current time to the next arrival
        if len(ready) == 0:
            next_arrival = -1
            for job in jobs:
                if not job["done"]:
                    if next_arrival == -1 or job["arrival"] < next_arrival:
                        next_arrival = job["arrival"]
            current_time = next_arrival
            continue

        # find the shortest burst
        shortest = ready[0]
        for job in ready:
            if job["burst"] < shortest["burst"]:
                shortest = job
            elif job["burst"] == shortest["burst"]:
                # tie breaker alphabetically
                if job["pid"] < shortest["pid"]:
                    shortest = job

        # run it
        start = current_time
        end = current_time + shortest["burst"]
        gantt.append({"pid": shortest["pid"], "start": start, "end": end})

        shortest["finish_time"] = end
        shortest["done"] = True
        current_time = end
        completed = completed + 1

    turnaround = {}
    waiting = {}
    for job in jobs:
        ta = job["finish_time"] - job["arrival"]
        wt = ta - job["burst"]
        turnaround[job["pid"]] = ta
        waiting[job["pid"]] = wt

    avg_ta = round(sum(turnaround.values()) / len(turnaround), 2)
    avg_wt = round(sum(waiting.values()) / len(waiting), 2)

    return {
        "policy": "SJF",
        "gantt": gantt,
        "metrics": {
            "turnaround": turnaround,
            "waiting": waiting,
            "avg_turnaround": avg_ta,
            "avg_waiting": avg_wt
        }
    }

def round_robin(jobs, quantum):
    # this one was a bit tricky. using deque for the queue
    unstarted = sorted(jobs, key=by_arrival_then_pid)
    
    # save original times since we modify the remaining burst
    remaining_burst = {job['pid']: job['burst'] for job in jobs}
    arrival_times = {job['pid']: job['arrival'] for job in jobs}
    burst_times = {job['pid']: job['burst'] for job in jobs}

    time = 0
    gantt = []
    ready_queue = deque()
    completed = []

    # helper to pull in new jobs so we dont repeat code
    def enqueue_arrived(current_time):
        arrived_now = []
        while unstarted and unstarted[0]['arrival'] <= current_time:
            arrived_now.append(unstarted.pop(0))
        
        arrived_now.sort(key=by_pid)
        for job in arrived_now:
            ready_queue.append(job)

    enqueue_arrived(time)

    while ready_queue or unstarted:
        
        # skip dead time if queue empty
        if not ready_queue:
            time = unstarted[0]['arrival']
            enqueue_arrived(time)

        current_job = ready_queue.popleft()
        pid = current_job['pid']

        # run for quantum or whatever burst is left
        execute_time = min(quantum, remaining_burst[pid])
        start_time = time
        time += execute_time
        remaining_burst[pid] -= execute_time

        # if the same process runs twice in a row, merge it to look cleaner in output
        if gantt and gantt[-1]['pid'] == pid:
            gantt[-1]['end'] = time
        else:
            gantt.append({"pid": pid, "start": start_time, "end": time})

        # pull in new arrivals BEFORE putting current job back in line
        enqueue_arrived(time)

        if remaining_burst[pid] > 0:
            ready_queue.append(current_job)
        else:
            completed.append({"pid": pid, "completion": time})

    return calculate_metrics("RR", completed, arrival_times, burst_times, gantt)

def priority_scheduling(jobs):
    unstarted = sorted(jobs, key=by_arrival_then_pid)
    arrival_times = {job['pid']: job['arrival'] for job in jobs}
    burst_times = {job['pid']: job['burst'] for job in jobs}

    time = 0
    gantt = []
    completed = []
    ready_queue = []

    while unstarted or ready_queue:
        # load everything that arrived into queue
        while unstarted and unstarted[0]['arrival'] <= time:
            ready_queue.append(unstarted.pop(0))

        if not ready_queue:
            time = unstarted[0]['arrival']
            continue

        # sort by priority. lowest number is highest prio
        ready_queue.sort(key=by_prio_then_pid)

        current_job = ready_queue.pop(0)
        pid = current_job['pid']
        burst = current_job['burst']

        start_time = time
        time += burst

        gantt.append({"pid": pid, "start": start_time, "end": time})
        completed.append({"pid": pid, "completion": time})

    return calculate_metrics("Priority", completed, arrival_times, burst_times, gantt)

if __name__ == "__main__":
    # check if they actually gave us a file
    if len(sys.argv) < 2:
        print("Usage: python3 main.py input.json", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "r") as file:
            jsonData = json.load(file)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # clean up string just in case there are weird spaces in the json file
    policy = jsonData.get("policy", "").strip()
    jobs = jsonData.get("jobs", [])
    output = None

    # figure out which one to run
    if policy == "RR":
        quantum = jsonData.get("quantum")
        output = round_robin(jobs, quantum)
    elif policy == "Priority":
        output = priority_scheduling(jobs)
    elif policy == "FIFO":
        output = fifo_scheduler(jobs)
    elif policy == "SJF":
        output = sjf_scheduler(jobs)
    else:
        print(f"Error: Unknown policy '{policy}'.", file=sys.stderr)
        sys.exit(1)

    # print it out as strict json or autograder will fail
    if output is not None:
        print(json.dumps(output, indent=2))