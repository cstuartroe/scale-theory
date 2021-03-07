import time
from tabulate import tabulate

class Timer:
    def __init__(self):
        self.task_times = {}
        self.task_iterations = {}
        self.current_task = None
        self.current_start_time = None

    def task(self, name):
        if self.current_task:
            self.__clear_certain()

        self.current_task = name
        self.current_start_time = time.time()

    def clear(self):
        if self.current_task:
            self.__clear_certain()

    def __clear_certain(self):
        self.task_times[self.current_task] = self.task_times.get(self.current_task, 0) + \
                                             (time.time() - self.current_start_time)

        self.task_iterations[self.current_task] = self.task_iterations.get(self.current_task, 0) + 1

        self.current_task = None

    def log(self, logger=None):
        s = tabulate(
            [
                (
                    task_name,
                    self.task_times[task_name],
                    self.task_iterations[task_name],
                    self.task_times[task_name]/self.task_iterations[task_name]
                )
                for task_name in self.task_times
            ],
            ("Task name", "Total time", "Number of iterations", "Average time"),
        )

        if logger:
            logger.info(s)
        else:
            print(s)
