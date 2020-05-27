import pygame
import random
import math
from pygame import mixer

#Initialize the pygame
pygame.init()

#Create the Screen
screen = pygame.display.set_mode((800,600))

# #Sound
# mixer.music.load("./sounds/background.mp3")
# mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders by Aihab")
icon = pygame.image.load("./icon/icon.png")
pygame.display.set_icon(icon)

#Score and Game over text
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 80)

#Background Loader
bgImage = pygame.image.load("./backgrounds/background1.jpg")

#Player
playerImg = pygame.image.load("./players/player1.png")
playerX = 370
playerY = 500
playerX_change = 0
playerY_change = 0

#Enemy1
enemyImg = pygame.image.load("./enemies/enemy1.png")

#Enemy2
enemyImg2 = pygame.image.load("./enemies/enemy2.png")

#Enemy3
enemyImg3 = pygame.image.load("./enemies/enemy3.png")

#Enemy4
enemyImg4 = pygame.image.load("./enemies/enemy4.png")

#Enemy5
enemyImg5 = pygame.image.load("./enemies/enemy5.png")

#Enemy6
enemyImg6 = pygame.image.load("./enemies/enemy7.png")

#Enemies
enemyImages = [enemyImg, enemyImg2, enemyImg3, enemyImg4, enemyImg5, enemyImg6]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(6):
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(20,100))
    enemyX_change.append(3) 
    enemyY_change.append(80)

#Bullet
bulletImg = pygame.image.load("./bullets/bullet.png")
bulletX = playerX
bulletY = playerY
bulletX_change = 0
bulletY_change = -12
bullet_state = "ready"

#Web
webImg = pygame.image.load("./bullets/web.png")
webX = enemyX[0]
webY = enemyY[0]
webX_change = 2
webY_change = 3
web_state = "ready"

#Bat
batImg = pygame.image.load("./bullets/bat.png")
batX = enemyX[1]
batY = enemyY[1]
batX_change = 3
batY_change = 3
bat_state = "ready"

#Punch
punchImg = pygame.image.load("./bullets/punch.png")
punchX = enemyX[2]
punchY = enemyY[2]
punchX_change = 0
punchY_change = 2
punch_state = "ready"

def player():
    screen.blit(playerImg, (playerX, playerY))
def enemy(x, y, i):
       screen.blit(enemyImages[i], (x, y))
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (150, 250))
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y))
def fire_web(x,y):
    global web_state
    web_state = "fire"
    screen.blit(webImg, (x+16,y))
def fire_bat(x,y):
    global bat_state
    bat_state = "fire"
    screen.blit(batImg, (x+16,y))
def fire_punch(x,y):
    global punch_state
    punch_state = "fire"
    screen.blit(punchImg, (x+16,y))
def isCollision(x, y, bulletX, bulletY):
    distance = math.sqrt(math.pow(bulletX-x, 2) + math.pow(bulletY - y, 2))
    if distance < 35:
        return True
    else:
        return False
def isCollisionAdvanced(x, y, bulletX, bulletY):
    distance = math.sqrt(math.pow(bulletX-x, 2) + math.pow(bulletY - y, 2))
    if distance < 25:
        return True
    else:
        return False

