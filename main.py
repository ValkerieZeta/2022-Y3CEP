import pygame

# initialize the pygame
pygame.init()
pygame.font.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("game")
icon = pygame.image.load('Logo.png')
pygame.display.set_icon(icon)

# bullet datas
damage = 1
# defined by [y value, which side of the screen 800 or -32, wait time]
stage1easy = [[0, 800, 0], [120, 800, 0], [240, 800, 0], [360, 800, 0],
              [480, 800, 0], [30, 800, 1000], [90, 800, 1000], [150, 800, 1000],
              [210, 800, 1000], [270, 800, 1000], [330, 800, 1000], [390, 800, 1000],
              [450, 800, 1000], [570, 800, 1000], [0, 800, 2000], [60, 800, 2000], [120, 800, 2000],
              [180, 800, 2000],
              [2400, 800, 2000], [300, 800, 2000], [360, 800, 2000], [410, 800, 2000],
              [480, 800, 2000], [540, 800, 2000]]

# hearts
lifeImg = pygame.image.load('heart.png')
lifeX = 5
lifeY = 5

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
dPlayerX = 0
dPlayerY = 0
life = 5
lastTakenDamage = 0

# stages
intro = True
stage1 = False
stage1begin = False
stage2 = False
stage3 = False
keyPressedX = ''
keyPressedY = ''
introCount = 0

# create bullet class

class Bullet:
    def __init__(self, x, y, wait):
        self.x = x
        self.y = y
        self.wait = wait
        self.spawned = False
        self.takenDamage = False
        self.enemyImg = pygame.image.load('bullet1.png')

    # spawning bullets function
    def spawnBullet(self):
        if stage1:
            now = pygame.time.get_ticks()
            if now - stage1tick >= self.wait:
                if stage1:
                    screen.blit(self.enemyImg, (self.x, self.y))
                    self.spawned = True


def player(x, y):
    screen.blit(playerImg, (x, y))


def hearts(a, b):
    screen.blit(lifeImg, (a, b))


class Background:
    def __init__(self, img):
        self.picture = img
        self.img = pygame.image.load(self.picture).convert_alpha()
        self.alpha = 255

    def set_alpha(self, alpha):
        self.img.set_alpha(alpha)


class Text:
    def __init__(self, p, q, colour, font, fontSize, text):
        self.font = pygame.font.Font(font, fontSize)
        self.fontSize = fontSize
        self.text = self.font.render(text, True, colour)
        self.x = p
        self.y = q

    def displayText(self):
        screen.blit(self.text, (self.x, self.x))


introTxt = Text(300, 400, (255, 255, 255), "Game Of Squids.ttf", 32, "GAME")
bg = Background('background.png')
bg.set_alpha(100)
# game loop

running = True
introMusic = pygame.mixer.Sound("Intro .mp3")
playIntroMusic = False
playedIntroMusic = False
introMusic.play()
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg.img, (0, 0))
    pygame.time.Clock().tick_busy_loop(200)



    

    for event in pygame.event.get():

        # quit
        if event.type == pygame.QUIT:
            running = False

        # player controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dPlayerX = -3
                keyPressedX = 'LEFT'
            if event.key == pygame.K_RIGHT:
                dPlayerX = 3
                keyPressedX = 'RIGHT'
            if event.key == pygame.K_UP:
                dPlayerY = -3
                keyPressedY = 'UP'
            if event.key == pygame.K_DOWN:
                dPlayerY = 3
                keyPressedY = 'DOWN'

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and keyPressedX == 'RIGHT':
                dPlayerX = 3
            if event.key == pygame.K_RIGHT and keyPressedX == 'LEFT':
                dPlayerX = -3
            if event.key == pygame.K_UP and keyPressedY == 'DOWN':
                dPlayerY = 3
            if event.key == pygame.K_DOWN and keyPressedY == 'UP':
                dPlayerY = 3
            if event.key == pygame.K_LEFT and keyPressedX == 'LEFT':
                dPlayerX = 0
                keyPressedX = 'RIGHT'
            elif event.key == pygame.K_RIGHT and keyPressedX == 'RIGHT':
                dPlayerX = -0
                keyPressedX = 'LEFT'
            elif event.key == pygame.K_UP and keyPressedY == 'UP':
                dPlayerY = 0
                keyPressedY = 'DOWN'
            elif event.key == pygame.K_DOWN and keyPressedY == 'DOWN':
                dPlayerY = 0
                keyPressedY = 'UP'

    if intro:
        introTxt.displayText()
        introCount += 1
        playIntroMusic = True
    
    if playIntroMusic == True and playedIntroMusic == False:
        introMusic.play()
        playIntroMusic = None
        playedIntroMusic = True

    if introCount == 100:
        stage1tick = pygame.time.get_ticks()
        introCount += 1

    if introCount >= 100:
        intro = False
        stage1 = True

    if stage1:

        for j in range(len(stage1easy)):
            if stage1easy[j][1] > -64:
                enemy = Bullet(stage1easy[j][1], stage1easy[j][0], stage1easy[j][2])
                enemy.spawnBullet()
                if enemy.spawned:
                    stage1easy[j][1] -= 6
                    if pygame.time.get_ticks() - lastTakenDamage >= 200:
                        if playerX + 2 <= enemy.x <= playerX + 30:
                            if not enemy.takenDamage:
                                if playerY <= enemy.y + 7 <= playerY + 29 or playerY <= enemy.y + 24 <= playerY + 29:
                                    life -= damage
                                    enemy.takenDamage = True
                                    lastTakenDamage = pygame.time.get_ticks()
        stage1 = False

    playerY += dPlayerY
    playerX += dPlayerX
    if playerX + 2 <= 0:
        playerX = -2
    if playerX + 2 >= 772:
        playerX = 770
    if playerY <= -4:
        playerY = -4
    if playerY >= 571:
        playerY = 571
    player(playerX, playerY)

    # display lives
    for i in range(life):
        hearts(lifeX + i * 32, lifeY)

    pygame.display.update()
