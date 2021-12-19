# dots_and_boxs
Dots and Boxes.

Popular game.  The goal is to have more than a half of the squares colored with your color.
Game includes walls and square. Each square have 4 walls. Closed squares are sharing the same wall. 
In your turn you chose a wall. If you chose the last empty walls, the square will be colored with your color. If the computer chose the last wall in a square, it will be colored with the computer color. After coloring a square, the player will get another turn to play.
 Game implemented to be user vs computer.
Files:
Game.py – main file that is importing and invoke the game.
GameModule.py – This file implements all the Algorithmic and the calculation behind the game. It has a classes like square & wall that represent the graphic parts, but it only data.\
GameGraphic.py – file implements the graphic parts. It just take care on the visuals elements. When need to check things, it send requests to the Game that move it forward to the Module.
Tools.py - a sort file that includes enum 

How to run it:
$python3 Game.py 
Python version 3.8

Implementation use A star function to the computer side.
