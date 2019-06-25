#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geocomp.common.prim import *
from .prims import *
from geocomp.common.point import Point
from geocomp.common.segment import Segment

class Edge:
    def __init__(self):
        self.target = None
        self.twin = None
        self.next = None
        self.prev = None
        self.face = None
        self.boundary = False
        self.helper = None
        
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

    def getHelper(self):
        return self.helper

    def setHelper(self, h):
        self.helper = h

    def getOrientedSegment(self):
        a = self.getOrigin().getPoint()
        b = self.getTarget().getPoint()
        return Segment(a, b)
        
    def getSegment(self):
        a = self.getTarget().getPoint()
        b = self.getOrigin().getPoint()

        if below(a, b): a,b = b,a

        return Segment(a, b)
    
    def __str__(self):
        return str(self.getOrigin()) + " " + str(self.getTarget())

class Vertex:
    def __init__(self, point, edge=None):
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
        #list of vertices in the face, in counter-clockwise order
        listV = []
        
        listV.append(self.edge.getTarget().getPoint())

        e = self.edge.getNext()

        while(e != self.edge):
            listV.append(e.getTarget().getPoint())
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

def addVertex(e, x, faces):
    print()
    print()
    print("e = ",e.getOrientedSegment() , " x = ", x.getPoint())
    e1 = e.getPrev()
    print("e1 = ",e1.getOrientedSegment())
    e2 = e.getNext()
    print("e2 = ",e2.getOrientedSegment())

    faces.remove(e.getFace())

    e3 = e.getTwin().getPrev()
    print("e3 = ", e3.getOrientedSegment())
    e4 = e.getTwin().getNext()
    print("e4 = ", e4.getOrientedSegment())

    e.getFace().setEdge(e1)
    #if(not e.getTwin().isBoundary()): e.getTwin().getFace().setEdge(e3)

    e_a = Edge()
    e_b = Edge()
    e_c = Edge()
    e_d = Edge()
    
    e_a.setTarget(x)
    e_b.setTarget(e.getTarget())
    e_c.setTarget(x)
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
    
def splitFace(u, v, h, f, faces):
    # u,v vertices
    # h edge with u as its target
    # f face incident to h
    
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
    u.setEdge(h1)
    v.setEdge(h2)

    h2.setNext(h.getNext()) # h's successor is now h2's successor

    (h2.getNext()).setPrev(h2) # h2's successors's predecessor is now h2

    h1.setPrev(h)
    h.setNext(h1)

    aux = h2

    while aux.getTarget().getPoint() != v.getPoint():
        aux.setFace(f2)
        aux = aux.getNext()

    aux.setFace(f2)

    h1.setNext(aux.getNext())
    (h1.getNext()).setPrev(h1)
    
    aux.setNext(h2)
    h2.setPrev(aux)

    aux = h1

    while aux.getTarget().getPoint() != u.getPoint():
        aux.setFace(f1)
        aux = aux.getNext()
    aux.setFace(f1)
        
    faces.remove(f)
    faces.append(f1)
    faces.append(f2)

def initDCEL(points):
    vertices = []
    edgesCCW = []
    edgesCW = []

    for i in range(len(points)):
        u = points[i]
        v = points[(i+1)%len(points)]

        vertexU = Vertex(u)
        vertexV = Vertex(v)

        e = Edge()
        e.setTarget(vertexV)
        

        e2 = Edge()
        e2.setTarget(vertexU)

        e.setTwin(e2)
        e2.setTwin(e)

        vertexU.setEdge(e)
        vertexV.setEdge(e2)

        edgesCCW.append(e)
        edgesCW.append(e2)
        vertices.append(vertexU)
        
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
    
    for i in reversed(range(len(edgesCW))):
        e = edgesCW[i]
        e_prev = edgesCW[(i+1)%len(edgesCW)]
        e_next = edgesCW[i-1]

        e.setBoundary()
        e.setPrev(e_prev)
        e.setNext(e_next)
    
    return vertices, edgesCCW, faces


def referenceEdge(u,v):
    """
    We need to find the half-edge h that is incident to u and is on the face that contains the diagonal
    u-v.
    To find it, we test every pair of half-edges incident to u and v until we find a pair belonging to
    the same face.

    """
    v1 = u
    v2 = v

    e1 = u.getEdge().getPrev()
    e2 = v.getEdge().getPrev()

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
    
def addDiagonal(u, v, f):
    #print("added diagonal ", u.getPoint(), v.getPoint())
    h = referenceEdge(u, v)
    #u.getPoint().lineto(v.getPoint())
    seg = Segment(u.getPoint(),v.getPoint())
    #seg.hilight("yellow")
    splitFace(u, v, h, h.getFace(), f)

def removeVertex(v, faces):
    e = v.getEdge()
    aux = None
    edgeList = []

    while aux != e:
        if aux is None: aux = e.getTwin().getNext()
        edgeList.append(aux)
        aux = aux.getTwin().getNext()

    for edge in edgeList: #contains every edge that has v as an origin, except for e
        removeEdge(edge, faces)

    e.getOrigin().setEdge(e.getNext())
    e.getNext().setPrev(e.getTwin().getPrev()) #deleting e, which does not create a new face
    e.getTwin().getPrev().setNext(e.getNext())
    del e
    del v
    

def removeEdge(e, faces): #merge Faces
    ePrev = e.getPrev()
    eNext = e.getNext()
    e2 = e.getTwin()
    e2Prev = e2.getPrev()
    e2Next = e2.getNext()
    f1 = e.getFace()
    f2 = e2.getFace()

    eNext.setPrev(e2Prev)
    e2Prev.setNext(eNext)

    ePrev.setNext(e2Next)
    e2Next.setPrev(ePrev)

    f = Face()
    f.setEdge(eNext)
    aux = None
    while aux != eNext:
        if aux is None: aux = eNext
        aux.setFace(f)
        aux = aux.getNext()
        
    faces.remove(f1)
    faces.remove(f2)
    faces.append(f)
    del e
