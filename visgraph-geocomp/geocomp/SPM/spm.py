#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geocomp import config
from geocomp.common.polygon import Polygon
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.prim import *
from geocomp.common.guiprim import *
from geocomp.sssp.singleSourceShortestPath import *
from functools import cmp_to_key
from .prims import *
from .triangulation import *
from .funnel import *
from .dcel import *
import math
    
    
def shortestPathMap(l):
    singleSourceShortestPath(l)
    verts, edges, faces = initDCEL(l)

    for i in range(len(verts)):
        l[i].vertex = verts[i] #clearing the triangulation DCEL on the points
        
    source = l[0]
    print("FACE ORIGINAL:")
    faces[0].printFace()
    print()
    faces[0].father = source

    l2 = []

    l[0].dist = 0

    for i in range(1,len(verts)):
        aux = l[i]
        l[i].dist = 0
        while aux.predecessor != None:
            l[i].dist += dist2(aux,aux.predecessor)
            aux = aux.predecessor
    
    for i in range(len(l)):
        a = l[i]
        b = l[(i+1)%len(l)]
        pathA = []
        pathB = []
        newPoints = []
        
        a2 = a
        while a2 != None:
            pathA.insert(0,a2)
            a2 = a2.predecessor

        b2 = b
        while b2 != None:
            pathB.insert(0,b2)
            b2 = b2.predecessor

        print("##################################################")
        print("a ",a," b ",b)
        #print("pathA ",pathA," pathB ",pathB)

        ind = 0
        if len(pathA) > len(pathB):
            for k in range(len(pathA)):
                if k < len(pathB) and pathA[k] == pathB[k]: ind = k
            apex = pathA[ind]
        else:
            for k in range(len(pathB)):
                if k < len(pathA) and pathA[k] == pathB[k]: ind = k
            apex = pathB[ind]
            
        pathA = list(reversed(pathA[ind+1:]))
        pathB = pathB[ind+1:]
            
        funnel = pathA + [apex] + pathB
        apex_i = len(funnel) - len(pathB) -1
        print(funnel)
        print()
        e = a.vertex.getEdge()
        while e.getTarget() != b:
            e = e.getTwin().getNext()
        
        if ind == -1: continue
        if len(funnel) == 2: continue
        for j in range(len(funnel)-1):
            u = funnel[j]
            v = funnel[j+1]

            x,y = intersectionPoint(a, b, u, v)
            print(x,y)
            if not (x == u.x and y == u.y) and not(x == v.x and y == v.y):
                p = Point(x, y)
                p.dist = 0
                newVertex = Vertex(p, None)
                p.vertex = newVertex
                addVertex(e, newVertex, faces)
                e = newVertex.getEdge()
                l2.append(p)


                if j < apex_i:
                    print("Inseri1 ", u, p)
                    addDiagonal(u.vertex, p.vertex, faces)

                    aux = p
                    p.predecessor = u
                    while aux.predecessor != None:
                        p.dist += dist2(aux, aux.predecessor)
                        aux = aux.predecessor
                    
                else:
                    print("Inseri2 ", v, p)
                    addDiagonal(v.vertex, p.vertex, faces)
                    
                    aux = p
                    p.predecessor = v
                    while aux.predecessor != None:
                        p.dist += dist2(aux, aux.predecessor)
                        aux = aux.predecessor
                    
            elif x == u.x and y == u.y:
                ve = v.vertex
                e1 = ve.getEdge()
                aux = None
                cont = False
                while aux != e1:
                    if aux is None: aux = e1

                    if aux.getTarget() == u: cont = True

                    aux = aux.getTwin().getNext()

                if cont: continue
                print("Inseri3 ", v, u)
                addDiagonal(v.vertex, u.vertex, faces)
                
            elif x == v.x and y == v.y:
                ve = u.vertex
                e1 = ve.getEdge()
                aux = None
                cont = False
                while aux != e1:
                    if aux is None: aux = e1

                    if aux.getTarget() == v: cont = True

                    aux = aux.getTwin().getNext()
                if cont: continue

                print("Inseri4 ", u, v)
                addDiagonal(u.vertex, v.vertex, faces)

        print("##################################################")

    for f in faces:
        lf = f.listFace()
        print("face = ",lf)

        for i in range(len(lf)):
            aux = Segment(lf[i],lf[(i+1)%len(lf)])
            aux.plot("purple")
            control.sleep()
            aux.hide()
        
        for i in range(len(lf)):
            lf[i].lineto(lf[(i+1)%len(lf)],'steel blue')
            #control.sleep()
        lf.sort(key = lambda x: x.dist)
        f.father = lf[0]

        f.father.hilight("yellow")
        control.sleep()
        f.father.unhilight()

