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

def above(a, b): #returns TRUE if a lies above b
    if a.y > b.y: return True
    if a.x == b.x and a.x < b.x: return True
    return False

def below(a, b):
    return not above(a, b)

def vertexType(p):
    v = p.getPoint()
    nextV = p.getEdge().getTarget().getPoint()
    prevV = p.getEdge().getTwin().getTarget().getPoint()

    if (above(nextV,v) and below(prevV,v)) or (above(antV,v) and below(prevV,v)):
        return "REGULAR" #return 1
    elif below(nextV,v) and below(prevV,v):
        if left_on(nextV,prevV,v) and right_on(prevV,v,nextV): #angle less than pi
            return "START" #return 2
        else:
            return "SPLIT" #return 3
    else:
      if left_on(nextV,prevV,v) and right_on(prevV,v,nextV): #angle less than pi
          return "END" #return 4
      else:
          return "MERGE" #return 5

def paintVertices(l):
    for p in l:
        aux = vertexType(p)
        if aux == "REGULAR": p.hilight("red")
        elif aux == "START": p.hilight("blue")
        elif aux == "SPLIT": p.hilight("green")
        elif aux == "END": p.hilight("yellow")
        else: p.hilight("pink")
