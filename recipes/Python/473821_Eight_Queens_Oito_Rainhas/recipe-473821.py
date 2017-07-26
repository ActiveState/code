#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#   Problem Of The Eight Queens <Problema das Oito Rainhas>.
#   Copyright (C) 2006 by Nycholas de Oliveira e Oliveira <nycholas@gmail.com>
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   <Este programa é software livre; você pode redistribuí-lo e/ou modificá-lo sob os
#   termos da Licença Pública Geral GNU conforme publicada pela Free Software Foundation;
#   tanto a versão 2 da Licença, como (a seu critério) qualquer versão posterior.>
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   <Este programa é distribuído na expectativa de que seja útil, porém, SEM NENHUMA
#   GARANTIA; nem mesmo a garantia implícita de COMERCIABILIDADE OU ADEQUAÇÃO A UMA 
#   FINALIDADE ESPECÍFICA. Consulte a Licença Pública Geral do GNU para mais detalhes.>
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#   <Você deve ter recebido uma cópia da Licença Pública Geral do GNU junto com este 
#   programa; se não, escreva para a Free Software Foundation, Inc., no endereço 59
#   Temple Street, Suite 330, Boston, MA 02111-1307 USA.>
#

#########################################################
# NOME        : Nycholas de Oliveira e Oliveira         #
# E-MAIL      : nycholas@gmail.com                      #
# ICQ         : 114965471                               #
# MSN         : o_lalertom@hotmail.com                  #
# JABBER      : nycholas@jabber.org                     #
# TALK        : nycholas@gmail.com                      #
# DESCRICAO   : Problema das Oito Rainhas               #
# LOCALIZACAO : Uberlândia - MG                         #
# LOCALIZACAO : Brasil                                  #
#########################################################

import random


