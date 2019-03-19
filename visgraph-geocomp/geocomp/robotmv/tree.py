#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	Árvore binário da busca. Suponho que as keys são
	segmentos
"""

from geocomp.common.segment import Segment
from geocomp.common.prim import *
from .minhasPrim import *

"""
DEFINES DE CONTROLE
"""

PINTA = False;

###################################3


class Folha:
	def __init__(self, key):
		self.key = key
		self.red = False



	def delete(self,x):
		s = self.key
		if(s is None): 
			return self 
		if(s.init == x.init and s.to == x.to): #Deveria sempre ser True
			return Folha(None);
		else:
			# Deleção falhou
			return self



	def insert(self,x):		
		s = self.key
		if(s is None): 
			self.key = x
			return self
		else:
			if(right(s.init, s.to, x.init)):
				return InCel(x, Folha(x), Folha(s), True)
			elif(collinear(s.init, s.to, x.init)):
				if(right(s.init, s.to, x.to)):
					return InCel(x, Folha(x), Folha(s), True)
				else:
					return InCel(s, Folha(s), Folha(x), True)
					
			else:
				return InCel(s, Folha(s), Folha(x), True)

	#Deleta a folha mais a direita. E retorna o irmão esquerdo dessa folha
	def delMax(self):
		return Folha(None);
        
	def delMin(self):
		return Folha(None)
		

	def getMin(self):
		return self.key

	def getMax(self):
		return self.key

	def procuraInter(self, seg):
		x = self.key
		if(x is not None and intersecta(seg,x)): return x
		else: return None

	def __repr__(self, level=0):
		x = self.key
		if(self.key is None): x = "NADA"
		ret = "\t"*level+repr(x)+"\n"
		return ret


	def getProx(self, p):
		return self.key



class InCel:
	def __init__(self, key, left, right, red):
		self.r = right
		self.l = left
		self.key = key
		self.red = red



	def delete(self,x):
		s = self.key
		if(s.init == x.init and s.to == x.to):
			#Achou o nó interno com chave igual
			### Balanceamento da rubro negra #####
			#Eu sei que vou deletar algo (o max) da esquerda
			#Preciso manter a invariante

			#Filho esquerdo é folha. Tentamos deletar. Se não der certo, não achou
			# x na árvore. se der certo, retornamos o filho direito (Também folha)
			if(isinstance(self.l, Folha)):
			        self.l = self.l.delete(x)
			        if(self.l.key is None): #Conseguiu deletar
			                return self.r
			        else: #Não achou x
			                return self

			#Caso contrário, nos preparamos para deletar algo a esquerda
			if(not self.l.red and not self.l.l.red):
			        self = self.moveRedLeft()                       

			######################################

			self.l = self.l.delMax()

			self.key = self.l.getMax()
			
		elif(right(s.init, s.to, x.to)): 
			# Compara com o fim de X
			### Balanceamento da rubro negra ####


			#Verifico se filho esquerdo é folha. Se for, o filho
			#esquerdo vai ser igual a key atual, e portanto não
			#achamos x na árvore. Verifico a key só para fins de
			#depuração
			if(isinstance(self.l, Folha)):
			        if(self.l.key.init == x.init and self.l.key.to == self.l.key.to):
			                #problema
			                print("Esse caso (1) não deveria acontecer. Erro!")
			        return self

			#Filho esquerdo não é folha, e a deleção vai para a esquerda.
			#Preparamos a árvore para manter a invariante
			if(not self.l.red and not self.l.l.red):
			        self = self.moveRedLeft() 
			        
			#################################

			self.l = self.l.delete(x)

		elif(collinear(s.init, s.to, x.to)):
			if(right(s.init, s.to, x.init)):
				### Balanceamento da rubro negra ###
				#Exatamente igual ao caso anterior

				if(isinstance(self.l, Folha)):
				        if(self.l.key.init == x.init and self.l.key.to == self.l.key.to):
				                #problema
				                print("Esse caso (2) não deveria acontecer. Erro!")
				        return self

				#Filho esquerdo não é folha, e a deleção vai para a esquerda.
				#Preparamos a árvore para manter a invariante
				if(not self.l.red and not self.l.l.red):
				        self = self.moveRedLeft() 
				##########################################
				self.l = self.l.delete(x)
                
			else:
				### Balanceamento da rubro negra ###

				#Se o filho direito é folha, tenta deletar
				if(isinstance(self.r, Folha)):
					self.r = self.r.delete(x)
					if(self.r.key is None): #Nó direito era x
							self.l.red = False #Corrigi balanceamento
							return self.l
					else: #Não encontrou x
						return self.balanceia() #(Precisa balancear?)

				#Filho direito não é folha. Deleção vai se propagar para
				# a direita. Vamos preparar a invariante da árvore
				if(not self.r.red and not self.r.l.red):
					self = self.moveRedRight()                                

				###################################

				self.r = self.r.delete(x)
                				
		else:

			### Balanceamento da rubro negra ####
			#Mesma coisa que o caso anterior
			if(isinstance(self.r, Folha)):
			    self.r = self.r.delete(x)
			    if(self.r.key is None): #Nó direito era x
			    	self.l.red = False #Corrigi balanceamento
			    	return self.l
			    else: #Não encontrou x
			    	return self.balanceia() #(Precisa balancear?)
			    
			if(not self.r.red and not self.r.l.red):
				self = self.moveRedRight()

			########################################
			self.r = self.r.delete(x)
		return self.balanceia()


	"""
          Deleta a maior Folha, e coloca no lugar do pai dessa folha uma folha
        com seu predecessor.
	"""

	def delMax(self):
		if(self.l.red): self = self.rotateR()
		if(isinstance(self.r, Folha)): return self.l #Folha com o predecessor do max.

		if(not self.r.red and not self.r.l.red):
			self = self.moveRedRight()


		self.r = self.r.delMax();

		return self;

	def getMax(self):
		return self.r.getMax();

	# x é um segmento novo
	def insert(self, x):
		s = self.key;
		if(right(s.init, s.to, x.init)):
			self.l = self.l.insert(x)
		elif(collinear(s.init, s.to, x.init)):
			if(right(s.init, s.to, x.to)): 

				self.l = self.l.insert(x)
			else:
				self.r = self.r.insert(x)
		else:
			self.r = self.r.insert(x)


		# Balanceamento da rubro-negra

		self = self.balanceia()
		return self

	def getMin(self):
		resp = self.l.getMin()
		if(resp is None): 
			return self.key 
			#Ou self.r.getMin().
			#Provavelmente tem o mesmo efeito, mas com possivelmente
			#maior tempo de execução
		else:
			return resp

	def procuraInter(self, seg):
		x = self.key
		if(intersecta(seg,x)): return x
		else:
			if(right(x.init, x.to, seg.init)):
				return self.l.procuraInter(seg)
			else:
				return self.r.procuraInter(seg)
	
	def delMin(self):
		if(isinstance(self.l, Folha)):
			return self.r #Que provavelmente é folha também.
            
		if(not self.l.red and not self.l.l.red):
			self = self.moveRedLeft()

		self.l = self.l.deleteMin()
		self = self.balanceia()

		return self;

	def getProx(self, p):
		x = self.key
		if(right(x.init, x.to,p)):
			return self.l.getProx(p)
		else:
			return self.r.getProx(p)

	def rotateL(self):
		x = self.r
		self.r = x.l
		x.l = self
		x.red = self.red
		self.red = True
		return x

	def rotateR(self):
		x = self.l
		self.l = x.r
		x.r = self
		x.red = self.red
		self.red = True
		return x
        
    ##############
    # Faz ou o nó da direita ser vermelho, ou seu filho direito ser vermelho.
    ###############
	def moveRedRight(self):
		self.colorFlip()
		if(self.l.l.red):
			self = self.rotateR()
			self.colorFlip()
		return self

    ##########
    # Faz ou o nó da esquerda ser vermelho, ou o filho esquerdo do nó esquerdo
    ############
	def moveRedLeft(self):
		self.colorFlip()
		if(self.r.l.red):
			self.r = self.r.rotateR()
			self = self.rotateL()
			self.colorFlip()
		return self

	def balanceia(self):
		if(self.r.red and not self.l.red): self = self.rotateL()
		if(self.l.red and self.l.l.red): self = self.rotateR()
		if(self.l.red and self.r.red): self.colorFlip()
		return self;
         



	def colorFlip(self):
		self.red = not self.red
		self.r.red = not self.r.red
		self.l.red = not self.l.red

	def __repr__(self, level=0):
		ret = ""
		if(self.red): ret += "#"
		ret += "\t"*level+repr(self.key)+"\n"
		ret += self.l.__repr__(level+1)
		ret += self.r.__repr__(level+1)
		return ret

class Tree:
	def __init__(self):
		self.root = Folha(None)

	def insert(self, x):
		if(PINTA): x.hilight('yellow')
		self.root = self.root.insert(x)
		self.root.red = False


	def getMin(self):
		return self.root.getMin()

	def delete(self, x):
		self.root.red = True
		self.root = self.root.delete(x)
		self.root.red = False
	

	def getProx(self,p):
		return self.root.getProx(p)

	def procuraInter(self, seg):
		self.root.procuraInter(seg);

	def delMin(self):
                if(isinstance(self.root, Folha)): 
                        self.root.delMin()
                elif(isinstance(self.root.l, Folha)): 
                        self.root = self.root.r #Sera?
                else:
                        self.root.red = True
                        self.root = self.root.delMin()
                        #Depois termino. Falta coisa
                self.root.red = False #Concerta

	def __repr__(self):
	 	return self.root.__repr__()



