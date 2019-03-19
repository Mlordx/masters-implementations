#!/usr/bin/env python
# -*- coding: utf-8 -*-

import heapq

REMOVED = '<removed-task>' 

"""

Implementação de piority queue com possibilidade de atualizar as chaves
sugerida na documentação do Python

"""


class MyPriorityQueue():


    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = 0    # unique sequence count

    def add_task(self,task, priority=0):
        'Add a new task or update the priority of an existing task'
        #print "Pushando", task
        if task in self.entry_finder:
            self.remove_task(task)
        self.counter = self.counter + 1;
        entry = [priority, self.counter, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self,task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = REMOVED


    def isEmpty(self):
        return (len(self.entry_finder) == 0)

    def pop_task(self):
       # print "Popando"
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not REMOVED:
               # print "Popado!", task
                del self.entry_finder[task]
                return task
           # print "Ops...", count
        raise KeyError('pop from an empty priority queue')