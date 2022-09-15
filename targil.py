
# imports
import subprocess
import sys

try:
    from numpy import zeros
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    from numpy import zeros

try:
    from pandas import read_csv
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    from pandas import read_csv

try:
    from os import getcwd,path
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "os"])
    from os import getcwd,path

try:
    import argparse
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "argparse"])
    import argparse

try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import argparse

#params
N=8
TURN=1
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE=WIDTH//N
WHITE=(255,255,255)
BLACK=(0,0,0)

def is_legal(board, turn, move):
    """
    check if a move is legal
    INPUT
    ------
    board : numpy array, shape = [8,8]
        8*8 board with current state of the game
    turn : int
        white(1) or black (-1)
    move : numpy array, shape = [1,4]
        a move (x0, y0, x1, y1). x0 is the source column, y0 is the source row, x1 and y1 are the target.

    OUTPUT
    ______
    ans : int
        0 for illegal move
        1 for legal
        2 for legal capture, when the next move should be capture
    """
    for c in move:
        if c < 0 or c > (len(board) - 1):  # does the move is outside the board?
            return 0
    if (board[move[1], move[0]] * turn != 1 or not(board[move[3],move[2]]==0)):  #check if the currect user was playing(+the cell is not empty),and check if the destenation was empty
        return 0
    board_update = board.copy()  # create new board to check if there is option to capture
    board_update[move[3], move[2]] = turn # create new board to check if there is option to capture
    if (caputre_move_check(move,turn)):  # check if it was a capture move
        x_3 = int((move[0] + move[2]) / 2)  # y location of the piece we capture
        y_3 = int((move[1] + move[3]) / 2)# x location of the piece we capture
        if(board[y_3, x_3]!=(turn*-1)): # check if we capture the rigth piece
            return 0
        if(capture_move_available(board_update, turn, move[2], move[3])):  # check if there is option to capture
            return 2 #2 for legal capture available
    elif(abs(move[0] - move[2]) == 1 and turn*(move[3] - move[1]) == 1):  # check if it was a regular move
        capture_move=check_option(board, turn, 0)# check if capture move was available
        if(capture_move):
            return 0 # in case there is a possible capture move, and a capture was not happen.
    else:
        return 0 #in case it was not a capture or regular move
    return 1
def make_move(board, turn, move):
    """
    update the board with the move
    INPUT
    ------
    board : numpy array, shape = [8,8]
        8*8 board with current state of the game
    turn : int
        white(1) or black (-1)
    move : numpy array, shape = [1,4]
        a move (x0, y0, x1, y1). x0 is the source column, y0 is the source row, x1 and y1 are the target.

    OUTPUT
    ______
    board : int
        update the board
    """
    board[move[1], move[0]] = 0  # delete the current loaction
    board[move[3], move[2]] = turn  # put the piece in the new location
    if (abs(move[0] - move[2]) == 2):  # check if it was a capture move
        x = int((move[1] + move[3]) / 2)
        y = int((move[0] + move[2]) / 2)
        board[x, y] = 0  # delete the piece
    return board

def winer_check(board, turn):
    """
    find the winer.
    "first", "second", "tie", or "incomplete game"
    INPUT
    ------
    board : numpy array, shape = [8,8]
        8*8 board with current state of the game
    turn : int
        white(1) or black (-1)

    OUTPUT
    ______
    printing the winner: "first", "second" , "tie"
    or "incomplete game"
    """
    # first we need to check if there are no possible moves for the player that should play now.
    more_moves=check_option(board, turn,1)
    if(more_moves):
        print('incomplete game')
        return
    white = 0
    black = 0
    for i in range(len(board)):
        for j in range((i + 1) % 2, len(board), 2):
            if (board[i, j] == 1):  # counting white
                white = white + 1
            elif (board[i, j] == -1):  # counting black
                black = black + 1
    if (black > white):  # check if black is the winner
        print("second")
    elif (black < white):  # check if white is the winner
        print("first")
    else:
        print("tie")

def check_option(board,turn,all_or_capture):
    """
    check if there is a possible move
    INPUT
    ------
    board : numpy array, shape = [8,8]
        8*8 board with current state of the game
    turn : int
        white(1) or black (-1)
    all_or_capture : int
        this value indicate if we check for capture and regular move or capture move
        1 check capture move and regular move
        0 check capture move
    OUTPUT
    ______
    ans: int
        0 there isn't a possible move
        1 there is a possible move
    """
    ans_regular=0# initializing

    for i in range(len(board)):
       for j in range((i + 1) % 2, len(board), 2):
           if(board[i,j]*turn==1): # if we are at location of the current player
                ans_capture=capture_move_available(board,turn,j,i)# does capture move is available
                if(all_or_capture):
                    ans_regular = regular_move_available(board, turn, j, i)  # does regular move is available
                if(ans_capture or ans_regular):
                    return 1
    return 0

