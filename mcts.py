#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from utc import Utc
from ataxx import *
from copy import copy, deepcopy
import numpy as np
import sys
import logging

utc = Utc()

class Node(object):
    def __init__(self):
        self.parent = None
        self.children = []
        self.state = None
        self.level = 0

    def get_random_child(self):
    	idx = np.random.randint(0,len(self.children))
    	return self.children[idx]

    def add_child(self,node):
    	self.children.append(node)

    def has_children(self):
    	return len(self.children) > 0

    def get_child_max_score(self):
    	if(not self.has_children()):
    		return None
    	max_score = self.children[0].state.get_score()
    	max_c = self.children[0]
    	for c in self.children:
    		score = c.state.get_score()
    		if(score > max_score):
    			max_score = score
    			max_c = c
    	return max_c


class Tree(object):
	def __init__(self): 
		self.root = Node()


class State(object):

	def __init__(self,board,player,balls):
		self.board = deepcopy(board)
		self.player = player
		self.balls = {}
		self.balls[-1] = balls[-1]
		self.balls[1] = balls[1]

		self.visit_count = 0
		self.win_score = 0


	def increment_visit(self):
		self.visit_count += 1

	def get_score(self):
		if(self.visit_count == 0):
			return 0
		return self.win_score * 1. / self.visit_count


	def increment_win_score(self):
		if self.win_score != -sys.maxint:
			self.win_score += 1

	def get_all_possible_states(self,game):
		# constructs a list of all possible states from current state

		possible_states = []
		game.update_board(self)
		game.toggle_player()
		moves = game.get_all_possible_moves()
		for m in moves:
			new_state = State(self.board,-1*self.player,self.balls)
			new_state.move = m
			game.update_board(new_state)
			game.move_with_position(m)
			new_state.balls[-1] = game.balls[-1]
			new_state.balls[1] = game.balls[1]
			
			possible_states.append(new_state)
		
		return possible_states


class MonteCarloTreeSearch(object):

	def __init__(self,state,**kwargs):
		self.game = Ataxx()
		self.initial_state = state
		self.oponnent = -1 * state.player
		self.initial_state.player = -1 * self.initial_state.player
		self.number_simulations = kwargs.get('number_simulations', 2)
		self.max_moves = kwargs.get('max_moves', 10)

	def select_promising_node(self,root_node):
		node = root_node
		while (node.has_children()):
			node = utc.find_best_node_utc(node)
		return node

	def expand_node(self,node):
		possible_states = node.state.get_all_possible_states(self.game)
		for state in possible_states:
			node_ = Node()
			node_.level = node.level + 1
			node_.state = state
			node_.parent = node
			node.add_child(node_)
			if(node_.level > self.max_level):
				self.max_level = node_.level
			self.cont_states += 1

	def back_propagation(self,node,player):
		while(node != None):
			node.state.increment_visit()
			if node.state.player == player:
				#self.game.update_board(self.final_state)
				#node.state.win_score += self.game.get_score(player)
				node.state.increment_win_score()
			node = node.parent

	def simulate_random_playout(self,node):
		game = self.game

		state_simulation = State(node.state.board,node.state.player,node.state.balls)
		game.update_board(state_simulation)

		cont_moves = 0
		while not game.is_game_over():
			game.toggle_player()
			game.move()

		return game.get_winner()


	def simulation(self):
		root = self.tree.root


		print "selection..."
		# Phase 1 - Selection
		promising_node = self.select_promising_node(root)
		print "done"

		print "expansion..."
		# Phase 2 - Expansion
		self.game.update_board(promising_node.state)
		if not self.game.is_game_over():
			self.expand_node(promising_node)
		print "done"

		print "simulation..."
		# Phase 3 - Simulation
		node_to_explore = promising_node
		if promising_node.has_children():
			node_to_explore = promising_node.get_random_child()
		winner = self.simulate_random_playout(node_to_explore)
		print "done"

		print "back propagation..."
		# Phase 4 - Update
		self.back_propagation(node_to_explore, winner)
		print "done"


	def get_play(self):

		self.tree = Tree()
		root = self.tree.root
		root.level = 1
		root.state = self.initial_state
		self.max_level = 1
		self.cont_states = 0
		
		for n in range(self.number_simulations):
			logging.info("simulation: {}".format(n+1))
			self.simulation()

 
		winner_node = root.get_child_max_score()
		if winner_node:
			return winner_node.state.move
		else:
			return None

# game = Ataxx()
# game.board = [[1, 0, 0, 0, 0, 0, -1], 
# [0, 0, 0, 0, 0, 0, 0], 
# [0, 0, 0, 0, 0, 0, 0], 
# [0, 0, 0, 0, 0, 0, 0], 
# [0, 0, 0, 0, 0, 0, 0], 
# [0, 0, 0, 0, 0, 0, 0], 
# [-1, 0, 0, 0, 0, 0, -1]]
# game.balls[1] = 1
# game.balls[-1] = 3
# state = State(game.board,game.current_player(),game.balls)
# mcst = MonteCarloTreeSearch(state,max_moves=1,number_simulations=1000)

# move = mcst.get_play()
# print move









