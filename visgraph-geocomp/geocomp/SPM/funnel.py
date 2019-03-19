#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Funnel:
    #implementantion of Funnel structure using a double-ended queue with a history of operations stack
    def __init__(self):
        self.deque = []
        self.history = []
        
    def length(self):
        return len(self.deque)

    def __getitem__(self,i):
        return self.deque[i]
    
    def addFront(self,x):
        self.deque.insert(0,x)
        self.history.append(("addFront",x))
        #print(self.deque," tam = ",self.length())
        
    def addBack(self,x):
        self.deque.append(x)
        self.history.append(("addBack",x))
        #print(self.deque," tam = ",self.length())

    def add(self,c,x):
        if c == 'f': self.addFront(x)
        elif c == 'b': self.addBack(x)
        
    def splitFront(self,i):
        rest = self.deque[i+1:]
        self.deque = self.deque[:i+1]
        self.history.append(("splitFront",rest))
        #print(self.deque," tam = ",self.length())
        return rest

    def splitBack(self,i):
        if i != self.length()-1:
            rest = self.deque[:i]
            self.deque = self.deque[i:]
        else:
            rest = [self.deque[0]]
            self.deque = [self.deque[1]]
        self.history.append(("splitBack",rest))
        #print(self.deque," tam = ",self.length())
        return rest

    def split(self,c,i):
        if c == 'f': self.splitFront(i)
        elif c == 'b': self.splitBack(i)
        
    def itemAt(self,i):
        return self.deque[i]

    def undo(self,k=1):
        for i in range(k):
            recent = self.history.pop(-1)
        
            if recent[0] == "addFront":
                self.deque.pop(0)
        
            elif recent[0] == "addBack":
                self.deque.pop(-1)

            elif recent[0] == "splitFront":
                self.deque.extend(recent[1])

            elif recent[0] == "splitBack":
                recent[1].extend(self.deque)
                self.deque = recent[1]

    def __repr__(self):
        return str(self.deque)