class OitoRainhas:
	def __init__(self):
		print self.printBegin()
		self.run()
	
	def printBegin(self):
		p = \
		" + Problema das Oito Rainhas\n" \
		"  * Copyright (C) 2006 by Nycholas de Oliveira e Oliveira <nycholas@gmail.com>\n\n" \
		">> Para melhor visualizar o conteúdo impresso em tela, o terminal deve esta setado com a coluna em 42.\n"
		return p
		
	def printRainha(self):
		p = \
		"\n==========================================\n" \
		" + " + str(len(self.posRainha)) + " Rainha\n\n" \
		+ str(self.t)
		return p
		
	def printEnd(self):
		p = \
		"\n\n >> Nycholas de Oliveira e Oliveira - o_lalertom - nycholas@gmail.com"
		return p
		
	def setVars(self):
		self.TABULEIRO = \
		"########\n" \
		"########\n" \
		"########\n" \
		"########\n" \
		"########\n" \
		"########\n" \
		"########\n" \
		"########\n"
		self.VAZIO, self.ATAQUE, self.RAINHA = "#", "+", "*"
		self.posRainha, self.posValida = [], []
		self.t = [list(line) for line in self.TABULEIRO.splitlines()]
		self.posValida = self.setPosValida()
		
	def setPosValida(self):
		l = []
		for y in range(len(self.t)):
			for x in range(len(self.t)):
				l.append([x,y])
		return l
		
	def setRainha(self, x=0, y=0):
		if 0 <= x <= 7 and 0 <= y <= 7:
			if self.t[x][y] == self.VAZIO:
				self.t[x][y] = self.RAINHA
				self.posRainha.append([x, y])
				self.posValida.remove([x, y])
				self.moveX(x, y)
				self.moveY(x, y)
				self.moveXYDir(x, y)
				self.moveXYEsq(x, y)
				print self.printRainha()

	def moveX(self, x=0, y=0):
		if 0 <= x <= 7:
			if self.t[x][y] == self.RAINHA:
				i = (map(lambda x: x == self.RAINHA, self.t[x])).index(True)
				self.t[x][:i] = list(len(self.t[x][:i])*self.ATAQUE)
				self.t[x][i+1:] = list(len(self.t[x][i+1:])*self.ATAQUE)
				for i in range(len(self.t[x])):
					if self.t[x][i] == self.ATAQUE:
						try:
							self.posValida.remove([x, i])
						except ValueError:
							pass
				return True
			else:
				if self.moveX(x+1, y) or self.moveX(x-1, y): pass
				return False
				
	def moveY(self, x=0, y=0):
		if 0 <= y <= 7:
			if self.t[x][y] == self.RAINHA:
				for i in range(len(self.t)):
					if self.t[i][y] <> self.RAINHA:
						self.t[i][y] = self.ATAQUE
						try:
							self.posValida.remove([i, y])
						except ValueError:
							pass
				return True
			else:
				if self.moveY(x, y+1) or self.moveX(x, y-1): pass
				return False
				
	def moveXYDir(self, x=0, y=0):
		if 0 <= x <= 7 and 0 <= y <= 7:
			if self.t[x][y] == self.RAINHA:
				try:
					for i in range(len(self.t[x])):
						if 0 <= (x+i) < len(self.t[x]) and 0 <= (y+i) < len(self.t[x]):
							if self.t[x+i][y+i] <> self.RAINHA:
								self.t[x+i][y+i] = self.ATAQUE
								try:
									self.posValida.remove([x+i, y+i])
								except ValueError:
									pass
				finally:
					for i in range(len(self.t[x])):
						#print (x-i), (y-i), len(self.t[x])
						if 0 <= (x-i) < len(self.t[x]) and 0 <= (y-i) < len(self.t[x]):
							if self.t[x-i][y-i] <> self.RAINHA:
								self.t[x-i][y-i] = self.ATAQUE
								try:
									self.posValida.remove([x-i, y-i])
								except ValueError:
									pass
				return True
			else:
				if self.moveXYDir(x+1, y+1) or self.moveXYDir(x-1, y-1): pass
				return False
	
	def moveXYEsq(self, x=0, y=0):
		if 0 <= x <= 7 and 0 <= y <= 7:
			if self.t[x][y] == self.RAINHA:
				try:
					for i in range(len(self.t[x])):
						if 0 <= (x-i) < len(self.t[x]) and 0 <= (y+i) < len(self.t[x]):
							if self.t[x-i][y+i] <> self.RAINHA:
								self.t[x-i][y+i] = self.ATAQUE
								try:
									self.posValida.remove([x-i, y+i])
								except ValueError:
									pass
				finally:
					for i in range(len(self.t[x])):
						if 0 <= (x+i) < len(self.t[x]) and 0 <= (y-i) < len(self.t[x]):
							if self.t[x+i][y-i] <> self.RAINHA:
								self.t[x+i][y-i] = self.ATAQUE
								try:
									self.posValida.remove([x+i, y-i])
								except ValueError:
									pass
				return True
			else:
				if self.moveXYEsq(x+1, y-1) or self.moveXYEsq(x+1, y-1): pass
				return False
		
	def testVazio(self):
		r = False
		for i in range(8):
			if len(filter(lambda x: x == self.VAZIO, self.t[i])) > 0:
				r = True
			else:
				r = False
		return r
	
	def loop(self):
		try:
			for i in range(8):
				x = self.posValida[random.randrange(0, 7, 1)][0]
				y = self.posValida[random.randrange(0, 7, 1)][1]
				if [x, y] in self.posValida:
					self.setRainha(x, y)
				else:
					continue
		except IndexError:
			pass
		if len(self.posRainha) < 8 and self.testVazio() == True:
			self.loop()
			
	def run(self):
		self.setVars()
		self.setRainha()
		self.loop()
		if 0 <= len(self.posRainha) < 8 and self.testVazio() == False:
			self.run()
		else:
			print self.printEnd()

if __name__ == "__main__":
	oitoRainhas = OitoRainhas()
