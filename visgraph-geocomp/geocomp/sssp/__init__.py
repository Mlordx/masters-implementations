# -*- coding: utf-8 -*-
"""Algoritmos para o problema do caminho mínimo entre dois pontos num polígono:

~Falta definição do problema~

Algoritmos disponíveis:
- Grafo de visibilidade
"""

from . import triangulation
from . import singleSourceShortestPath
from . import monotoneTriangulation
from . import monotoneDecomposition

# cada entrada deve ter:
#  [ 'nome-do-modulo', 'nome-da-funcao', 'nome do algoritmo' ]
children = ( 
	( 'triangulation', 'triangulationByEars', 'Triangulação por orelhas' ),
    ('singleSourceShortestPath', 'singleSourceShortestPath', 'Árvore de caminhos mínimos'),
	('monotoneTriangulation', 'triangulate', 'triangulação de Monotonos'),
    ('monotoneDecomposition', 'decompose', 'decomposicao em monotonos'),
    
)

__all__ = [a[0] for a in children]
