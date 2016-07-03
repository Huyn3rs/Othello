# Huy Dinh Pham 64849059
# ICS 32 Lab 6
# Project #5

BLACK = 'X'
WHITE = 'O'
NONE = '.'




class InvalidOthelloMoveError(Exception):
    '''Raised whenever an invalid move is made.'''
    
def valid_board_size(ROWS: str, COLS: str)-> bool:
    '''Checks the rows and columns to see if they follow the specific format.'''
    try:
        if int(ROWS)% 2 == 0 and  4 <= int(ROWS) <= 16 and \
           int(COLS)% 2 == 0 and  4 <= int(COLS) <= 16:
            return True
        else:
            return False
    except ValueError:
        return False

def valid_row_and_column(row: int, col: int, ROWS: int, COLS: int) -> bool:
    '''checks if the row and column input are valid.'''
    if 0 <= row <= ROWS and \
        0 <= col <= COLS:
        return True
    
    else:
        raise InvalidOthelloMoveError()

def valid_move(board: [[str]], pieces: [str], row: int, col: int) -> bool:
    '''Checks if a move is valid or not by indicating
    whether a piece is able to flip other pieces when placed.'''

    if board[row][col] == '.' and \
       len(pieces) != 0:
           
        return True
    else:
        raise InvalidOthelloMoveError()



def beginning_setup(board: [[str]], turn: str, rows: str, columns: str) -> [[str]]:
    '''places the four center pieces on the board in the standardized format.'''
    
    board[int((rows - 1) / 2)][int((columns - 1) / 2)] = turn
    board[int((rows + 1) / 2)][int((columns + 1) / 2)] = turn
    board[int((rows + 1) / 2)][int((columns - 1) / 2)] = opposite(turn)
    board[int((rows - 1) / 2)][int((columns + 1) / 2)] = opposite(turn)

def place_move(board: [[str]], player: str, move: tuple):
    x, y = move
    board[x][y] = player
    

def flip_pieces(board: [[str]], player: str, ROWS: int, COLS: int, row: int, col: int):
    '''Flips the pieces that correspond with the placment of a piece. '''
    
    pieces = []
    
    pieces.extend(check_pieces(board, player, ROWS, COLS, row, col,-1, 0))
    pieces.extend(check_pieces(board, player, ROWS, COLS, row, col, -1, 1))
    pieces.extend(check_pieces(board, player, ROWS, COLS, row, col, 0, 1))
    pieces.extend(check_pieces(board, player, ROWS, COLS, row, col, 1, 1))
    pieces.extend(check_pieces(board, player, ROWS, COLS, row, col, 1, 0))
    pieces.extend(check_pieces(board, player, ROWS, COLS, row, col, 1, -1))
    pieces.extend(check_pieces(board, player, ROWS, COLS, row, col, 0, -1))
    pieces.extend(check_pieces(board, player, ROWS, COLS, row, col, -1, -1))
    
    return pieces

def check_pieces(board: [[str]], player: str, ROWS: int, COLS: int, row: int, col: int, x: int, y: int):
    '''checks the board to see if any pieces are flipped with a piece is played.'''

    pieces = []
    try:
        for num in range(1, 17):
            
            if valid_row_and_column(row + (x * num), col + (y * num), ROWS, COLS):
                if board[row + (x * num)][col + (y * num)] == opposite(player):
                    pieces.append((row + x * num, col + y * num))
                    
                elif board[row + x * num][col + y * num] == player: 
                    return pieces
                
                else:
                    return []
            
    except InvalidOthelloMoveError:
        return []
        

def check_winner(board: [[str]], player: str, ROWS: int, COLS:int) -> bool:
    '''Returns true if both player cannot make any further moves.'''
    
    return not possible_moves(board, player, ROWS, COLS) and \
           not possible_moves(board, opposite(player), ROWS, COLS)

def declare_winner(board: [[str]], mode: str, player: str) -> None:
    '''if a winner is found, this function prints a statement depending on the mode specified in the beginning.'''

    if piece_count(board, player) > \
       piece_count(board, opposite(player)):
        return player
    elif piece_count(board, player) < \
         piece_count(board, opposite(player)):
        return opposite(player)
    else:
        return None
            

def possible_moves(board: [[str]], player: str, ROWS: int, COLS:int) -> bool:
    
    count = 0
    for row in range(ROWS + 1):
        for col in range(COLS + 1):
            if board[row][col] == NONE:
                if len(flip_pieces(board, player, ROWS, COLS, row, col)) != 0:
                    
                    count += 1

    return count != 0

def piece_count(board: [[str]], player: str) -> int:
    '''counts the pieces on the board.'''
    count = 0
    for row in board:
        for piece in row:
            if piece == player:
                count += 1

    return count

def opposite(player: str) -> str:
    '''returns the opposite player.'''
    if player == WHITE:
        return BLACK
    elif player == BLACK:
        return WHITE
    
    
def icon(player: str) -> str:
    '''replaces the color with the icon.'''
    if player == WHITE:
        return 'WHITE'
    elif player == BLACK:
        return 'BLACK'

def create_board(ROWS: int, COLUMNS: int) -> [[str]]:
    '''creates a board with specified rows and columns.'''
    board = []

    for row in range(int(ROWS)):
        rows = []
        for col in range(int(COLUMNS)):
            rows.append(NONE)
        board.append(rows)

    return board


def display_hints(board: [[str]], player: str, ROWS: int, COLS:int) -> bool:
    '''displays hints for possible moves'''

    possible = []
    
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == NONE:
                if len(flip_pieces(board, player, ROWS - 1, COLS - 1, row, col)) != 0:
                    possible.append((row ,col))
                
    return possible


