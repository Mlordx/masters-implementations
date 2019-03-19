#!/usr/bin/env python
"""Modulo para leitura de um arquivo de dados"""

from .point import Point

def open_file (name):
	"""Le o arquivo passado, e retorna o seu conteudo
	
	Atualmente, ele espera que o arquivo contenha uma lista de pontos,
	um ponto por linha, as duas coordenadas em cada linha. Exemplo:
	
	0 0
	0 1
	10 100
	
	"""
	f = open (name, 'r')
	#t = range (5000)
	lista = []
	cont = 0

	for linha in f.readlines ():
		if linha[0] == '#': continue

		coord = linha.split()

		fields = len (coord)
		if fields == 0: continue
		if fields != 2: raise 'cada linha deve conter 2 coordenadas'

		x = float (coord[0])
		y = float (coord[1])
		lista.append (Point (x, y))

	return lista

if __name__ == '__main__':
	import sys

	for i in sys.argv[1:]:
		print((i,':'))
		lista = open_file (i)
		print(('  ',repr(len(lista)), 'pontos:'))
		for p in lista:
			print(p)
