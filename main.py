"""
Journey of the Prairie King
Kuba Calik
ICS-3U1
Submitted to Mr.Ferreira
"""
import math
import pygame
import random

pygame.init()
pygame.mixer.init()

screen_height = 600
screen_width = 600

screen = pygame.display.set_mode((screen_width, screen_height))
display_screen = pygame.Surface((304, 304))

pygame.display.set_caption("Journey of the Prairie King")
pygame.display.set_icon(pygame.image.load("Contents/Interface/icon.png"))

clock = pygame.time.Clock()
font = pygame.font.Font("Contents/Interface/valley.ttf", 18)

#Define the Player Class
class Player():
    def __init__(self, x, y, speed):
        super().__init__()
        self.object = pygame.image.load("Contents/Sprites/player.png").convert_alpha()
        self.object_back = pygame.image.load("Contents/Sprites/player_back.png").convert_alpha()
        self.dead = pygame.image.load("Contents/Sprites/player_dead.png").convert_alpha()
        self.x = x
        self.y = y
        self.width = self.object.get_width()
        self.height = self.object.get_height()
        self.speed = speed
        self.direction = "forward"
        self.rect = pygame.Rect(self.x, self.y, 12, 12)

    def display(self):
        if self.direction == "forward":
            display_screen.blit(self.object, (self.x, self.y))
        elif self.direction == "backward":
            display_screen.blit(self.object_back, (self.x, self.y))

    def update(self, displacement, tiles):
        #Update the player's rect position and factor in collisions (x-axis)
        self.rect.x += self.speed * displacement[0]

        for tile in tiles:
            if self.rect.colliderect(tile):
                if displacement[0] == 1:
                    self.rect.right = tile.left
                elif displacement[0] == -1:
                    self.rect.left = tile.right
        
        #Update the player's rect position and factor in collisions (y-axis)
        self.rect.y += self.speed * displacement[1]

        for tile in tiles:
            if self.rect.colliderect(tile):
                if displacement[1] == 1:
                    self.rect.bottom = tile.top
                elif displacement[1] == -1:
                    self.rect.top = tile.bottom

        #After calculating their position including collisions, update their actual position
        self.x = self.rect.x
        self.y = self.rect.y
        
        if displacement[1] == -1:
            self.direction = "backward"
        else:
            self.direction = "forward"

        if self.y <= 16:
            self.y = 16
        elif self.y + self.height >= 288:
            self.y = 288 - self.height
        if self.x <= 16:
            self.x = 16
        elif self.x + self.width >= 288:
            self.x  = 288 - self.width

#Define the Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Contents/Sprites/bullet.png").convert_alpha()
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction

        self.rect = pygame.Rect(x, y, 16, 16)

    def update(self, tiles):
        if self.direction == "up":
            self.rect.y -= self.speed

        if self.direction == "up_right":
            self.rect.y -= self.speed
            self.rect.x += self.speed

        if self.direction == "up_left":
            self.rect.y -= self.speed
            self.rect.x -= self.speed

        if self.direction == "down":
            self.rect.y += self.speed

        if self.direction == "down_right":
            self.rect.y += self.speed
            self.rect.x += self.speed

        if self.direction == "down_left":
            self.rect.y += self.speed
            self.rect.x -= self.speed

        if self.direction == "right":
            self.rect.x += self.speed

        if self.direction == "left":
            self.rect.x -= self.speed

        if self.rect.x < 0 or self.rect.x > 288 or self.rect.y < 0 or self.rect.y > 288:
            self.kill()
        
        for tile in tiles:
            if self.rect.colliderect(tile):
                self.kill()

