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
from .dcel import *

def triangulationByEars(lv):
    l = lv[:]
    n = len(l)
    diagonals = []

    Polygon(l).plot("deep sky blue")
    
    for i in range(n):
        j = i-1
        k = (i+1)%n

        l[i].ear = False
        l[i].prev = l[j]
        l[i].next = l[k]
    
    aux = []
    checkEars(l)

    v2 = l[0]
    while len(l) > 3:
        while not v2.ear: v2 = v2.next
        v1 = v2.prev
        v3 = v2.next

        diagonals.append(Segment(v1,v3))
        aux.append(Segment(v1,v3))

        l.remove(v2)
        v1.next = v3
        v3.prev = v1
        
        v1.ear = isEarCorner(l,v1)
        v3.ear = isEarCorner(l,v3)
        
        v2 = v3 #proceeds to the next vertex
        
    for d in diagonals:
        d.init.lineto(d.to,"yellow")

    
    vs, ccw , f = initDCEL(lv)
    
    for i in range(len(lv)): lv[i].vertex = vs[i]
        
    for d in diagonals:
        u = d.init
        v = d.to
        h = referenceEdge(u,v)
        splitFace(u,v,h,h.getFace(),f)
        
    print("\n")
    for face in f: face.printFace()

    return f,diagonals


def triangulation(l):
    return triangulationByEars(l)
