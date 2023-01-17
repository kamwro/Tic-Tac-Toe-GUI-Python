import PySimpleGUI as sg
from game_window import GameWindow

sg.theme('LightGrey1')

player1_name = "O"
player2_name = "X"

main_color = "DarkGrey"

welcome_text = [
            [sg.Text("Welcome to the Tic Tac Toe game!", font = "Any 25")],
            [sg.Text("This is a two player game without the AI or in the player vs AI mode.", font = "Any 18")],
            [sg.Text("Choose the game mode!", font = "Any 18")]
]

pvp_button = [sg.Button("Player vs Player", font = "Any 15", size = (30,2))]
pvr_button = [sg.Button("Player vs Random Computer", font = "Any 15", size = (30,2))]
pvs_button = [sg.Button("Player vs Smart Computer", font = "Any 15", size = (30,2))]
exit_button = [sg.Button("No, take me away!", font = "Any 14", size = (30,2), tooltip = "Press to exit")]

options_layout = [
            pvp_button, pvr_button, pvs_button, exit_button
        ]

layout = [
            welcome_text, [sg.Column(options_layout, expand_x=False, pad = 10)]
        ]

window = sg.Window("Tic Tac Toe", layout, use_default_focus = False, margins=(150,150), element_justification='c')

def event_loop():
    """ event loop for initial window. Player has option to start one of the 3 game modes in game window or exit the initial window
        
    """
    while True:
        event = window.read()[0]

        if event in ["Player vs Player", "Player vs Random Computer", "Player vs Smart Computer"]:
            window.Hide()
            game_window = GameWindow (event, player1_name, player2_name)
            game_window.event_loop()
            game_window.window.close()
            window.UnHide()
            
        if event == sg.WIN_CLOSED or event == "No, take me away!":
            break

event_loop()