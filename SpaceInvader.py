import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((640, 320))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.png")
background = pygame.image.load("cityskyline.png")
font = pygame.font.Font("freesansbold.ttf", 32)
over = pygame.font.Font("freesansbold.ttf", 64)
game_over = over.render("GAME OVER", True, (255, 255, 255))
pygame.display.set_icon(icon)


def gameOver():
    screen.blit(game_over, (150, 140))


playerX = 300
playerY = 270
playerChangeX = 0
playerImg = pygame.image.load("player.png")


def player(x, y):
    screen.blit(playerImg, (x, y))


rockX = []
rockY = []
rockImg = []
rockChangeX = []
rockChangeY = []
num_of_enemies = 6
for i in range(num_of_enemies):
    rockX.append(random.randint(0, 600))
    rockY.append(random.randint(0, 20))
    rockChangeX.append(4)
    rockChangeY.append(0)
    rockImg.append(pygame.image.load("rock.png"))
score = 0


def show_score(score):
    score_disp = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_disp, (10, 10))


def rock(x, y, i):
    screen.blit(rockImg[i], (x, y))


fireX = playerX
fireY = playerY
fireChangeX = 4
fireChangeY = -4
fireImg = pygame.image.load("fire.png")
fireState = "ready"


def shootFire(x, y):
    global fireState
    screen.blit(fireImg, (x + 4, y - 20))
    fireState = "fired"


def isCollision(rockX, rockY, fireX, fireY):
    global score
    distance = math.sqrt((math.pow(rockX - fireX, 2) + math.pow(rockY - fireY, 2)))
    if (distance < 27):
        score += 1
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerChangeX = 5
            elif event.key == pygame.K_LEFT:
                playerChangeX = -5
            if event.key == pygame.K_SPACE:
                if fireState == "ready":
                    fireX = playerX
                    fireY = playerY
                    shootFire(fireX, fireY)


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                playerChangeX = 0
            elif event.key == pygame.K_LEFT:
                playerChangeX = 0
    playerX += playerChangeX
    if playerX <= 0:
        playerX = 0
    elif playerX >= 608:
        playerX = 608
    for i in range(num_of_enemies):
        rockChangeY[i] = 0
        if rockY[i] >= 230:
            for j in range(num_of_enemies):
                rockY[j] = 2000
            gameOver()
        if rockX[i] <= 0:
            rockX[i] = 0
            rockChangeX[i] = 4
            rockChangeY[i] = 15
        elif rockX[i] >= 608:
            rockX[i] = 608
            rockChangeX[i] = -4
            rockChangeY[i] = 15
        rockX[i] += rockChangeX[i]
        rockY[i] += rockChangeY[i]
        if isCollision(rockX[i], rockY[i], fireX, fireY):
            rockX[i] = random.randint(0, 600)
            rockY[i] = random.randint(0, 20)

        rock(rockX[i], rockY[i], i)
    if fireState == "ready":
        fireX = playerX
        fireY = playerY
    if fireState == "fired":
        fireY += fireChangeY
        shootFire(fireX, fireY)
    if fireY <= 0:
        fireY = 0
        fireState = "ready"
    show_score(score)
    player(playerX, playerY)
    pygame.display.update()
