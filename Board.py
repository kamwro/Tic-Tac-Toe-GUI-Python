class Board:
    board = []

    def __init__(self):
        """ initializes a new instance of the Board class. Sets a board variable with all empty slots (with " ")
        
        """
        self.board = [3*[" "] for _ in range(3)]

   
    def __repr__(self):
        """ prints the actual board list and the corresponding helper list with field ID's in it

        Returns:
            str: board list + helper list
        """
        rep = ""
        for i in range(3):
            rep += (" | ".join(self.board[i]) + "              {} | {} | {}  ".format(i*3+1, i*3+2, i*3+3) + "\n")
        return rep

    def update_with_field_ID(self, name: str, fieldID: int):
        """ updates the board field with the player name, given the board ID

        Args:
            name (str): player name (X, O)
            fieldID (int): ID of the board's field
        """
        coords = Board.get_coordinates(fieldID)
        row = coords[0]
        col = coords[1]
        self.board[row][col] = name

    def reset(self):
        """ resets the board
        """
        self.board = [[" "] for _ in range(3)]

    def update_with_coords(self, name: str, coords: tuple):
        """ updates the board field with the player name, given the row and column coordinates

        Args:
            name (str): player name (X, O)
            coords (tuple): (row, col)
        """
        row = coords[0]
        col = coords[1]
        if row in range(0,3) and col in range(0,3) and type(row) == int and type(col) == int:
            self.board[row][col] = name
        else:
            raise Exception("Coords should be pairs of the integers from 0 to 2")
            
    @staticmethod
    def get_coordinates(field_ID: int) -> tuple:
        """ returns the coordinates of the board's fields, given the field ID (static method)

        Args:
            fieldID (int): ID of the board's field

        Returns:
            tuple: (row, col)
        """
        if field_ID in range(1,10) and type(field_ID) == int:
            if field_ID == 1:
                return (0, 0)
            elif field_ID == 2:
                return (0, 1)
            elif field_ID == 3:
                return (0, 2)
            elif field_ID == 4:
                return (1, 0)
            elif field_ID == 5:
                return (1, 1)
            elif field_ID == 6:
                return (1, 2)   
            elif field_ID == 7:
                return (2, 0) 
            elif field_ID == 8:
                return (2, 1) 
            elif field_ID == 9:
                return (2, 2)
            else:
                return (0, 0)
        else:
            raise Exception("Field ID should be an integer between 1 and 9")

    @staticmethod
    def get_field_ID(coords: tuple) -> int:
        """ returns the board's field ID based on the given coordinates (static method)

        Args:
            coords (tuple): (row, col)

        Returns:
            int: board's field ID
        """
        row = coords[0]
        col = coords[1]
        if row in range(0,3) and col in range(0,3) and type(row) == int and type(col) == int:
            if row == 0:
                if col == 0:
                    return 1
                elif col == 1:
                    return 2
                else:
                    return 3
            elif row == 1:
                if col == 0:
                    return 4
                elif col == 1:
                    return 5
                else:
                    return 6
            else:
                if col == 0:
                    return 7
                elif col == 1:
                    return 8
                else:
                    return 9
        else:
            raise Exception("Coords should be pairs of the integers from 0 to 2")

    def replace(self, replacement_board: list):
        """ replaces the current board with another provided board

        Args:
            replacementBoard (list): a new board
        """
        if len(replacement_board) == 3 and len(replacement_board[0] == 3):
            self.board = replacement_board
        else:
            raise Exception("The board should be 2D list 3x3")

    def get_validate_move(self) -> int:
        """ takes the user input (should be one of the board's fields ID's), validates it and returns it

        Returns:
            int: empty and existing field ID
        """
        while True:
            print ("choose the empty existing field (1-9): ")
            choice = int(input())
            if choice not in range(1, 10):
                continue
            coords = Board.get_coordinates(choice)
            row = coords[0]
            col = coords[1]
            if self.board[row][col] == " ":
                return choice

    @staticmethod
    def is_AI_move_valid(move: int, board: list) -> bool:
        """ takes an AI move as a desired field number, and returns the info if AI can move to that field

        Args:
            move (int): AI choice
            board: board

        Returns:
            bool: if the AI move is validate
        """
        coords = Board.get_coordinates(move)
        row = coords[0]
        col = coords[1]
        if board[row][col] == " " and move in range(1, 10):
            return True
        return False

    def get_game_status_for_rows_and_cols(self) -> str:
        """ returns one of the game statuses (1 for ongoing game, player name for player win) based ONLY on the rows and columns situation

        Returns:
            str: one of the game statuses
        """
        for i in range(3):
    
            if self.board[i][0] != ' ' and self.board[i][0] == self.board[i][1] and self.board[i][0] == self.board[i][2]:
                return self.board[i][0]
            if self.board[0][i] != ' ' and self.board[0][i] == self.board[1][i] and self.board[0][i] == self.board[2][i]:
                return self.board[0][i]
    
        return "1"

    def get_game_status_for_diagonals(self) -> str:
        """ returns one of the game statuses (1 for ongoing game, D for draw, player name for player win) based ONLY on the diagonals situation

        Returns:
            str: one of the game statuses
        """
        if self.board[0][0] != " " and self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        if self.board[0][2] != " " and self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0]:
            return self.board[0][2]
        return "1"    

    def is_there_free_field(self) -> bool:
        """ returns true if there is at least one free (filled with ' ') field on the board

        Returns:
            bool: if there is any free field
        """
        for row in self.board:
            if row.count(" ") > 0:
                return True
        return False
    
    def is_given_field_empty(self, row: int, col: int) -> bool:
        """ returns true if a field of the given coordinates is empty

        Args:
            row (int): row coordinate
            col (int): column coordinategi

        Returns:
            bool: if given board's field is empty
        """
        return self.board[row][col] == " "

    
        
            
        

