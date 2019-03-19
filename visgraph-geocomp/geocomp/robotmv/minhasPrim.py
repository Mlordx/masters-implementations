#!/usr/bin/env python
# -*- coding: utf-8 -*-


from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.prim import *
import math


def intersectaProp(seg1, seg2):
	a = seg1.init; b = seg1.to; c = seg2.init; d = seg2.to;
	if(collinear(a,b,c) or collinear(a,b,d) or collinear(c,d,a) or collinear(c,d,b)):
			return False
	else:
		return ( (left(a,b,c) ^ left(a,b,d)) and (left(c,d,a) ^ left(c,d,b)) )

def intersecta(seg1, seg2):
	if(intersectaProp(seg1,seg2)): return True
	a = seg1.init; b = seg1.to; c = seg2.init; d = seg2.to;
	return (entre(seg1, c) or entre(seg1, d) or entre(seg2, a) or entre(seg2, b))


def entre(seg1, c):
	a = seg1.init; b = seg1.to;
	if(not collinear(a,b,c)): return False
	if(a.x != b.x):
		return ((a.x <= c.x and c.x <= b.x) or (b.x <= c.x and c.x <= a.x))
	else:
		return ((a.y <= c.y and c.y <= b.y) or (b.y <= c.y and c.y <= a.y))

#Teste se o ponto d esta no cone definido por a->b->c

def noCone(a, b, c, d):
	if(left_on(a,b,c)): #convexo
		return (left(b,d,a) and left(d,b,c))
	else:
		return not (left_on(d,b,a) and left_on(b,d,c))


"""
Essa função pega uma lista e da um roll de n. Vou explicar
melhor depois...


"""


def shift(seq, n):
        return seq[n:] + seq[:n]



"""
Angulo formado entre p1->p2 e o eixo x no sentido
anti-horário 

"""

def anguloX(p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        if(dy == 0 and dx == 0): return 0
        if(dy >= 0): return math.atan2(dy, dx)
        #dy é negativo
        return math.atan2(dy,dx) + 2*math.pi


"""

Retorna -1 se ang(v1,v2) < ang(w1,w2)
Retorna 0 se ang(v1,v2) == ang(w1,w2)
Retorna 1 se ang(v1,v2) > ang(w1,w2)

"""

def menorAnguloX(v1,v2, w1, w2):
        a = Point(v2.x - v1.x, v2.y - v1.y)
        b = Point(w2.x - w1.x, w2.y - w1.y)
        if((a.y >= 0) != (b.y >= 0)):
                if(a.y >= 0):
                        return -1
                else: 
                        return 1
        else:
                if(left(Point(0,0), a, b)):
                        return -1;
                elif(right(Point(0,0), a, b)):
                        return 1;
                else: return 0;
                
                



"""
Retorna o polígono que seria a soma de minkowski
de dois poligonos com lista de pontos l1 e l2


"""



def somaMinkowski(lista1, lista2):
        n = len(lista1); m = len(lista2);
        #l1 e l2 serão as listas deslocadas de forma que
        #o primeiro ponto tenha coordenada minima dentre os
        #pontos do polígono
        
        pmin = lista1[0]
        imin = 0
        for i in range(len(lista1)):
                p = lista1[i]
                if(p.y < pmin.y):
                        pmin = p
                        imin = i
                elif(p.y == pmin.y and p.x < pmin.x):
                        pmin = p
                        imin = i
        l1 = shift(lista1, imin)
        
        pmin = lista2[0]
        imin = 0
        for i in range(len(lista2)):
                p = lista2[i]
                if(p.y < pmin.y):
                        pmin = p
                        imin = i
                elif(p.y == pmin.y and p.x < pmin.x):
                        pmin = p
                        imin = i
        l2 = shift(lista2, imin)

        # adicionando sentinelas...

        l2.append(l2[0]); l2.append(l2[1]);
        l1.append(l1[0]); l1.append(l1[1]);


        i = 0; j = 0;
        soma = []
        while True:
                soma.append(Point(l1[i].x + l2[j].x, l1[i].y + l2[j].y))
                

                ### condições de parada
                if(i == n):
                        j = j + 1
                elif(j == m):
                        i = i + 1
                #####

                elif(menorAnguloX(l1[i],l1[i+1],l2[j],l2[j+1]) == -1): 
                        i = i + 1
                elif(menorAnguloX(l1[i],l1[i+1],l2[j],l2[j+1]) == 1): 
                        j = j + 1
                else:
                        i = i + 1
                        j = j + 1
                if(i == n and j == m): break;
        
        return soma


