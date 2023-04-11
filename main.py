import pygame
from game import Game

# Initialize PyGame
pygame.init()

# Creating a new instance of Game
game = Game()
# Calling the run_game_loop method
game.run_game_loop()

# Quit PyGame
pygame.quit()
quit()