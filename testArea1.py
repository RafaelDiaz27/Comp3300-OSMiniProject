import json
import sys

#Create the functions for each of the algorithm here, then we call that algorithm later.

#FIFO
def fifo_scheduler(data):
    jobs=data["jobs"]

    # Sort by arrival time, then PID
    jobs.sort(key=lambda x: (x["arrival"], x["pid"]))

    current_time = 0
    gantt = []
    turnaround = {}
    waiting = {}

    for job in jobs:
        pid = job["pid"]
        arrival = job["arrival"]
        burst = job["burst"]

        # Handle idle CPU
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

# Main program - reading the file
if len(sys.argv) < 2:
    print("Usage: python main.py input.json > output.json")

with open(sys.argv[1], "r") as file:
    jsonData = json.load(file) #jsonData contains the json file now.


if (jsonData["policy"] == "RR"): # RoundRobin
    print("Round Robin")

elif jsonData["policy"] == "FIFO":
    result = fifo_scheduler(jsonData)
    print(json.dumps(result, indent=2))

elif (jsonData["policy"] == "SJF"): #SJF
    print("SJF")

elif (jsonData["policy"] == "Priority"): #Priority
    print("Priority")

