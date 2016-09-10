from Queue import PriorityQueue
pq=PriorityQueue()

pq.put((1,"priority 1-1"))
pq.put((9,"priority 9-1"))
pq.put((12,"priority 12"))
pq.put((6,"priority 6"))
pq.put((-1,"priority -1"))
pq.put((45,"priority 45"))
pq.put((7,"priority 7"))
pq.put((9,"priority 9-2"))
pq.put((1,"priority 1-2"))

while True:
    print pq.get()[1]
    if pq.empty():
        break
