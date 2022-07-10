from math import inf, sqrt, log
from random import randint
from copy import deepcopy
import time
boards = 0
#board = ['X', ' ', 'X', ' ', ' ', ' ', ' ', 'O', ' ']
#board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', 'O', ' ', ' ', ' ', ' ', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
class Node:
    """
    # Node
    The Node class defines a node in a
    Monte-Carlo Search Tree, with all
    requisite parameters.
    """
    def __init__(self, board, player_id, move):
        self.wins = 0.0
        self.games = 0.0
        self.move = move
        self.board = board
        self.player_id = player_id
        self.children = []

def player(board) -> str:
    """Returns player who has the next turn on a board."""
    x_count = 0
    o_count = 0
    for i in board:
        if i == 'X':
            x_count += 1
        if i == 'O':
            o_count += 1 
        
    if x_count > o_count:
        return 'O'
    else:
        return 'X'

def check_win_3x3(board):
    """
    This function checks for all possible four-in-a-row wins on a
    3x3 tic-tac-toe board.
    """
    # Possible Horizontal Wins
    horizontal = [0, 3, 6]
    for i in horizontal:
        if (board[i] != ' '
           and board[i] == board[i + 1] == board[i + 2]):
            return board[i]

    # Possible Diagonal wins, left to right
    l_diagonal = 0
    i = l_diagonal
    if (board[i] != ' 'and board[i] == board[i + 3 + 1] == board[i + 6 + 2] ):
        return board[i]
    # Possible Diagonal wins, right to left
    r_diagonal = 2
    i = r_diagonal
    if (board[i] != ' 'and board[i] == board[i + 3 - 1] == board[i + 6 - 2] ):
        return board[i]

    # Possible Vertical wins
    for i in range(3):
        if (board[i] != ' '
           and board[i] == board[i + 3] == board[i + 6]):
            return board[i]

    # Possible draw
    draw = True
    for char in board:
        if char == ' ':
            draw = False

    if draw:
        return "draw"

    return ' '
def check_win_5x5(board):
    """
    This function checks for all possible four-in-a-row wins on a
    5x5 tic-tac-toe board.
    """
    # Possible Horizontal Wins
    horizontal = [0, 1, 5, 6, 10, 11, 15, 16, 20, 21]
    for i in horizontal:
        if (board[i] != ' '
           and board[i] == board[i + 1] == board[i + 2] == board[i + 3]):
            return board[i]

    # Possible Diagonal wins, left to right
    l_diagonal = [0, 1, 5, 6]
    for i in l_diagonal:
        if (board[i] != ' '
           and board[i] == board[i + 5 + 1] == board[i + 10 + 2] == board[i + 15 + 3]):
            return board[i]

    # Possible Diagonal wins, right to left
    r_diagonal = [3, 4, 8, 9]
    for i in r_diagonal:
        if (board[i] != ' '
           and board[i] == board[i + 5 - 1] == board[i + 10 - 2] == board[i + 15 - 3]):
            return board[i]

    # Possible Vertical wins
    for i in range(10):
        if (board[i] != ' '
           and board[i] == board[i + 5] == board[i + 10] == board[i + 15]):
            return board[i]

    # Possible draw
    draw = True
    for char in board:
        if char == ' ':
            draw = False

    if draw:
        return "draw"

    return ' '
def check_win_7x7(board):
    """
    This function checks for all possible four-in-a-row wins on a
    5x5 tic-tac-toe board.
    """
    # Possible Horizontal Wins
    horizontal = [0, 1, 2, 7, 8, 9, 14, 15, 16, 21, 22, 23, 28, 29, 30, 35, 36, 37, 42, 43, 44]
    for i in horizontal:
        if (board[i] != ' '
           and board[i] == board[i + 1] == board[i + 2] == board[i + 3] == board[i + 4]):
            return board[i]

    # Possible Diagonal wins, left to right
    l_diagonal = [0, 1, 2, 7, 8, 9, 14, 15, 16]
    for i in l_diagonal:
        if (board[i] != ' '
           and board[i] == board[i + 7*1 + 1] == board[i + 7*2 + 2] == board[i + 7*3 + 3] == board[i+7*4+4]):
            return board[i]

    # Possible Diagonal wins, right to left
    r_diagonal = [4, 5, 6, 11, 12, 13, 18, 19, 20]
    for i in r_diagonal:
        if (board[i] != ' '
           and board[i] == board[i + 7*1 - 1] == board[i + 7*2 - 2] == board[i + 7*3 - 3] == board[i + 7*4 - 4]):
            return board[i]

    # Possible Vertical wins
    for i in range(21):
        if (board[i] != ' '
           and board[i] == board[i + 7] == board[i + 7*2] == board[i + 7*3] == board[i+ 7*4]):
            return board[i]

    # Possible draw
    draw = True
    for char in board:
        if char == ' ':
            draw = False

    if draw:
        return "draw"

    return ' '
def mcts(node, check_win , ROWS, COLS, expanding=False):
    """
    # mcts
    This function implements Monte-Carlo Tree Search.
    """
    global boards
    boards += 1

    node.games += 1
    if check_win(node.board) != ' ':
        if check_win(node.board) == 'X' or check_win(node.board) == 'O':
            node.wins += 1
        return

    # Selection
    move = -1
    next_player = 'O' if node.player_id == 'X' else 'X'
    next_board = deepcopy(node.board)
    if len(node.children) == ROWS * COLS:
        max_uct = -inf
        for child in node.children:
            uct = child.wins/child.games + sqrt(log(node.games) / child.games)
            if uct > max_uct:
                max_uct = uct
                move = child.move

    # Expansion and Simulation
    elif not expanding:
        for move_expansion in range(ROWS* COLS):
            if node.board[move_expansion] != ' ':
                continue
            next_board = deepcopy(node.board)
            next_board[move_expansion] = node.player_id
            next_node = Node(next_board, next_player, move_expansion)
            is_child = False
            for child in node.children:
                if child.board == next_board:
                    next_node = child
                    is_child = True
            if not is_child:
                node.children.append(next_node)
            mcts(next_node, check_win, ROWS, COLS, True)
    else:
        move = randint(0, ROWS * COLS - 1)
        while node.board[move] != ' ':
            move = randint(0, ROWS * COLS - 1)
        next_board[move] = node.player_id
        next_node = Node(next_board, next_player, move)
        is_child = False
        for child in node.children:
            if child.board == next_board:
                next_node = child
                is_child = True
        if not is_child:
            node.children.append(next_node)
        mcts(next_node, check_win, ROWS, COLS, expanding)

    # Back-Propagation
    node.wins = 0
    node.games = 0
    if node.children:
        for child in node.children:
            node.wins += child.games - child.wins
            node.games += child.games

def ai_move(board, player_id, check_win, ROWS, COLS, level):
    algorithm = "mcts"
    if algorithm == "mcts":

        move = -1
        root = Node(board, player_id, -1)
        start = time.time()
        turn_length = level
        while time.time() < start + turn_length:
            mcts(root, check_win, ROWS, COLS)

        best_score = -inf
        print(f"length of children: {len(root.children)}")
        for child in root.children:
            if child.wins / child.games > best_score:
                move = child.move
                best_score = child.wins / child.games

        if move == -1:
            print("Random move")
            move = randint(0, ROWS*COLS - 1)

        board[move] = player_id
        print(f"Calls to mcts: {boards}")
    return move


#ROWS, COLS = 5,5
#move = (ai_move(board,'O',check_win_5x5, ROWS, COLS))
#print(board)