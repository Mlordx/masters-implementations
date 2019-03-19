#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Algoritmo de Grafo de Visibilidade"""


from geocomp.common.polygon import Polygon
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.guiprim import *
from geocomp import config
from .tree import Tree
from .minhasPrim import *
from .graph import *
from .robo import Robo
from functools import cmp_to_key


"""Função do algoritmo em si. Supomos aqui que:

-> Os primeiros pontos são o polígono que definem o robo. O
	polígono acaba no momento em que se repete o primeiro ponto.
	Se os 2 primeiros pontos forem iguais, o robo é um robo pontual
	definido por esse ponto repetido.

-> Os outros polígonos, limitados da mesma forma, serão os obstáculos
	do robo. 


"""

def visGraphAlg(l):
	poligs = leEntrada(l)

	robo = poligs[0]
	destino = None

	desenhaTudo(l) #Muito codigo igual ao de baixo...mas deixa

	if(len(robo) == 1):
		print("Robo ponto na posicao ", robo[0]) 
		probo = robo[0]
		destino = poligs[1][0] #Suponho ser um ponto
	else:
		robo = Robo(robo)
		probo = poligs[1][0] # Suponho ser um ponto
		poligs.pop(0) #Removo o polígono do robo da lista, iremos tratar só com o ponto
		destino = poligs[1][0] # Suponho ser um ponto
		for i in range(len(poligs)):
			if(len(poligs[i]) > 1):
				poligs[i] = robo.deformaPolig(poligs[i])
				Polygon(poligs[i]).plot()
				control.sleep()

	pontos = []
	for i in range(len(poligs)):
		poligs[i] = Polygon(poligs[i])
		poligs[i].hilight()
		pontos.extend(poligs[i].to_list())
		control.sleep()


	probo.prev = probo.__next__ = probo

	
	
	compara = criaCompara(probo)
	pontos.sort(key = cmp_to_key(compara), reverse = True)

	
	#Grafo
	G = Grafo(len(pontos))

	#Numerando os pontos
	for i in range(len(pontos)):
		pontos[i].i = i;

	for pi in pontos:
		W = verticesVisiveis(pi, poligs)
		for pj in W:
			G.addAresta(pi.i,pj.i, dist2(pi,pj)**0.5)
		



	path, dist = G.dijkstra(probo.i, destino.i)
	for i in range(len(path)-1):
		v = path[i]; u = path[i+1]
		pontos[v].lineto(pontos[u], 'red')

		




"""

	Testa se o segmento a-b intersecta o segmento
	p.x-inf+

"""

def passaEixoX(a,b,p):
	#Acerta quem é a e b para acertarmos a orientação
	if(a.y < b.y):
		aux = a; a = b; b = aux;
	elif(a.y == b.y):
		if(a.x > b.x):
			aux = a; a = b; b = aux;

	if(a.y > p.y and b.y <= p.y and right(a,b,p)):
		return True #cruza o eixo p.x-inf+
	else: return False






def leEntrada(l):
	poligs = []
	temp = []
	for i in range(len(l)):
		if( len(temp) == 0 ): 
			temp.append(l[i])
		elif( l[i].x == temp[0].x and l[i].y == temp[0].y ):
			poligs.append(temp)
			temp = []
		else:
			temp.append(l[i])
	return poligs


"""
	Cria uma função para comparação angular ao redor do ponto p
	que os ordena em ordem horária a partir do eixo x positivo

"""
def criaCompara(p):
	def menor(a, b):
		if( (p.y == a.y) and (p.y == b.y) ):
			#"Caso degenerado"
			if( (p.x < a.x) != (p.x < b.x) ):
				if(p.x < a.x): return 1
				else: return -1 
			else: #Ve pela distancia
				da = dist2(a,p); db = dist2(b,p);
				if( da < db ): return 1
				elif( da > db): return -1
				else: return 0
		if( ((p.y >= a.y) == (p.y >= b.y))): #Estão no mesmo hemisfério
			#"Caso 1"
			if( left(p,a,b) ): return -1
			elif( collinear(a, b, p) ):
				da = dist2(a,p); db = dist2(b,p);
				if( da < db ): return 1
				elif( da > db): return -1
				else: return 0
			else: return 1 # b esta a direita de p->a
		else: #a e b estão em lados diferentes da bola
			#"Caso2"
			if( a.y <= p.y ): return 1;
			else: return -1
	return menor


