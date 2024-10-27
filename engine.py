import chess
import copy
import search
import pesto_eval as pesto

"""UTILITY METHODS"""


def turn_to_string(turn):
    """
    Turns the turn from chess.WHITE to "white"

    Parameters:
    turn (chess.WHITE or chess.BLACK): who has the turn

    Returns:
    string: string representation of the turn
    """
    return "white" if (turn == chess.WHITE) else "black"


def check_end_game(board, turn):
    """
    checks if the game has ended, and prints out the corresponding message
    NOTE: assume you are checking before you make a move

    Parameters:
    board (chess.Board): board we are examining
    turn (chess.WHITE or chess.BLACK): board we are 

    Returns:
    boolean: True if the game has ended, False if it hasn't
    """

    # outcome is in enum chess.Termination
    outcome = board.outcome()

    # continue playing
    if (outcome == None):
        return False

    # game has ended, output the correct message
    # for additional info about documentaiton, go look it up
    if (outcome == 1):
        print(turn_to_string + "got checkmated!")
    if (outcome == 2):
        print("Stalemate!")
    if (outcome == 3):
        print("Insufficient Material!\nDraw!")
    if (outcome == 6):
        print("Fifty Move Rule!\nDraw!")
    if (outcome == 7):
        print("Threefold Repitition!\nDraw!")

    return True


"""MAIN FUNCTION"""

# need to initialize the tables first dumbass
pesto.init_tables()

# gotta cast to int dumbass
time = int(
    input("how many seconds do you want the engine to take to make a move? "))

engine_input = input("0 if you want engine to be white, 1 if black. ")

# sets the color the engine will be playing as
engine_color = chess.WHITE if engine_input == '0' else chess.BLACK

"""TODO: ENCORPERATE OPENING/ENDING BOOKS"""

# we will be playing using this board
board = chess.Board()

# prints the initial board state
print(board)

# engine plays as white
if (engine_color == chess.WHITE):
    # we will move in a two move cycle
    while (not check_end_game(board, chess.WHITE)):
        # searching fucks up the original board, make a copy to push the move
        board_copy = copy.deepcopy(board)
        # computer searching
        search_result = search.search(board, engine_color, time)
        # play the move
        board_copy.push(search_result[0])
        board = board_copy

        # updates the board
        print(board)

        # prints the estimated evaluation
        print("Estimated evaluation: " + str((search_result[1])/100))
        print("Move: " + str(search_result[0]))

        # checks if the game has ended
        if (check_end_game(board, chess.WHITE)):
            break

        # process to read in the board
        move_played = False
        player_move = input("Please input your move using UCI notation: ")
        while (not move_played):
            try:
                board.push_uci(player_move)
                move_played = True
            except:
                player_move = input("Invalid move, please enter another one: ")

        # updates the board
        print(board)
        # the move stack is preserved
        # print(board.move_stack)
# engine plays as black
else:
    # we will move in a two move cycle
    while (not check_end_game(board, chess.BLACK)):
        # process to read in the board
        move_played = False
        player_move = input("Please input your move using UCI notation: ")
        while (not move_played):
            try:
                board.push_uci(player_move)
                move_played = True
            except:
                player_move = input("Invalid move, please enter another one: ")

        # update the board
        print(board)

        # checks if the game has ended
        if (check_end_game(board, chess.BLACK)):
            break

        # computer searching
        # searching fucks up the original board, make a copy to push the move
        board_copy = copy.deepcopy(board)
        search_result = search.search(board, engine_color, time)
        # play the move
        board_copy.push(search_result[0])
        board = board_copy
        print(board)

        # prints the estimated evaluation
        print("Estimated evaluation: " + str((- search_result[1])/100))
        print("Move: " + str(search_result[0]))
