import PySimpleGUI as sg
from Board import Board
from AI import AI
from GameMaster import GameMaster

main_color = "LightGrey"
other_color = "DarkBlue"

class GameWindow:

    def __init__(self, game_mode: str, player_1_name: str, player_2_name: str):
        """ initializes an instance of the GameWindow object, sets the board, player, game mode, players names, object for AI, layout, theme and window

        Args:
            game_mode (str): 'Player vs Player', 'Player vs Random Computer' or 'Player vs Smart Computer'
            player_1_name (str): name of the first player (preferably 'O')
            player_2_name (str): name of the second player (preferably 'X')
        """

        self.board = {}
        #0 for player1, 1 for player2 (AI is always player2)
        self.player = 0
        #Player vs Player, Player vs Random Computer or Player vs Smart Computer
        self.game_mode = game_mode 
        self.player_1_name = player_1_name
        self.player_2_name = player_2_name
        #AI
        self.computer = AI(player_2_name, self.game_mode)

        self.players_names_validation()

        #buttons
        next_turn_button = [sg.Button('Next Turn', size = (44,1), visible = (False if self.game_mode == "Player vs Player" else True), disabled = True, pad = 5, key = "next_turn_button", button_color = main_color)]
        reset_button = sg.Button('Reset', size = (13,2), pad = 5, button_color = other_color)
        change_mode_button = sg.Button("Change mode", size = (13,2), pad = 5, button_color = other_color)
        leave_button = sg.Button("Leave", size = (13,2), pad = 5, button_color = other_color)

        tiles_buttons = [[sg.Button(size=(13, 5), key = (row, col), button_color = main_color) for col in range(3)] for row in range(3)]

        #texts
        game_mode_info = [sg.Text(self.game_mode, font = "Any 20", key = "mode_info", pad = 5, justification = "center")]
        player_info = [sg.Text("Player 1 move!", font = "Any 20", key = "player_info", pad = 5, justification = "center")]

        self.layout = [
            game_mode_info,
            player_info,
            next_turn_button,
            tiles_buttons,
            [reset_button, change_mode_button, leave_button]
        ]
        
        sg.theme('LightGrey')
        self.window = sg.Window("Tic Tac Toe", self.layout, use_default_focus = False, margins = (88,22), finalize = True)

    #game loop
    def event_loop(self):
        """ game (event) loop. Event are: leaving the game, resetting the game, changing game mode, clicking on one of the tiles or AI choosing one of the tile
        """

        while True:
            event = self.window.read()[0]

            if event == "Leave" or event == sg.WIN_CLOSED:
                exit()
                
            elif event == "Reset":
                self.reset()

            elif event == "Change mode":
                break
            
            #player2 turn and player2 == computer player
            elif self.player and self.game_mode != "Player vs Player":
                self.computer_turn()

            #one of the human players clicked on the active tile
            elif event not in self.board:
                self.next_player_turn(event)

            #refresh
            else:
                self.window.read(timeout=400)

    ## methods

    def computer_turn(self):
        """ computer (AI) turn in which one of the tile is updated and the board is evaluated, and then player switched
        """
        self.update_the_tile_AI()
        self.evaluate_the_board()

    def next_player_turn(self, event):
        """ human player turn in which one of the tile is updated and the board is evaluated, and then player switched

        Args:
            event (tuple): coordinates of the player choice
        """
        self.update_the_tile_human(event)
        self.evaluate_the_board()

    def update_the_tile_AI(self):
        """ updates the tile with the AI name and disables it
        """
        event = self.computer.get_player_move(self.convert_board_to_list(), self.player_1_name)
        self.board[event] = self.player
        self.window[event].update(self.player_2_name, disabled = True, button_color = "Black")

    def update_the_tile_human(self, event):
        """ updates the tile with the player name and disables it

        Args:
            event (tuple): coordinates of the player choice
        """
        self.board[event] = self.player
        self.window[event].update(self.player_2_name if self.player else self.player_1_name, disabled = True, button_color = ("Black" if self.player else "Purple"))

    def evaluate_the_board(self):
        """ prepares the board for the next turn, switches the turn and checks if game is draw or if someone winned
        """
        self.prepare_the_board_for_next_turn()
        self.switch_turn()
        self.check_the_game_status()
        
    def prepare_the_board_for_next_turn(self):
        """ after AI turn enables back the empty tile buttons and disables next turn button or
            after human player turn, disables all the tile buttons and enables next turn button if player 2 is computer
        """
        if self.player and self.game_mode != "Player vs Player":
            self.enable_the_tiles_buttons_disable_next_turn_button()
        else:
            self.window["next_turn_button"].update(disabled = False, button_color = other_color)
            if self.game_mode != "Player vs Player":
                self.disable_the_tile_buttons()

    def switch_turn(self):
        """ changes the current player and updates the player info in the window
        """
        self.player = 1 - self.player
        self.window['player_info'].update("Player {} move!".format(str(self.player+1)))

    def check_the_game_status(self):
        """ checks if game is draw or someone has winned and if so stop the game and show appropriate message
        """
        gm = GameMaster() 
        gm.evaluate_the_game_status(self.convert_board_to_list())
        game_status = gm.get_the_game_status()
        if game_status == "0":
            self.window['mode_info'].update("Draw!        ")
            self.window['player_info'].update("Nobody wins.")
            self.disable_the_board()
        elif game_status == "1":
            pass
        else:
            self.window['mode_info'].update("Game over!    ")
            self.window['player_info'].update("Player {} wins!".format("1" if game_status == self.player_1_name else "2"))
            self.disable_the_board()

    def convert_board_to_list(self) -> list:
        """ converts the board used by game window (which is dict with pairs: coords(tuple): player (0 or 1)) to pythonic 2D 9-grid list with board's fields
        (to help evaluate the board in the minimax algorithm method)

        Returns:
            list: pythonic 2D 9-grid list with board's fields 
        """
        board = Board()
        for coords, player in self.board.items():
            if player:
                player_tag = self.player_2_name 
            else:
                player_tag = self.player_1_name
            board.update_with_coords(player_tag, coords)
        return board.board
    
    def disable_the_board(self):
        """ disables the next turn button and tiles buttons
        """
        self.window["next_turn_button"].update(disabled = True, button_color = main_color)
        self.disable_the_tile_buttons()

    def disable_the_tile_buttons(self):
        """ disables the tiles buttons
        """
        for row in range(3):
            for col in range(3):
                self.window[(row, col)].update(disabled = True)

    def enable_the_tiles_buttons_disable_next_turn_button(self):
        """ enables the tiles buttons but disables the next turn button
        """
        self.window["next_turn_button"].update(disabled = True, button_color = other_color)
        for row in range(3):
            for col in range(3):
                try:
                    self.board[(row,col)]
                except KeyError:
                    self.window[(row, col)].update(disabled = False)

    def players_names_validation(self):
        """ if one at least one of player names are "0" or "1" they need to be changed in order to not interfere with GameMaster evaluate_the_game_status method
        """
        for name in [self.player_1_name, self.player_2_name]:
            if (name == "0"):
                name = "zero"
            elif (name == "1"):
                name = "one"

    def reset(self):
        """ resets the board and player attributes, next turn button and mode and player infos to their initial values, and cleans all the tiles buttons
        """
        self.board, self.player = {}, 0
        for row in range(3):
            for col in range(3):
                self.window[(row, col)].update(" ", disabled = False, button_color = main_color)
        self.window["next_turn_button"].update(disabled = True)        
        self.window['mode_info'].update(self.game_mode)
        self.window['player_info'].update("Player 1 move!")