#Define the Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.object = pygame.image.load("Contents/Sprites/enemy.png")
        self.spawns = random.choice([[0, random.randint(125, 160)], [290, random.randint(125, 160)], [random.randint(125, 160), 0], [random.randint(125, 160), 290]])
        self.x = self.spawns[0]
        self.y = self.spawns[1]
        self.speed = random.uniform(0.5, 1.25)
        self.width = self.object.get_width()
        self.height = self.object.get_height()

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def display(self):
        display_screen.blit(self.object, (self.x, self.y))

    def update(self, tiles):
        distance_x = player.x - self.x
        distance_y = player.y - self.y
        self.angle = math.atan2(distance_y, distance_x)

        #Move enemy in x-axis and determine collisions
        self.x += self.speed * math.cos(self.angle)
        self.rect.x = self.x
        
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.speed * math.cos(self.angle) > 0:
                    self.rect.right = tile.left
                elif self.speed * math.cos(self.angle) < 0:
                    self.rect.left = tile.right
                self.x = self.rect.x

        #Move enemy in y-axis and determine collisions   
        self.y += self.speed * math.sin(self.angle)
        self.rect.y = self.y

        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.speed * math.sin(self.angle) > 0:
                    self.rect.bottom = tile.top
                elif self.speed * math.sin(self.angle) < 0:
                    self.rect.top = tile.bottom
                self.y = self.rect.y

#Create Floor Garbage Class
class Rubbage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Contents/Sprites/enemy_killed.png")
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def display(self):
        display_screen.blit(self.image, (self.x, self.y))

#Load sound effects and music track
game_music = pygame.mixer.music.load("Contents/Audio/game.mp3")
sound_effects = [
    pygame.mixer.Sound("Contents/Audio/crunch.wav"),
    pygame.mixer.Sound("Contents/Audio/death.mp3"),
    pygame.mixer.Sound("Contents/Audio/startup.mp3")
]

#Render Tiles (check each row and column and extract its number to a corresponding sprite)
tiles = {
    0:pygame.image.load("Contents/Tiles/tile_dirt.png"),
    1:pygame.image.load("Contents/Tiles/tile_grass.png"),
    2:pygame.image.load("Contents/Tiles/tile_cactus.png"),
    3:pygame.image.load("Contents/Tiles/tile_planks.png"),
    4:pygame.image.load("Contents/Tiles/mulch_tile.png")
}

level = 1
level_loader = open("Levels/level_" + str(level) + ".txt", "r")
tilemap =  [list(map(int, i.strip().split(','))) for i in level_loader]

def render_tiles(tilemap):
    level_loader = open("Levels/level_" + str(level) + ".txt", "r")
    tilemap =  [list(map(int, i.strip().split(','))) for i in level_loader]
    collidable_tiles = []
    for x, row in enumerate(tilemap):
        for y, tile in enumerate(row):
            tile_image = tiles.get(tile)
            if tile_image:
                display_screen.blit(tile_image, (y * 16, x * 16))
                if tile in [2, 3]:
                    tile_rect = pygame.Rect(y * 16, x * 16, 12, 12)
                    collidable_tiles.append(tile_rect)
    return collidable_tiles

#Create User Events, Sprite Groups and Global Variables

bullets_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
rubbage_group = pygame.sprite.Group()

bullet_speed = 3
gamestate = "title"
shot_delay = 25
tile_size = 32
wave_count = 32
universal_waves = 32

SPAWNEVENT = pygame.USEREVENT + 0
pygame.time.set_timer(SPAWNEVENT, 1500)

running = True

#Create Basic Menus
def Title_Screen():
    screen.fill((0, 0, 0))
    title_card = pygame.image.load("Contents/Interface/title.png").convert_alpha()
    credits = font.render("Made by Kuba Calik!", True, (255, 255, 255))
    start = pygame.font.Font("Contents/Interface/valley.ttf", 14).render("Press Enter to Start!", True, (255, 255, 255))
    display_screen.blit(title_card, (105, 100))
    display_screen.blit(credits, (90, 275))
    display_screen.blit(start, (95, 175))
    screen.blit(pygame.transform.scale(display_screen, (600, 600)), (0, 0))
    pygame.display.update()

def Level_Load():
    screen.fill((0, 0, 0))
    pygame.display.update()

