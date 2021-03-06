#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Controla a visualizacao dos algoritmos do ponto de vista do front-end"""

skip = 0
gui = None

import time
from . import prim
from . import control


def init_display (toolkit, master):
	"Inicializa o toolkit (Tk, GNOME,...) especificado"
	global gui
	gui = toolkit
	gui.init_display (master)
	control.set_gui (gui)

def hide_all ():
	"""Impede que mudancas sejas desenhadas, e passa a ignorar ordens para dormir

	Como, em geral, um algoritmo leva mais tempo para desenhar 
	na tela linhas/pontos/... do que para calcular o que ele precisa,
	 interessante permitir que um algoritmo rode sem que ele mostre nenhuma
	saida, apenas contando o numero de operacoes primitivas realizadas.
	Essa funcao, junto com unhide_all permite isso."""
	global skip
	skip = 1
	control.set_skip (1)

def unhide_all ():
	"""Permite que mudancas sejam desenhadas, e volta e aceitar ordens para dormir

	Veja hide_all"""
	#globals ()['skip'] = 0
	global skip
	skip = 0
	control.set_skip (0)

def config_canvas (pontos):
	"""Configura o canvas para mostrar os pontos passados."""
	
	if len (pontos) == 0: 
		return

	minx = pontos[0].x
	miny = pontos[0].y
	maxx = pontos[0].x
	maxy = pontos[0].y

	for i in pontos[1:]:
		if i.x < minx:
			minx = i.x
		if i.y < miny:
			miny = i.y
		if i.x > maxx:
			maxx = i.x
		if i.y > maxy:
			maxy = i.y
	
	if minx == maxx:
		if minx == 0:
			minx = -1
			maxx = 1
		else:
			minx = int (0.9 * minx)
			maxx = int (1.1 * maxx)
	
	if miny == maxy:
		if miny == 0:
			miny = -1
			maxy = 1
		else:
			miny = int (0.9 * minx)
			maxx = int (1.1 * maxx)


	control.freeze_update ()
	gui.config_canvas (minx, maxx, miny, maxy)

	for p in pontos:
		p.plot ()
	# para "garantir" que os updates nao estao congelados
	control.thaw_update (10000000)

def run_algorithm (alg, input):
	"""roda o algoritmo alg, usando input como entrada
	
	Retorna uma lista contendo o total de operacoes primitivas executadas 
	e uma string opcionalmente retornada pelo algoritmo"""
	config_canvas (input)

	show = 1
	if gui.hide_algorithm ():
		show = 0
		hide_all ()
	
	input_dup = input[:]

	ret = alg (input_dup)

	if not show:
		unhide_all ()
		control.freeze_update ()
		if hasattr (ret, 'hilight'):
			ret.hilight ()
		elif hasattr (ret, 'plot'):
			ret.plot ()
		control.thaw_update ()

	extra_info = None
	if hasattr (ret, 'extra_info'):
		extra_info = ret.extra_info

	cont = prim.get_count ()
	prim.reset_count ()

	return (cont, extra_info)
