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
from geocomp.robotmv.tree import *

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

def addDiagonal(u, v, f):
    print("added diagonal ", u.getPoint(), v.getPoint())
    h = referenceEdge(u, v)
    u.getPoint().lineto(v.getPoint())
    splitFace(u, v, h, h.getFace(), f)

def handleStartVertex(v, t, f):
    edge = Segment(v.getPoint(),v.getEdge().getTarget())
    edge.helper = v
    t.insert(edge)

def handleEndVertex(v, t, f):
    e = v.getEdge()
    u = e.helper
    if u and vertexType(u) == "MERGE": addDiagonal(u, v, f)
    segment = Segment(v.getPoint(),e.getTarget())
    t.delete(segment)

def handleSplitVertex(v, t, f):
    e_j = t.getAnt(v.getPoint()) #edge to the left of v in T
    u = e_j.helper
    addDiagonal(u, v, f)
    e_j.helper = v
    
    e = v.getEdge()
    segment = Segment(v.getPoint(),e.getTarget())
    segment.helper = v
    t.insert(segment)

def handleMergeVertex(v, t, f):
    e = v.getEdge().getPrev()
    u = e.helper
    if u and vertexType(u) == "MERGE": addDiagonal(u, v, f)
    segment = Segment(e.getPrev().getTarget(),v.getPoint())
    t.delete(segment)

    e_j = t.getAnt(v.getPoint())
    print("previous on tree: ", e_j)
    u = e_j.helper
    if vertexType(u) == "MERGE": addDiagonal(u, v, f)
    e_j.helper = v

def handleRegularVertex(v, t, f):
    nextV = v.getEdge().getTarget()
    #prevV = v.getEdge().getTwin().getNext().getTarget()

    if nextV.y > v.getPoint().y or (nextV.y == v.getPoint().y and nextV.x < v.getPoint().x): #the interior of P is to the right of v
        e = v.getEdge().getPrev()
        u = e.helper
        if u and vertexType(u) == "MERGE": addDiagonal(u, v, f)
        segment = Segment(e.getPrev().getTarget(),v.getPoint())
        t.delete(segment)
        segment = Segment(v.getPoint(), v.getEdge().getTarget())
        segment.helper = v
        t.insert(segment)
    else:
        e_j = t.getAnt(v.getPoint())
        u = e_j.helper
        if u and vertexType(u) == "MERGE": addDiagonal(u, v, f)
        e_j.helper = v

def handleVertex(v, t, f):
    tp = vertexType(v)
    paintVertex(v, tp)
    if tp == "REGULAR": handleRegularVertex(v, t, f)
    elif tp == "START": handleStartVertex(v, t, f)
    elif tp == "SPLIT": handleSplitVertex(v, t, f)
    elif tp == "MERGE": handleMergeVertex(v, t, f)
    elif tp == "END": handleEndVertex(v, t, f)

def decompose(l):
    Polygon(l).plot("cyan")
    vertices, ccw, faces = initDCEL(l)
    verts = sorted(vertices, key = lambda p: (p.getPoint().y, -p.getPoint().x), reverse = True)
    tree = Tree()

    for p in verts:
        p.getEdge().helper = None
        p.getEdge().getTwin().helper = None
    
    for p in verts: handleVertex(p, tree, faces)

    for f in faces: f.printFace()
