#!/usr/bin/env python
# -*- coding: utf-8 -*-
#max_depth = 3


def minimax(board, state,depth_minimax):
	"""Return a best move for a sign in a board."""
	cont = 0

	max_depth = depth_minimax

	depth = 0

	moves = board.legal_plays(state)

	if(len(moves) == 0):
		return None

	best_move = moves[0]
	best_score = float('-inf')
	for move in moves:
		cont += 1
		clone = board.next_state(state,move)
		score,cont_ = min_play(board,clone,depth,max_depth)
		cont += cont_
		if score > best_score:
			best_move = move
			best_score = score

	#print "Cont minimax",cont
	return best_move

def min_play(board,state,depth,max_depth):
	cont = 0
	depth += 1
	#print "depth",depth,state.board
	winner = board.winner(state)
	if depth >= max_depth or winner:
		return evaluate(board,state),0
	

	moves = board.legal_plays(state)
	#if evaluate_without_winner(board,state,moves):
	#	return 0

	best_score = float('inf')
	for move in moves:
		cont += 1
		clone = board.next_state(state,move)
		score,cont_ = max_play(board,clone,depth,max_depth)
		cont += cont_
		#print board.current_player(state),move,depth,"min"
		if score < best_score:
			best_move = move
			best_score = score
	#print "board"
	return best_score,cont

def max_play(board,state,depth,max_depth):
	cont = 0
	depth += 1
	#print "depth",depth,state.board
	winner = board.winner(state)
	if depth >= max_depth or winner:
		return evaluate(board,state),0

	moves = board.legal_plays(state)
	#if evaluate_without_winner(board,state,moves):
	#	return 0
	best_score = float('-inf')
	for move in moves:
		cont += 1
		clone = board.next_state(state,move)
		score,cont_ = min_play(board,clone,depth,max_depth)
		cont += cont_
		#print "score",score
		if score > best_score:
			best_move = move
			best_score = score
	return best_score,cont

def evaluate(board,state):
	winner = board.winner(state)
	player = -1 * board.current_player(state)
	if(winner == player):
		return float('inf')
	elif (winner == -1 * player):
		return float('-inf')
	else:
		return board.get_score(state,player)
