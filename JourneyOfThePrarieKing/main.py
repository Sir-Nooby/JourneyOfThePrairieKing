"""
Journey of the Prairie King
Kuba Calik
ICS-3U1
Submitted to Mr.Ferreira
"""
import pygame

pygame.init()

screen_height = 600
screen_width = 600

screen = pygame.display.set_mode((screen_width, screen_height))
display_screen = pygame.Surface((304, 304))

pygame.display.set_caption("Journey of the Prairie King")
pygame.display.set_icon(pygame.image.load("Contents/Interface/icon.png"))

clock = pygame.time.Clock()


#Define the Player Class
class Player():
    def __init__(self, x, y, speed):
        super().__init__()
        self.object = pygame.image.load("Contents/Sprites/player.png").convert_alpha()
        self.object_back = pygame.image.load("Contents/Sprites/player_back.png").convert_alpha()
        self.x = x
        self.y = y
        self.width = self.object.get_width()
        self.height = self.object.get_height()
        self.speed = speed
        self.direction = "forward"
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def display(self):
        if self.direction == "forward":
            display_screen.blit(self.object, (self.x, self.y))
        elif self.direction == "backward":
            display_screen.blit(self.object_back, (self.x, self.y))

    def update(self, displacement, tiles):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.x += self.speed*displacement[0]
        self.y += self.speed*displacement[1]

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

        for tile in tiles:
            if displacement[0] == 1:
                self.x = tile.left - self.width
            elif displacement[0] == -1:
                self.x = tile.right
            if displacement[1] == 1:
                self.y = tile.top - self.height
            elif displacement[1] == -1:
                self.y = tile.bottom

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

    def update(self):
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

#Render Tiles (check each row and column and extract its number to a corresponding sprite)
tiles = {
    0:pygame.image.load("Contents/Tiles/tile_dirt.png"),
    1:pygame.image.load("Contents/Tiles/tile_grass.png"),
    2:pygame.image.load("Contents/Tiles/tile_cactus.png"),
    3:pygame.image.load("Contents/Tiles/tile_planks.png"),
    4:pygame.image.load("Contents/Tiles/mulch_tile.png")
}

tilemap = [
    [2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [4, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2]
]

def render_tiles(tilemap):
    tile_rects = []
    for x, row in enumerate(tilemap):
        for y, tile in enumerate(row):
            tile_image = tiles.get(tile)
            if tile_image:
                display_screen.blit(tile_image, (y * 16, x * 16))
                if tile == 3:
                    tile_rect = pygame.Rect(y * 16, x * 16, 10, 10)
                    if tile_rect.colliderect(player.rect):
                        pygame.draw.rect(display_screen, (255, 0, 0), (y * 16, x * 16, 16, 16))
                        tile_rects.append(tile_rect)
    return tile_rects



#Create Initial Classes, Sprite Groups and Global Variables
player = Player(150, 150, 1)
bullets_group = pygame.sprite.Group()

bullet_speed = 3
gamestate = "game"
level = 0
shot_delay = 25
tile_size = 32

running = True


#Start the Game Loop
while running:
    movement = [0, 0]
    
    display_screen.fill((50, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Gather keys and relay movement
    keys = pygame.key.get_pressed()
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
        elif keys[pygame.K_SPACE]:
            print(player.x, player.y)
        shot_delay = 25
    shot_delay -= 1

    # Render the map, players and bullets
    tile_rects = render_tiles(tilemap)

    player.update(movement, tile_rects)
    
    player.display()

    bullets_group.update()

    bullets_group.draw(display_screen)
    
    
    screen.blit(pygame.transform.scale(display_screen, screen.get_size()), (0, 0))
    pygame.display.update()

    clock.tick(60)

