#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Primitivas geometricas usadas nos algoritmos

Use o modulo geocomp.common.guiprim para que essas primitivas sejam
desenhadas na tela  medida que elas so usadas. Tambm  possvel
desenh-las de um jeito especfico para um determinado algoritmo.
Veja geocomp.convexhull.quickhull para um exemplo.
"""

# Numero de vezes que a funcao area2 foi chamada
num_area2 = 0
# Numero de vezes que a funcao dist2 foi chamada
num_dist = 0

def area2 (a, b, c):
	"Retorna duas vezes a rea do tringulo determinado por a, b, c"
	global num_area2
	num_area2 = num_area2 + 1
	return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

def left (a, b, c):
	"Verdadeiro se c est  esquerda do segmento orientado ab"
	return area2 (a, b, c) > 0

def left_on (a, b, c):
	"Verdadeiro se c est  esquerda ou sobre o segmento orientado ab"
	return area2 (a, b, c) >= 0

def collinear (a, b, c):
	"Verdadeiro se a, b, c sao colineares"
	return area2 (a, b, c) == 0

def right (a, b, c):
	"Verdadeiro se c est  direita do segmento orientado ab"
	return not (left_on (a, b, c))

def right_on (a, b, c):
	"Verdadeiro se c est  direita ou sobre o segmento orientado ab"
	return not (left (a, b, c))

def dist2 (a, b):
	"Retorna o quadrado da distancia entre os pontos a e b"
	global num_dist
	num_dist = num_dist + 1
	dy = b.y - a.y
	dx = b.x - a.x

	return dy*dy + dx*dx

def get_count ():
	"Retorna o numero total de operacoes primitivas realizadas"
	return num_area2 + num_dist

def reset_count ():
	"Zera os contadores de operacoes primitivas"
	global num_area2, num_dist
	num_area2 = 0
	num_dist = 0
