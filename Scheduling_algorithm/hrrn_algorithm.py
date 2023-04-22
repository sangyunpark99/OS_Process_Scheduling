import heapq

def calculate_hrrn(processes):
    processes = sorted(processes, key=lambda x: x[0])
    n = len(processes)
    waiting_time = [0] * n
    completion_time = [0] * n
    total_time = 0
    pq = []

    index = 0
    while processes or pq:
        while processes and processes[0][0] <= total_time:
            arrival, burst = processes.pop(0)
            response_ratio = 1 + (total_time - arrival) / burst
            heapq.heappush(pq, (-response_ratio, arrival, burst, index))
            index += 1

        if pq:
            _, arrival, burst, idx = heapq.heappop(pq)
            waiting_time[idx] = total_time - arrival
            completion_time[idx] = total_time + burst
            total_time += burst
        else:
            total_time = processes[0][0]

    return waiting_time, completion_time


def main():
    processes = [
        (1, 5),
        (2, 3),
        (4, 1),
        (6, 4),
    ]
    waiting_time, completion_time = calculate_hrrn(processes)
    print("Process\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\t\t NTT")
    for i in range(len(processes)):
        arrival, burst = processes[i]
        waiting = waiting_time[i]
        tt_time = completion_time[i]
        tt_bt = (completion_time[i] - arrival) / burst
        print(f"P{i+1}\t\t\t{arrival}\t\t\t\t{burst}\t\t\t{waiting}\t\t\t\t{tt_time}\t\t\t\t{tt_bt:.2f}")


if __name__ == "__main__":
    main()
