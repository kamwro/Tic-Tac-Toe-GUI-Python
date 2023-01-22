class WrongCoordinatesError(Exception):
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __repr__(self):
        return "Coords should be pairs of the integers from 0 to 2, meanwhile provided coords: {} {}".format(self.row, self.col)
    
class WrongFieldIDError(Exception):
     def __init__(self, field_ID):
        self.field_ID = field_ID
     def __repr__(self):
        return "Field ID should be an integer between 1 and 9, meanwhile provided Field ID: {}".format(self.field_ID)   


class WrongBoardError(Exception):
    def __init__(self, board):
        self.board = board
    def __repr__(self):
        return "The board should be 2D list 3x3. Provided board: {}".format(self.board)