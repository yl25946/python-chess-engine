import chess

# NULL_MOVE = "0000"

"""EVALUATION PORTION OF THE PROGRAM: PeSTO"""

"""NOTE: PESTO PIECE VALUES ARE 1 LESS THAN chess PACKAGE"""

"""NOTE: PESTO WHITE VALUE IS 0, WHILE PYTHON-CHESS IS 1"""

# initiates the constants
WHITE = 0
BLACK = 1


# values for doing something that I don't know what it's doing
mg_value = [82, 337, 365, 477, 1025,  0]
eg_value = [94, 281, 297, 512,  936,  0]

# eval tables, remain constant so we don't have to construct them every time we call eval()
mg_pawn_table = [
    0,   0,   0,   0,   0,   0,  0,   0,
    98, 134,  61,  95,  68, 126, 34, -11,
    -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
    0,   0,   0,   0,   0,   0,  0,   0,
]

eg_pawn_table = [
    0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
    94, 100,  85,  67,  56,  53,  82,  84,
    32,  24,  13,   5,  -2,   4,  17,  17,
    13,   9,  -3,  -7,  -7,  -8,   3,  -1,
    4,   7,  -6,   1,   0,  -5,  -1,  -8,
    13,   8,   8,  10,  13,   0,   2,  -7,
    0,   0,   0,   0,   0,   0,   0,   0,
]

mg_knight_table = [
    -167, -89, -34, -49,  61, -97, -15, -107,
    -73, -41,  72,  36,  23,  62,   7,  -17,
    -47,  60,  37,  65,  84, 129,  73,   44,
    -9,  17,  19,  53,  37,  69,  18,   22,
    -13,   4,  16,  13,  28,  19,  21,   -8,
    -23,  -9,  12,  10,  19,  17,  25,  -16,
    -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23,
]

eg_knight_table = [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64,
]

mg_bishop_table = [
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
    -4,   5,  19,  50,  37,  37,   7,  -2,
    -6,  13,  13,  26,  34,  12,  10,   4,
    0,  15,  15,  15,  14,  27,  18,  10,
    4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,
]

eg_bishop_table = [
    -14, -21, -11,  -8, -7,  -9, -17, -24,
    -8,  -4,   7, -12, -3, -13,  -4, -14,
    2,  -8,   0,  -1, -2,   6,   0,   4,
    -3,   9,  12,   9, 14,  10,   3,   2,
    -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17,
]

mg_rook_table = [
    32,  42,  32,  51, 63,  9,  31,  43,
    27,  32,  58,  62, 80, 67,  26,  44,
    -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26,
]

eg_rook_table = [
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
    7,  7,  7,  5,  4,  -3,  -5,  -3,
    4,  3, 13,  1,  2,   1,  -1,   2,
    3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20,
]

mg_queen_table = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
    -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
    -1, -18,  -9,  10, -15, -25, -31, -50,
]

eg_queen_table = [
    -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
    3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41,
]

mg_king_table = [
    -65,  23,  16, -15, -56, -34,   2,  13,
    29,  -1, -20,  -7,  -8,  -4, -38, -29,
    -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
    1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
]

eg_king_table = [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
    10,  17,  23,  15,  20,  45,  44,  13,
    -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43
]

mg_pesto_table = [
    mg_pawn_table,
    mg_knight_table,
    mg_bishop_table,
    mg_rook_table,
    mg_queen_table,
    mg_king_table
]

eg_pesto_table = [
    eg_pawn_table,
    eg_knight_table,
    eg_bishop_table,
    eg_rook_table,
    eg_queen_table,
    eg_king_table
]

gamephaseInc = [0, 0, 1, 1, 1, 1, 2, 2, 4, 4, 0, 0]
# creates the tables
mg_table = [[0 for i in range(64)] for j in range(12)]
eg_table = [[0 for i in range(64)] for j in range(12)]


def piece_value(piece):
    """Get's the value of the piece evaluated, specified in the PeSTO code

    Parameters:
    piece (chess.Piece): the piece you want to convert to a int

    Return:
    int: integer value of the piece"""

    # not it to get the correct value for PeSTO
    return ((2*(piece.piece_type - 1)) + (not piece.color))


def flip(square):
    """flips the square to the other side of the board

    Parameter:
    square (int): the square you want to flip to the other side of the board

    Return:
    int: the flipped square"""

    return square ^ 56


def init_tables():
    """
    Initializes the tables
    """

    # chess.PAWN is one greater than PeSTO's
    piece = chess.PAWN - 1
    #  2 * piece value + color
    piece_color = 0

    # some magic fuckery happens here, figure this out later
    # chess.KING is one greater than PeSTO's
    while (piece < chess.KING):
        for square in range(64):
            # flip white because python-chess a1 = 0, but PeSTO a8 = 0
            mg_table[piece_color][square] = mg_value[piece] + \
                mg_pesto_table[piece][flip(square)]
            eg_table[piece_color][flip(square)] = eg_value[piece] + \
                eg_pesto_table[piece][square]
            mg_table[piece_color + 1][square] = mg_value[piece] + \
                mg_pesto_table[piece][square]
            eg_table[piece_color + 1][square] = eg_value[piece] + \
                eg_pesto_table[piece][square]
        # increment the counters, outside the for loop
        piece_color += 2
        piece += 1


def eval(board, side2move):
    """
    Evaluates the board position using PeSTO's hand-crafted evalution

    Parameters:
    board (chess.BaseBoard): the board to evaluate
    side2move (chess constant): which side is moving (Chess.WHITE, Chess.BLACK)

    Returns:
    float: evaluation of the position
    """

    # checking end-states
    if (board.is_checkmate()):
        return -10000
    if (board.is_stalemate()):
        return 0
    if (board.is_insufficient_material()):
        return 0
    if (board.is_fifty_moves()):
        return 0
    # TODO: ADD IN EFFICIENT REPITITION

    # convert side2move from python-chess notation to PeSTO notation
    # so what the fuck I don't need this?
    # if something breaks, add it back in
    side2move ^= 1

    mg = [0, 0]
    eg = [0, 0]
    gamePhase = 0

    # evaluates each piece
    for square in range(64):
        piece = board.piece_at(square)
        if (piece != None):
            # value of the piece including color
            piece_color = piece_value(piece)
            # finds the color of the piece
            mg[piece_color & 1] += mg_table[piece_color][square]
            eg[piece_color & 1] += mg_table[piece_color][square]
            # determines the game phase
            gamePhase += gamephaseInc[piece_color]

    # tapered eval
    # sidemove ^ 1 finds the other side
    mgScore = mg[side2move] - mg[side2move ^ 1]
    egScore = eg[side2move] - eg[side2move ^ 1]
    mgPhase = gamePhase
    if (gamePhase > 24):
        mgPhase = 24  # in case of early promotion ()
    egPhase = 24 - mgPhase
    return ((mgScore * mgPhase) + (egScore * egPhase))//24


# init_tables()
# board = chess.Board()
# board.set_fen("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
# print(eval(board, chess.BLACK))
