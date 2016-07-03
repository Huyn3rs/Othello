# Huy Dinh Pham 64849059
# ICS 32 Lab 6
# Project #5

import tkinter
import othello_logic as othello

DEFAULT_FONT = ('Comic Sans MS', 15)
ERROR_FONT = ('Times New Roman', 15)

class OthelloDialog:
    def __init__(self):
        self._dialog_window = tkinter.Tk()

        othello_welcome = tkinter.Label(master = self._dialog_window,
                                        text = 'Welcome to Othello!',
                                        font = DEFAULT_FONT,
                                        fg = 'green')

        othello_welcome.grid(row = 0, column = 0, padx = 5, pady = 5,
                            sticky = tkinter.S)
        

##        othello rows
        othello_rows = tkinter.Label(
            master = self._dialog_window,
            text = 'Rows: (4 to 16)',
            font = DEFAULT_FONT)
        othello_rows.grid(row = 1, column = 0, sticky = tkinter.S)

        self._othello_rows_entry = tkinter.Entry(
            master = self._dialog_window,
            width = 10, font = DEFAULT_FONT)
        self._othello_rows_entry.grid(row = 1, column = 1, sticky = tkinter.S)

##        othello columns
        othello_columns = tkinter.Label(
            master = self._dialog_window,
            text = 'Columns: (4 to 16)',
            font = DEFAULT_FONT)
        othello_columns.grid(row = 2, column = 0, sticky = tkinter.S)

        self._othello_columns_entry = tkinter.Entry(
            master = self._dialog_window,
            width = 10, font = DEFAULT_FONT)
        self._othello_columns_entry.grid(row = 2, column = 1, sticky = tkinter.S)
        
##        who goes first
        othello_player = tkinter.Label(
            master = self._dialog_window,
            text = 'Who goes first: (B or W)',
            font = DEFAULT_FONT)
        othello_player.grid(row = 3, column = 0, sticky = tkinter.S)

        self._othello_player_entry = tkinter.Entry(
            master = self._dialog_window,
            width = 10, font = DEFAULT_FONT)
        self._othello_player_entry.grid(row = 3, column = 1, sticky = tkinter.S)
        
##        upper-left
        othello_center = tkinter.Label(
            master = self._dialog_window,
            text = 'Upper Left: (B or W)',
            font = DEFAULT_FONT)
        othello_center.grid(row = 4, column = 0, sticky = tkinter.S)

        self._othello_center_entry = tkinter.Entry(
            master = self._dialog_window,
            width = 10, font = DEFAULT_FONT)
        self._othello_center_entry.grid(row = 4, column = 1, sticky = tkinter.S)

##        othello mode
        othello_mode = tkinter.Label(
            master = self._dialog_window,
            text = 'Mode: (most or fewest)',
            font = DEFAULT_FONT)
        othello_mode.grid(row = 5, column = 0, sticky = tkinter.S)

        self._othello_mode_entry = tkinter.Entry(
            master = self._dialog_window,
            width = 10, font = DEFAULT_FONT)
        self._othello_mode_entry.grid(row = 5, column = 1, sticky = tkinter.S)

