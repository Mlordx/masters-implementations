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

def addDiagonal(u, v, f):
    print("added diagonal ", u.getPoint(), v.getPoint())
    h = referenceEdge(u, v)
    print(h)
    splitFace(u, v, h, h.getFace(), f)


def triangulationByEars(lv):
    l = lv[:]
    n = len(l)
    diagonals = []

    Polygon(l).plot("deep sky blue")
    vs, ccw , f = initDCEL(lv)    
    for i in range(n):
        j = i-1
        k = (i+1)%n

        lv[i].vertex = vs[i]
        l[i].vertex = vs[i]
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

        diag = Segment(v1,v3)
        diagonals.append(diag)
        diag.hilight("yellow")
        addDiagonal(v1.vertex, v3.vertex, f)

        l.remove(v2)
        v1.next = v3
        v3.prev = v1
        
        v1.ear = isEarCorner(l,v1)
        v3.ear = isEarCorner(l,v3)
        
        v2 = v3 #proceeds to the next vertex
        
    print("\n")
    for face in f: face.printFace()

    return f,diagonals

def triangulation(l):
    return triangulationByEars(l)
