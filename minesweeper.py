#!/usr/bin/env python3
"""
This is my rendition of the classic minesweeper game written in python.
As of now it is only a terminal based game; however, I intend to have a GUI
component once the terminal based version is complete.
"""

import argparse
import random
import time
import shlex
import subprocess

# default global variables
PERCENT = 15
ROWS = COLUMNS = 8
MINES = (PERCENT * ROWS * COLUMNS)//100
COUNT = ROWS*COLUMNS - MINES
FLAGS_PLACED = MINES

def shuffle():
    """Returns a randomized board with the settings above"""
    grid = ['M']*MINES
    grid.extend(['0']*(ROWS*COLUMNS-MINES))
    random.shuffle(grid)

    for loc in list(map(lambda z: str(z%ROWS)+','+str(z//ROWS),
        [i for i, v in enumerate(grid) if v == 'M'])):
        init_cells(grid, loc)

    return grid

def init_cells(grid, loc):
    a,b = loc.split(',')
    a = int(a)
    b = int(b)

    # TOP LEFT CORNER
    if a-1 >= 0 and b-1 >=0 and get_index(grid,a-1,b-1) != 'M':
        set_index(grid,a-1,b-1,str(int(get_index(grid,a-1,b-1))+1))

    # TOP MIDDLE
    if a-1 >= 0 and get_index(grid,a-1,b) != 'M':
        set_index(grid,a-1,b,str(int(get_index(grid,a-1,b))+1))

    # TOP RIGHT CORNER
    if a-1 >= 0 and b+1 <= COLUMNS-1 and get_index(grid,a-1,b+1) != 'M':
        set_index(grid,a-1,b+1,str(int(get_index(grid,a-1,b+1))+1))

    # LEFT MIDDLE
    if b-1 >= 0 and get_index(grid,a,b-1) != 'M':
        set_index(grid,a,b-1,str(int(get_index(grid,a,b-1))+1))

    # RIGHT MIDDLE
    if b+1 <= COLUMNS-1 and get_index(grid,a,b+1) != 'M':
        set_index(grid,a,b+1,str(int(get_index(grid,a,b+1))+1))

    # BOTTOM LEFT CORNER
    if a+1 <= ROWS-1 and b-1 >= 0 and get_index(grid,a+1,b-1) != 'M':
        set_index(grid,a+1,b-1,str(int(get_index(grid,a+1,b-1))+1))

    # BOTTOM MIDDLE
    if a+1 <= ROWS-1 and get_index(grid,a+1,b) != 'M':
        set_index(grid,a+1,b,str(int(get_index(grid,a+1,b))+1))

    # BOTTOM RIGHT
    if a+1 <= ROWS-1 and b+1 <= COLUMNS-1 and get_index(grid,a+1,b+1) != 'M':
        set_index(grid,a+1,b+1,str(int(get_index(grid,a+1,b+1))+1))

def set_index(grid, x, y, value):
    grid[x+(y*ROWS)] = value

def get_index(grid, x, y):
    value = grid[x+(y*ROWS)]
    if value is None:
        return ' '
    return value

def display(grid):
    print(' '*5,end='')
    for c in range(COLUMNS):
        if c >= 10:
            print(str(c) + ' '*2,end='')
        else:
            print(str(c) + ' '*3,end='')
    print('\n   '+"+---"*COLUMNS + '+')

    for r in range(ROWS):
        if r < 10:
            print(' '+str(r) + ' ',end='')
        else:
            print(str(r) + ' ',end='')
        for c in range(COLUMNS):
            print("| " + add_color(get_index(grid,c,r))+' ',end='')
        print("|\n   " + "+---"*COLUMNS + '+')
    print("Mines left:", FLAGS_PLACED)

def add_color(value):
    color = ''
    if value == 'M':
        color = '\033[0;31mM\033[0m'
    elif value in ('F','?'):
        color = '\033[1;33m'+value+'\033[0m'
    elif value == '1':
        color = '\033[0;34m'+value+'\033[0m'
    elif value == '2':
        color = '\033[0;32m'+value+'\033[0m'
    elif value == '3':
        color = '\033[1;31m'+value+'\033[0m'
    elif value == '4':
        color = '\033[0;35m'+value+'\033[0m'
    elif value == '5':
        color = '\033[0;33m'+value+'\033[0m'
    elif value == '6':
        color = '\033[0;36m'+value+'\033[0m'
    elif value == '7':
        color = '\033[1;30m'+value+'\033[0m'
    elif value == '8':
        color = '\033[0;37m'+value+'\033[0m'
    else: #0
        return value
    return color

def input_board(layer, grid, x, y, flag=None):
    global COUNT
    global FLAGS_PLACED
    value = get_index(layer, x, y)
    if value in (' ','?') and flag is None: # found unchosen
        reveal = get_index(grid, x, y)
        set_index(layer, x, y, reveal)
        if reveal == 'M':
            return True
        if reveal == '0':
            auto_reveal(layer, grid, (x, y))
        COUNT -= 1
    elif value in ('F','?') and flag == 'U':
        if value == 'F':
            FLAGS_PLACED += 1
        set_index(layer, x, y, None)
    elif value in (' ','F','?') and flag is not None:
        if flag == 'F':
            FLAGS_PLACED -= 1
        if flag != 'U':
            set_index(layer, x, y, flag)
    return False

def auto_reveal(layer, grid, current, positions=[]):
    #Check 8 positions surrounding
    a,b = current

    # TOP LEFT CORNER
    if a-1 >= 0 and b-1 >=0 and get_index(grid,a-1,b-1) != 'M':
        positions.append((a-1,b-1))

    # TOP MIDDLE
    if a-1 >= 0 and  get_index(grid,a-1,b) != 'M':
        positions.append((a-1,b))

    # TOP RIGHT CORNER
    if a-1 >= 0 and b+1 <= COLUMNS-1 and get_index(grid,a-1,b+1) != 'M':
        positions.append((a-1,b+1))

    # LEFT MIDDLE
    if b-1 >= 0 and get_index(grid,a,b-1) != 'M':
        positions.append((a,b-1))

    # RIGHT MIDDLE
    if b+1 <= COLUMNS-1 and get_index(grid,a,b+1) != 'M':
        positions.append((a,b+1))

    # BOTTOM LEFT CORNER
    if a+1 <= ROWS-1 and b-1 >= 0 and get_index(grid,a+1,b-1) != 'M':
        positions.append((a+1,b-1))

    # BOTTOM MIDDLE
    if a+1 <= ROWS-1 and get_index(grid,a+1,b) != 'M':
        positions.append((a+1,b))

    # BOTTOM RIGHT
    if a+1 <= ROWS-1 and b+1 <= COLUMNS-1 and get_index(grid,a+1,b+1) != 'M':
        positions.append((a+1,b+1))

    while positions != []: #Base Case
        x,y = positions.pop()
        input_board(layer, grid, x, y)

def print_message(start, win):
    end = time.time() - start
    minutes = int(end // 60)
    seconds = int(end % 60)
    if win:
        print("\033[0;32mYou Win!\033[0m")
    else:
        print("\033[0;31mGameover!\033[0m")
    print("Elapsed time: ", end='')
    if minutes > 0 and seconds > 0:
        print(minutes, "minutes", seconds, "seconds")
    elif minutes == 0:
        print(seconds, "seconds")
    elif seconds == 0:
        print(minutes, "minutes")
    else:
        print("0 seconds")

def main():
    win = gameover = False
    start = time.time()
    display(layer)
    while not gameover:
        try:
            string = input("Select a position: ex. 'f x y', 'x y'\n> ")
            if string not in ("quit","exit","abort"):
                if string[0].lower() == 'f' or string[0] == '?' or \
                    string[0].lower() == 'u':
                    char, coord_x, coord_y = string.split()
                    char = char.upper()
                else:
                    coord_x, coord_y = string.split()
                    char = None
                gameover = input_board(layer, board, int(coord_x), int(coord_y),
                     char)
                win = COUNT == 0
            else:
                gameover = True
        except IndexError:
            print("ERROR: Index out of bounds.\nRows must be between [0, " + \
                str(ROWS-1) + "]\nColumns must be between [0,"+\
                str(COLUMNS-1)+"]\n")
        except ValueError:
            print("ERROR: Bad imput, try again.")
        if win:
            gameover = True
        display(layer)
    print_message(start, win)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A terminal based minesweeper\
        game. To end the game, type either: \"quit\", \"exit\", or \"abort\"",
        epilog="Author: Connor Christian")

    group1 = parser.add_argument_group("Gamemodes",
        description="Default mode is set to 'Easy'")
    gamemode = group1.add_mutually_exclusive_group()
    gamemode.add_argument("-E", "--easy",
        help="easy difficulty: 15 percent mines on an 8x8 grid",
        action="store_true", default=True)
    gamemode.add_argument("-M", "--medium",
        help="medium difficulty: 20 percent mines on an 16x16 grid",
        action="store_true")
    gamemode.add_argument("-H", "--hard",
        help="hard difficulty: 30 percent mines on a 30x16 grid",
        action="store_true")

    group2 = parser.add_argument_group("Custom settings",
        description="Override how many rows, \
        columns, and mines your game will have.")
    group2.add_argument("-m", "--mines", type=int,
        help="specify percentage of mines in range [15,99]",
        choices=range(15,100),
        metavar="{15,...,99}")
    group2.add_argument("-r", "--rows", type=int,
        help="specify number of rows in range [4,100]",
        choices=range(4,101),
        metavar="{4,...,100}")
    group2.add_argument("-c", "--columns", type=int,
        help="specify number of columns in range [4,100]",
        choices=range(4,101),
        metavar="{4,...,100}")
    group2.add_argument("-d", "--dimensions", type=int,
        help="specify number for rows and columns in range [4,100]",
        choices=range(4,101),
        metavar="{4,...,100}")
    group2.add_argument("-f", "--fullscreen",
        help="maximize gameboard to encompass the terminal window",
        action="store_true")

    args = parser.parse_args()

    if args.hard:
        PERCENT = 30
        ROWS = 30
        COLUMNS = 16
    elif args.medium:
        PERCENT = 20
        ROWS = COLUMNS = 16
    elif args.easy:
        PERCENT = 15
        ROWS = COLUMNS = 8

    if args.rows is not None:
        ROWS = args.rows
    if args.columns is not None:
        COLUMNS = args.columns
    if args.dimensions is not None:
        ROWS = COLUMNS = args.dimensions
    if args.fullscreen:
        cmd = shlex.split("tput lines")
        ROWS = int(subprocess.check_output(cmd))
        # rows-2 accounts for indexing; -2 at end accounts for error message
        ROWS = (ROWS-2)//2 -2
        cmd = shlex.split("tput cols")
        COLUMNS = int(subprocess.check_output(cmd))
        # columns-3 accounts for indexing
        COLUMNS = (COLUMNS-3)//4
        # The max values for rows & columns is 100, if exceeds set to 100
        if ROWS > 100:
            ROWS = 100
        if COLUMNS > 100:
            COLUMNS = 100

    if args.mines is not None:
        PERCENT = args.mines
    MINES = (PERCENT * ROWS * COLUMNS)//100

    COUNT = ROWS*COLUMNS - MINES
    FLAGS_PLACED = MINES

    layer = [None]*(ROWS*COLUMNS)
    board = shuffle()

    main()
