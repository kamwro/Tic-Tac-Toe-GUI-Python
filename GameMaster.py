from Board import Board

class GameMaster:
    game_status = '1'

    def get_the_game_status(self) -> str:
        """ returns the game status (1 for ongoing game, 0 for draw, player name for each player victory)

        Returns:
            str: one of the game statuses
        """
        return self.game_status

    def evaluate_the_game_status(self, board_list: list):
        """ evaluate game status to one of the four statuses (1 for ongoing game, 0 for draw, player name for each player victory) using Board class methods to check for game status

        Args:
            board (list): board represented as the 2D 9 grid list
        """
        board = Board()
        board.replace(board_list)
        game_status = board.get_game_status_for_diagonals()
        if game_status == '1':
            game_status = board.get_game_status_for_rows_and_cols()
        if game_status == '1':
            if board.is_there_free_field():
                game_status = '1'
            else:
                game_status = '0'
        self.game_status = game_status