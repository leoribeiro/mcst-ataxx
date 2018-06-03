#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import numpy as np
from copy import deepcopy
from collections import deque as dl
## 1 é o branco
## -1 é o preto
class Ataxx:
	def __init__(self):
		self.balls = {}
		self.moves = {}
		self.balls[1] = 0
		self.balls[-1] = 0
		self.moves[1] = 0
		self.moves[-1] = 0
		self.n_fields = 7
		self.board = [[0 for x in range(self.n_fields)] for y in range(self.n_fields)]
		
		self.turn_player = 1

		self.add_ball(0,0)
		self.add_ball(self.n_fields-1,self.n_fields-1)

		self.turn_player = -1

		self.add_ball(0,self.n_fields-1)
		self.add_ball(self.n_fields-1,0)

		self.turn_player = 1

		self.last_pos = -1
		self.last_player = 0
		self.cont_last_pos = 0
		self.stop_game = False


	def get_all_possible_moves(self):
		pos_copy = [(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,-1),(1,-1)]
		pos_jump = [(-2,2),(-2,1),(-2,0),(-2,-1),(-2,-2),(-1,2),(-1,-2),
		(0,2),(0,-2),(1,2),(1,-2),(2,2),(2,1),(2,0),(2,-1),(2,-2)]

		possible_moves = []
		for x in range(self.n_fields):
			for y in range(self.n_fields):
				if(self.board[x][y] != self.turn_player):
					continue
				b = (x,y)
				for p in self.get_empty_pos(b,pos_copy):
					possible_moves.append(('c',p))

				for p in self.get_empty_pos(b,pos_jump):
					possible_moves.append(('j',p,b))

		return possible_moves

	def update_board(self,state):
		self.board = state.board
		self.turn_player = state.player
		
		self.balls[-1] = state.balls[-1]
		self.balls[1] = state.balls[1]

	def toggle_player(self):
		self.turn_player = -1 * self.turn_player

	def current_player(self):
		return self.turn_player

	def move_with_position(self,position):
		if(position[0] == 'c'):
			self.copy_stone_position(position[1])
		else:
			self.jump_stone_position(position[1],position[2])

	def copy_stone_position(self,p):
		x,y = p[0],p[1]
		self.add_ball(x,y)
		self.take_stones(x,y)
		self.increase_move()

	def jump_stone_position(self,p,b):
		x,y = p[0],p[1]
		self.add_ball(x,y)
		self.remove_ball(b[0],b[1])
		self.take_stones(x,y)
		self.increase_move()

	####### monte carlo

	def move(self):
		moves = self.get_all_possible_moves()
		if moves:
			idx = np.random.randint(0,len(moves))
			self.move_with_position(moves[idx])


	def increase_move(self):
		self.moves[self.turn_player] += 1

	def get_amount_moves(self):
		return self.moves[1] + self.moves[-1]

	def get_empty_pos(self,b,pos):
		vs_e = []
		for x,y in pos:
			x_m = b[0]+x
			y_m = b[1]+y
			if(x_m < 0 or x_m > self.n_fields-1):
				continue
			if(y_m < 0 or y_m > self.n_fields-1):
				continue

			if(self.is_empty(x_m,y_m)):
				vs_e.append((x_m,y_m))
		return vs_e

	def get_full_pos(self,b,pos):
		vs_e = []
		for x,y in pos:
			x_m = b[0]+x
			y_m = b[1]+y
			if(x_m < 0 or x_m > self.n_fields-1):
				continue
			if(y_m < 0 or y_m > self.n_fields-1):
				continue

			if(not self.is_empty(x_m,y_m)):
				vs_e.append((x_m,y_m))
		return vs_e


	def get_copy_position(self,b):
		pos = [(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,-1),(1,-1)]

		vs = self.get_empty_pos(b,pos)

		if(len(vs) == 0):
			return b

		x_m,y_m = vs[np.random.randint(0,len(vs))]
	
		return x_m,y_m

	def get_jump_position(self,b):
		pos = [(-2,2),(-2,1),(-2,0),(-2,-1),(-2,-2),(-1,2),(-1,-2),
		(0,2),(0,-2),(1,2),(1,-2),(2,2),(2,1),(2,0),(2,-1),(2,-2)]

		vs = self.get_empty_pos(b,pos)

		if(len(vs) == 0):
			return b

		x_m,y_m = vs[np.random.randint(0,len(vs))]
		return x_m,y_m


	def choose_ball(self):
		#balls = self.balls[self.turn_player]
		idx = np.random.randint(1,self.balls[self.turn_player]+1)
		cont = 1
		for x in range(self.n_fields):
			for y in range(self.n_fields):
				if(self.board[x][y] == self.turn_player):
					if(cont == idx):
						return [x,y]
					cont += 1		

	def copy_stone(self):
		b = self.choose_ball()
		[x,y] = b
		#print "copy b",b
		while([x,y] == b):
			x,y = self.get_copy_position(b)
		
		self.add_ball(x,y)
		self.take_stones(x,y)
		self.increase_move()

	def jump_stone(self):
		b = self.choose_ball()
		#print "move b",b
		x,y = self.get_jump_position(b)
		if([x,y] != b):
			self.add_ball(x,y)
			self.remove_ball(b[0],b[1])
			self.take_stones(x,y)
			self.increase_move()

	def take_stones(self,x,y):
		b = [x,y]
		pos = [(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,-1),(1,-1)]
		pos = self.get_full_pos(b,pos)
		for x,y in pos:
			# bola não é do jogador atual
			if(self.turn_player == -1 and self.board[x][y] == 1):
				self.change_ball_player(x,y)
			elif(self.turn_player == 1 and self.board[x][y] == -1):
				self.change_ball_player(x,y)

	def change_ball_player(self,x,y):
		self.board[x][y] = -1*self.board[x][y]
		self.balls[self.turn_player] += 1
		self.balls[-1*self.turn_player] -= 1
		assert self.balls[-1] >= 0
		assert self.balls[1] >= 0


	def is_empty(self,x,y):
		return self.board[x][y] == 0

	def add_ball(self,x,y):
		assert self.board[x][y] == 0
		self.board[x][y] = self.turn_player
		self.balls[self.turn_player] += 1

	def remove_ball(self,x,y):
		assert self.board[x][y] != 0
		self.board[x][y] = 0
		self.balls[self.turn_player] -= 1

	def full_squares(self):
		if(self.balls[1] + self.balls[-1] >= (self.n_fields)*(self.n_fields)):
			return True
		return False

	def is_game_over(self):
		if(self.stop_game):
			return True
		if(self.balls[1] == 0 or self.balls[-1] == 0):
			return True
		if(self.full_squares()):
			return True
		return False

	def print_winner(self):
		# print "Bolas:"
		# print self.balls[1]
		# print self.balls[-1]
		if(self.balls[1] > self.balls[-1]):
			print "Winner: Branco. Gamer 1"
		elif(self.balls[-1] > self.balls[1]):
			print "Winner: Preto. Gamer 2"
		else:
			print "Draw"

	def get_winner(self):
		#self.print_winner()
		if(self.balls[-1] > self.balls[1]):
			return -1
		elif(self.balls[1] > self.balls[-1]):
			return 1
		else:
			return 100

	def get_winner_without_gameover(self):
	#self.print_winner()
		if(self.balls[-1] > self.balls[1]):
			return -1
		elif(self.balls[1] > self.balls[-1]):
			return 1
		else:
			return 0

	def get_score(self,player):
		assert self.balls[1] >=0
		assert self.balls[-1] >=0
		return (self.balls[player] * 1.) / (self.balls[1] + self.balls[-1])

	def get_score_pieces(self,player):
		return (self.balls[player] * 1.) / (self.n_fields**2)

	def print_board(self):
		print "Player:",self.turn_player
		s = [[str(e) for e in row] for row in self.board]
		lens = [max(map(len, col)) for col in zip(*s)]
		fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
		table = [fmt.format(*row) for row in s]
		print '\n'.join(table)
		print "Peças Branco: "+str(self.balls[1]),"Peças Preto: "+str(self.balls[-1])

	def show_board(self):
		msg = "Player: "+str(self.turn_player)+"\n"
		s = [[str(e) for e in row] for row in self.board]
		lens = [max(map(len, col)) for col in zip(*s)]
		fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
		table = [fmt.format(*row) for row in s]
		msg += '\n'.join(table)
		msg += "\n Peças Branco: "+str(self.balls[1])
		msg += " | Peças Preto: "+str(self.balls[-1])
		return msg

	def play(self):
		c = 1
		while not self.is_game_over():
			#print "jogada",c
			self.move()
			self.turn_player = -1 * self.turn_player
			#c += 1
		#self.print_winner()

