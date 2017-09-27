#!/usr/bin/env python
import argparse, sys, random, time

def shuffle():
    # Returns a randomized board with the settings above
    grid = ['M']*mines
    grid.extend(['0']*(rows*columns -mines))
    random.shuffle(grid)

    for loc in list(map(lambda z: str(z%rows)+','+str(z/rows), [i for i, x in \
        enumerate(grid) if x == 'M'])):
        init_cells(grid, loc)

    return grid

def init_cells(grid, loc):
    a,b = loc.split(',')
    a = int(a)
    b = int(b)
    if a-1 >= 0 and b-1 >=0: # TOP LEFT CORNER
        if get_index(grid,a-1,b-1) != 'M':
            set_index(grid,a-1,b-1,\
                str(int(get_index(grid,a-1,b-1))+1))

    if a-1 >= 0: # TOP MIDDLE
        if get_index(grid,a-1,b) != 'M':
            set_index(grid,a-1,b,\
                str(int(get_index(grid,a-1,b))+1))

    if a-1 >= 0 and b+1 <= columns-1: # TOP RIGHT CORNER
        if get_index(grid,a-1,b+1) != 'M':
            set_index(grid,a-1,b+1,\
                str(int(get_index(grid,a-1,b+1))+1))

    if b-1 >= 0: # LEFT MIDDLE
        if get_index(grid,a,b-1) != 'M':
            set_index(grid,a,b-1,\
                str(int(get_index(grid,a,b-1))+1))

    if b+1 <= columns-1: # RIGHT MIDDLE
        if get_index(grid,a,b+1) != 'M':
            set_index(grid,a,b+1,\
                str(int(get_index(grid,a,b+1))+1))

    if a+1 <= rows-1 and b-1 >= 0: # BOTTOM LEFT CORNER
        if get_index(grid,a+1,b-1) != 'M':
            set_index(grid,a+1,b-1,\
                str(int(get_index(grid,a+1,b-1))+1))

    if a+1 <= rows-1: # BOTTOM MIDDLE
        if get_index(grid,a+1,b) != 'M':
            set_index(grid,a+1,b,\
                str(int(get_index(grid,a+1,b))+1))

    if a+1 <= rows-1 and b+1 <= columns-1: # BOTTOM RIGHT
        if get_index(grid,a+1,b+1) != 'M':
            set_index(grid,a+1,b+1,\
                str(int(get_index(grid,a+1,b+1))+1))

def set_index(grid, x, y, value):
    grid[x+(y*rows)] = value

def get_index(grid, x, y):
    value = grid[x+(y*rows)]
    if value == None:
        return ' '
    return value

def display(grid):
    print '    ',
    for c in range(columns):
        if c >= 10:
            print str(c) + ' ',
        else:
            print str(c) + "  ",
    print '\n   '+"+---"*columns + '+'
    
    for r in range(rows):
        if r < 10:
            print str(r) + ' ',
        else:
            print r,
        for c in range(columns):
            print "| " + add_color(get_index(grid,r,c)),
        print "|\n   " + "+---"*columns + '+'
    print "Mines left:", flagsPlaced

def add_color(value):
    if value == 'M':
        return '\033[0;31mM\033[0m'
    elif value == 'F' or value == '?':
        return '\033[1;33m'+value+'\033[0m'
    elif value == '1':
        return '\033[0;34m'+value+'\033[0m'
    elif value == '2':
        return '\033[0;32m'+value+'\033[0m'
    elif value == '3':
        return '\033[1;31m'+value+'\033[0m'
    elif value == '4':
        return '\033[0;35m'+value+'\033[0m'
    elif value == '5':
        return '\033[0;33m'+value+'\033[0m'
    elif value == '6':
        return '\033[0;36m'+value+'\033[0m'
    elif value == '7':
        return '\033[1;30m'+value+'\033[0m'
    elif value == '8':
        return '\033[0;37m'+value+'\033[0m'
    else: #0
        return value

def input_board(layer, grid, x, y, flag=None):
    global flagsPlaced
    global minesFound
    value = get_index(layer, x, y)
    if (value == ' ' or value == '?') and flag is None: # found unchosen
        reveal = get_index(grid, x, y)
        set_index(layer, x, y, reveal)
        if reveal == 'M':
            return True
        else:
            if reveal == '0':
                auto_reveal(layer, grid, (x, y))
            global count
            count -= 1
    elif (value == 'F' or value == '?') and flag == 'U':
        if value == 'F':
            flagsPlaced += 1
            if get_index(grid, x, y) == 'M': #mine flagged
                minesFound -= 1
        set_index(layer, x, y, None)
    elif (value == ' ' or value == 'F' or value == '?') and flag is not None:
        if flag == 'F':
            flagsPlaced -= 1
            if get_index(grid, x, y) == 'M': #mine flagged
                minesFound += 1
        if flag != 'U':
            set_index(layer, x, y, flag)
    return False