def Tutorial():
    controls = pygame.image.load("Contents/Interface/controls.png").convert_alpha()
    display_screen.blit(controls, (115, 175))
    screen.blit(pygame.transform.scale(display_screen, (600, 600)), (0, 0))
    pygame.display.update()

def Game_Over():
    gameover = pygame.image.load("Contents/Sprites/game_over.png").convert_alpha()
    display_screen.blit(gameover, (110, 115))
    screen.blit(pygame.transform.scale(display_screen, (600, 600)), (0, 0))
    pygame.display.update()
    
sound_effects[2].play()
#Start the Game Loop
while running:
    movement = [0, 0]
    
    display_screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWNEVENT and gamestate == "game":
            for i in range(level + 1):
                enemies_group.add(Enemy())
            wave_count -= 1

        #Close if user hits escape
        if keys[pygame.K_ESCAPE]:
            pygame.quit()

    #Game State Checking
    if gamestate == "title":
        Title_Screen()
        if keys[pygame.K_RETURN]:
            gamestate = "game"
            player = Player(145, 115, 1)  
    elif gamestate == "game":
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
              
        #Gather keys and relay movement
        if keys[pygame.K_w]:
            movement[1] = -1
        if keys[pygame.K_s]:
            movement[1] = 1
        if keys[pygame.K_d]:
            movement[0] = 1
        if keys[pygame.K_a]:
            movement[0] = -1

        #Relay bullet direction
        if shot_delay <= 0:
            if keys[pygame.K_UP]:
                if keys[pygame.K_RIGHT]:
                    bullets_group.add(Bullet(player.x, player.y, bullet_speed-1, "up_right"))
                elif keys[pygame.K_LEFT]:
                    bullets_group.add(Bullet(player.x, player.y, bullet_speed-1, "up_left"))
                else:
                    bullets_group.add(Bullet(player.x, player.y, bullet_speed, "up"))

            elif keys[pygame.K_DOWN]:
                if keys[pygame.K_RIGHT]:
                    bullets_group.add(Bullet(player.x, player.y, bullet_speed-1, "down_right"))
                elif keys[pygame.K_LEFT]:
                    bullets_group.add(Bullet(player.x, player.y, bullet_speed-1, "down_left"))
                else:
                    bullets_group.add(Bullet(player.x, player.y, bullet_speed, "down"))

            elif keys[pygame.K_RIGHT]:
                bullets_group.add(Bullet(player.x, player.y, bullet_speed, "right"))
            elif keys[pygame.K_LEFT]:
                bullets_group.add(Bullet(player.x, player.y, bullet_speed, "left"))
            shot_delay = 25
        shot_delay -= 1

        # Render the map, player, bullets and rubbage
        tile_rects = render_tiles(tilemap)

        rubbage_group.draw(display_screen)

        player.update(movement, tile_rects)

        player.display()
        
        bullets_group.update(tile_rects)

        bullets_group.draw(display_screen)

        #Update each enemy
        for enemy in enemies_group:
            enemy.update(tile_rects)
            enemy.display()
        #If a collision occurs, clean the game and reset the player
            if enemy.rect.colliderect(player.rect):
                pygame.mixer.music.stop()
                sound_effects[1].play()
                level = 1
                Game_Over()
                wave_count = universal_waves
                for i in [enemies_group, rubbage_group]:
                    for v in i:
                        v.kill()
                gamestate = "title"
                pygame.time.delay(3000)

        #Kill enemies that have been shot, remove them
            if pygame.sprite.spritecollide(enemy, bullets_group, True):
                rubbage_group.add(Rubbage(enemy.x, enemy.y))
                sound_effects[0].play()
                enemy.kill()
        print(wave_count)

        #Detects the current wave number and check if player has won
        if wave_count >= 31:
            Tutorial()
        if wave_count == 0:
            if level != 3:
                wave_count = universal_waves
                level += 1
            else:
                pygame.quit() #Add a congratulatory message here
            for i in [enemies_group, rubbage_group]:
                for v in i:
                    v.kill()
            gamestate = "title"

        screen.blit(pygame.transform.scale(display_screen, screen.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(60)