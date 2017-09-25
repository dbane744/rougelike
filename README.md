# rougelike
My first attempt at building a rougelike using Python and the libtcodpy library.
It follows the tutorial by /u/AetherGrey available at http://rogueliketutorials.com/libtcod/1.

The game follows the tradtional rougelike principles of representing all entities through ASCII characters - however, tilesets/graphics will be added eventually.

The game is currently in development; many more features are to be added!

Run engine.py to run the game.

CONTROLS
----------------------------------------
Arrow keys or numpad keys to move (UP=8,LEFT=4,RIGHT=6,DOWN=2,DIAGONAL MOVEMENT=7,9,1,3.)

Attack enemies by 'moving' onto their tile.

I : Inventory

G : Pickup item on the same tile as player.

ESC : Exit the game

Alt + Enter : Fullscreen

KNOWN BUGS
----------------------------------------
The game loop does not end when the player dies - an infinite loop is reached (so try not to die).