def auto_reveal(layer, grid, current, positions=[]):
    '''
    Called when user uncovers a 0. This function will recursively call
    input_board() until every neighboring 0 is uncovered.
,
    Parameters: 'current' is a tuple with the position of a 0
    'positions' is a default parameter that stores all the surrounding cells
    that need to be checked for 0's

    Base Case: at the end of the function, if the positions list is empty, 
    don't recursively call
    '''
    #Check 8 positions surrounding
    a,b = current
    if a-1 >= 0 and b-1 >=0: # TOP LEFT CORNER
        if get_index(grid,a-1,b-1) != 'M':
            positions.append((a-1,b-1))

    if a-1 >= 0: # TOP MIDDLE
        if get_index(grid,a-1,b) != 'M':
            positions.append((a-1,b))

    if a-1 >= 0 and b+1 <= columns-1: # TOP RIGHT CORNER
        if get_index(grid,a-1,b+1) != 'M':
            positions.append((a-1,b+1))

    if b-1 >= 0: # LEFT MIDDLE
        if get_index(grid,a,b-1) != 'M':
            positions.append((a,b-1))

    if b+1 <= columns-1: # RIGHT MIDDLE
        if get_index(grid,a,b+1) != 'M':
            positions.append((a,b+1))

    if a+1 <= rows-1 and b-1 >= 0: # BOTTOM LEFT CORNER
        if get_index(grid,a+1,b-1) != 'M':
            positions.append((a+1,b-1))

    if a+1 <= rows-1: # BOTTOM MIDDLE
        if get_index(grid,a+1,b) != 'M':
            positions.append((a+1,b))

    if a+1 <= rows-1 and b+1 <= columns-1: # BOTTOM RIGHT
        if get_index(grid,a+1,b+1) != 'M':
            positions.append((a+1,b+1))

    while positions != []: #Base Case
        x,y = positions.pop()
        input_board(layer, grid, x, y)

def check_win(count, flagsPlaced, minesFound):
    if count == 0:
        return True
    if flagsPlaced == 0 and minesFound == 0:
        return True
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A terminal based minesweeper\
        game\nTo end the game, type either: \"quit\", \"exit\", or \"abort\"",
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
        choices=xrange(15,100),
        metavar="{15,...,99}")
    group2.add_argument("-r", "--rows", type=int,
        help="specify number of rows in range [4,30]",
        choices=xrange(4,100),
        metavar="{4,...,99}")
    group2.add_argument("-c", "--columns", type=int,
        help="specify number of columns in range [4,30]",
        choices=xrange(4,100),
        metavar="{4,...,99}")
    group2.add_argument("-d", "--dimensions", type=int,
        help="specify number for rows and columns in range [4,30]",
        choices=xrange(4,100),
        metavar="{4,...,99}")

    args = parser.parse_args()

    if args.hard:
        percent = 30
        rows = 30
        columns = 16
    elif args.medium:
        percent = 20 
        rows = columns = 16
    elif args.easy:
        percent = 15
        rows = columns = 8

    if args.rows is not None:
        rows = args.rows
    if args.columns is not None:
        columns = args.columns
    if args.dimensions is not None:
        rows = columns = args.dimensions

    if args.mines is not None:
        percent = args.mines
    mines = (percent * rows * columns)/100
    
    win = gameover = False
    count = rows*columns - mines
    flagsPlaced = mines
    minesFound = 0

    layer = [None]*(rows*columns)
    board = shuffle()
   
    start = time.time() 
    display(layer)
    while gameover == False:
        try:
            string = raw_input("Select a position: ex. 'f x y', 'x y'\n> ")
            if string != "quit" and string != "exit" and string != "abort":
                if string[0].lower() == 'f' or string[0] == '?' or \
                    string[0].lower() == 'u':
                    char, coord_x, coord_y = string.split()
                    char = char.upper()
                else:
                    coord_x, coord_y = string.split()
                    char = None
                gameover = input_board(layer, board, int(coord_x), int(coord_y),
                     char)
                win = check_win(count, flagsPlaced, mines - minesFound)
            else:
                gameover = True
        except IndexError:
            print "ERROR: Index out of bounds.\nRows must be between [0, " + \
                str(rows-1) + "]\nColumns must be between [0,"+\
                str(columns-1)+"]\n"
        except ValueError:
            print "ERROR: Bad imput, try again."
        if gameover:
            end = time.time() - start
            minutes = int(end / 60)
            seconds = int(end % 60)
            print '\033[0;31mGameover!\033[0m'
            print "Elapsed time:", 
            if minutes > 0:
                print minutes, "minutes",
            if seconds > 0:
                print seconds, "seconds"
        if win:
            end = time.time() - start
            minutes = int(end / 60)
            seconds = int(end % 60)
            print '\033[0;32mYou Win!\033[0m'
            print "Elapsed time:", 
            if minutes > 0:
                print minutes, "minutes",
            if seconds > 0:
                print seconds, "seconds"
            gameover = True
        display(layer)
