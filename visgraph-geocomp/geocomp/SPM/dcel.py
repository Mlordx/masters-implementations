#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geocomp.common.prim import *
from geocomp.common.point import Point


class Edge:
    def __init__(self):
        self.target = None
        self.twin = None
        self.next = None
        self.prev = None
        self.face = None
        self.boundary = False
        
    def setFace(self,f):
        self.face = f

    def setTwin(self,t):
        self.twin = t

    def setNext(self,n):
        self.next = n

    def setPrev(self,p):
        self.prev = p
        
    def setTarget(self,v):
        self.target = v

    def getFace(self):
        return self.face
    
    def getTarget(self):
        return self.target

    def getEdge(self):
        return self.edge

    def getTwin(self):
        return self.twin

    def getNext(self):
        return self.next

    def getPrev(self):
        return self.prev

    def getOrigin(self):
        return self.prev.getTarget()

    def isBoundary(self):
        return self.boundary

    def setBoundary(self):
        self.boundary = True

    def getOppVertex(self):
        return self.getNext().getTarget()
    
    def __str__(self):
        return str(self.getOrigin()) + " " + str(self.getTarget())

class Vertex:
    def __init__(self,point,edge):
        self.point = point
        self.edge = edge

    def setEdge(self,edge):
        self.edge = edge
        
    def getPoint(self):
        return self.point

    def getEdge(self):
        return self.edge

class Face:
    def __init__(self):
        self.edge = None
        
    def setEdge(self,edge):
        self.edge = edge

    def getEdge(self):
        return self.edge

    def listFace(self):
        #list of vertices in the face, in clockwise order
        listV = []
        
        listV.append(self.edge.getTarget())

        e = self.edge.getNext()

        while(e != self.edge):
            listV.append(e.getTarget())
            e = e.getNext()

        return listV

    def printFace(self):
        print(self.listFace())

    def lenFace(self):
        cont = 1

        e = self.edge.getNext()

        while e != self.edge:
            cont+=1
            e = e.getNext()

        return cont

    def returnOppDiagonal(self,v):
        e = self.getEdge()

        aux = e.getNext()
        while aux != e:
            if aux.getTarget() != v and aux.getPrev().getTarget() != v:
                return aux.getTwin()

            aux = aux.getNext()
        
extFace = Face()

def initDCEL(points):
    vertices = []
    edgesCCW = []
    edgesCW = []

    for i in range(len(points)):
        u = points[i]
        v = points[(i+1)%len(points)]

        e = Edge()
        e.setTarget(v)

        e2 = Edge()
        e2.setTarget(u)

        e.setTwin(e2)
        e2.setTwin(e)

        u2 = Vertex(u,e)

        edgesCCW.append(e)
        edgesCW.append(e2)
        vertices.append(u2)
        
    faces = []
    f = Face()
    f.setEdge(edgesCCW[0])
    faces.append(f)
    
    for i in range(len(edgesCCW)):
        e = edgesCCW[i]
        e_prev = edgesCCW[i-1]
        e_next = edgesCCW[(i+1)%len(edgesCCW)]
            
        e.setPrev(e_prev)
        e.setNext(e_next)
        e.setFace(f)

    global extFace
    extFace.setEdge(edgesCW[0])
    for i in reversed(range(len(edgesCW))):
        e = edgesCW[i]
        e_prev = edgesCW[(i+1)%len(edgesCW)]
        e_next = edgesCW[i-1]

        e.setBoundary()
        e.setFace(extFace)
        e.setPrev(e_prev)
        e.setNext(e_next)
    
    return vertices,edgesCCW,faces


def referenceEdge(u,v):
    """
    We need to find the half-edge h that is incident to u and is on the face that contains the diagonal
    u-v.
    To find it, we test every pair of half-edges incident to u and v until we find a pair belonging to
    the same face.

    """
    v1 = u.vertex
    v2 = v.vertex

    e1 = u.vertex.getEdge().getPrev()
    e2 = v.vertex.getEdge().getPrev()

    aux = None #aux is an half-edge incident to u    
    while aux != e1:
        if aux is None: aux = e1
        aux2 = None #aux2 is an half-edge incident to v

        while aux2 != e2:
            if aux2 is None: aux2 = e2
            if aux.getFace() == aux2.getFace(): return aux
            aux2 = aux2.getNext().getTwin()            

        aux = aux.getNext().getTwin()

    return e1

def splitFace(u,v,h,f,faces):
    # u,v vertices
    # h edge with u as its target
    # f face incident to h

    faces.remove(f)
    
    f1 = Face()
    f2 = Face()
    h1 = Edge()
    h2 = Edge()

    f1.setEdge(h1)
    f2.setEdge(h2)
    
    h1.setTwin(h2)
    h2.setTwin(h1)

    h1.setTarget(v)
    h2.setTarget(u)
    u.vertex.setEdge(h1)
    v.vertex.setEdge(h2)

    h2.setNext(h.getNext()) # h's successor is now h2's successor

    (h2.getNext()).setPrev(h2) # h2's successors's predecessor is now h2

    h1.setPrev(h)
    h.setNext(h1)

    aux = h2
    while aux.getTarget() != v:
        aux.setFace(f2)
        aux = aux.getNext()

    aux.setFace(f2)

    h1.setNext(aux.getNext())
    (h1.getNext()).setPrev(h1)
    
    aux.setNext(h2)
    h2.setPrev(aux)

    aux = h1

    while aux.getTarget() != u:
        aux.setFace(f1)
        aux = aux.getNext()
    aux.setFace(f1)

    faces.append(f1)
    faces.append(f2)
    f2.father = u

def addVertex(e,x,faces):
    print()
    print()
    print("e = ",e, " x = ",x.getPoint())
    e1 = e.getPrev()
    print("e1 = ",e1)
    e2 = e.getNext()
    print("e2 = ",e2)

    faces.remove(e.getFace())

    e3 = e.getTwin().getPrev()
    print("e3 = ",e3)
    e4 = e.getTwin().getNext()
    print("e4 = ",e4)

    e.getFace().setEdge(e1)
    if(not e.getTwin().isBoundary()): e.getTwin().getFace().setEdge(e3)

    e_a = Edge()
    e_b = Edge()
    e_c = Edge()
    e_d = Edge()
    
    e_a.setTarget(x.getPoint())
    e_b.setTarget(e.getTarget())
    e_c.setTarget(x.getPoint())
    e_d.setTarget(e.getTwin().getTarget())
    
    e_a.setTwin(e_d)
    e_b.setTwin(e_c)
    e_c.setTwin(e_b)
    e_d.setTwin(e_a)

    e_a.setFace(e.getFace())
    e_b.setFace(e.getFace())
    e_c.setFace(e.getTwin().getFace())
    e_d.setFace(e.getTwin().getFace())
    
    e_a.setNext(e_b)
    e_b.setPrev(e_a)

    e_c.setNext(e_d)
    e_d.setPrev(e_c)

    e_a.setPrev(e1)
    e1.setNext(e_a)

    e_b.setNext(e2)
    e2.setPrev(e_b)

    e3.setNext(e_c)
    e_c.setPrev(e3)

    e_d.setNext(e4)
    e4.setPrev(e_d)

    x.setEdge(e_b)

    faces.append(e1.getFace())
    print()
    print()
