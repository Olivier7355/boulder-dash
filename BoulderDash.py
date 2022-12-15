import pygame
from pygame.locals import *

class World():
    def __init__(self, data):
        self.tile_list = []
        
        sprite_sheet_image = pygame.image.load('images/sprites_sheet.png')
        static_boulder = sprite_sheet_image.subsurface(0, 0, 32, 32)
        wall = sprite_sheet_image.subsurface(32, 192, 32, 32)
        brick = sprite_sheet_image.subsurface(96, 192, 32, 32)
        dirt = sprite_sheet_image.subsurface(32, 224, 32, 32)
        rock = sprite_sheet_image.subsurface(0, 224, 32, 32)

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 0:
                    img = pygame.transform.scale(dirt, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 1:
                    img = pygame.transform.scale(wall, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(static_boulder, (32, 32))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(rock, (32, 32))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(brick, (32, 32))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect, '4')
                    self.tile_list.append(tile)
                if tile == 5:
                    blob = TheDiamonds(col_count * tile_size, row_count * tile_size)
                    blob_group.add(blob)
                if tile == 6:
                    blob = TheExit(col_count * tile_size, row_count * tile_size)
                    The_exit.add(blob)        
                col_count += 1
            row_count += 1
        # print(self.tile_list)
        # (<Surface(32x32x24 SW)>, <rect(96, 352, 32, 32)>, '4')
        
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            

class TheExit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.exit_frames = []
        self.index = 0
        self.counter = 0
        #load images
        sprite_sheet_image = pygame.image.load('images/sprites_sheet.png')
        for i in range(0, sprite_sheet_image.get_width(), 32):
            self.exit_frames.append(sprite_sheet_image.subsurface(pygame.Rect(i, 288, 32, 32)))
        
        self.image = self.exit_frames[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x+16, y+16]
        
    def update(self):
        
        #handle the animation
        self.counter += 1
        flap_cooldown = 3
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.exit_frames):
                self.index = 0
        self.image = self.exit_frames[self.index]
                       
            
class TheDiamonds(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.diamond_frames = []
        self.index = 0
        self.counter = 0
        #load images
        sprite_sheet_image = pygame.image.load('images/sprites_sheet.png')
        for i in range(0, sprite_sheet_image.get_width(), 32):
            self.diamond_frames.append(sprite_sheet_image.subsurface(pygame.Rect(i, 320, 32, 32)))
        
        self.image = self.diamond_frames[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x+16, y+16]
        
    def update(self):
        
        #handle the animation
        self.counter += 1
        flap_cooldown = 2
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.diamond_frames):
                self.index = 0
        self.image = self.diamond_frames[self.index]
        

class MyBoulder():
    def __init__(self, x, y):
        #img = pygame.image.load('imgages/sprites_sheet.png')
        #self.lemmingsStop = pygame.image.load('img/lemmings-stop.png')
        #self.lemStop = pygame.transform.scale(self.lemmingsStop, (50, 70))
        
        
        self.walkink_boulder_frames =[]
        #load images
        sprite_sheet_image = pygame.image.load('images/sprites_sheet.png')
        self.static_boulder = sprite_sheet_image.subsurface(0, 0, 32, 32)
        for i in range(0, sprite_sheet_image.get_width(), 32):
            self.walkink_boulder_frames.append(sprite_sheet_image.subsurface(pygame.Rect(i, 160, 32, 32)))
                
        self.image = self.walkink_boulder_frames[1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        
        self.animation_steps = 8
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 10
        self.frame = 0

    def walking_boulder_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.walkink_boulder_frames) :
                self.frame = 0
       

    def update(self):
        dx = 0
        dy = 0
        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= 3
            self.walking_boulder_animation()
            
        if key[pygame.K_RIGHT]:
            dx += 3
            self.walking_boulder_animation()
  
        if key[pygame.K_DOWN]:
            dy += 3
            self.walking_boulder_animation()
        if key[pygame.K_UP]:
            dy -= 3
            self.walking_boulder_animation()
        
        """
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0
                dx += 3
                
            elif tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
        """        

        self.rect.x += dx
        self.rect.y += dy

        # display Boulder
        if (key[pygame.K_LEFT]) : 
            screen.blit(pygame.transform.flip(self.walkink_boulder_frames[self.frame], True, False), self.rect)
        elif (key[pygame.K_RIGHT]) :
            screen.blit(self.walkink_boulder_frames[self.frame], self.rect)
        elif (key[pygame.K_DOWN]) :
            screen.blit(self.walkink_boulder_frames[self.frame], self.rect)
        elif (key[pygame.K_UP]) :
            screen.blit(self.walkink_boulder_frames[self.frame], self.rect)
        else :
            screen.blit(self.static_boulder, self.rect)
            pass



        #pygame.draw.rect(screen, (255,255,255), self.rect, 2)


pygame.init()
clock = pygame.time.Clock()
fps = 30

screen_width = 1000
screen_height = 1000
tile_size = 32

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Boulder Dash')

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


blob_group = pygame.sprite.Group()
The_exit = pygame.sprite.Group()
world = World(world_data)
Boulder = MyBoulder(100,100)

run = True
while run:

    clock.tick(fps)
    screen.fill((0,0,0))
    world.draw()
    blob_group.update()
    blob_group.draw(screen)
    The_exit.update()
    The_exit.draw(screen)

    Boulder.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()