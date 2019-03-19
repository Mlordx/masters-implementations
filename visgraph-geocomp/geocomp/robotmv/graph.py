#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .myPriorityQueue import MyPriorityQueue


class Grafo:
	def __init__(self, V):
		self.V = V
		self.adj = [[] for i in range(V)]

	def addAresta(self, a, b, w):
		aresta = Aresta(a,b,w);
		if(self.adjacente(a,b)): return;
		self.adj[a].append(aresta)
		self.adj[b].append(aresta)

	def listaAdj(self, a):
		return self.adj[a]

	def adjacente(self,a,b):
		for edg in self.adj[a]:
			if(edg.ponta(a) == b): return True
		return False

		#Calcula um s-t caminha de peso mínimo
	def dijkstra(self, s, t):
		Q = MyPriorityQueue() #Heap
		# S[0..V-1] um vetor onde S[v] é True <=> v está em S
		S = [False for x in range(self.V)]
		prnt = [-1 for x in range(self.V)]
		dist = [float("inf") for i in range(self.V)]
		for i in range(self.V):
			if(i == s): dist[i] = 0
			Q.add_task(i,dist[i])

		while(not Q.isEmpty()):
			u = Q.pop_task();
			S[u] = True;
			for edg in self.adj[u]:
				v = edg.ponta(u)
				if(dist[v] > dist[u] + edg.w):
					dist[v] = dist[u] + edg.w
					Q.add_task(v, dist[v]) #Atualiza o peso no Heap
					prnt[v] = u

		#Vamos monstar uma lista com os vértices do caminho.
		pilhaTemp = []
		v = t
		while(v != -1):
			pilhaTemp.append(v)
			v = prnt[v]

		path = []
		while pilhaTemp:
			path.append(pilhaTemp.pop())

		return (path, dist[t])


class Aresta:
	def __init__(self, a, b, w):
		self.a = a
		self.b = b
		self.w = w

	def ponta(self, x):
		if(x == self.a): return self.b
		elif(x == self.b): return self.a
		else: return None #Uso indevido do método



