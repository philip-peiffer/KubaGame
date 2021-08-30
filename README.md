This is an implementation of the Kuba board game, using Python for the backend and the Pygame package for the UI. To play - open the KubaGUI.py file and run.

This program contains a class named KubaGame for playing a board game called Kuba. You can see the rules [here](https://sites.google.com/site/boardandpieces/list-of-games/kuba).
A good video resource to watch this game rules is [here](https://www.youtube.com/watch?v=XglqkfzsXYc).

Game ends when a player wins. A players wins by pushing off and capturing seven neutral stones or by pushing off all of the opposing stones. A player who has no legal moves available has lost the game.

Any player can start the game, but players must take turns on the remaining moves (no repeating moves as is the case with other kuba implementations).

Rules to move a marble:
- You need an empty space(or the edge of the board) on the side you are pushing away from. This is as shown in the video.
- A player cannot undo a move the opponent just made (if it leads to the exact same board position)

To move a marble:
- Click on the marble that you would like to push.
- Use the keyboard arrows to indicate which direction you would like to push (up arrow pushes the marbles upwards, right pushes the marbles to the right, etc.).
- If the move is invalid, the program will not perform the operation and the current player must go again until a valid move is entered.
