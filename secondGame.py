import pygame
import os

WIDTH = 800
HEIGHT = 600
FPS = 10

# define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
magenta = (255, 0, 255)

player1Select = 0
player2Select = 0

# images
# where folders are to setup assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

alucard_folder = os.path.join(img_folder, "alucardSprites")
alucard = [pygame.image.load(os.path.join(alucard_folder, "1.png")),
           pygame.image.load(os.path.join(alucard_folder, "2.png")),
           pygame.image.load(os.path.join(alucard_folder, "3.png")),
           pygame.image.load(os.path.join(alucard_folder, "4.png")),
           pygame.image.load(os.path.join(alucard_folder, "crouch_1.png"))]

alucardRun = [pygame.image.load(os.path.join(alucard_folder, "run_1.png")),
              pygame.image.load(os.path.join(alucard_folder, "run_2.png")),
              pygame.image.load(os.path.join(alucard_folder, "run_3.png"))]

alucardJump = [pygame.image.load(os.path.join(alucard_folder, "jump_1.png")),
               pygame.image.load(os.path.join(alucard_folder, "jump_2.png")),
               pygame.image.load(os.path.join(alucard_folder, "jump_3.png")),
               pygame.image.load(os.path.join(alucard_folder, "jump_4.png")),
               pygame.image.load(os.path.join(alucard_folder, "jump_5.png"))]

alucardKick = [pygame.image.load(os.path.join(alucard_folder, "crouchLight_1.png")),
               pygame.image.load(os.path.join(alucard_folder, "crouchLight_2.png")),
               pygame.image.load(os.path.join(alucard_folder, "crouchLight_3.png"))]


alucard_run = 5
alucard_back = 0
alucard_Kick = 0
alucard_stand = 0
frames = 0


# setup player
class Player(pygame.sprite.Sprite):
    # sprite for the player


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = alucard[0].convert()
        self.image.set_colorkey(magenta)
        self.rect = self.image.get_rect()  # each sprite is a rectangle
        self.rect.center = (100, HEIGHT - 175)  # set start position
        self.x_speed = 20
        self.y_speed = 10

    def update(self):
        self.x_speed = 0
        self.y_speed = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.image = alucard[alucard_back]
            self.image.set_colorkey(magenta)
            self.rect.bottom = HEIGHT - 125
            self.x_speed = -7
        '''
        if keys[pygame.K_w]:
            self.y_speed = 10
        '''
        if keys[pygame.K_d]:

            self.image = alucardRun[alucard_run]
            self.image.set_colorkey(magenta)
            self.rect.bottom = HEIGHT - 110
            self.x_speed = 15

        if keys[pygame.K_s]:
            self.image = alucard[4]
            self.image.set_colorkey(magenta)
            self.rect.bottom = HEIGHT - 95
            self.x_speed = 0


        if not keys[pygame.K_d] and not keys[pygame.K_a] and not keys[pygame.K_s]:
            self.image = alucard[alucard_stand]
            self.image.set_colorkey(magenta)
            self.rect.bottom = HEIGHT - 120


        if keys[pygame.K_u] and keys[pygame.K_s]:
            self.image = alucardKick[alucard_Kick]
            self.image.set_colorkey(magenta)
            self.rect.bottom = HEIGHT - 85
            p1LowAttack = True

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        if pygame.sprite.collide_mask(player, player2):  # Checks for collisions
            print("Collide!")
            if keys[pygame.K_d]:
                self.x_speed = 0

        self.rect.right += self.x_speed
        self.rect.bottom -= self.y_speed

def alucardAnimate():
    global alucard_run
    global alucard_back
    global alucard_Kick
    global alucard_stand
    global frames
    frames += 1
    if frames >= 2:
        alucard_run += 1
    if alucard_run >= 2:
        alucard_run = 0
        frames = 0
    alucard_back += 1
    if alucard_back >= 4:
        alucard_back = 2
    alucard_Kick += 1
    if alucard_Kick >= 2:
        alucard_Kick = 0
    alucard_stand += 1
    if alucard_stand >= 1:
        alucard_stand = 0



class Player2(pygame.sprite.Sprite):  # MONSTER CLASS CODE
    # sprite for the monster

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # initialize the sprite
        self.image = pygame.transform.flip(pygame.image.load(os.path.join(alucard_folder, "1.png")).convert(), True, False)
        self.image.set_colorkey(magenta)
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # self.rect.center= (WIDTH / 2, HEIGHT / 2)
        self.rect.center = (WIDTH - 100, HEIGHT - 175)
        self.y_speed = 0

    def update(self):
        self.rect.x += 0
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT - 100:
            self.y_speed = - 0
        if self.rect.top < 100:
            self.y_speed = 0
        if self.rect.left > WIDTH:
            self.rect.right = 0


# load graphics


# background
background = pygame.image.load(os.path.join(img_folder, "stage_1.jpg"))
background_rect = background.get_rect()


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game name")
clock = pygame.time.Clock()

# group all sprites
all_sprites = pygame.sprite.Group()

# get our player
player = Player()
all_sprites.add(player)

# get our monster
player2 = Player2()
all_sprites.add(player2)

# game loop
running = True
while running:  # keep loop running at the speed
    clock.tick(FPS)
    p1Low_Attack = False
    p1Attack = False
    p1Block = False
    p1Jump = False
    # process inputs(events)
    for event in pygame.event.get():
        # close the window
        if event.type == pygame.QUIT:
            running = False
    # update
    all_sprites.update()
    alucardAnimate()
    # draw /render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # * after drawing everything, flip the display
    pygame.display.flip()
pygame.quit()
