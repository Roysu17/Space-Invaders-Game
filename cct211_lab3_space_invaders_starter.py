"""
    Space Invaders 
    Demo of Sprites and Class Structure for Pygame
    CCT 211
    Week 3 Lab 
    Prof. Michael Nixon
"""
import pygame
import random

# --- Game Classes


class enemy(pygame.sprite.Sprite):
    """ This class represents the blocks. """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.move_scale = 1

        original_image = pygame.image.load('alien.png')
        self.image = pygame.transform.scale(original_image, (20, 15))

        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.x -= self.move_scale

        # Check if the enemy block reached the left or right edge
        if self.rect.x <= 0 or self.rect.x >= 640 - self.rect.width:
            self.move_scale *= -1
            self.rect.y += 15


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        original_image = pygame.image.load('space_ship.png')
        self.image = pygame.transform.scale(original_image, (20, 20))


        self.rect = self.image.get_rect()

    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.x = pos[0]


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 10])

        self.image.fill(pygame.color.THECOLORS['black'])

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3

class EnemyBullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 10])

        self.image.fill(pygame.color.THECOLORS['red'])

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y += 3


class Game:
    """ This class represents the Game. It contains all the game objects. """

    def __init__(self):
        """ Set up the game on creation. """

        # Initialize Pygame
        pygame.init()
        # --- Create the window
        # Set the height and width of the screen
        self.screen_width = 640
        self.screen_height = 480
        self.screen = pygame.display.set_mode(
            [self.screen_width, self.screen_height])

        self.num_blocks = 50
        self.running = False
        # --- Sprite lists

        # This is a list of every sprite. All blocks and the player block as well.
        self.all_sprites_list = pygame.sprite.Group()

        # List of each block in the game
        self.block_list = pygame.sprite.Group()

        # List of each bullet
        self.bullet_list = pygame.sprite.Group()
        
        # List of each enemy bullet
        self.enemy_bullet_list = pygame.sprite.Group()

        # --- Create the sprites

        for i in range(self.num_blocks):
            # This represents a block
            block = enemy()

            # Set a random location for the block
            block.rect.x = random.randrange(1, self.screen_width-block.rect.width)
            block.rect.y = random.randrange(self.screen_height//2)  # don't go all the way down

            # Add the block to the list of objects
            self.block_list.add(block)
            self.all_sprites_list.add(block)
        

        # Create a red player block
        self.player = Player()
        self.all_sprites_list.add(self.player)


        self.score = 0
        # this number is fairly arbitrary - just move the player off the bottom of the screen a bit based on the height of the player
        self.player.rect.y = self.screen_height - self.player.rect.height * 2

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button
                bullet = Bullet()
                # Set the bullet so it is where the player is
                bullet.rect.x = self.player.rect.x+9
                bullet.rect.y = self.player.rect.y
                # Add the bullet to the lists
                self.all_sprites_list.add(bullet)
                self.bullet_list.add(bullet)
            
            for enemy in self.block_list:
                if random.random() < 0.003:
                    # Fire a bullet from the enemy
                    bullet = EnemyBullet()
                    # Set the bullet so it is where the player is
                    bullet.rect.x = enemy.rect.x + (enemy.rect.width/2)
                    bullet.rect.y = enemy.rect.y + enemy.rect.height
                    # Add the bullet to the lists
                    self.all_sprites_list.add(bullet)
                    self.enemy_bullet_list.add(bullet)

    def update(self):
        if len(self.block_list) is 0:
            print("You Win")
            self.running = False
        # Call the update() method on all the sprites
        self.all_sprites_list.update()

        # Calculate mechanics for each enemy bullet
        for bullet in self.enemy_bullet_list:
            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(
                self.player, self.enemy_bullet_list, True)

            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                self.enemy_bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)
                print("You lose")
                self.running = False

            # Remove the bullet if it flies up off the screen
            if bullet.rect.y > (self.screen_height - bullet.rect.height):
                self.enemy_bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)

        # Calculate mechanics for each bullet
        for bullet in self.bullet_list:

            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(
                bullet, self.block_list, True)

            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)
                self.score += 1
                print(self.score)

            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < (0 - bullet.rect.height):
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)
        
        for block in self.block_list:
            if block.rect.y >= self.screen_height - block.rect.height:
                self.all_sprites_list.remove(block)
                self.block_list.remove(block)
                self.score -=1
                print(self.score)
                if self.score < 0:
                    print("You lose")
                    self.running = False
                
            
            

    def draw(self):
        # Clear the screen
        self.screen.fill(pygame.color.THECOLORS['white'])
        # Draw all the spites
        self.all_sprites_list.draw(self.screen)

    def run(self):
        self.running = True
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while self.running:
            # --- Event processing
            self.poll()

            # --- Handle game logic
            self.update()

            # --- Draw a frame
            self.draw()

            # Update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit the frames per second
            clock.tick(60)


if __name__ == '__main__':
    g = Game()
    print("starting...")
    g.run()
    print("shuting down...")
    pygame.quit()
