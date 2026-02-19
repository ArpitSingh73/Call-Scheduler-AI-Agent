from collections import deque

my_queue = deque()
# Enqueue (add) items to the right end
my_queue.append("Task 1")
my_queue.append("Task 2")
my_queue.append("Task 3")

while(not len(my_queue) == 0):
    print(my_queue.popleft()) 