To run the genetic algorithm, set PLAYER_CONTROL=False; to play the game set PLAYER_CONTROL=True

Unless IGNORE_SAVE is set Program will attempt to load from the /last_save folder (or /generationX if the GENERATION_TO_LOAD variable is set)


plotting.py adds a visualization of the genetic algorithms progress.
The data.txt file needs to be manually cleaned up, else multiple runs will overlap.





python packages: numpy, pygame
matplotlib (if plotting.py is wanted)
Cython (if you want to change the .pyx source files)