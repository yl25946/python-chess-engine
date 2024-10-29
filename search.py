import chess
import copy
import time as stopwatch
import pesto_eval as pesto

# counter to measure the performance of the engine
nodes_evaluated = 0


def search(board, turn, time):
    """
    Uses alpha-beta pruning with negamax to find the best move in this position

    Uses iterative deepening

    Implements null-move pruning

    NOTE: will fuck up the original board, please make a copy

    LITERALLY JUST AN ABSTRACTION OF ALPHA_BETA_NEGAMAX

    Parameters:
    board (chess.Board()): the current board
    turn (chess.WHITE or chess.BLACK): color you want to find the best move
    time (int): number of seconds to calculate a move

    Return:
    chess.Move: the best move in that position
    int: the evaluation of the fed into board
    """
    depthCounter = 1
    end_time = stopwatch.time() + time
    last_completed_search = None
    # resets the counter
    global nodes_evaluated
    nodes_evaluated = 0
    previousEval = -10000
    # null_move_cutoff = 100000
    # implements iterative deepening
    try:
        while (True):
            last_completed_search = alpha_beta_negamax_search(
                board, turn, depthCounter, -100000, 100000, end_time)
            # if checkmate, then just play it, why the fuck are we searching more
            if (last_completed_search[1] == 10000):
                return last_completed_search
            depthCounter += 1
    # time is up
    except Exception as e:
        # print(e)
        print("Searched Depth(half-moves): " + str(depthCounter - 1))
        print("Searched " + str(nodes_evaluated / time) + " nodes per second")
        return last_completed_search


def alpha_beta_negamax_search(board, turn, depth, alpha, beta, end_time):
    """
    Uses alpha-beta pruning with negamax to find the best move in this position

    Parameters:
    board (chess.Board()): the current board
    turn (chess.WHITE or chess.BLACK): color you want to find the best move
    depth (int): number of half-moves you want to search
    alpha (int): worst you can get
    beta (int): the best your opponent can get
    end_time (long): time we want to finish calculations by

    Return:
    chess.Move: the best move in that position
    int: the evaluation of the fed into board

    TODO: Add in null-move heuristic
    TODO: add queistence search
    TODO: Add transposition table
    """

    # check if time is up, then throw an exception
    if (stopwatch.time() >= end_time):
        raise Exception("Out of time!")

    # we've starting to evaluate a node, increment the counter
    global nodes_evaluated
    nodes_evaluated += 1

    # if we ever check for a move here we're FUCKED

    # return heuristic evaluation if the game hasn't ended
    if (depth == 0):
        # print(board.fen())
        # print(pesto.eval(board, turn))
        return None, quiesce_search(board, turn, alpha, beta, end_time)

    # implements null move pruning
    if depth >= 3 and not board.is_check():
        null_board = copy.deepcopy(board)
        null_board.push(chess.Move.null())
        null_move_search = alpha_beta_negamax_search(
            null_board, turn ^ 1, depth - 2, -beta, -beta + 1, end_time)
        null_move_cutoff = -null_move_search[1]
        # prune if above cutoff
        if null_move_cutoff >= beta:
            return None, null_move_cutoff
        # print(null_move_cutoff)

    # start the search
    legal_moves = board.legal_moves
    # best_eval = -10000
    best_move = None

    # TODO: ADD GOOD MOVE ORDERING
    # curr_move is the current move we are searching
    for curr_move in legal_moves:
        board.push(curr_move)
        # turn ^ 1 flips the turn
        search_result = alpha_beta_negamax_search(
            board, turn ^ 1, depth - 1, -beta, -alpha, end_time)
        board.pop()
        eval = - search_result[1]
        if (eval >= beta):
            # uh if it does this on the first move we're kinda fucked
            # but if it returns we never use it?
            return curr_move, beta
        if (eval > alpha):
            # alpha acts like max in MiniMax
            alpha = eval
            best_move = curr_move
    return best_move, alpha


def quiesce_search(board, turn, alpha, beta, end_time):
    """
    Performes a Quiescent Search to make sure we aren't throwing the move

    Parameters:
    board (chess.Board): the board position you want to perform the search on
    alpha (int): worst you could do 
    beta (int): the best your opponent could do
    end_time (long): time we want to finish calculations by

    return
    int: evaulation of the position in centripawns
    """

    # check if time is up, then throw an exception
    if (stopwatch.time() >= end_time):
        raise Exception("Out of time!")

    # increments the node searched
    global nodes_evaluated
    nodes_evaluated += 1

    # fail soft
    stand_pat = pesto.eval(board, turn)
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat

    capture_moves = [
        move for move in board.legal_moves if board.is_capture(move)]

    for move in capture_moves:
        # if there aren't any captures
        if (move == None):
            continue
        board.push(move)
        # turn ^ 1 switches the turn to the other side
        score = - quiesce_search(board, turn ^ 1, -beta, -alpha, end_time)
        board.pop()

        if (score >= beta):
            return beta
        if (score > alpha):
            alpha = score

    return alpha

# def negamax(board, turn, depth, end_time):
#     """
#     Uses alpha-beta pruning with negamax to find the best move in this position

#     Parameters:
#     board (chess.Board()): the current board
#     turn (chess.WHITE or chess.BLACK): color you want to find the best move
#     depth (int): number of half-moves you want to search
#     alpha (int): worst you can get
#     beta (int): the best your opponent can get
#     end_time (long): time we want to finish calculations by

#     Return:
#     chess.Move: the best move in that position
#     int: the evaluation of the fed into board

#     TODO: Add in null-move heuristic
#     TODO: add queistence search
#     TODO: Add transposition table
#     """

#     # check if time is up, then throw an exception
#     if (stopwatch.time() >= end_time):
#         print(end_time)
#         print(stopwatch.time())
#         raise Exception("Out of time!")

#     # if we ever check for a move here we're FUCKED

#     # checking end-states
#     if (board.is_checkmate()):
#         return None, -10000
#     if (board.is_stalemate()):
#         return None, 0
#     if (board.is_insufficient_material()):
#         return None, 0
#     if (board.is_fifty_moves()):
#         return None, 0
#     # TODO: ADD IN EFFICIENT REPITITION

#     # return heuristic evaluation if the game hasn't ended
#     # TODO: ADD QUIESCE HERE
#     if (depth == 0):
#         # print(board.fen())
#         # print(pesto.eval(board, turn))
#         return None, pesto.eval(board, turn)

#     # start the search
#     legal_moves = board.legal_moves
#     best_eval = -10000
#     best_move = None

#     # TODO: ADD GOOD MOVE ORDERING
#     # curr_move is the current move we are searching
#     for curr_move in legal_moves:
#         # make a copy of the board and search it
#         board_copy = copy.deepcopy(board)
#         board_copy.push(curr_move)
#         # turn ^ 1 flips the turn
#         search_result = negamax(
#             board_copy, turn ^ 1, depth - 1, end_time)
#         if (search_result[1] > best_eval):
#             best_move = search_result[0]
#             best_eval = search_result[1]
#     return best_move, best_eval


# pesto.init_tables()
# board = chess.Board()
# board.set_fen(
#     "rnbq1rk1/pppn1ppp/4p3/3pP3/1b1P4/2NB1N2/PPP2PPP/R1BQK2R w KQq - 0 1")
# print(board)
# print(search(board, chess.WHITE, 15))
