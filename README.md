# simplified checkers game

Input: Text file with the players moves. Each row includes source (x and y axis location) and destination (x and y axis location). multiple
capture appears as multiple lines.

Output: print the winner- "first","second","tie". In case of illegal move- print the illegal move, or if the game was not completed- print "incomplete". 

Rules that are different from the original game or varies between of his versions:
* White opens the game, then players alternate their turns. 
* If there is a possible capture move, capture must be made.
* There is no option to upgrade a piece to a queen.
* The play ends when there is no possible move for the last player.
* The winner is the player with the higher number of pieces left on the board at the end of the game.
* The location of the pieces are such that: 

<img src="https://user-images.githubusercontent.com/71435004/190424948-09c690e7-fb9b-4e19-88ab-0aff56190ab1.jpg" width="300" height="300">
  
The upper left is (0,0) and the lower right is (7,7)

# How to run the code:
1. Add the file targil.py to the input files folder.
2. Add an input file, containing all the moves, to the input files folder.
3. Write in the terminal targil and the input file name. For example - targil input.txt
