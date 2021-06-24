# https://www.flaticon.com/
# https://freesound.org/

import random
import math
import time

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


# enemy
class Enemy:
    def __init__(self, type):
        if type == 0:
            self.image = pygame.image.load('image/ufo_0.png')
            self.x = random.randint(0, 535)
            self.y = random.randint(50, 150)
            self.delta_x = random.choice([-13, -10, -9, -8, -7, 7, 8, 9, 10, 13])
            self.delta_y = 50
            self.size = 25  # radius
            self.enable_enemy_bullet = False

        elif type == 1:
            self.image = pygame.image.load('image/monster.png')
            self.x = random.randint(0, 535)
            self.y = random.randint(50, 150)
            self.delta_x = random.choice([-19, -15, -13, 13, 15, 19])
            self.delta_y = 60
            self.size = 35
            self.enable_enemy_bullet = False

        elif type == 2:
            self.image = pygame.image.load('image/ufo_1.png')
            self.x = random.randint(0, 535)
            self.y = random.randint(50, 150)
            self.delta_x = random.choice([-13, -10, -9, -8, -7, 7, 8, 9, 10, 13])
            self.delta_y = 50
            self.size = 20
            self.enable_enemy_bullet = True
            self.bullet = EnemyBullet()

        elif type == 3:
            self.image = pygame.image.load('image/ufo_2.png')
            self.x = random.randint(0, 535)
            self.y = random.randint(50, 150)
            self.delta_x = random.choice([-19, -15, -13, 13, 15, 19])
            self.delta_y = 0
            self.size = 20
            self.enable_enemy_bullet = True
            self.bullet = EnemyBullet()

    def show(self):
        screen.blit(self.image, (self.x, self.y))

    def fire_bullet(self):
        self.bullet.state = 'fire'
        self.bullet.x = self.x
        self.bullet.y = self.y + 27
        screen.blit(self.bullet.image, (self.bullet.x, self.bullet.y))


class EnemyBullet:
    def __init__(self):
        self.image = pygame.image.load('image/enemybullet.png')
        self.x = 0
        self.y = 0
        self.delta_y = 18
        self.state = 'ready'


class Player:
    def __init__(self):
        self.image = pygame.image.load('image/player.png')
        self.x = 270
        self.y = 680
        self.delta_x = 0
        self.delta_y = 0
        self.size = 35
        self.bullet_type = "single"
        self.bullets = []

    def init_bullets(self):
        if self.bullet_type == "single":
            self.bullets = []
            self.bullets.append(PlayerBullet(bullet_up_image, self.x + 18, self.y, 0, 40))
        elif self.bullet_type == "double":
            self.bullets = []
            self.bullets.append(PlayerBullet(bullet_up_image, self.x - 5, self.y, 0, 40))
            self.bullets.append(PlayerBullet(bullet_up_image, self.x + 40, self.y, 0, 40))
        elif self.bullet_type == "triple":
            self.bullets = []
            self.bullets.append(PlayerBullet(bullet_dot_image, self.x - 5, self.y, -10, 40))
            self.bullets.append(PlayerBullet(bullet_up_image, self.x + 18, self.y, 0, 40))
            self.bullets.append(PlayerBullet(bullet_dot_image, self.x + 40, self.y, 10, 40))
        elif self.bullet_type == "quadra":
            self.bullets = []
            self.bullets.append(PlayerBullet(bullet_upperleft_image, self.x - 5, self.y, -25, 25))
            self.bullets.append(PlayerBullet(bullet_up_image, self.x - 5, self.y, 0, 40))
            self.bullets.append(PlayerBullet(bullet_up_image, self.x + 40, self.y, 0, 40))
            self.bullets.append(PlayerBullet(bullet_upperright_image, self.x + 40, self.y, 25, 25))

    def show(self):
        screen.blit(self.image, (self.x, self.y))

    def fire_bullet(self):
        global bullet_state
        bullet_state = 'fire'
        for bullet in self.bullets:
            bullet.state = 'fire'
            bullet.fire()

    def set_bullet_x(self):
        if self.bullet_type == "single":
            self.bullets[0].x = self.x + 18
        elif self.bullet_type == "double":
            self.bullets[0].x = self.x - 5
            self.bullets[1].x = self.x + 40
        elif self.bullet_type == "triple":
            self.bullets[0].x = self.x - 5
            self.bullets[1].x = self.x + 18
            self.bullets[2].x = self.x + 40
        elif self.bullet_type == "quadra":
            self.bullets[0].x = self.x - 5
            self.bullets[1].x = self.x - 5
            self.bullets[2].x = self.x + 40
            self.bullets[3].x = self.x + 40


class PlayerBullet:
    def __init__(self, image, x, y, delta_x, delta_y):
        self.image = image
        self.x = x
        self.y = y
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.state = 'ready'

    def fire(self):
        self.state = 'fire'
        screen.blit(self.image, (self.x, self.y))


class Parachute:
    def __init__(self, buff: str, x, y, delta_x, delta_y):
        self.image = None
        self.x = x
        self.y = y
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.size = 30
        self.buff = buff
        if self.buff == "double":
            self.image = parachute1_image
        elif self.buff == "triple":
            self.image = parachute2_image
        elif self.buff == "quadra":
            self.image = parachute3_image

    def show(self):
        screen.blit(self.image, (self.x, self.y))


parachute1_image = pygame.image.load("image/parachute-1.png")
parachute2_image = pygame.image.load("image/parachute-2.png")
parachute3_image = pygame.image.load("image/parachute-3.png")
parachute4_image = pygame.image.load("image/parachute-4.png")
parachute5_image = pygame.image.load("image/parachute-5.png")