def capture_move_available(board, turn,x_0,y_0):
    """
    check if there is a possible capture move
    INPUT
    ------
    board : numpy array, shape = [8,8]
       8*8 board with current state of the game
    turn : int
       white(1) or black (-1)
    move : numpy array, shape = [1,4]
       a move (x0, y0, x1, y1). x0 is the source column, y0 is the source row, x1 and y1 are the target.

    OUTPUT
    ______
     ans : int
       1 capture move is available
       0 capture move is not available
    """
    x_1=x_0+2
    x_2=x_0-2
    y_1=y_0+2*turn
    if(is_legal(board,turn,[x_0,y_0,x_1,y_1]) or is_legal(board, turn, [x_0,y_0,x_2,y_1])):
        return 1
    return 0

def regular_move_available(board, turn,x_0,y_0):
    """
    check if there is a possible regular move
    INPUT
    ------
    board : numpy array, shape = [8,8]
       8*8 board with current state of the game
    turn : int
       white(1) or black (-1)
    move : numpy array, shape = [1,4]
       a move (x0, y0, x1, y1). x0 is the source column, y0 is the source row, x1 and y1 are the target.

    OUTPUT
    ______
     ans : int
       1 regular move is available
       0 regular move is not available
    """
    x_1=x_0+1
    x_2=x_0-1
    y_1=y_0+1*turn
    if(is_legal(board, turn, [x_0,y_0,x_1,y_1]) or is_legal(board, turn, [x_0,y_0,x_2,y_1])):
        return 1
    return 0

def caputre_move_check(move,turn):
    """
    check if the move was capture move
    INPUT
    ------
    turn : int
       white(1) or black (-1)
    move : numpy array, shape = [1,4]
       a move (x0, y0, x1, y1). x0 is the source column, y0 is the source row, x1 and y1 are the target.

    OUTPUT
    ______
    ans : Boolean
       1 the move is a capture move
       0 the move is not a capture move
    """
    return abs(move[0] - move[2]) == 2 and turn*(move[3] - move[1]) == 2

def print_illegal_move(counter,move):
    """
    printing illegal move
    INPUT
    ------
    counter : int
       the line from the txt file
    move : numpy array, shape = [1,4]
       a move (x0, y0, x1, y1). x0 is the source column, y0 is the source row, x1 and y1 are the target.
    """
    counter=counter+1
    print("line", counter, "illegal move: ",end="")
    print(move[0],",",move[1],",",move[2],",",move[3],sep="")

def initialization(file_name):
    """
    initialization: reading file from the user in the current directory and initialising the board
    INPUT
    -----
    file_name : string
        the file name
    OUTPUT
    ------
    board : numpy array, shape = [8,8]
       8*8 board with current state of the game
    data : numpy array
       input from the file name the user define
    turn : int
       white(1) or black (-1)
       the white(1) user starts the game, therefore 'turn' initialized  to 1
    """
    cwd = getcwd()
    file_name= file_name.file_name#input('Please enter the file name: ' ) # TODO - check input
    path_file = path.join(cwd, file_name)
    data = read_csv(path_file, header=None)
    data = data.to_numpy()
    # initializing the board
    # 0 is nun -1 is black and 1 is white,
    turn = TURN  # the white user starts the game
    brd_size= N  # the board size

    WIN = pygane.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_captions('Checkers')

    board = zeros((brd_size, brd_size))
    for i in range(3):
        for j in range((i + 1) % 2, brd_size, 2):
            board[i, j] = 1  # initializng white
    for i in range(brd_size - 3, brd_size):
        for j in range((i + 1) % 2, brd_size, 2):
            board[i, j] = -1  # initializng black
    return [board,data,turn]

def main(file_name):
    """
    the main function
    input
    ------
    file_name : string
        the file name
    """
    [board,data,turn]=initialization(file_name)
    for counter, move in enumerate(data): #go over the moves
        legal=is_legal(board,turn,move) #check if the move was legal
        if(legal==0): #for illegal move
            print_illegal_move(counter,move) #stop the game
            break
        board=make_move(board,turn,move) # make move
        if(legal == 2): # in case of multiple-capture sequences.
            next_move = data[counter + 1]  # does the next step is eating the next piece?
            # check if the next step is capture move and if the next step starts in the current location:
            if (not (caputre_move_check(next_move, turn)) and next_move[0] != move[2] and next_move[1] != move[3]):
                print_illegal_move(counter,move)
                break
            turn = turn * -1  #next turn for the same player
        turn = turn * -1
    if(legal==1):
        winer_check(board, turn)

if __name__ == '__main__':
    # parser
    parser = argparse.ArgumentParser(description='Checkers Programming Exercise')
    parser.add_argument('file_name',type=str)
    args = parser.parse_args()
    main(args)