##        buttons
        button_frame = tkinter.Frame(master = self._dialog_window)

        button_frame.grid(row = 6, column = 0, columnspan = 2,sticky = tkinter.E + tkinter.S)

        ok_button = tkinter.Button(
            master = button_frame,
            text = 'OK',
            font = DEFAULT_FONT,
            command = self._on_ok_button)
        ok_button.grid(row = 0, column = 0, padx = 5, pady = 5)


        cancel_button = tkinter.Button(
            master = button_frame,
            text = 'CANCEL',
            font = DEFAULT_FONT,
            command = self._on_cancel_button)
        cancel_button.grid(row = 0, column = 1, padx = 5, pady = 5)

       

        self._dialog_window.rowconfigure(0, weight = 1)
        self._dialog_window.rowconfigure(1, weight = 1)
        self._dialog_window.columnconfigure(0, weight = 1)

        
        self._rows = None
        self._columns = None
        self._player = None
        self._center = None
        self._mode = None
        self._ok_button = False

    
    def start(self):
        self._dialog_window.mainloop()

    def _on_ok_button(self):
        self._ok_button = True
        self._rows = self._othello_rows_entry.get()
        self._columns = self._othello_columns_entry.get()
        self._player = self._othello_player_entry.get()
        self._center = self._othello_center_entry.get()
        self._mode = self._othello_mode_entry.get()
        
        error = invalid_input(self._rows, self._columns, self._player, self._center, self._mode)
        if error == None:
            self._rows = int(self._rows)
            self._columns = int(self._columns)
            self._dialog_window.destroy()
        else:
            error_box = ErrorDialog(error)
            error_box.show()
            
    def _on_cancel_button(self):
        self._dialog_window.destroy()


    def rows(self):
        return self._rows
    def columns(self):
        return self._columns
    def player(self):
        if self._player.upper().strip() == 'B':
            return 'X'
        else:
            return 'O'
    def center(self):
        if self._center.upper().strip() == 'B':
            return 'X'
        else:
            return 'O'
    def mode(self):
        return self._mode.strip()
    def ok_clicked(self):
        return self._ok_button


class ErrorDialog:
    def __init__(self, text_error: str):
        self._error_window = tkinter.Toplevel()

        error_label = tkinter.Label(
            master = self._error_window,
            text = text_error,
            font = ERROR_FONT)
        error_label.grid(row = 0, column = 0, sticky = tkinter.S)

        error_button = tkinter.Button(
            master = self._error_window,
            text = 'OK',
            font = ERROR_FONT,
            command = self._ok_button)
        error_button.grid(row = 1, column = 0, sticky = tkinter.S + tkinter.E)
                
    def show(self) -> None:
        self._error_window.grab_set()
        self._error_window.wait_window()

        
    def _ok_button(self):
        self._error_window.destroy()


class WinnerDialog:
    def __init__(self, winner: str):
        self._winner_window = tkinter.Toplevel()
##        winner label
        winner_label = tkinter.Label(
            master = self._winner_window,
            text = winner,
            font = ERROR_FONT)
        winner_label.grid(row = 0, column = 0, sticky = tkinter.S)
        
##        ask again 
        ask_label = tkinter.Label(
            master = self._winner_window,
            text = 'Would you like to play again?',
            font = ERROR_FONT)
        ask_label.grid(row = 1, column = 0, sticky = tkinter.S)
        
##        button
        button_frame = tkinter.Frame(master = self._winner_window)
        button_frame.grid(row = 2, column = 0, columnspan = 2,sticky = tkinter.E + tkinter.S)

        yes_button = tkinter.Button(
            master = button_frame,
            text = 'YES',
            font = ERROR_FONT,
            command = self._on_yes_button)
        yes_button.grid(row = 0, column = 0, padx = 5, pady = 5)

        no_button = tkinter.Button(
            master = button_frame,
            text = 'NO',
            font = ERROR_FONT,
            command = self._on_no_button)
        no_button.grid(row = 0, column = 1, padx = 5, pady = 5)
        
        self._yes_button = False
        
    def show(self) -> None:
        self._winner_window.grab_set()
        self._winner_window.wait_window()


    def _on_yes_button(self):
        self._yes_button = True
        self._winner_window.destroy()

    def _on_no_button(self):
        self._winner_window.destroy()
  

    def _yes_clicked(self):
        return self._yes_button
    


def invalid_input(ROWS: int, COLS: int, player: str, center: str, mode: str) -> bool:
    if not othello.valid_board_size(ROWS, COLS):
        return ('Please enter the correct rows and columns.')
    if not(player.upper().strip() == 'B' or player.upper().strip() == 'W'):
        return('Please enter the correct player.')
    if not(center.upper().strip() == 'B' or center.upper().strip() == 'W'):
        return('Please enter the correct player for center.')
    if not(mode.upper().strip() == 'MOST' or mode.upper().strip() == 'FEWEST'):
        return('Please enter the correct mode.')
    else:
        return None
    


