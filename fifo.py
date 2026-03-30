def fifo_scheduler(data):
    jobs=data["jobs"]

    #sort by arrival time, then PID
    jobs.sort(key=lambda x: (x["arrival"], x["pid"]))

    current_time=0
    gantt=[]
    turnarount={}
    waiting={}

    for job in jobs:
        pid=job["pid"]
        arrival=job["arrival"]
        burst=job["burst"]

        #Handle CPU idle time
        if current_time<arrival:
            current_time=arrival

        start=current_time
        end=start+burst

        gantt.append({
            "pid": pid,
            "start": start,
            "end": end
        })

        turnaround[pid]=end-arrival
        waiting[pid]=turnaround[pid]-burst
        current_time=end

        avg_turnaround=sum(turnaround.values())/len(jobs)
        avg_waiting=sum(waiting.values())/len(jobs)

        return{
            "policy": "FIFO",
            "gantt": gantt,
            "metrics": {
                "turnaround": turnaround,
                "waiting": waiting,
                "avg_turnaround": round(avg_turnaround, 2),
                "avg_waiting": round(avg_waiting, 2)
            }
        }