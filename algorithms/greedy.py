from dataclasses import dataclass
from typing import Optional


@dataclass
class Process:
    start: int
    finish: int

    def __repr__(self):
        return f"Process({self.start}, {self.finish})"


class Scheduler:
    def __init__(self, processes: list[Process]):
        self.processes: list[Process] = sorted(processes, key=lambda x: x.finish)

    def find_last_non_conflicting(self, index: int) -> int:
        for j in range(index - 1, -1, -1):
            if self.processes[index].start >= self.processes[j].finish:
                return j
        return -1

    # def find_last_non_conflicting(self, index: int) -> int:
    #     left, right = 0, index - 1
    #     while left <= right:
    #         mid = (left + right) // 2
    #         if self.processes[mid].finish <= self.processes[index].start:
    #             if self.processes[mid + 1].finish <= self.processes[index].start:
    #                 left = mid + 1
    #             else:
    #                 return mid
    #         else:
    #             right = mid - 1
    #     return -1

    def dynamic_programming(self) -> tuple[int, list[Process]]:
        n = len(self.processes)
        dp = [0] * n
        prev = [-1] * n
        dp[0] = 1

        for i in range(1, n):
            include = 1
            last_non_conflicting = self.find_last_non_conflicting(i)
            if last_non_conflicting != -1:
                include += dp[last_non_conflicting]
            dp[i] = max(dp[i - 1], include)
            prev[i] = last_non_conflicting if dp[i] == include else prev[i - 1]

        selected_processes = []
        i = n - 1
        while i >= 0:
            if prev[i] != prev[i - 1]:
                selected_processes.append(self.processes[i])
                i = prev[i]
            else:
                i -= 1
        selected_processes.reverse()

        return dp[-1], selected_processes

    def greedy_recursive(self, index: Optional[int] = None, last_finish: int = 0) -> tuple[int, list[Process]]:
        if index is None:
            index = len(self.processes) - 1

        if index < 0:
            return 0, []

        current_process = self.processes[index]
        if current_process.finish <= last_finish:
            return self.greedy_recursive(index - 1, last_finish)

        include_value, include_set = self.greedy_recursive(
            index - 1, current_process.finish
        )
        include_value += 1

        exclude_value, exclude_set = self.greedy_recursive(index - 1, last_finish)

        if include_value > exclude_value:
            return include_value, include_set + [current_process]
        return exclude_value, exclude_set

    def greedy_iterative(self) -> tuple[int, list[Process]]:
        selected_processes = []
        last_finish_time = 0

        for process in self.processes:
            if process.start >= last_finish_time:
                selected_processes.append(process)
                last_finish_time = process.finish

        return len(selected_processes), selected_processes


if __name__ == '__main__':
    import timeit

    processes_data = [
        (1, 1, 4),
        (2, 3, 5),
        (3, 0, 6),
        (4, 5, 7),
        (5, 3, 9),
        (6, 5, 9),
        (7, 6, 10),
        (8, 8, 11),
        (9, 8, 12),
        (10, 2, 14),
        (11, 12, 16),
    ]

    scheduler = Scheduler(processes=[Process(s, f) for _, s, f in processes_data])

    dp_result = scheduler.dynamic_programming()
    print("Dynamic Programming Result:")
    print("Max size:", dp_result[0])
    print("Selected processes:", dp_result[1])
    print(f"Time for 100 runs: {timeit.timeit(lambda: scheduler.dynamic_programming(), number=1000)}")

    greedy_recursive_result = scheduler.greedy_recursive()
    print("\nGreedy Recursive Result:")
    print("Max size:", greedy_recursive_result[0])
    print("Selected processes:", greedy_recursive_result[1])
    print(f"Time for 100 runs: {timeit.timeit(lambda: scheduler.greedy_recursive(), number=1000)}")

    greedy_iterative_result = scheduler.greedy_iterative()
    print("\nGreedy Iterative Result:")
    print("Max size:", greedy_iterative_result[0])
    print("Selected processes:", greedy_iterative_result[1])
    print(f"Time for 100 runs: {timeit.timeit(lambda: scheduler.greedy_iterative(), number=1000)}")
