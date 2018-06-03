#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ataxx import *
from copy import deepcopy

class StateMinimax(object):
    def __init__(self,board,player,balls):
        self.board = deepcopy(board)
        self.player = player
        self.balls = {}
        self.balls[-1] = balls[-1]
        self.balls[1] = balls[1]

    def print_state(self):
        print "Player:",self.player
        s = [[str(e) for e in row] for row in self.board]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print '\n'.join(table)

    def __str__(self):
        return str(self.player) + " - " + str(self.board) + str(self.balls[1]) + str(self.balls[-1])

    def __hash__(self):
        return hash(str(self))

    def __eq__(self,other):
        return self.player == other.player and self.board == other.board and self.balls[-1] == other.balls[-1] and self.balls[1] == other.balls[1]

class Board(object):

    def __init__(self):
        self.game = Ataxx()

    def current_player(self, state):
        return state.player

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.

        s = StateMinimax(state.board,state.player,state.balls)

        self.game.update_board(s)

        self.game.move_with_position(play)
        self.game.turn_player = -1 * self.game.turn_player
        
        #update state with values of game
        s.player = self.game.turn_player
        s.balls[-1] = self.game.balls[-1]
        s.balls[1] = self.game.balls[1]
        
        return s

    def legal_plays(self, state):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        self.game.update_board(state)
        moves = self.game.get_all_possible_moves()
        return moves


    def is_gameover(self,state):
        self.game.update_board(state)
        return self.game.is_game_over()

    def winner(self, state):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        self.game.update_board(state)
        is_game_over = self.game.is_game_over()
        if(not is_game_over):
            return 0

        return self.game.get_winner()



    def get_score(self,state,player):
        self.game.update_board(state)
        return self.game.get_score(player)

    def get_score_pieces(self,state,player):
        self.game.update_board(state)
        return self.game.get_score_pieces(player)