#Game Loop
running = True
while running:
    #Background Screen
    screen.fill((0,0,0))
    screen.blit(bgImage, (0,0)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Controlling movements using keystrokes
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -8
        if event.key == pygame.K_RIGHT:
            playerX_change = 8
        if event.key == pygame.K_UP:
            playerY_change = -6
        if event.key == pygame.K_DOWN:
            playerY_change = 6
        if event.key == pygame.K_SPACE:
            if bullet_state is "ready":
                bulletX = playerX
                bulletY = playerY
                bulletSound = mixer.Sound("./sounds/laser.wav")
                bulletSound.play()
                fire_bullet(bulletX, bulletY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT and playerX_change < 0 :  
            playerX_change = 0
        elif event.key == pygame.K_RIGHT and playerX_change > 0 :
            playerX_change = 0
        elif event.key == pygame.K_UP and playerY_change < 0:
            playerY_change = 0
        elif event.key == pygame.K_DOWN and playerY_change > 0:
            playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    if playerY <= 360:
        playerY = 360
    if playerY >= 500:
        playerY = 500          

    #Enemy Movement
    for i in range(6):
       # Game Over
       if enemyY[i] > 530:
            for j in range(6):
                enemyY[0] = 2000
                enemyY[1] = 2000
                enemyY[2] = 2000
                enemyY[3] = 2000
                enemyY[4] = 2000
                enemyY[5] = 2000
                game_over()
                break
     
       enemyX[i] += enemyX_change[i]

       if enemyX[i] >= 736:
              enemyX_change[i] = -3
              enemyY[i] += enemyY_change[i]
       if enemyX[i] <= 0:
              enemyX_change[i] = 3
              enemyY[i] += enemyY_change[i]
      
       #Collision
       collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
       if collision:
          explosionSound = mixer.Sound("./sounds/explosion.wav")
          explosionSound.play()
          bullet_state = "ready"
          bulletY = 600
          enemyX[i] = random.randint(0,736)
          enemyY[i] = random.randint(20, 150)
          score_value += 1

       endgameCollision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
       if endgameCollision:     
           for j in range(6):
                enemyY[0] = 2000
                enemyY[1] = 2000
                enemyY[2] = 2000
                enemyY[3] = 2000
                enemyY[4] = 2000
                enemyY[5] = 2000
                game_over()
                break

       collisionWithWeb = isCollisionAdvanced(webX, webY, playerX, playerY)
       if collisionWithWeb:
           for j in range(6):
                enemyY[0] = 2000              
                enemyY[1] = 2000
                enemyY[2] = 2000
                enemyY[3] = 2000
                enemyY[4] = 2000
                enemyY[5] = 2000
                game_over()
                webX_change = 0
                webY_change = 0
                break

       collisionWithBat = isCollisionAdvanced(batX, batY, playerX, playerY)
       if collisionWithBat:
           for j in range(6):
                enemyY[0] = 2000              
                enemyY[1] = 2000
                enemyY[2] = 2000
                enemyY[3] = 2000
                enemyY[4] = 2000
                enemyY[5] = 2000
                game_over()
                batX_change = 0
                batY_change = 0
                break

       collisionWithPunch = isCollisionAdvanced(punchX, punchY, playerX, playerY)
       if collisionWithPunch:
           for j in range(6):
                enemyY[0] = 2000              
                enemyY[1] = 2000
                enemyY[2] = 2000
                enemyY[3] = 2000
                enemyY[4] = 2000
                enemyY[5] = 2000
                game_over()
                punchX_change = 0
                punchY_change = 0
                break    

       enemy(enemyX[i], enemyY[i], i)

    #Bullet Movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change                           

    if bulletY <=0:
        bullet_state = "ready"
        bulletY = 480

    #Web Firing
    if web_state is "ready":
                webX = enemyX[0]
                webY = enemyY[0]
                fire_web(webX, webY)
    if web_state is "fire":
       webY += webY_change
       if enemyX_change[0] > 0:
           webX += webX_change
       else:
           webX -= webX_change
       screen.blit(webImg, (webX+16,webY))        

    if webY >= 580:
        web_state = "ready"
        webY = enemyY[0]
        webX = enemyX[0]

    #Bat Firing
    if bat_state is "ready":
                batX = enemyX[1]
                batY = enemyY[1]
                fire_bat(batX, batY)
    if bat_state is "fire":
       batY += batY_change
       if enemyX_change[1] > 0:
           batX += batX_change
       else:
           batX -= batX_change
       screen.blit(batImg, (batX+16,batY))        

    if batY >= 580:
        bat_state = "ready"
        batY = enemyY[1]
        batX = enemyX[1]

    #Punch Firing
    if punch_state is "ready":
                punchX = enemyX[2]
                punchY = enemyY[2]
                fire_punch(punchX, punchY)
    if punch_state is "fire":
       punchY += punchY_change
       if enemyX_change[2] > 0:
           punchX += punchX_change
       else:
           punchX -= punchX_change
       screen.blit(punchImg, (punchX+16,punchY))        

    if punchY >= 580:
        punch_state = "ready"
        punchY = enemyY[2]
        punchX = enemyX[2]         
    
    player()
    show_score(10, 10)
    #To constantly update the screen
    pygame.display.update()