from collections import deque

class Task:
    def __init__(self, pool):
        self.generator = self.main()
        pool.add(self)
    def main(self):
        "Must be a generator"
        pass

class TaskPool:
    """
    NOTE max speed ~~ 20000 task switches per second per 100MHz
    NOTE using pyrex or psyco ~~ 25% speed improvement
    NOTE ram usage ~~ 1KB per task
    """
    def __init__(self):
        self.tasks = deque()
    def add(self, task):
        self.tasks.append(task)
    def iteration(self, iter_cnt=1):
        tasks = self.tasks
        for i in range(iter_cnt):
            try:
                tasks[0].generator.next()
                tasks.rotate(-1)
            except StopIteration:
                del tasks[0]
            except IndexError:
                # allow internal exception to propagate
                if len(tasks) > 0: raise


#### EXAMPLE #########################################################

class ExampleTask(Task):
    def __init__(self, pool, name, max_iterations):
        self.name = name
        self.max_iterations = max_iterations
        Task.__init__(self, pool)
    def main(self):
        i = 0
        while i < self.max_iterations:
            print self.name, i
            i += 1
            yield 0
        print self.name, 'finishing'

pool = TaskPool()
task_a = ExampleTask(pool, 'AAA',  5)
task_b = ExampleTask(pool, 'bbb', 10)
for i in xrange(100):
    pool.iteration()
