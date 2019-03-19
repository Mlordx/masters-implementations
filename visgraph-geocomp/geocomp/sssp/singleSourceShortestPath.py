#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geocomp import config
from geocomp.common.polygon import Polygon
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.prim import *
from geocomp.common.guiprim import *
from functools import cmp_to_key
from .prims import *
from .triangulation import *
from .funnel import *
import math

def singleSourceShortestPath(l):
    source = l[0]

    for v in l: v.predecessor = v

    source.predecessor = None
    
    print(source)

    faces,diagonals = triangulation(l)

    sourceF = source.vertex.getEdge().getFace()

    for d in diagonals: d.plot('yellow')
    
    recursivePath(source)#,sourceF)

    for d in diagonals: d.hide()
    for v in l:
        aux = v

        while aux != source:
            aux.lineto(aux.predecessor,'red')
            aux = aux.predecessor
            
    for v in l:
        if v is source: v.hilight("blue")
        else: v.hilight()
        
def recursivePath(s):
    d = s.vertex.getEdge().getNext() 

    print("s = ", s, "  d = ", d)
    funnel = Funnel()
    
    a = d.getTarget()
    b = d.getPrev().getTarget()

    funnel.add('b',a); funnel.add('b',s); funnel.add('b',b); #initial Funnel

    a.predecessor = b.predecessor = s

    splitFunnel(d,funnel,1)


def splitFunnel(d,f,i,side=None):
    print()
    print()
    #d a certain diagonal
    #f is the funnel associated with d
    #i is the index of the apex of f
    a = f[i]

    d = d.getTwin()

    if d.isBoundary(): return #d is a boundary edge

    x = d.getOppVertex()

    if x.predecessor != x: return

    print("DIAGONAL = ",d, "::::: vertice oposto = ",x)
    print("FUNIL: ",f.deque, "apice = ", a)
    
    ######## animation commands ##############
    polyF = Polygon(f.deque)
    polyF.plot('forest green')
    control.sleep()
    new_d = Segment(d.getOrigin(),d.getTarget())
    new_d.plot("lemon chiffon")
    a.hilight('firebrick')
    x.hilight('deep pink')
    control.sleep()
    ##################################################

    d1 = d.getPrev()
    d2 = d.getNext()
    if f.length() >= 3:

        v1 = f[i-1]
        v2 = f[i+1]

        bla = 0

        if right(a,v1,x) and left(a,v2,x): #v = a
            v = a
            k = i
            bla = 1
        elif left_on(a,v1,x) and left(a,v2,x): #search upper chain

            for m in range(0,i):
                if m == i-1: break
                if right(f[m],f[m+1],x) and left(f[m],f[m-1],x): break

            v = f[m]
            k = m
            bla = 2 
        elif right(a,v1,x) and right_on(a,v2,x): #search lower chain

            for m in range(i+1,f.length()):
                if m == f.length()-1: break
                if right(f[m],f[m+1],x) and left(f[m],f[m-1],x): break
                
            v = f[m]
            k = m
            bla = 3

        print(bla," v = ", v)
        x.predecessor = v
        ######## animation commands ##############
        new_seg = Segment(v,x)
        new_seg.plot('deep pink')
        control.sleep()
        new_seg.hide()
        control.sleep()
        polyF.hide()
        new_d.hide()
        a.unhilight()
        x.unhilight()
        ##################################################
        
        if 0 < k and k < i : #vertex is in the upper chain
            
            f.split('f',k); f.add('b',x);
            splitFunnel(d1,f,k)
            f.undo(); f.undo();

            f.split('b',k);
            f.add('f',x)
            splitFunnel(d2,f,i-k+1)
            f.undo(); f.undo()
            
        if i <= k and k < f.length()-1: #vertex is in the lower chain
            f.split('f',k); f.add('b',x)
            splitFunnel(d1,f,i)
            f.undo(); f.undo();

            f.split('b',k); f.add('f',x)
            splitFunnel(d2,f,1)
            f.undo(); f.undo();
        else:
            if k == 0: #vertex is the first in the funnel
                f.add('f',x)
                # pol = Polygon(f.deque)
                # pol.plot("light slate blue")
                # seg = Segment(d2.getTarget(),d2.getOrigin())
                # seg.plot("red")
                # control.sleep()
                # pol.hide()
                # seg.hide()
                splitFunnel(d2,f,i+1)
                f.undo()

                newFunnel = Funnel()
                newFunnel.add('f',x)
                newFunnel.add('f',f[0])
                splitFunnel(d1,newFunnel,0,side='upper')
                
            elif k == f.length()-1: #vertex is the last in the funnel
                f.add('b',x);
                splitFunnel(d1,f,i)
                f.undo()

                newFunnel = Funnel()
                newFunnel.add('f',f[f.length()-1])
                newFunnel.add('f',x)
                splitFunnel(d2,newFunnel,1,side='lower')
        
    else: #degenerate funnel
        x.predecessor = a

        ######## animation commands ##############
        new_seg = Segment(a,x)
        new_seg.plot('deep pink')
        control.sleep()
        new_seg.hide()
        control.sleep()
        polyF.hide()
        new_d.hide()
        a.unhilight()
        x.unhilight()
        ##################################################

        if i == 1:
            print("AAAAAAAA")
            f.add('b',x)
            # pol = Polygon(f.deque)
            # pol.plot("light slate blue")
            # seg = Segment(d1.getTarget(),d1.getOrigin())
            # seg.plot("red")
            # control.sleep()
            # pol.hide()
            # seg.hide()
            splitFunnel(d1,f,1)
            f.undo()
            
            #f.split('b',1);f.add('f',x)
            newFunnel = Funnel()
            newFunnel.deque = [x,f[1]]
            
            # pol = Polygon(newFunnel.deque)
            # pol.plot("light slate blue")
            # seg = Segment(d2.getTarget(),d2.getOrigin())
            # seg.plot("red")
            # control.sleep()
            # pol.hide()
            # seg.hide()
            splitFunnel(d2,newFunnel,1)
            #f.undo(); f.undo()


        elif i == 0:
            print("BBBBBB")
            f.add('f',x)
            # pol = Polygon(f.deque)
            # pol.plot("light slate blue")
            # seg = Segment(d2.getTarget(),d2.getOrigin())
            # seg.plot("red")
            # control.sleep()
            # pol.hide()
            # seg.hide()
            splitFunnel(d2,f,1)
            f.undo()

            #f.split('f',1);f.add('b',x)
            newFunnel = Funnel()
            newFunnel.deque = [f[0],x]
            # pol = Polygon(newFunnel.deque)
            # pol.plot("light slate blue")
            # seg = Segment(d1.getTarget(),d1.getOrigin())
            # seg.plot("red")
            # control.sleep()
            # pol.hide()
            # seg.hide()
            splitFunnel(d1,newFunnel,1)
            #f.undo(); f.undo()
            
