#!/usr/bin/env python
import sys, random

#default settings
mines = 10 
rows = columns = 8

def shuffle():
    # Returns a randomized board with the settings above
    grid = ['m']*mines
    grid.extend([' ']*(rows*columns -mines))
    random.shuffle(grid)
    
    return grid

def set_index(grid, x, y, value):
    grid[x+(y*columns)] = value

def get_index(grid, x, y):
    return grid[x+(y*columns)]

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
    board = shuffle()
    display(board)
