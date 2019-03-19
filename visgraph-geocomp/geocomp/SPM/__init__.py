# -*- coding: utf-8 -*-
"""Algoritmos para o problema do caminho mínimo entre dois pontos num polígono:

~Falta definição do problema~

Algoritmos disponíveis:
- Grafo de visibilidade
"""

from . import triangulation
from . import spm

# cada entrada deve ter:
#  [ 'nome-do-modulo', 'nome-da-funcao', 'nome do algoritmo' ]
children = ( 
	( 'triangulation', 'triangulationByEars', 'Triangulação por orelhas' ),
    ('spm', 'shortestPathMap', 'Teste SPM'),
    
)

__all__ = [a[0] for a in children]
