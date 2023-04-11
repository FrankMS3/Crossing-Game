import pygame
from gameObject import GameObject
from player import Player
from enemy import Enemy

class Game:

    def __init__(self):
        self.width = 600
        self.height = 600
        self.white_colour = (255, 255, 255)

        # Creating the game window
        self.game_window = pygame.display.set_mode((self.width, self.height))

        # Creating a clock variable
        self.clock = pygame.time.Clock()

        # Loading and resizing game assets
        self.background = GameObject(0, 0, self.width, self.height, 'assets/background.png')
        self.treasure = GameObject(275, 50, 50, 50, 'assets/treasure.png')
        self.player = Player(275, 550, 50, 50, 'assets/player.png', 5)
        
        # Difficulty level
        self.level = 1.0

        self.reset_map()

    def reset_map(self):
        self.player = Player(275, 550, 50, 50, 'assets/player.png', 5)
        # Increases enemy speed as level goes up
        speed = 1 + (self.level * 3)

        # Increases number of enemies as level goes up
        if self.level >= 4.0:
            self.enemies = [
            Enemy(0, 450, 50, 50, 'assets/enemy.png', speed),
            Enemy(550, 300, 50, 50, 'assets/enemy.png', speed),
            Enemy(0, 150, 50, 50, 'assets/enemy.png', speed)
        ]
        elif self.level >= 2.0:
            self.enemies = [
            Enemy(0, 450, 50, 50, 'assets/enemy.png', speed),
            Enemy(550, 300, 50, 50, 'assets/enemy.png', speed)
        ]
        else:
            self.enemies = [
            Enemy(550, 300, 50, 50, 'assets/enemy.png', speed)
        ]

    def draw_objects(self):
        # Update display
        self.game_window.fill(self.white_colour)

        # Blitting assets to the screen
        self.game_window.blit(self.background.image, (self.background.x, self.background.y))
        self.game_window.blit(self.treasure.image, (self.treasure.x, self.treasure.y))
        self.game_window.blit(self.player.image, (self.player.x, self.player.y))
        for enemy in self.enemies:
            self.game_window.blit(enemy.image, (enemy.x, enemy.y))

        # Updates the changes to the window
        pygame.display.update()

    def move_objects(self, player_direction):
        self.player.move(player_direction, self.height)
        for enemy in self.enemies:
            enemy.move(self.width)

    # Implementing collision detection between objects
    def detect_collision(self, object_1, object_2):
        if object_1.y > (object_2.y + object_2.height):
            return False
        elif (object_1.y + object_1.height) < object_2.y:
            return False
        if object_1.x > (object_2.x + object_2.width):
            return False
        elif (object_1.x + object_1.width) < object_2.x:
            return False
        return True
    
    def check_if_collided(self):
        # Reset difficulty level if player collides with enemy
        for enemy in self.enemies:
            if self.detect_collision(self.player, enemy):
                self.level = 1.0
                return True
        # Increase difficulty level by 0.5 if player reaches treasure
        if self.detect_collision(self.player, self.treasure):
            self.level += 0.5
            return True
        return False

    # Game loop
    def run_game_loop(self):
        player_direction = 0
        while True:
            # Handle events
            events = pygame.event.get()
            for event in events:
                # Breaks the game loop by exiting the whole function
                if event.type == pygame.QUIT:
                    return
                # Move player up and down
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_direction = -1
                    elif event.key == pygame.K_DOWN:
                        player_direction = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player_direction = 0

            # Execute logic
            self.move_objects(player_direction)

            # Update display
            self.draw_objects()

            # Detect collisions
            if self.check_if_collided():
                # Increases difficulty or resets game
                self.reset_map()

            # The number of times per second the game window will be updated
            self.clock.tick(60)