from Board import Board
from GameMaster import GameMaster

from random import randint
import math


class AI:
    strategy = "Player vs Player"
    name = "X"
    testing_board = Board()
    
    def __init__(self, name: str, strategy: str):
        """ initializes a new instance of the AI class. Sets the name, id and the strategy

        Args:
            name (str): name of the AI player
            strategy (str): name of the AI's strategy
        """
        if type(name) != str:
            raise TypeError("\"name\" should be of str class")
        if type(strategy) != str:
            raise TypeError("\"strategy\" should be of str class")
        self.name = name
        self.strategy = strategy

    def set_testing_board(self, board: Board):
        self.testing_board = board

    def get_player_move(self, board: list, opponentName: str) -> tuple:
        """ returns the valid move as the coordinates of the board's field, random or minimax way depending on the strategy

        Args:
            board (list): board represented as a 2D 9 grid list
            opponentName (str): name of the human player (required for minimax evaluation)

        Returns:
            tuple: row, col
        """
        if self.strategy == "Player vs Smart Computer":
            self.testing_board.replace(board)
            return self.get_best_move(opponentName)
        else:
            return self.get_random_move(board)
            

    def get_random_move(self, board: list) -> tuple:
        """ returns the random valid move as the coordinates of the board's field

        Args:
            board (list): board represented as a 2D 9 grid list

        Returns:
            tuple: row, col
        """
        while True:
            move = randint(1,9)
            if Board.is_AI_move_valid(move, board):
                return Board.get_coordinates(move)

    def get_best_move(self, opponent_name: str) -> tuple:
        best_score = -math.inf
        best_move = {'row': -1, 'col': -1, 'depth': 0}
        
        for row in range(3):
            for col in range(3):
                if self.testing_board.is_given_field_empty(row, col):
                    self.testing_board.update_with_coords(self.name, (row, col))
                    temp_score, temp_depth = self.minimax(0, -math.inf, math.inf, False, opponent_name)
                    self.testing_board.update_with_coords(" ", (row, col))
                    
                    if best_score < temp_score or (best_score == temp_score and best_move['depth'] > temp_depth): # depth optimization
                        best_move.update({'row': row, 'col': col, 'depth': temp_depth})
                        best_score = temp_score
                

        return best_move['row'], best_move['col']

    def minimax(self, depth: int, alpha: float, beta: float, is_maximizer_turn: bool, opponent_name: str):
        """ minimax function based on the Minimax algorithm with addition of alpha-pruning to save computational time. The idea is to traverse all the possible moves and get the highest move value. One player is maximizer, which will always choose the best move, and another one is minimizer which will choose the worst move for the maximizer every single time.
            After searching all the possible moves from the current state, the function will return the highest possible score of the move evaluated in the get_best_move, and its depth.

        Args:
            depth (int): number of steps needed to get to the particular move
            alpha (float), beta (float): values needed for alpha-pruning
            is_maximizer_turn (bool): maximizer turn (true) or minimizer turn (false)
            opponent_name (str): name of the player

        Returns:
            tuple: score, depth
        """
        
        best_score = self.evaluate_current_state(opponent_name)
        best_depth = depth

        if best_score in [-1, 0, 1]:
            pass
    
        elif is_maximizer_turn:
            best_score = -math.inf
            for row in range(3):
                for col in range(3):
                    if self.testing_board.is_given_field_empty(row, col):
                        self.testing_board.update_with_coords(self.name, (row, col))
                        temp_score = self.minimax(depth + 1, alpha, beta, False, opponent_name)[0]
                        self.testing_board.update_with_coords(" ", (row, col))
                        
                        # depth optimization part
                        if temp_score > best_score:
                            best_depth = depth+1                     
                        best_score = max([best_score, temp_score])

                        # alpha beta pruning part
                        if best_score >= beta:
                            return best_score, depth
                        alpha = max([alpha, best_score])
 

        else: # minimizer turn   
            best_score = math.inf
            for row in range(3):
                for col in range(3):
                    if self.testing_board.is_given_field_empty(row, col):
                        self.testing_board.update_with_coords(opponent_name, (row, col))
                        temp_score = self.minimax(depth + 1, alpha, beta, True, opponent_name)[0]
                        self.testing_board.update_with_coords(" ", (row, col))

                        # depth optimization part
                        if temp_score < best_score:
                            best_depth = depth+1 
                        best_score = min([best_score, temp_score])

                        # alpha beta pruning part
                        if best_score <= alpha:
                            return best_score, depth
                        beta = min([beta, best_score])

        return best_score, best_depth


    def evaluate_current_state(self, opponent_name: str) -> int:
        """ returns a score value for current state on the board (0 for tie, 1 for maximizer win, -1 for minimizer win, -2 for ongoing game). This is the part of the Minimax algorithm.

        Args:
            opponent_name (str): name of the human player

        Returns:
            int: score value (0 for tie, 1 for maximizer win, -1 for minimizer win, -2 for ongoing game)
        """
        gm = GameMaster()
        gm.evaluate_the_game_status(self.testing_board.board)
        game_status = gm.get_the_game_status()
        evaluations = {self.name: 1, opponent_name: -1, "0": 0}
        return evaluations.get(game_status, -2)
