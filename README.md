## ABOUT:
This is my rendition of the classic minesweeper game written in python.
As of now it is only a terminal based game; however, I intend to have a GUI
component once the terminal based version is complete.

## NOTICE:
Currently the game is incomplete.

## USAGE:
usage: minesweeper.py [-h] [-E | -M | -H] [-m {15,...,99}] [-r
{4,...,30}] [-c {4,...,30}] [-d {4,...,30}]
* Default setting is "Easy mode":
  * mines = 15%
  * rows = columns = 8
* minimum mine percentage is 15%
* mazimum mine percentage is 99%

## RUN:
```
./minesweeper.py
```

## FORMAT:
* Unknown:      ' '
* Flag:         'F'
* Mark:         '?'
* Explosion:    'X'
* Mines:        'M'
* Warnings:     '1',...,'8'
* Empty         '0'
