# -*- coding: utf-8 -*-

"""Algoritmos de Geometria Computacional

Sub-modulos:
- convexhull: algoritmos para o problema do Fecho Convexo bidimensional
- farthest:   algoritmos para encontrar o par de pontos mais distante

- common:     classes e operacoes usadas por diversos algoritmos
- gui:        implementacoes das operacoes graficas
"""

from . import convexhull
from . import farthest
from . import robotmv
from . import shortestpath
from . import sssp
from . import SPM
from .common.guicontrol import init_display
from .common.guicontrol import config_canvas
from .common.guicontrol import run_algorithm
from .common.io import open_file
from .common.prim import get_count
from .common.prim import reset_count

children = (   ( 'convexhull', None, 'Fecho Convexo' ),
		( 'farthest',  None, 'Par Mais Distante' ),
		( 'robotmv',  None, 'Movimento de robo' ),
               ('shortestpath', None, 'Caminho mínimo' ),
               ('sssp', None, "Caminho mínimo com fonte única"),
               ('SPM', None, "Mapa de caminhos mínimos"),
               
	)

__all__ = [p[0] for p in children]
