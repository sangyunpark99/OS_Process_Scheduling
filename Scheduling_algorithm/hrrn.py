import heapq
import matplotlib.pyplot as plt
import numpy as np


def hrrn_algorithm(processes, pcore, ecore, arrival_time, burst_time):
    # 각 프로세스의 대기 시간, 반환 시간, 정규화된 반환 시간을 저장할 리스트 초기화
    waiting_time = [0] * processes
    turnaround_time = [0] * processes
    normalized_turnaround_time = [0] * processes
    core_consumption = {f"P{i + 1}": 0 for i in range(pcore)}
    core_consumption.update({f"E{i + 1}": 0 for i in range(ecore)})

    process_queue = []  # 실행해야 할 프로세스들의 집합
    pcore_heap = [(0, f"P{i + 1}") for i in range(pcore)]  # pcore가 할당된 프로세스들의 집합
    ecore_heap = [(0, f"E{i + 1}") for i in range(ecore)]  # ecore가 할당된 프로세스들의 집합

    for i in range(processes):
        heapq.heappush(process_queue, (arrival_time[i], i))  # 도착시간에 따라 힙정렬

    while process_queue:  # 미완료된 프로세스가 있을 경우
        arrival, process_id = heapq.heappop(process_queue)
        # 할당할 pcore가 있고 / ecore가 비어있거나, pcore heap의 finsih_time이 더 작은 경우
        if pcore_heap and (not ecore_heap or pcore_heap[0][0] <= arrival):
            finish_time, processor_id = heapq.heappop(pcore_heap)
            processor_type = "P"

        # 할당할 ecore가 있으면
        elif (ecore_heap[0][0] <= arrival):
            finish_time, processor_id = heapq.heappop(ecore_heap)
            processor_type = "E"

        else:
            # 다시 넣기
            # 도착한 프로세스 중 response_ratio가 가장 짧은 프로세스에게 코어를 할당하므로
            heapq.heappush(process_queue, (arrival, process_id))
            # finish_time, processor_id = find_core_allocate(process_queue, pcore_heap, ecore_heap, burst_time)

            # 두 core_heap에서 가장 빨리 끝나는 core 찾기

            min_arrival_time = float('inf')
            if (pcore_heap):
                if pcore_heap[0][0] < min_arrival_time:  # pcore가 가장 빨리 끝나면
                    min_arrival_time = pcore_heap[0][0]
                    whatcore = True

            if (ecore_heap):
                if ecore_heap[0][0] < min_arrival_time:  # ecore가 가장 빨리 끝나면
                    min_arrival_time = ecore_heap[0][0]
                    whatcore = False

            if (whatcore):
                finish_time, processor_id = heapq.heappop(pcore_heap)
                processor_type = "P"
            else:
                finish_time, processor_id = heapq.heappop(ecore_heap)
                processor_type = "E"

            # process_queue에서 min_arrival_time보다 작은 도착 시간을 갖는 프로세스
            # = 일찍 도착해서 기다리고 있는 프로세스
            smaller_arrival_time_processes = [process for process in process_queue if process[0] <= min_arrival_time]

            for process in smaller_arrival_time_processes:
                x = process[1]  # 튜플 값 중 2번째 인덱스 값을 x에 할당
                waiting_time[x] = start_time - arrival  # waiting_time 리스트의 x번째 인덱스 값 변경

            # response_ratio 값을 기준으로 대기 프로세스 오름차순 정렬
            smaller_arrival_time_processes.sort(
                key=lambda x: calculate_response_ratio(waiting_time[x[1]], burst_time[x[1]]), reverse=True)

            # response_ratio가 가장 짧은 프로세스 선택 및 process_queue에서 삭제
            arrival, process_id = smaller_arrival_time_processes[0]

            process_queue.remove(smaller_arrival_time_processes[0])
            heapq.heapify(process_queue)

        # 실행 시작 시간 계산 = 프로세스 도착 시간, finish_time 비교

        # 각 프로세스마다 필요한 실행시간
        work_left = burst_time[process_id]

        if processor_type == "P":
            work_done_per_second = 2
            power_consumption = 3
            startup_power = 0.5

        else:
            work_done_per_second = 1
            power_consumption = 1
            startup_power = 0.1

        # 초기 시동전력
        if (arrival == 0):
            core_consumption[processor_id] += startup_power

        # 시동전력 소모, 코어 유휴시간 o
        if (arrival > finish_time):
            start_time = arrival

            # 시동 전력 계산
            core_consumption[processor_id] += startup_power

        # 시동전력 미소모, 코어 유휴시간 x
        else:
            start_time = finish_time

        # 작업 완료 시간 계산
        work_seconds = -(-work_left // work_done_per_second)  # 작업 시간, 올림 나눗셈
        end_time = start_time + work_seconds  # 도착 시간 + 작업 완료 시간

        waiting_time[process_id] = start_time - arrival
        turnaround_time[process_id] = end_time - arrival
        normalized_turnaround_time[process_id] = turnaround_time[process_id] / burst_time[process_id]

        # 코어 소비전력
        core_consumption[processor_id] += work_seconds * power_consumption

        # pcore, ecore_heap으로 finish_time 오름차순 정렬
        if processor_type == "P":
            heapq.heappush(pcore_heap, (end_time, processor_id))
        else:
            heapq.heappush(ecore_heap, (end_time, processor_id))

    return waiting_time, turnaround_time, normalized_turnaround_time, core_consumption


def calculate_response_ratio(waiting_time, burst_time):
    response_ratio = 1 + (waiting_time / burst_time)
    return response_ratio


def draw_gantt_chart(scheduling_order, start_times, end_times, processors_used):
    plt.figure(figsize=(10, 6))

    for i, (start, end, process) in enumerate(zip(start_times, end_times, scheduling_order)):
        plt.barh(process, end - start, left=start, height=0.5)
        plt.text(start + (end - start) / 2, process, f"P{i + 1}", color='white', fontsize=12, ha='center', va='center')

    plt.xlabel("Time")
    plt.ylabel("Processor")
    plt.title("Gantt Chart")
    plt.grid(True)
    plt.show()


processes = int(input("# of Processes: "))
processors = int(input("# of Processors: "))
pcore = int(input("# of P core: "))
ecore = int(input("# of E core: "))

input_arrival = input("Arrival time: ")
arrival_time = list(map(int, input_arrival.split()))
input_burst = input("Burst time: ")
burst_time = list(map(int, input_burst.split()))

waiting_times, turnaround_times, normalized_turnaround_times, core_consumption = hrrn_algorithm(processes, pcore, ecore,
                                                                                                arrival_time,
                                                                                                burst_time)

# 결과 출력
for i in range(processes):
    print(f"P{i + 1}: WT = {waiting_times[i]}, TT = {turnaround_times[i]}, NTT = {normalized_turnaround_times[i]:.2f}")

print("\nCore Consumption:")
for core_id, consumption in core_consumption.items():
    print("{}: {:.1f}W".format(core_id, consumption))
total_consumption = sum(core_consumption.values())
print("\nTotal Consumption: {:.1f}W".format(total_consumption))
