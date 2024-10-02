import pygame
from pygame import mixer
import math
import random
import sys

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')
background_X = 0
background_Y = 1200

# Sound
mixer.music.load("background.mp3")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(30)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
verydamaged_font = pygame.font.Font('veryDamaged.ttf', 32)
textX = 10
testY = 10

# High score
high_score_file = open('High_score','r')
high_score_value_str = high_score_file.readline()
sys.set_int_max_str_digits(30000)
high_score_value = int(high_score_value_str)

# Game Over
over_font = pygame.font.Font('VeryDamaged.ttf', 130)

# Intro
intro_img = pygame.image.load('ufo.png')
intro_img_X = 150
intro_img_Y = 50
skip_text = pygame.font.Font('freesansbold.ttf', 25)
title_font = pygame.font.Font('VeryDamaged.ttf', 100)
title_font_X = 1000
title_font_Y = 200


def show_intro(x, y):
    screen.blit(intro_img, (x, y))


def show_skip():
    skip_show = skip_text.render("##PRESS 'SPACE' TO SKIP##", True, (0, 250, 0))
    screen.blit(skip_show, (225, 550))

def show_title(x, y):
    title_text = title_font.render('SPACE INVADERS', True, (236, 21, 21))
    screen.blit(title_text, (x,y))

def show_score(x, y):
    score = verydamaged_font.render("Score : " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

def show_high_score(high_score_value):
    high_score = verydamaged_font.render("High Score : " + str(high_score_value), True, (0, 255, 0))
    screen.blit(high_score, (550, 10))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (21,255, 0))
    screen.blit(over_text, (100, 200))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Intro
running1 = 2
while running1 < 3:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running1 = 5
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running1 = 7

    intro_img_Y -= 0.5

    if title_font_X < 65:
        title_font_X = 65
    else:
        title_font_X -= 0.5

    if background_Y < 0:
        background_Y = 0
        title_font_Y -= 0.1
    else:
        background_Y -= 0.5

    if title_font_Y < -100:
        running1 = 7

    screen.blit(background, (background_X, background_Y))
    show_intro(intro_img_X, intro_img_Y)
    show_title(title_font_X, title_font_Y)
    show_skip()
    pygame.display.update()

# Game Loop
running2 = True
while running2:

    if running1 == 5:
        running2 = False

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running2 = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if score_value >= high_score_value:
        high_score_value = score_value

    player(playerX, playerY)
    show_score(textX, testY)
    show_high_score(high_score_value)
    pygame.display.update()

high_score_file.close()
if score_value >= high_score_value:
    high_score_file = open('High_score','w')
    high_score_file.write(str(score_value))
