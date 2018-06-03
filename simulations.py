#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from ucb_monte_carlo import MonteCarlo
from minimax import minimax
from board import *
from mcts import *
from ataxx import *
from concurrent.futures import ProcessPoolExecutor, as_completed
from time import sleep
import cPickle as pickle
import argparse, logging
import time

parser = argparse.ArgumentParser(description='Values')
parser.add_argument('--number-simulations', type=int,
                    help='number of simulations')
parser.add_argument('--number-moves', type=int,
                    help='number of moves to mcmc')
parser.add_argument('--number-games', type=int,
                    help='number of games')
parser.add_argument('--depth-minimax', type=int,
                    help='depth-minimax')

args = parser.parse_args()
number_simulations = args.number_simulations
number_moves = args.number_moves
number_games = args.number_games
depth_minimax = args.depth_minimax

logging.basicConfig(filename= \
	"data-ucb1-number_simulations-"+str(number_simulations)+"--" +
	"number_moves-"+str(number_moves)+"--" +
	"number_games-"+str(number_games)+"--" +
	"depth_minimax-"+str(depth_minimax)+".log",filemode='w',
	level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info("Parametros:")
logging.info("number_simulations: {}".format(number_simulations))
logging.info("number_moves: {}".format(number_moves))
logging.info("number_games: {}".format(number_games))
logging.info("depth_minimax: {}".format(depth_minimax))



board = Board()
dados = {}
jogadas = []
per_preto = 0
data_best_moves = {}
moves = {}
cont_moves = {}
for i in range(number_games):
	moves[-1] = []
	moves[1] = []
	cont_moves[-1] = 0 
	cont_moves[1] = 0 
	game = Ataxx()
	
	c = 1

	logging.info("Jogo: {}".format(i))

	while not game.is_game_over():


		logging.info("Jogada Nº: {} Branco: Jogada minimax...".format(c))
		state = StateMinimax(game.board,game.current_player(),game.balls)
		begin = time.time()
		move = minimax(board,state,depth_minimax)
		logging.info("time: {}".format(time.time() - begin))

		player = game.current_player()
		if move:
			if move in moves[player]:
				cont_moves[player] += 1
			else:
				cont_moves[player] = 0
				moves[player].append(move)

			game.move_with_position(move)

		if(cont_moves[game.current_player()] > 6):
			logging.info("jogada repetiu")
			break

		if(len(moves[player]) > 6):
			moves[player] = []
			cont_moves[player] = 0


		logging.info("Branco terminou jogada.")
		logging.info(game.show_board())

		game.toggle_player()

		if(game.is_game_over()):
			break

		c += 1

		#jogada mcst
		logging.info("Jogada Nº: {} Branco: Jogada MCST...".format(c))
		state = State(game.board,game.current_player(),game.balls)
		mc = MonteCarloTreeSearch(state,max_moves=number_moves,number_simulations=number_simulations)
		
		begin = time.time()
		move = mc.get_play()
		logging.info("time: {}".format(time.time() - begin))

		if(move):
			game.move_with_position(move)

		logging.info("Jogada: {}".format(move))

		logging.info("Preto terminou jogada.")
		logging.info(game.show_board())

		game.toggle_player()

		c += 1
	
	ga = game.get_winner()
	logging.info("Número de jogadas: {}".format(c))
	if(ga not in dados):
		dados[ga] = 0
	dados[ga] += 1
	jogadas.append({'jogadas':c,'ganhador':ga})
	logging.info("Parcial:")
	logging.info("Jogos: {}".format(dados))
	logging.info("Jogadas: {}".format(jogadas))


logging.info("Acabou execução.")
logging.info("Jogos: {}".format(dados))
logging.info("Jogadas: {}".format(jogadas))
logging.info("data_best_moves: {}".format(data_best_moves))

with open("data-ucb1-number_simulations-"+str(number_simulations)+"--" +
	"number_moves-"+str(number_moves)+"--" +
	"number_games-"+str(number_games)+"--" +
	"depth_minimax-"+str(depth_minimax)+
	".pickle", 'wb') as handle:
    pickle.dump(data_best_moves, handle, protocol=pickle.HIGHEST_PROTOCOL)





