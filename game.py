# -*- coding: utf-8 -*-
"""
@author: Junxiao Song
"""

from __future__ import print_function
import numpy as np
from renju import Renju_Rule


class Board(object):
    """board for the game"""

    def __init__(self, **kwargs):
        self.width = int(kwargs.get('width', 8))
        self.height = int(kwargs.get('height', 8))
        # board states stored as a dict,
        # key: move as location on the board,
        # value: player as pieces type
        self.states = {}
        # need how many pieces in a row to win
        self.n_in_row = int(kwargs.get('n_in_row', 5))
        self.players = [1, 2]  # player1 and player2
        self.renju = False

    def init_board(self, start_player=0):
        if self.width < self.n_in_row or self.height < self.n_in_row:
            raise Exception('board width and height can not be '
                            'less than {}'.format(self.n_in_row))
        self.current_player = self.players[start_player]  # start player
        # keep available moves in a list
        self.availables = list(range(self.width * self.height))
        self.black_availables = None
        self.states = {}
        self.change = True
        self.order = 0
        self.last_move = -1

    def move_to_location(self, move):
        """
        3*3 board's moves like:
        6 7 8
        3 4 5
        0 1 2
        and move 5's location is (1,2)
        """
        h = move // self.width
        w = move % self.width
        return [h, w]

    def location_to_move(self, location):
        if len(location) != 2:
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if move not in range(self.width * self.height):
            return -1
        return move

    def current_state(self):
        """return the board state from the perspective of the current player.
        state shape: 4*width*height
        """

        square_state = np.zeros((4, self.width, self.height))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            move_curr = moves[players == self.current_player]
            move_oppo = moves[players != self.current_player]
            square_state[0][move_curr // self.width,
                            move_curr % self.height] = 1.0
            square_state[1][move_oppo // self.width,
                            move_oppo % self.height] = 1.0
            # indicate the last move location
            square_state[2][self.last_move // self.width,
                            self.last_move % self.height] = 1.0
        if len(self.states) % 2 == 0:
            square_state[3][:, :] = 1.0  # indicate the colour to play
        return square_state[:, ::-1, :]

    def do_move(self, move):
        self.states[move] = self.current_player
        self.availables.remove(move)
        self.current_player = (
            self.players[0] if self.current_player == self.players[1]
            else self.players[1]
        )
        self.change = True
        self.order = self.order ^ 1
        self.last_move = move

    def has_a_winner(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n_in_row

        moved = np.array(list(set(range(width * height)) - set(self.availables)))
        if len(moved) < self.n_in_row *2-1:
            return False, -1

        moves, players = np.array(list(zip(*states.items())))
        states = np.zeros(width * height)
        states[moves] = players

        h = moved // width
        w = moved % width
        
        temp = moved[w < width - n + 1]
        result = [len(set(states[i:i+n])) for i in temp]
        if 1 in result:
            idx = temp[result.index(1)]
            return True, states[idx]

        temp1 = moved[w < width - n + 1]
        idx1 = temp1.reshape(-1, 1) + np.arange(n)

        temp2 = moved[h < height - n + 1]
        idx2 = temp2.reshape(-1, 1) + np.arange(0, n * width, width)

        temp3 = moved[(w < width - n + 1) & (h < height - n + 1)]
        idx3 = temp3.reshape(-1, 1) + np.arange(0, n * (width + 1), width + 1)

        temp4 = moved[(w > n - 2) & (h < height - n + 1)]
        idx4 = temp4.reshape(-1, 1) + np.arange(0, n * (width - 1), width - 1)

        temp = [temp1, temp2, temp3, temp4]
        idx = np.concatenate([idx1, idx2, idx3, idx4])
        result = np.take(states, idx)
        result -= result[:, 0].reshape(-1, 1)
        result = np.all(result == 0, axis=1).tolist()
        if True in result:
            idx = result.index(True)
            for i in range(4):
                if idx < len(temp[i]):
                    return True, states[temp[i][idx]]
                idx -= len(temp[i])

        return False, -1

        # for m in moved:
        #     h = m // width
        #     w = m % width
        #     player = states[m]

        #     if (w < width - n + 1 and
        #             len(set(states[m : m+n])) == 1):
        #             # len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
        #         return True, player

        #     if (h < height - n + 1 and
        #             len(set(states[m : m + n * width : width])) == 1):
        #             # len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
        #         return True, player

        #     if (w < width - n + 1 and h < height - n + 1 and
        #             len(set(states[m : m + n * (width + 1) : width + 1])) == 1):
        #             # len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
        #         return True, player

        #     if (w > n - 2 and h < height - n + 1 and
        #             len(set(states[m : m + n * (width - 1) : width - 1])) == 1):
        #             # len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
        #         return True, player

        # return False, -1       

    def game_end(self):
        """Check whether the game is ended or not"""
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        elif not len(self.get_availables()):
            return True, -1
        return False, -1

    def get_current_player(self):
        return self.current_player
    
    def get_availables(self):
        if self.renju:
            if self.order == 0:
                if self.change == True:
                    if len(self.states) > 1:
                        square_state = np.zeros((self.width, self.height))
                        moves, players = np.array(list(zip(*self.states.items())))
                        move_curr = moves[players == self.current_player]
                        move_oppo = moves[players != self.current_player]
                        square_state[move_curr // self.width,
                                        move_curr % self.height] = 1
                        square_state[move_oppo // self.width,
                                        move_oppo % self.height] = 2
                        rule = Renju_Rule(square_state, self.width)
                        forbid = rule.get_forbidden_points(1)
                        forbid = [self.location_to_move(loc) for loc in forbid]
                        self.black_availables = list(set(self.availables) - set(forbid))
                        self.change = False
                    else:
                        self.black_availables = self.availables
                return self.black_availables
            if self.order == 1:
                return self.availables
        else:
            return self.availables


class Game(object):
    """game server"""

    def __init__(self, board, **kwargs):
        self.board = board

    def graphic(self, board, player1, player2):
        """Draw the board and show game info"""
        width = board.width
        height = board.height

        print("Player", player1, "with X".rjust(3))
        print("Player", player2, "with O".rjust(3))
        print()
        for x in range(width):
            print("{0:8}".format(x), end='')
        print('\r\n')
        for i in range(height - 1, -1, -1):
            print("{0:4d}".format(i), end='')
            for j in range(width):
                loc = i * width + j
                p = board.states.get(loc, -1)
                if p == player1:
                    print('X'.center(8), end='')
                elif p == player2:
                    print('O'.center(8), end='')
                else:
                    print('_'.center(8), end='')
            print('\r\n\r\n')

    def start_play(self, player1, player2, start_player=0, is_shown=1):
        """start a game between two players"""
        if start_player not in (0, 1):
            raise Exception('start_player should be either 0 (player1 first) '
                            'or 1 (player2 first)')
        self.board.init_board(start_player)
        p1, p2 = self.board.players
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players = {p1: player1, p2: player2}
        if is_shown:
            self.graphic(self.board, player1.player, player2.player)
        while True:
            current_player = self.board.get_current_player()
            player_in_turn = players[current_player]
            move = player_in_turn.get_action(self.board)
            self.board.do_move(move)
            if is_shown:
                self.graphic(self.board, player1.player, player2.player)
            end, winner = self.board.game_end()
            if end:
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is", players[winner])
                    else:
                        print("Game end. Tie")
                return winner

    def start_self_play(self, player, is_shown=0, temp=1e-3):
        """ start a self-play game using a MCTS player, reuse the search tree,
        and store the self-play data: (state, mcts_probs, z) for training
        """
        self.board.init_board()
        p1, p2 = self.board.players
        states, mcts_probs, current_players = [], [], []
        while True:
            move, move_probs = player.get_action(self.board,
                                                 temp=temp,
                                                 return_prob=1)
            # store the data
            states.append(self.board.current_state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.current_player)
            # perform a move
            self.board.do_move(move)
            if is_shown:
                self.graphic(self.board, p1, p2)
            end, winner = self.board.game_end()
            if end:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                # reset MCTS root node
                player.reset_player()
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is player:", winner)
                    else:
                        print("Game end. Tie")
                return winner, zip(states, mcts_probs, winners_z)
