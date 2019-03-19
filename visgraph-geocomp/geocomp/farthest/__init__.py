# -*- coding: utf-8 -*-
"""Algoritmos para o problema do Par Mais Distante:

Dado um conjunto de pontos S, determinar dois cuja distancia entre eles 
maxima

Algoritmos disponveis:
- Fora bruta
- Diametro
"""
from . import diameter
from . import brute

children = [
	[ 'diameter', 'Diameter', 'Diametro' ],
	[ 'brute', 'Brute', 'Forca Bruta' ]
]

__all__ = [a[0] for a in children]
