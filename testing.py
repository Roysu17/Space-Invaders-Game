import pygame
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface([20, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(pygame.color.THECOLORS['red'])
        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(pygame.color.THECOLORS['black'])
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 3

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('alien.png')  # Replace with actual image file
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 640 - self.rect.width)
        self.rect.y = random.randrange(0, 100)
        self.speed = 3
        self.direction = 1
        self.shoot_chance = 0.01
        self.bullet_speed = 5

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.right >= 640 or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y += self.rect.height
        if self.rect.bottom >= 480:
            global score
            score -= 1
            if score < 0:
                print("Game Over - You Lose!")
                pygame.quit()
                exit()
        if random.random() < self.shoot_chance:
            self.shoot()

    def shoot(self):
        bullet = Bullet()
        bullet.rect.x = self.rect.centerx
        bullet.rect.y = self.rect.bottom
        all_sprites_list.add(bullet)
        enemy_bullets_list.add(bullet)

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 640
        self.screen_height = 480
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        self.num_blocks = 50
        self.running = False
        self.all_sprites_list = pygame.sprite.Group()
        self.block_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        for i in range(self.num_blocks):
            block = Block(pygame.color.THECOLORS['blue'])
            block.rect.x = random.randrange(self.screen_width)
            block.rect.y = random.randrange(self.screen_height / 2)
            self.block_list.add(block)
            self.all_sprites_list.add(block)
        self.player = Player()
        self.all_sprites_list.add(self.player)
        self.score = 0
        self.player.rect.y = self.screen_height - self.player.rect.height * 2

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet()
                bullet.rect.x = self.player.rect.x
                bullet.rect.y = self.player.rect.y
                self.all_sprites_list.add(bullet)
                self.bullet_list.add(bullet)

    def update(self):
        self.all_sprites_list.update()
        for bullet in self.bullet_list:
            block_hit_list = pygame.sprite.spritecollide(bullet, self.block_list, True)
            for block in block_hit_list:
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)
                self.score += 1
                print(self.score)
            if bullet.rect.y < (0 - bullet.rect.height):
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)

        for enemy in self.enemy_list:
            if pygame.sprite.spritecollide(enemy, self.bullet_list, True):
                self.enemy_list.remove(enemy)
                self.all_sprites_list.remove(enemy)
                self.score += 1
                print(self.score)

    def draw(self):
        self.screen.fill(pygame.color.THECOLORS['white'])
        self.all_sprites_list.draw(self.screen)

    def run(self):
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            self.poll()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    g = Game()
    print("starting...")
    g.run()
    print("shutting down...")
    pygame.quit()