bullet_up_image = pygame.image.load('image/bullet_up.png')
bullet_upperleft_image = pygame.image.load('image/bullet_upper_left.png')
bullet_upperright_image = pygame.image.load('image/bullet_upper_right.png')
bullet_dot_image = pygame.image.load('image/bullet_dot.png')

player = Player()
player.init_bullets()

parachutes = []

bullet_state = 'ready'


# functions
def victory_text(x, y):
    victory = font.render("Victory!", True, (128, 0, 0))
    screen.blit(victory, (x, y))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))
    if score_value == num_of_enemies_all:
        victory_text(x + 10, y + 80)


def create_enemy(difficulty_list):
    enemy_selector = random.choice(difficulty_list)
    return Enemy(enemy_selector)


def isCollision(enemyX, enemyY, bulletX, bulletY, d):
    distance = math.sqrt((math.pow(enemyX + d/2 - bulletX - 5, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < d:
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

# score
score_value = 0
full_marks = 7
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)
over_music = "explosion2.mp3"
music_played = False

def over_music():
    global music_played

    mixer.music.load('explosion2.mp3')
    mixer.music.play()
    time.sleep(2)
    mixer.music.stop()
    music_played = True


def game_over_text():
    if not music_played:
        over_music()
    over_text = over_font.render('Game Over! ', True, (200, 0, 0))
    screen.blit(over_text, (100, 350))
    show_score(230, 440)

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
                player.delta_x = -15
            if event.key == pygame.K_RIGHT:
                player.delta_x = 15
            if event.key == pygame.K_SPACE:
                print("player.x: ", player.x)
                print("bullet.x: ", [bullet.x for bullet in player.bullets])
                if bullet_state is 'ready':
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    player.set_bullet_x()
                    for bullet in player.bullets:
                        player.fire_bullet()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.delta_x = 0

    player.x += player.delta_x

    # boundary setting
    if player.x <= 0:
        player.x = 0
    elif player.x >= 536:
        player.x = 536

    if score_value == full_marks:
        show_score(230, 380)

    # loop through each enemy
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
            for parachute in parachutes:
                parachute.y = 2000
            existing_enemy_idx = []
            game_over_text()
            break

        # enemy movement
        enemy[i].x += enemy[i].delta_x
        if enemy[i].x <= 0 or enemy[i].x >= 536:
            enemy[i].delta_x = -enemy[i].delta_x
            enemy[i].y += enemy[i].delta_y

        # collision detection
        for bullet in player.bullets:
            if isCollision(enemy[i].x, enemy[i].y, bullet.x, bullet.y, enemy[i].size):
                existing_enemy_idx.remove(i)
                dead_enemy.append(i)

                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
                bullet.y = 680
                bullet.state = 'ready'
                score_value += 1
                # enemy[i].x = random.randint(0, 535)
                # enemy[i].y = random.randint(50, 150)
                enemy[i].y = -100  # delete the enemy

        show_score(textX, textY)
        enemy[i].show()

        # print("existing: ", existing_enemy_idx)
        # print("dead: ", dead_enemy)

    # parachute
    if not (score_value % 4 == 0 and score_value != 0):
        has_appended = False

    if not has_appended:
        if score_value % 4 == 0 and score_value != 0:
            parachutes.append(
                Parachute(random.choice(["double", "triple", "quadra"]), random.randrange(30, 530), 0,
                                                random.randrange(1, 3), random.randrange(3, 5))
            )
            has_appended = True

    if len(parachutes) != 0:
        for parachute in parachutes:
            if parachute.x > 600 or parachute.x < 0 or parachute.y > 800:
                parachute.y = 2000
                continue
            parachute.x += parachute.delta_x
            parachute.y += parachute.delta_y
            parachute.show()

            # collision detection
            for bullet in player.bullets:

                if isCollision(parachute.x, parachute.y, bullet.x, bullet.y, parachute.size):
                    explosion_Sound = mixer.Sound('explosion.wav')
                    explosion_Sound.play()
                    bullet.y = 680
                    bullet.state = 'ready'
                    parachutes.remove(parachute)

                    player.bullet_type = parachute.buff
                    player.init_bullets()


    # bullet movement
    bullet_state = 'ready'
    for bullet in player.bullets:
        if bullet.state == 'fire':
            bullet_state = 'fire'
            break

    for bullet in player.bullets:
        if bullet.y <= 0 or bullet.x <= 0 or bullet.x >= 600:
            bullet.y = 680
            bullet.state = 'ready'
        if bullet.state is 'fire':
            bullet.fire()
            bullet.x += bullet.delta_x
            bullet.y -= bullet.delta_y

    # enemy bullet movement
    for i in existing_enemy_idx:
        if enemy[i].enable_enemy_bullet:

            # collision detection of enemy bullet (game over)
            if isCollision(player.x, player.y, enemy[i].bullet.x, enemy[i].bullet.y, player.size):
                for j in range(num_of_enemies_all):
                    enemy[j].y = 2000
                for bullet in player.bullets:
                    bullet.y = 680
                existing_enemy_idx = []
                game_over_text()
                break

            if enemy[i].bullet.y >= 800:
                enemy[i].bullet.y = enemy[i].y
                enemy[i].bullet.x = enemy[i].x
                enemy[i].bullet.state = 'ready'

            if enemy[i].bullet.state == 'fire':
                enemy[i].bullet.y += enemy[i].bullet.delta_y
                screen.blit(enemy[i].bullet.image, (enemy[i].bullet.x, enemy[i].bullet.y))

            elif enemy[i].bullet.state == 'ready':
                fire = random.choice([False] * 40 + [True])
                if fire:
                    enemy[i].fire_bullet()

    player.show()
    pygame.display.update()
