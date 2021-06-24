import random
import math

import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()
pygame.key.set_repeat(1, 0)

# create the screen
screen = pygame.display.set_mode((600, 800))

# background
background = pygame.image.load('image/background.png')

# sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# caption and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('image/space-invaders.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('image/player.png')
playerX = 270
playerY = 680
playerX_change = 0


# enemy
class Enemy:
    def __init__(self, type):
        if type == 0:
            self.image = pygame.image.load('image/ufo_0.png')
            self.x = random.randint(0, 535)
            self.y = random.randint(50, 150)
            self.delta_x = random.choice([-13, -10, -9, -8, -7, 7, 8, 9, 10, 13])
            self.delta_y = 50

        if type == 1:
            self.image = pygame.image.load('image/monster.png')
            self.x = random.randint(0, 535)
            self.y = random.randint(50, 150)
            self.delta_x = random.choice([-19, -15, -13, 13, 15, 19])
            self.delta_y = 60

        if type == 2:
            self.image = pygame.image.load('image/ufo_1.png')
            self.x = random.randint(0, 535)
            self.y = random.randint(50, 150)
            self.delta_x = random.choice([-23, -20, 20, 23])
            self.delta_y = 80

        if type == 3:
            self.image = pygame.image.load('image/ufo_2.png')
            self.x = random.randint(0, 535)
            self.y = random.randint(50, 150)
            self.delta_x = random.choice([-25, -23, 23, 25])
            self.delta_y = 90


# functions

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def create_enemy(difficulty_list):
    enemy_selector = random.choice(difficulty_list)
    return Enemy(enemy_selector)


def show_enemy(i):
    screen.blit(enemy[i].image, (enemy[i].x, enemy[i].y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y - 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 35:
        return True
    else:
        return False


# create enemy list
enemy = []

for i in range(10):
    enemy.append(Enemy(0))
for i in range(5):
    enemy.append(Enemy(1))
for i in range(3):
    enemy.append(Enemy(2))
for i in range(2):
    enemy.append(Enemy(3))

num_of_enemies_all = len(enemy)
existing_enemy_idx = []
dead_enemy = []

# create enemy list with difficulty list
# for i in range(num_of_enemies_all):
#     enemy.append(create_enemy([0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 3]))

# bullet
bulletImg = pygame.image.load('image/bullet_up.png')
bulletX = 0
bulletY = 680
bulletY_change = 40
bullet_state = 'ready'

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render('Game Over! ', True, (200, 0, 0))
    screen.blit(over_text, (100, 350))

# game loop
running = True
while running:

    screen.fill((255, 255, 255))
    screen.blit(background, (-100, -600))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -15
            if event.key == pygame.K_RIGHT:
                playerX_change = 15
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # boundary setting
    if playerX <= 0:
        playerX = 0
    elif playerX >= 536:
        playerX = 536

    # game over
    for i in range(num_of_enemies_all):

        if len(existing_enemy_idx) > 5:
            break

        if i in dead_enemy:
            continue

        if i not in existing_enemy_idx:
            if len(existing_enemy_idx) < 5:
                existing_enemy_idx.append(i)
            else:
                break

        # Game Over
        if enemy[i].y > 640:
            for j in range(num_of_enemies_all):
                enemy[j].y = 2000
            game_over_text()
            break

        enemy[i].x += enemy[i].delta_x
        if enemy[i].x <= 0 or enemy[i].x >= 536:
            enemy[i].delta_x = -enemy[i].delta_x
            enemy[i].y += enemy[i].delta_y

        # collision
        collision = isCollision(enemy[i].x, enemy[i].y, bulletX, bulletY)
        if collision:
            existing_enemy_idx.remove(i)
            dead_enemy.append(i)

            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 680
            bullet_state = 'ready'
            score_value += 1
            # enemy[i].x = random.randint(0, 535)
            # enemy[i].y = random.randint(50, 150)
            enemy[i].y = -100 # delete the enemy

        show_score(textX, textY)
        show_enemy(i)

        print("existing: ", existing_enemy_idx)
        print("dead: ", dead_enemy)


    # bullet movement
    if bulletY <= 0:
        bulletY = 680
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    pygame.display.update()