"""
A função recebe uma arvore T, um vetor de pontos ordenados
S, ponto de referencia p, e o índice i do ponto que queremos analisar.

Suponho que o teste ja foi feito para S[0..i-1]


"""

def visivel(T, S, p, i):

	a = S[i]
	a.visivel = False #Até que se prove o contrário

	if( a is p):
		a.visivel = True
		return a.visivel

	#Testa se a reta p->s[i] passa por dentro do polígono
	# de p.
	if(p.prev != p): #p está em algum polígono
		if(noCone(p.prev,p,p.next,a) ):
			a.visivel = False
			#Falhou no cone
			return a.visivel


	if(i == 0 or not collinear(p, S[i-1], a)):
		segMin = T.getMin()
		if(segMin is None): 
			a.visivel = True
			#seg min é null
			return a.visivel
		#Testando intersec com min
		a.visivel = not intersectaProp(segMin, Segment(p,a)) 
	elif( not S[i-1].visivel ):
		# Anterior não é visível
		a.visivel = False
	else: 
		if(S[i-1].prev != S[i-1]): #S[i-1] esta em um polígono
			if(noCone(S[i-1].prev, S[i-1], S[i-1].next, a)): 
				a.visivel = False
				print("Falhou no cone 2")
				return a.visivel

		segTemp = Segment(S[i-1],a)
		seg2 = T.getProx(S[i-1])		
		# Testando o segmento do meio #
		
		
		if(seg2 is None): 
			a.visivel = True
		else:
			a.visivel = not intersectaProp(seg2, segTemp)

	return a.visivel


def verticesVisiveis(p, poligs):
	pontos = []
	for i in range(len(poligs)):
		pontos.extend(poligs[i].to_list())
	compara = criaCompara(p)

	#Intersecta p.x -> inf+
	T = Tree();

	pontos.sort(key = cmp_to_key(compara), reverse = True)
	for i in range(len(poligs)):
		listaPs = poligs[i].to_list()
		n = len(listaPs)
		for j in range(n):
			a = listaPs[j]; b = listaPs[(j+1)%n];
			if(passaEixoX(a, b, p)):
				if(left_on(p,b,a)): T.insert(Segment(a,b));
				else: T.insert(Segment(b,a));

	W = []; 
	for i in range(len(pontos)):
		a = pontos[i]

		idBranco = p.lineto(a, 'white')
		a.hilight('yellow')
		control.sleep()
		a.hilight('red')
		a.unhilight()

		if(visivel(T, pontos, p, i)): 
			if(a is not p):
				W.append(a)
				p.remove_lineto(a, idBranco)
				p.lineto(a, 'blue')
			else: continue; 
		else: p.remove_lineto(a, idBranco)
		
		b = a.prev; c = a.next;
		
		if( a.x == b.x and a.y == b.y): continue #a não está em um
                #polígono		
		if(left_on(p,a,b)):
			T.delete(Segment(b,a))
	
		if(left_on(p,a,c)): 
			T.delete(Segment(c,a))

		else:
			T.insert(Segment(a,c))

		#else do primeiro if
		#Tentando evitar q na hora da inserção tenha segmentos terminando
		#na linha de varredura.
		if(right(p,a,b)): 
			T.insert(Segment(a,b))


	return W



def  desenhaTudo(l):
	poligs = leEntrada(l)

	robo = poligs[0]
	probo = destino = None

	if(len(robo) == 1):
		print("Robo ponto na posicao ", robo[0]) 
		probo = robo[0]
		probo.hilight('yellow')
		destino = poligs[1][0] #Suponho ser um ponto
	else:
		for p in robo:
			p.plot("black")
		robo = Robo(robo)
		probo = poligs[1][0] # Suponho ser um ponto
		Polygon(robo.getPontos(probo.x, probo.y)).plot("yellow")
		poligs.pop(0) #Removo o polígono do robo da lista, iremos tratar só com o ponto
		destino = poligs[1][0] # Suponho ser um ponto


	
	for i in range(len(poligs)):
		for p in poligs[i]:
			p.plot()
		if(len(poligs[i]) > 1):
			Polygon(poligs[i]).plot("cyan")

	probo.hilight("green"); destino.hilight("red")
					
			




	
