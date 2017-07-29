#!/usr/bin/env python
import argparse, sys, random, time

def shuffle():
    # Returns a randomized board with the settings above
    grid = ['m']*mines
    grid.extend([' ']*(rows*columns -mines))
    random.shuffle(grid)
    
    return grid

def set_index(grid, x, y, value):
    grid[x+(y*columns)] = value

def get_index(grid, x, y):
    return grid[x+(y*rows)]

def display(grid):
    print ' ',
    for c in range(columns):
        print '  ' + str(c),
    print '\n  '+"----"*columns + '-'
    
    for r in range(rows):
        print r,
        for c in range(columns):
            print "| " + get_index(grid,r,c),
        print "|\n  " + "----"*columns + '-'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A terminal based minesweeper game",
                                    epilog="Author: Connor Christian")
    
    group1 = parser.add_argument_group("Gamemodes")
    gamemode = group1.add_mutually_exclusive_group() 
    gamemode.add_argument("-E", "--easy", 
                            help="easy difficulty: 10 mines on an 8x8 grid (Default)", 
                            action="store_true", default=True)
    gamemode.add_argument("-M", "--medium", 
                            help="medium difficulty: 40 mines on an 16x16 grid", 
                            action="store_true")
    gamemode.add_argument("-H", "--hard", 
                            help="hard difficulty: 99 mines on a 30x16 grid", 
                            action="store_true")
    
    group2 = parser.add_argument_group("Custom settings",
                                        description="Override how many rows, \
                                    columns, and mines your game will have.")
    group2.add_argument("-m", "--mines", type=int,
                                help="specify number of mines in range [5,rows*columns]",
                                metavar="{5,...,rows*columns}")
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
        mines = 99
        rows = 30
        columns = 16
    elif args.medium:
        mines = 40 
        rows = columns = 16
    elif args.easy:
        mines = 10 
        rows = columns = 8

    if args.mines is not None:
        mines = args.mines
    if args.rows is not None:
        rows = args.rows
    if args.columns is not None:
        columns = args.columns
    if args.dimensions is not None:
        rows = columns = args.dimensions

    # Print error in the same style as argparse
    if mines >= rows*columns:
        parser.print_usage()
        print sys.argv[0][2:] + ": error: argument -m/--mines: invalid choice:", 
        print "{} (choose from {})".format(args.mines, str(range(5,rows*columns))[1:-1])
        print "Cannot have mines greater than or equal to the grid area"
        sys.exit(2)
    elif mines < 5:
        parser.print_usage()
        print sys.argv[0][2:] + ": error: argument -m/--mines: invalid choice:",
        print "{} (choose from {})".format(args.mines, str(range(5,rows*columns))[1:-1])
        print "Cannot have less then 5 mines"
        sys.exit(2)

    board = shuffle()
    display(board)
