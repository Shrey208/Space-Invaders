VERSION = "1.0.1<shreyansh>"
import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
backgroud = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
score_value = 0
level_value = 1
space_num = 0
x = 0
t = 0
num_of_enemies = 50 + level_value
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1 * level_value)
    enemyY_change.append(40)
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"
font = pygame.font.Font('myfont.ttf', 32)
over_font = pygame.font.Font('myfont.ttf', 64)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    level = font.render("Level : " + str(level_value), True, (255, 255, 255))
    screen.blit(level, (330, 10))
    screen.blit(score, (x, y))
    if t == 0:
        bulletsfired = font.render("Bullets Fired : " + str(space_num), True, (255, 255, 255))
        screen.blit(bulletsfired, (600, 10))


def game_over_text():
    bulletsfired = font.render("Bullets Fired : " + str(total_space), True, (255, 255, 255))
    screen.blit(bulletsfired, (600, 10))
    end_score = font.render("Accuracy : " + str(round((score_value / total_space) * 100)) + " %", True, (255, 255, 255))
    screen.blit(end_score, (330, 150))
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (280, 250))


def player(x, y):
    if t == 0:
        screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    if t == 0:
        screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(backgroud, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    if t == 0:
                        bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    space_num += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            bullet_state = "ready"
            t = 1
            if x == 0:
                total_space = space_num
            x += 1
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            if (score_value) % 10 == 0:
                level_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
