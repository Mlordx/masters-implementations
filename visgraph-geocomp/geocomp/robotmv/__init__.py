# -*- coding: utf-8 -*-
"""Algoritmos para o problema do Plano de Locomoção de Robôs,:

~Falta definição do problema~

Algoritmos disponíveis:
- Grafo de visibilidade
"""

from . import visgraph

# cada entrada deve ter:
#  [ 'nome-do-modulo', 'nome-da-funcao', 'nome do algoritmo' ]
children = ( 
	( 'visgraph', 'visGraphAlg', 'Grafo de visibilidade' ),
	( 'visgraph', 'desenhaTudo', 'Desenha')
	
)

#children = algorithms

#__all__ = [ 'graham', 'gift' ]
__all__ = [a[0] for a in children]
