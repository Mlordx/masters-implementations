#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.prim import *
import math

def isVertex(p,l):
    # True if p belongs to the polygon border
    if p in l: return True
    return not p is p.prev
    
def inside(a, b, c, d):
    #True if d is inside the triangle abc
    if left_on(a,b,c): return left(b,d,a) and left(d,b,c)
    else: return not (left_on(d,b,a) and left_on(b,d,c))
    
def intersectsProp(seg1, seg2):
    # True if seg1 intersects properly with seg2
    a = seg1.init; b = seg1.to; c = seg2.init; d = seg2.to;
    if(collinear(a,b,c) or collinear(a,b,d) or collinear(c,d,a) or collinear(c,d,b)):
        return False
    else: return (left(a,b,c) ^ left(a,b,d)) and (left(c,d,a) ^ left(c,d,b))

def intersects(seg1, seg2):
    # True if seg1 intersects with seg2
    if intersectaProp(seg1,seg2): return True
    a = seg1.init; b = seg1.to; c = seg2.init; d = seg2.to;
    return between(seg1, c) or between(seg1, d) or between(seg2, a) or between(seg2, b)

def between(seg1, c):
    # True if c is inside seg1
    a = seg1.init; b = seg1.to;
    if not collinear(a,b,c): return False
    
    if(a.x != b.x): return (a.x <= c.x and c.x <= b.x) or (b.x <= c.x and c.x <= a.x)
    else: return (a.y <= c.y and c.y <= b.y) or (b.y <= c.y and c.y <= a.y)           

def intersectsHalfLine(a, b, p):
    # True if the segment a->b intersects the half-line p->+inf
    if a.y < b.y: a,b = b,a
    elif a.y == b.y:
        if a.x > b.x: a,b = b,a

    if a.y > p.y and b.y <= p.y and right(a,b,p): return True
    else: return False

def comparison(p):
    # Comparison class for clockwise angular sorting around a given point 'p'
    def less(a,b):
        if p.y == a.y and p.y == b.y:
            if (p.x < a.x) != (p.x < b.x):
                if p.x < a.x: return 1
                else: return -1
            else:
                distA = dist2(a,p); distB = dist2(b,p)
                if distA < distB: return 1
                elif distA > distB: return -1
                else: return 0

        if (p.y >= a.y) == (p.y >= b.y):
            if left(p,a,b): return -1
            elif collinear(a,b,p):
                distA = dist2(a,p); distB = dist2(b,p)
                if distA < distB: return 1
                elif distA > distB: return -1
                else: return 0
            else: return 1
        else:
            if a.y <= p.y: return 1
            else: return -1

    return less
