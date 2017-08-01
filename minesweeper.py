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
    return grid[x+(y*rows)]

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
            print "| " + get_index(grid,r,c),
        print "|\n   " + "+---"*columns + '+'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A terminal based minesweeper game",
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
        choices=xrange(4,31),
        metavar="{4,...,30}")
    group2.add_argument("-c", "--columns", type=int,
        help="specify number of columns in range [4,30]",
        choices=xrange(4,31),
        metavar="{4,...,30}")
    group2.add_argument("-d", "--dimensions", type=int,
        help="specify number for rows and columns in range [4,30]",
        choices=xrange(4,31),
        metavar="{4,...,30}")

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

    board = shuffle()
    display(board)
