#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geocomp import config
from geocomp.common.polygon import Polygon
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.prim import *
from geocomp.common.guiprim import *
from geocomp.robotmv.tree import Tree
from functools import cmp_to_key
from .prims import *
from .graph import *

def shortestPathVisGraph(l):
    s,t = l[0:2]
    verts = l[2:]
    pol = Polygon(verts)

    pol.plot("cyan")

    s.number = 0
    t.number = 1
    
    for i in range(len(verts)):
        verts[i].prev = verts[i-1]
        verts[i].next = verts[(i+1)%len(verts)]
        verts[i].number = i+2
        
    s.prev = s; s.next = s
    t.prev = t; t.next = t
    
    G = Graph(l)

    comp = comparison(s)
    l2 = l[:]
    l2.sort(key = cmp_to_key(comp), reverse = True)
    
    for v in l:
        W = visibleVertices(v,verts)
        for p in W: G.addEdge(v.number,p.number,dist2(v,p)**0.5)
                
    path, distance = G.dijkstra(0,1)
    print(path)
    pol.plot("cyan")
    for i in range(len(path)-1):
        u = path[i]; v = path[i+1]
        l[u].lineto(l[v], 'red')

    s.hilight("yellow"); t.hilight("yellow")

        
def visibleVertices(p,l):
    #l is the list of vertices of the polygon and p is a point in the interior
    comp = comparison(p)
    sorted = l[:]
    sorted.sort(key = cmp_to_key(comp),reverse = True)

    T = Tree()
    n = len(sorted)
    for i in range(n):
        a = l[i]
        b = l[(i+1)%n]
        if intersectsHalfLine(a,b,p):
            if left_on(p,b,a): T.insert(Segment(a,b))
            else: T.insert(Segment(b,a))
                
    W = []
    for i in range(len(sorted)): sorted[i].visible = False
    
    i = 0
    for i in range(n):
        a = sorted[i]
        
        id_a = p.lineto(a,'white')
        a.hilight('green')
        control.sleep()
        a.unhilight()
        
        if visible(T,sorted,p,i):
            if a is not p:
                W.append(a)
                p.remove_lineto(a,id_a)
                p.lineto(a,'blue')
            else: continue
            
        else:
            p.remove_lineto(a,id_a)

        prev = a.prev
        next = a.next

        if prev is next: continue

        if left_on(p,a,prev): T.delete(Segment(prev,a))

        if left_on(p,a,next): T.delete(Segment(next,a))
        else: T.insert(Segment(a,next))
        if right(p,a,prev): T.insert(Segment(a,prev))

    return W


def visible(T, l, p, i):
    a = l[i]
            
    if a is p: # a point sees itself
        a.visible = True
        return a.visible

    if isVertex(p,l) and inside(p.prev,p,p.next,a):
        a.visible = False
        return a.visible

    if isVertex(a,l) and inside(a.prev,a,a.next,p):
        a.visible = False
        return a.visible

    if i == 0 or not collinear(p,l[i-1],a):
        minimum = T.getMin() #returns the leftmost edge
        #minimum = T.getProx(p)
        
        if minimum is None:
            a.visible = True
            return a.visible
        a.visible = not intersectsProp(minimum,Segment(p,a))
    elif not l[i-1].visible:
               a.visible = False
    else:
        if isVertex(l[i-1],l) and inside(l[i-1].prev,l[i-1],l[i-1].next,a):
            a.visible = False
            return a.visible
        
        seg = Segment(l[i-1],a)
        seg2 = T.getProx(l[i-1]) #returns the first obstacle edge to the right of l_{i-1}
        
        if seg2 is None:
            a.visible = True
        else:
          a.visible = not intersectsProp(seg2,seg)

    return a.visible
