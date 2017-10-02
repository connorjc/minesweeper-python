## ABOUT:
This is my rendition of the classic minesweeper game written in python.
As of now it is only a terminal based game; however, I intend to have a GUI
component once the terminal based version is complete.

## NOTICE:
The GUI is not yet implemented.

## USAGE:
usage: minesweeper.py [-h] [-E | -M | -H] [-m {15,...,99}] [-r
{4,...,100}] [-c {4,...,100}] [-d {4,...,100}]
* Default setting is "Easy mode":
  * mines = 15%
  * grid size = 8x8
* minimum mine percentage is 15%
* maximum mine percentage is 99%
* minimum grid size is 4x4
* maximum grid size is 100x100

## RUN:
```
./minesweeper.py
```

## FORMAT:
* Unknown:      ' '
* Flag:         'F'
* Remove Flag:  'U'
* Mark:         '?'
* Mines:        'M'
* Warnings:     '1',...,'8'
* Empty         '0'
