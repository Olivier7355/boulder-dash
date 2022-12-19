import pygame
from pygame.locals import *
from pygame import mixer

class World():
    def __init__(self, data):
        self.tile_list = []
        
        sprite_sheet_image = pygame.image.load('images/sprites_sheet.png')
        static_boulder = sprite_sheet_image.subsurface(0, 0, 32, 32)
        wall = sprite_sheet_image.subsurface(32, 192, 32, 32)
        brick = sprite_sheet_image.subsurface(96, 192, 32, 32)
        rock = sprite_sheet_image.subsurface(0, 224, 32, 32)

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 0:
                    self.dirt = TheDirt(col_count * tile_size, row_count * tile_size)
                    dirt_group.add(self.dirt)
                    
                if tile == 1:
                    img = pygame.transform.scale(wall, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    pass
                    """
                    img = pygame.transform.scale(static_boulder, (32, 32))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    """
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
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 5:
                    self.diamonds = TheDiamonds(col_count * tile_size, row_count * tile_size)
                    diamonds_group.add(self.diamonds)
                if tile == 6:
                    self.sortie = TheExit(col_count * tile_size, row_count * tile_size)
                    The_exit.add(self.sortie)        
                col_count += 1
            row_count += 1

        
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
        
class TheDirt(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet_image = pygame.image.load('images/sprites_sheet.png')
        dirt = sprite_sheet_image.subsurface(32, 224, 32, 32)
        self.image = dirt
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        

class MyBoulder():
    def __init__(self, x, y):        
        self.walkink_boulder_frames =[]
        
        #load images
        sprite_sheet_image = pygame.image.load('images/sprites_sheet.png')
        self.static_boulder = sprite_sheet_image.subsurface(0, 0, 32, 32)
        for i in range(0, sprite_sheet_image.get_width(), 32):
            self.walkink_boulder_frames.append(sprite_sheet_image.subsurface(pygame.Rect(i, 160, 32, 32)))
                
        self.image = self.walkink_boulder_frames[1]
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(0, 0, 25, 25)
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
        
        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and not (key[pygame.K_DOWN] or key[pygame.K_UP]):
            dx -= 32
            self.walking_boulder_animation()          
        if key[pygame.K_RIGHT] and not (key[pygame.K_DOWN] or key[pygame.K_UP]):
            dx += 32
            self.walking_boulder_animation()
        if key[pygame.K_DOWN]:
            dy += 32
            self.walking_boulder_animation()
        if key[pygame.K_UP]:
            dy -= 32
            self.walking_boulder_animation()
        
        #check for collision with briks and wall
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0                
            elif tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
           
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

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 7

screen_width = 1000
screen_height = 1040
tile_size = 32
diamonds_collected = 0


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Boulder Dash')

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
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


diamonds_group = pygame.sprite.Group()
The_exit = pygame.sprite.Group()
dirt_group = pygame.sprite.Group()

world = World(world_data)
Boulder = MyBoulder(64,128)

#create dummy diamond for showing the score
score_diamond = TheDiamonds(tile_size // 2 , 1001)
diamonds_group.add(score_diamond)

#define colours
white = (255, 255, 255)
blue = (0, 0, 255)

#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 50)

#load sounds
#pygame.mixer.music.load('img/music.wav')
#pygame.mixer.music.play(-1, 0.0, 5000)
diamond_fx = pygame.mixer.Sound('sounds/boulder_sounds_diamond.ogg')
diamond_fx.set_volume(0.5)
dirt_walk_fx = pygame.mixer.Sound('sounds/boulder_sounds_walk_dirt.ogg')
dirt_walk_fx.set_volume(0.5)
finish_fx = pygame.mixer.Sound('sounds/boulder_sounds_finished.ogg')
finish_fx.set_volume(0.5)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

run = True
while run:

    clock.tick(fps)
    screen.fill((0,0,0))
    world.draw()
    diamonds_group.update()
    diamonds_group.draw(screen)
    The_exit.update()
    The_exit.draw(screen)
    dirt_group.draw(screen)

    Boulder.update()
    
    #Check if any of the diamond sprites collide with the player sprite
    for i, world.diamonds in enumerate(diamonds_group):
        if pygame.sprite.collide_rect(Boulder, world.diamonds):
            diamonds_group.remove(world.diamonds)
            diamonds_collected +=1
            diamond_fx.play()
    draw_text(str(diamonds_collected), font_score, white, 60, 1001)
            
    #Check if any of the dirt sprites collide with the player sprite
    for i, world.dirt in enumerate(dirt_group):
        if pygame.sprite.collide_rect(Boulder, world.dirt):
            dirt_group.remove(world.dirt)
            dirt_walk_fx.play()
            
    # Check if any of the rock bottom sprites collide with the dirt
    # if not rock should move from y+32
    
       
    #Check if any of the exit sprites collide with the player sprite whan all diamonds have been collected
    for i, world.sortie in enumerate(The_exit):
        if (pygame.sprite.collide_rect(Boulder, world.sortie)) and (diamonds_collected ==9):
            dirt_group.remove(world.sortie)
            draw_text('WELL DONE!', font, white, (screen_width // 2) - 140, screen_height // 2)
            finish_fx.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()