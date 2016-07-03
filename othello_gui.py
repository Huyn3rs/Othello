# Huy Dinh Pham 64849059
# ICS 32 Lab 6
# Project #5

import tkinter
import othello_logic as othello
import othello_setup

DEFAULT_FONT = ('Comic Sans MS', 20)


class Othello:
    def __init__(self, ROWS, COLS, player, center, mode):
        self._rows = ROWS
        self._columns = COLS
        self._player = player
        self._center = center
        self._mode = mode

        self._radius_x = 0.8 * (1/(self._columns * 2))
        self._radius_y = 0.8 * (1/(self._rows * 2))
        
        
        self._board = create_board(self._rows, self._columns, self._center)
        

        self._root_window = tkinter.Tk()
        
##        othello title
        title_label = tkinter.Label(master = self._root_window,
                                    text = 'Othello',
                                    font = DEFAULT_FONT)

        title_label.grid(row = 0, column = 0,columnspan = 2,
                         sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

##        othello canvas
        self._canvas = tkinter.Canvas(
            master = self._root_window, width = 500, height = 500,
            background = '#006000')
        
        self._canvas.grid(
            row = 1, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        
##        othello score
        self._score = tkinter.StringVar()
        self._score.set(print_score(self._board))
        
        player_count = tkinter.Label(master = self._root_window,
                                    textvariable = self._score,
                                    font = DEFAULT_FONT)

        player_count.grid(row = 2, column = 0, columnspan = 2,
                          sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

##        othello turn
        self._turn = tkinter.StringVar()
        self._turn.set('Turn: ' + othello.icon(self._player))
        
        player_turn = tkinter.Label(master = self._root_window,
                                    textvariable = self._turn,
                                    font = ('Comic Sans MS', 12))

        player_turn.grid(row = 3, column = 0, padx = 5, pady = 5,
                         sticky = tkinter.W)

        hint_button = tkinter.Button(master = self._root_window,
                                     text = 'Hint',
                                     font = ('Comic Sans MS', 12),
                                     command = self._hints)
        hint_button.grid(row = 3, column = 1, padx = 5, pady = 5)

    

        self._canvas.bind('<Configure>', self._redraw_canvas)
        self._canvas.bind('<Button-1>', self._click_canvas)
        

        self._root_window.rowconfigure(1, weight = 1, minsize = 50)
        self._root_window.columnconfigure(0, weight = 1, minsize = 50)
      
    def start(self) -> None:
        self._root_window.mainloop()

    def _click_canvas(self, event: tkinter.Event) -> None:
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        x = event.x
        y = event.y
        
        row, col = pixels_to_coord(self._rows, self._columns,
                                           width, height,
                                           x, y)
        
        pieces = othello.flip_pieces(self._board, self._player,
                             self._rows - 1, self._columns - 1, row, col)
        try:
        
            if othello.valid_move(self._board, pieces, row, col):
                
                othello.place_move(self._board, self._player, (row, col))
                for piece in pieces:
                    othello.place_move(self._board, self._player, piece)

                self._player = othello.opposite(self._player)

                
                
                if not othello.possible_moves(self._board, self._player, self._rows - 1, self._columns - 1):
                    self._score.set(othello.icon(self._player) + ' cannot move.')
                    self._player = othello.opposite(self._player)
                    self._turn.set('Turn: ' + othello.icon(self._player))
                    
                    self._redraw_canvas(event)
                else:
                    self._score.set(print_score(self._board))
                    self._turn.set('Turn: ' + othello.icon(self._player))
                    
                    self._redraw_canvas(event)

        
                self.check_winner()
                

        except othello.InvalidOthelloMoveError:
            self._score.set('ERROR')

    def _redraw_canvas(self, event:tkinter.Event):
        self._canvas.delete(tkinter.ALL)
        
        self._redraw_board()
        self._redraw_pieces()
  
    def _redraw_board(self):
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
       

        rows = height / self._rows
        columns = width / self._columns
      
        for number in range(self._rows):
            self._canvas.create_line(0, rows * number,
                                     width, rows * number,
                                     fill = 'black')

        for number in range(self._columns):
            self._canvas.create_line(columns * number, 0,
                                     columns * number, height,
                                     fill = 'black') 


    def _redraw_pieces(self):
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        
        board_to_canvas(self._canvas, self._board, self._rows, self._columns, width, height, self._radius_x, self._radius_y)


    def _hints(self):
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        
        possible = othello.display_hints(self._board, self._player, self._rows, self._columns)
        for piece in possible:
            coord_to_piece(self._canvas, self._rows, self._columns,
                           width, height, piece, 'gray',
                           0.15 * (1/(self._columns * 2)), 0.15 * (1/(self._rows * 2)))

    def check_winner(self):
        if othello.check_winner(self._board, self._player, self._rows - 1, self._columns - 1):
            self._score.set(print_score(self._board))
            winner = othello.declare_winner(self._board, self._mode, self._player)
            
            play_again = othello_setup.WinnerDialog(print_winner(self._mode, winner))
            play_again.show()
            if play_again._yes_clicked():
                self._root_window.destroy()
                Othello(self._rows, self._columns, self._player, self._center, self._mode).start()
            else:
                self._root_window.destroy()
            
            

def create_board(ROWS: int, COLS: int, turn: str) -> [[str]]:
    board = othello.create_board(ROWS, COLS)
    othello.beginning_setup(board, turn, ROWS, COLS)

    return board

def pixels_to_coord(ROWS: int, COLS: int,
                    width_window: int, height_window: int,
                    x_pixel: int, y_pixel: int) -> tuple:
    '''takes pixel coordinates and converts it into a tuple of row and column coordinate.'''
    for row in range(ROWS):
        if row / ROWS < y_pixel/height_window <= (row + 1)/ROWS:
            x = row
    for column in range(COLS):
        if column / COLS < x_pixel/width_window <= (column + 1)/COLS:
            y = column
            
    return (x, y)

def board_to_canvas(canvas: tkinter, board: [[str]], ROWS: int, COLS: int,
                    width_window: int, height_window: int,
                    radius_x: float, radius_y: float) -> None:

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == othello.BLACK:
                coord_to_piece(canvas, ROWS, COLS, width_window, height_window, (row,col), 'black', radius_x, radius_y)
            elif board[row][col] == othello.WHITE:
                coord_to_piece(canvas, ROWS, COLS, width_window, height_window, (row,col), 'white', radius_x, radius_y)
    


def coord_to_piece(canvas: tkinter, ROWS: int, COLS: int,
                   width_window: int, height_window: int,
                   coordinate: tuple, color: str,
                   radius_x: float, radius_y: float) -> None:

    center_x = ((coordinate[1] * 2) + 1)/(COLS * 2) * width_window
    center_y = ((coordinate[0] * 2) + 1)/(ROWS * 2) * height_window

    radius_x *= width_window
    radius_y *= height_window

    canvas.create_oval(
        center_x - radius_x, center_y - radius_y,
        center_x + radius_x, center_y + radius_y,
        fill = color)
    


def print_score(board: [[str]]) -> str:
    black = othello.piece_count(board, 'X')
    white = othello.piece_count(board, 'O')
    return 'Black: {}        White: {}'.format(black, white)

def print_winner(mode: str, winner: str) -> None:
    '''Prints out a statement indicating the winner, depending on the mode.'''
    if winner in [othello.BLACK, othello.WHITE]:
        if mode == 'most':
            return('Player ' + othello.icon(winner) + ' won!!')
        elif mode == 'fewest':
            return('Player ' + othello.icon(othello.opposite(winner)) + ' won!!')
    else:
        return('It\'s a tie!!')


    

if __name__ == '__main__':
    setup = othello_setup.OthelloDialog()
    setup.start()
    
    if setup.ok_clicked():
        Othello(setup.rows(), setup.columns(), setup.player(), setup.center(), setup.mode()).start()
