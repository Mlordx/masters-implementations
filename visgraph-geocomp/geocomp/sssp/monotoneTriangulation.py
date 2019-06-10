#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque
from geocomp import config
from geocomp.common.polygon import Polygon
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.prim import *
from geocomp.common.guiprim import *
from functools import cmp_to_key
from .prims import *
from .dcel import *


def mergeChains(l):
    n = len(l)
    yMin = 2**30
    yMax = -2**30
    indMin = 0
    indMax = n-1

    for i in range(n):
        if l[i].y == yMax and l[i].x < l[indMax].x: indMax = i
        if l[i].y == yMin and l[i].x > l[indMin].x: indMin = i
        if l[i].y > yMax:
            indMax = i
            yMax = l[i].y
        if l[i].y < yMin:
            indMin = i
            yMin = l[i].y

    chain1 = deque()
    i = (indMin+1)%n
    while i != indMax:
        chain1.appendleft(l[i])
        i = (i+1)%n


    chain2 = deque()
    i = (indMax+1)%n

    while i != indMin:
        chain2.append(l[i])
        i = (i+1)%n

    set1 = set(chain1)
    set2 = set(chain2)
    sortedPoints = deque()

    while chain1 and chain2:
        if chain1[0].y > chain2[0].y:
            sortedPoints.append(chain1[0])
            chain1.popleft()
        elif chain2[0].y > chain1[0].y:
            sortedPoints.append(chain2[0])
            chain2.popleft()
        elif chain1[0].y == chain2[0].y and chain1[0].x < chain2[0].x:
            sortedPoints.append(chain1[0])
            chain1.popleft()
        else:
            sortedPoints.append(chain2[0])
            chain2.popleft()

    while chain1:
        sortedPoints.append(chain1[0])
        chain1.popleft()
    
    while chain2:
        sortedPoints.append(chain2[0])
        chain2.popleft()    

    sortedPoints.append(l[indMin])
    sortedPoints.appendleft(l[indMax])
    return (list(sortedPoints),set1,set2)

def adjacent(p1, p2):
    #print("p1 = ", p1.getPoint(), " p1 edge = ", str(p1.getEdge()))
    #print("p2 = ", p2.getPoint(), " p2 edge = ", str(p2.getEdge()))
    if p1.getEdge().getTarget() == p2.getPoint() or p2.getEdge().getTarget() == p1.getPoint():
        #print(p1.getPoint(), " is adjacent to ", p2.getPoint())
        return True
    else:
        #print(p1.getPoint(), " is NOT adjacent to ", p2.getPoint())
        return False
    
def triangulateMonotone(l, f):
    stack = []
    points, chain1, chain2 = mergeChains(l)

    stack.append(points[0])
    stack.append(points[1])
    diagonals = []
    
    for j in range(2,len(points)-1):
        #print("-------------------------")
       # print("j = ", j, " points[j] = ", points[j].getPoint())
        points[j].getPoint().hilight("red")
        aux = []
        for i in range(len(stack)-1): aux.append(Segment(stack[i].getPoint(),stack[i+1].getPoint()))
        for e in aux: e.plot("green")
        control.sleep()
        for e in aux: e.hide()
        control.sleep()
        points[j].getPoint().unhilight()
        
        if adjacent(points[j], stack[-1]):
            print("CASE A")
            top = stack[-1]
            t = len(stack)-1
            sees = False
            if points[j].getEdge().getTarget() == top.getPoint(): sees = left_on(stack[t], stack[t-1], points[j])
            else: sees = right_on(stack[t], stack[t-1], points[j])
            print("points[j] = ", points[j].getPoint(), " top = ", top.getPoint(), " sees = ", sees)
            while t >= 1 and sees:
                stack.pop()
                t -=1
                print("added diagonal ", Segment(points[j].getPoint(),stack[t].getPoint())) 
                diagonals.append(Segment(points[j].getPoint(),stack[t].getPoint()))
                if points[j].getEdge().getTarget() == top.getPoint(): sees = left_on(stack[t], stack[t-1], points[j])
                else: sees = right_on(stack[t], stack[t-1], points[j])

            stack.append(points[j])
        else:
            print("CASE B")
            top = stack[-1]
            t = len(stack)-1
            while t>=1:
                print("added diagonal ", Segment(points[j].getPoint(),stack[t].getPoint())) 
                diagonals.append(Segment(points[j].getPoint(),stack[t].getPoint()))
                stack.pop()
                t -=1
            stack.pop()
            stack.append(top)
            stack.append(points[j])
            #stack = [top,points[j]]
    print("-------------------------")
    t = len(stack)-1
    print("stack at the end:")
    for p in stack: print(p.getPoint())
    points[-1].getPoint().hilight("red")
    aux = []
    for i in range(len(stack)-1): aux.append(Segment(stack[i].getPoint(),stack[i+1].getPoint()))
    for e in aux: e.plot("green")
    control.sleep()
    for e in aux: e.hide()
    control.sleep()
    points[-1].getPoint().unhilight()

    while t>=2:
        t -=1
        diagonals.append(Segment(points[-1].getPoint(),stack[t].getPoint()))
        stack.pop()
        
    for d in diagonals:
        print(d)
        d.init.lineto(d.to,"yellow")
    #for d in diagonals:
    #    u = d.init
    #    v = d.to
    #    h = referenceEdge(u,v)
    #    splitFace(u,v,h,h.getFace(),f)

    print("\n")
            
def triangulate(l):
    Polygon(l).plot("deep sky blue")
    vertices, ccw, faces = initDCEL(l)
    for v in vertices:
        v.x = v.getPoint().x
        v.y = v.getPoint().y
    triangulateMonotone(vertices, faces)
