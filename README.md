## ABOUT:
This is my rendition of the classic minesweeper game written in python.
As of now it is only a terminal based game; however, I intend to have a GUI
component once the terminal based version is complete.

## NOTICE:
Currently the game is incomplete.

## USAGE:
usage: minesweeper.py [-h] [-E | -M | -H] [-m {5,...,rows*columns}] [-r
{4,...,30}] [-c {4,...,30}] [-d {4,...,30}]

* By default:
  * mines = 10
  * rows = columns =  8
* If rows or columns are overwritten with the r/c/d flags, the value for mines
    must still fit within the range
## RUN:
```
./minesweeper.py
```

## FORMAT:
* Unknown:      ' '
* Mines:        'M'
* Explosion:    'X'
* Flag:         'F'
* Mark:         '?'
* Warnings:     '1',...,'8'
* Empty         '0'
