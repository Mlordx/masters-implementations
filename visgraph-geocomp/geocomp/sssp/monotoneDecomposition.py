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
from .tree import *

def vertexType(p):
    v = p.getPoint()
    nextV = p.getEdge().getTarget()
    prevV = p.getEdge().getTwin().getNext().getTarget()

    if (above(nextV,v) and below(prevV,v)) or (above(prevV,v) and below(nextV,v)):
        return "REGULAR" #return 1
    elif below(nextV,v) and below(prevV,v):
        if left_on(v,nextV,prevV) and right_on(v,prevV,nextV): #angle less than pi
            return "START" #return 2
        else:
            return "SPLIT" #return 3
    else:
        if left_on(v,nextV,prevV) and right_on(v,prevV,nextV): #angle less than pi
            return "END" #return 4
        else:
            return "MERGE" #return 5

def paintVertex(v, t):    
    if t == "REGULAR": v.getPoint().hilight("red")
    elif t == "START": v.getPoint().hilight("blue")
    elif t == "SPLIT": v.getPoint().hilight("green")
    elif t == "END": v.getPoint().hilight("yellow")
    else: v.getPoint().hilight("pink") #MERGE
    control.sleep()

def handleStartVertex(v, t, f):
    v.getEdge().setHelper(v)

    print("Inserted ", v.getEdge().getSegment(), " on the tree, with helper ", v.getEdge().getHelper().getPoint())
    print()
    t.insert(v.getEdge())
    

def handleEndVertex(v, t, f):
    e = v.getEdge()
    u = e.getHelper()
    if u and vertexType(u) == "MERGE": addDiagonal(u, v, f)

    print("Removed ", e.getSegment(), " from the tree")
    print()
    t.delete(e)

def handleSplitVertex(v, t, f):
    e_j = t.getAnt(v.getPoint()) #edge to the left of v in T
    u = e_j.getHelper()
    addDiagonal(u, v, f)
    e_j.setHelper(v)
    
    e = v.getEdge()
    e.setHelper(v)

    print("Inserted ", e.getSegment(), " on the tree, with helper ", e.getHelper().getPoint())
    print()
    t.insert(e)

def handleMergeVertex(v, t, f):
    e = v.getEdge().getPrev()
    u = e.getHelper()
    if u and vertexType(u) == "MERGE": addDiagonal(u, v, f)
    print("Removed ", e.getSegment(), " from tree")
    print()
    t.delete(e)

    e_j = t.getAnt(v.getPoint())
    u = e_j.getHelper()
    if vertexType(u) == "MERGE": addDiagonal(u, v, f)
    e_j.setHelper(v)
    print(e_j.getSegment(), " new helper = ", e_j.getHelper().getPoint())
    print()

def handleRegularVertex(v, t, f):
    nextV = v.getEdge().getTarget()

    if below(nextV, v.getPoint()): #the interior of P is to the right of v
        e = v.getEdge().getPrev()
        u = e.getHelper()
        if u and vertexType(u) == "MERGE": addDiagonal(u, v, f)
        print("Removed ", e.getSegment(), " from tree")
        t.delete(e)

        e = v.getEdge()
        e.setHelper(v)
        print("Inserted ", e.getSegment(), " on the tree, with helper ", e.getHelper().getPoint())
        t.insert(e)
    else:
        e_j = t.getAnt(v.getPoint())
        u = e_j.getHelper()
        #print("previous on tree: ", e_j, " with helper ", e_j.getHelper().getPoint())
        if u and vertexType(u) == "MERGE": addDiagonal(u, v, f)
        e_j.setHelper(v)
        print(e_j.getSegment(), " new helper = ", e_j.getHelper().getPoint())

    print()


def handleVertex(v, t, f):
    print("vertex = ", v.getPoint())
    tp = vertexType(v)
    paintVertex(v, tp)
    if tp == "REGULAR": handleRegularVertex(v, t, f)
    elif tp == "START": handleStartVertex(v, t, f)
    elif tp == "SPLIT": handleSplitVertex(v, t, f)
    elif tp == "MERGE": handleMergeVertex(v, t, f)
    elif tp == "END": handleEndVertex(v, t, f)
    print("tree = ", t)
    print("-------------\n")

def decompose(l):
    Polygon(l).plot("cyan")
    vertices, ccw, faces = initDCEL(l)
    verts = sorted(vertices, key = lambda p: (p.getPoint().y, -p.getPoint().x), reverse = True)
    tree = Tree()

    for p in verts: handleVertex(p, tree, faces)

    for f in faces: f.printFace()
    return faces
