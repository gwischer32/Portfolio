import sys
import heapq

class Process:
    def __init__(self, name, priority, arrival_time, total_time, block_interval):
        self.name = name
        self.priority = priority
        self.arrival_time = arrival_time
        self.total_time = total_time
        self.block_interval = block_interval

        # Dynamic state
        self.time_used = 0            # total CPU time consumed so far
        self.time_since_block = 0     # time since last block
        self.unblock_time = None      # if blocked, when it becomes ready

    def __lt__(self, other):
        # Needed for PriorityQueue tie-breaking
        return self.name < other.name



# Helper: PriorityQueue wrapper (min-heap but reversed priority)
class PriorityQueue:
    def __init__(self):
        self.heap = []  # (priority sorting key, counter, process)
        self.counter = 0

    def push(self, priority_key, process):
        heapq.heappush(self.heap, (priority_key, self.counter, process))
        self.counter += 1

    def pop(self):
        if not self.heap:
            return None
        return heapq.heappop(self.heap)[2]

    def peek(self):
        if not self.heap:
            return None
        return self.heap[0][2]

    def empty(self):
        return len(self.heap) == 0

# Main scheduler
def main():

    if len(sys.argv) != 4:
        print("Usage: python3 scheduler.py joblist.txt time_slice block_duration")
        sys.exit(1)

    jobfile = sys.argv[1]
    time_slice = int(sys.argv[2])
    block_duration = int(sys.argv[3])

    # Read processes 
    Arrival = PriorityQueue()
    Ready = PriorityQueue()
    Blocked = PriorityQueue()

    processes = []

    with open(jobfile) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name, pr, arr, tot, blk = line.split()
            p = Process(name, int(pr), int(arr), int(tot), int(blk))
            processes.append(p)

            # Arrival ordered by arrival_time
            Arrival.push(p.arrival_time, p)

    print(f"timeSlice: {time_slice}\tblockDuration: {block_duration}")

    sim_time = 0
    completed = []
    active = None  # the process currently running

    # Main loop
    while len(completed) < len(processes):

        # Move arrivals to Ready
        while (not Arrival.empty()) and Arrival.peek().arrival_time <= sim_time:
            p = Arrival.pop()
            Ready.push((-p.priority, sim_time), p)   # prioritize by priority desc

        # Move unblocked to Ready
        while (not Blocked.empty()) and Blocked.peek().unblock_time <= sim_time:
            p = Blocked.pop()
            p.time_since_block = 0
            Ready.push((-p.priority, sim_time), p)

        # Select process 
        if active is None:
            if Ready.empty():
                # CPU idle — jump to next arrival/unblock
                next_event = None
                t1 = Arrival.peek().arrival_time if not Arrival.empty() else None
                t2 = Blocked.peek().unblock_time if not Blocked.empty() else None

                if t1 is not None:
                    next_event = t1
                if t2 is not None:
                    next_event = t2 if next_event is None else min(next_event, t2)

                interval = next_event - sim_time
                print(f"{sim_time}\t(IDLE)\t{interval}\tI")
                sim_time = next_event
                continue
            else:
                active = Ready.pop()

        # Determine run interval end
        run_time_remaining = active.total_time - active.time_used
        time_until_block = active.block_interval - active.time_since_block

        end_times = [
            time_slice,          # P
            run_time_remaining,  # T
            time_until_block     # B
        ]
        run_interval = min(end_times)

        # Run the process
        start_time = sim_time
        sim_time += run_interval
        active.time_used += run_interval
        active.time_since_block += run_interval

        # Determine why interval ended 
        reason = ""
        if active.time_used >= active.total_time:
            reason = "T"
        elif active.time_since_block >= active.block_interval:
            reason = "B"
        else:
            reason = "P"

        print(f"{start_time}\t{active.name}\t{run_interval}\t{reason}")

        # Handle result 
        if reason == "T":  # terminated
            completed.append(active)
            turnaround = sim_time - active.arrival_time
            active.turnaround = turnaround
            active = None

        elif reason == "B":  # block
            active.time_since_block = 0
            active.unblock_time = sim_time + block_duration
            Blocked.push(active.unblock_time, active)
            active = None

        else:  # reason == P — time slice expired
            Ready.push((-active.priority, sim_time), active)
            active = None

    # After loop: average turnaround
    avg = sum(p.turnaround for p in completed) / len(completed)
    print(f"Average turnaround time: {avg}")
    

if __name__ == "__main__":
    main()
