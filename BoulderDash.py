#! /usr/bin/env python3

# Boulder Dash clone
# This module is in development
# By Olivier Charles olivier7355@gmail.com
# Released under a GNU GPL 3.0 license

import pygame, sys, os
from pygame.locals import *
from pygame import mixer
import datetime
import time

FPS = 30 # frames per second to update the screen
WINWIDTH =1280 # width of the program's window, in pixels
WINHEIGHT = 760 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
COUNTER = 150

# The total width and height of each tile in pixels.
TILEWIDTH = 32
TILEHEIGHT = 32

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 51)
BGCOLOR = BLACK
TEXTCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


# Load the sounds
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init() 
diamond_fx = pygame.mixer.Sound('sounds/boulder_sounds_diamond.ogg')
diamond_fx.set_volume(0.5)
collectDiamond_fx = pygame.mixer.Sound('sounds/boulder_sounds_collectdiamond.ogg')
collectDiamond_fx.set_volume(0.5)
dirt_walk_fx = pygame.mixer.Sound('sounds/boulder_sounds_walk_dirt.ogg')
dirt_walk_fx.set_volume(0.5)
fallingRock_fx = pygame.mixer.Sound('sounds/boulder_sounds_falling-rock.ogg')
fallingRock_fx.set_volume(0.5)
crack_fx = pygame.mixer.Sound('sounds/boulder_sounds_crack.ogg')
crack_fx.set_volume(0.5)
finish_fx = pygame.mixer.Sound('sounds/boulder_sounds_finished.ogg')
finish_fx.set_volume(0.5)
explosion_fx = pygame.mixer.Sound('sounds/boulder_sounds_explosion.ogg')
explosion_fx.set_volume(0.5)


def terminate():
    pygame.quit()
    sys.exit()
    
    
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    DISPLAYSURF.blit(img, (x, y))

    
def startScreen():
    """Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None."""
    
    #load sounds
    title_intro_fx = pygame.mixer.Sound('sounds/boulder_sounds_intro.ogg')
    title_intro_fx.set_volume(0.2)

    # Position the title image.
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 150 # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    instructionText = ['Pres any key to start']

    # Start with drawing a blank color to the entire window:
    DISPLAYSURF.fill(BGCOLOR)

    # Draw the title image to the window:
    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

    # Position and draw the text.
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 70 # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    while True: # Main loop for the start screen.
        title_intro_fx.play()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return # user has pressed a key, so return.

        # Display the DISPLAYSURF contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()
        
        

def readLevelsFile(filename):
    assert os.path.exists(filename), 'Cannot find the level file: %s' % (filename)
    mapFile = open(filename, 'r')
    # Each level must end with a blank line
    content = mapFile.readlines() + ['\r\n']
    mapFile.close()
    
    levels = [] # Will contain a list of level objects.
    levelNum = 0
    mapTextLines = [] # contains the lines for a single level's map.
    mapObj = [] # the map object made from the data in mapTextLines
    for lineNum in range(len(content)):
        # Process each line that was in the level file.
        line = content[lineNum].rstrip('\r\n')

        if ';' in line:
            # Ignore the ; lines, they're comments in the level file.
            line = line[:line.find(';')]

        if line != '':
            # This line is part of the map.
            mapTextLines.append(line)
        elif line == '' and len(mapTextLines) > 0:
            # A blank line indicates the end of a level's map in the file.
            # Convert the text in mapTextLines into a level object.

            # Find the longest row in the map.
            maxWidth = -1
            for i in range(len(mapTextLines)):
                if len(mapTextLines[i]) > maxWidth:
                    maxWidth = len(mapTextLines[i])
            # Add spaces to the ends of the shorter rows. This
            # ensures the map will be rectangular.
            for i in range(len(mapTextLines)):
                mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))

            # Convert mapTextLines to a map object.
            for x in range(len(mapTextLines[0])):
                mapObj.append([])
            for y in range(len(mapTextLines)):
                for x in range(maxWidth):
                    mapObj[x].append(mapTextLines[y][x])

            # Loop through the spaces in the map and find the @, ., and $
            # characters for the starting game state.
            startx = None # The x and y for the player's starting position
            starty = None
            exitx = None # The x and y for the exit position
            exity = None
            rocks = [] # list of (x, y) tuples for each rock.
            diamonds = [] # list of (x, y) for each diamond.
            for x in range(maxWidth):
                for y in range(len(mapObj[x])):
                    if mapObj[x][y] in ('@'):
                        # '@' is player
                        startx = x
                        starty = y
                    if mapObj[x][y] in ('o'):
                        # 'o' is rock
                        rocks.append((x, y))
                    if mapObj[x][y] in ('d'):
                        # 'd' is diamond
                        diamonds.append((x, y))
                    if mapObj[x][y] in ('e'):
                        # 'e' is the exit
                        doorx = x
                        doory = y

            # Create level object and starting game state object.
            gameStateObj = {'player': (startx, starty),
                            'door': (doorx, doory),
                            'stepCounter': 0,
                            'rocks': rocks,
                            'diamonds': diamonds}
            levelObj = {'width': maxWidth,
                        'height': len(mapObj),
                        'mapObj': mapObj,
                        'startState': gameStateObj}

            levels.append(levelObj)

            # Reset the variables for reading the next map.
            mapTextLines = []
            mapObj = []
            gameStateObj = {}
            levelNum += 1
            print(levels)
    return levels


def drawMap(mapObj, gameStateObj):
    global diamonds_group, diamondsIns
    # Draws the map to a Surface object, including the player. This function does not call pygame.display.update().
    mapSurfWidth = len(mapObj) * TILEWIDTH
    mapSurfHeight = (len(mapObj[0])) * TILEHEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    mapSurf.fill(BGCOLOR) # start with a blank color on the surface.
    
    
    # Draw the tile sprites onto this surface.
    for x in range(len(mapObj)):
        for y in range(len(mapObj[x])):
            spaceRect = pygame.Rect((x * TILEWIDTH, y * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))
            #print(mapObj[x][y], end=' ')
            if (mapObj[x][y] in TILEMAPPING) and (mapObj[x][y] != 'd'):
                baseTile = TILEMAPPING[mapObj[x][y]]
                
            if mapObj[x][y] == 'd' :
                #diamondsIns = TheDiamonds(x*32,y*32) # Create an instance of the animated diamonds
                #diamonds_group.add(diamondsIns) # Add the diamond to the sprite group
                baseTile = TILEMAPPING[mapObj[x][y]]
                
                
            # First draw the base ground/wall tile.
            mapSurf.blit(baseTile, spaceRect)

            # Last draw the player on the board.
            if (x, y) == gameStateObj['player']:
                # Note: The value "currentImage" refers
                # to a key in "PLAYERIMAGES" which has the
                # specific player image we want to show.
                mapSurf.blit(PLAYERIMAGES[currentImage], spaceRect)

    return mapSurf


def isWallorBrick(mapObj, x, y):
    """Returns True if the (x, y) position on
    the map is a wall or a brick, otherwise return False."""
    if x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return False # x and y aren't actually on the map.
    elif mapObj[x][y] in ('#', '='):
        return True # wall or brick is blocking
    return False
   
    
def RockisBlocked (mapObj, gameStateObj, x, y):
    """Returns True if the (x, y) position on the map is
    blocked by a dirt, a wall, a brick or a diamond otherwise return False."""

    if mapObj[x][y] in ('#', '=', 'x', 'o', 'd'):
        return True

    elif x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return True # x and y aren't actually on the map.

    #elif (x, y) in gameStateObj['rocks']:
    #    return True # a rock is blocking

    return False

def makeMove(mapObj, gameStateObj, playerMoveTo):
    global diamondsCatched, diamonds_group, diamondsIns
    """Given a map and game state object, see if it is possible for the
    player to make the given move. If it is, then change the player's
    position. If not, do nothing.

    Returns True if the player moved, otherwise False."""

    # Make sure the player can move in the direction they want.
    playerx, playery = gameStateObj['player']
   
    rocks = gameStateObj['rocks']
    diamonds = gameStateObj['diamonds']

    # The code for handling each of the directions is so similar aside
    # from adding or subtracting 1 to the x/y coordinates. We can
    # simplify it by using the xOffset and yOffset variables.
    if playerMoveTo == UP:
        xOffset = 0
        yOffset = -1
    elif playerMoveTo == RIGHT:
        xOffset = 1
        yOffset = 0
    elif playerMoveTo == DOWN:
        xOffset = 0
        yOffset = 1
    elif playerMoveTo == LEFT:
        xOffset = -1
        yOffset = 0
        
    # See if the player can move in that direction.
    if isWallorBrick(mapObj, playerx + xOffset, playery + yOffset):
        return False
    else:   
        if (playerx + xOffset, playery + yOffset) in rocks:
            # There is a rock in the way, see if the player can push it.
            if not RockisBlocked(mapObj, gameStateObj, playerx + (xOffset*2), playery + (yOffset*2)):
                # Move the rock.
                ind = rocks.index((playerx + xOffset, playery + yOffset))
                rocks[ind] = (rocks[ind][0] + xOffset, rocks[ind][1] + yOffset)
                mapObj[playerx+ (xOffset*2)][playery] ='o'
                fallingRock_fx.play()
                                    
            else:
                return False
            
        # There is a diamond in the way    
        if (playerx + xOffset, playery + yOffset) in diamonds:
            mapObj[playerx + xOffset][playery] ='s'
            diamondsCatched += 1
            print(diamondsCatched)
            collectDiamond_fx.play()
            
            # Delete the diamond from the list of diamonds in the curent level.
            ind = diamonds.index((playerx + xOffset, playery + yOffset))
            del diamonds[ind]
            
            if not diamonds :
                crack_fx.play()
                showExit = True 
            
         
        # Move the player upwards.
        gameStateObj['player'] = (playerx + xOffset, playery + yOffset)
        dirt_walk_fx.play()
        
        # Clean the space at the previous player position
        mapObj[playerx][playery] ='s'
        return True
 
def isLevelFinished(levelObj, gameStateObj):
    
    # Returns True if all the diamonds have been collected and Rockford has reach the exit.
    diamonds = gameStateObj['diamonds']
    Rockford = gameStateObj['player']
    door = gameStateObj['door']
    
    if not diamonds and (Rockford[0] == door[0]) and (Rockford[1] == door[1]) :
        print('Game completed !!!')
        finish_fx.play() 
        return True
    
    return False 
 
def rockHasToFall(mapObj, gameStateObj):
    global deadRockford
    rocks = gameStateObj['rocks']
    diamonds = gameStateObj['diamonds']
    Rockford = gameStateObj['player']
    elementList = [rocks, diamonds]
    rockOrDiamonds =['o','d'] 
    
    for element in elementList :
        for x, y in element :
            
            # A rock or a diamond falls on Rockford
            if ((mapObj[x][y+1] == 's') and  (x == Rockford[0] and y+2 == Rockford[1])):
                print('You are dead !')
                
                # Display the explosion
                mapObj[x][y] = 's'
                for j in range(1,4) :
                    mapObj[x][y+j] = 'b'
                    mapObj[x-1][y+j] = 'b'
                    mapObj[x+1][y+j] = 'b'
            
                explosion_fx.play()
                deadRockford = True
                return True
            elif ((mapObj[x][y+1] == 'o') and (mapObj[x-1][y] == 's') and (mapObj[x-1][y+1] == 's') and (x-1 == Rockford[0] and y+2 == Rockford[1])):
                print('You are dead !')
                
                # Display the explosion
                mapObj[x][y] = 's'
                for j in range(1,4) :
                    mapObj[x-1][y+j] = 'b'
                    mapObj[x-2][y+j] = 'b'
                    mapObj[x][y+j] = 'b'
            
                explosion_fx.play()
                deadRockford = True
                return True
                                      
                        
            # The rock move to y+1 if this space is empty 
            if mapObj[x][y+1] == 's' :
                mapObj[x][y] = 's'
                if element == rocks : # update the rocks position in the list of rocks
                    mapObj[x][y+1] = 'o'
                    fallingRock_fx.play()
                elif element == diamonds : # update the diamond position in the list of diamonds
                    mapObj[x][y+1] = 'd' 
                    diamond_fx.play()
                
                ind = element.index((x, y))
                element[ind] = (x,y+1)
                return True
            
            # The rock move to x-1 and y+1 if this space is empty and a rock or a diamond is at x,y+1
            if (mapObj[x-1][y+1] == 's') and (mapObj[x][y+1] in rockOrDiamonds) and (mapObj[x-1][y] == 's') and (x-1 != Rockford[0] and y+1 != Rockford[1]):
                mapObj[x][y] = 's'
                if element == rocks : # update the rocks position in the list of rocks
                    mapObj[x-1][y+1] = 'o'
                    fallingRock_fx.play()    
                    
                elif element == diamonds : # update the diamond position in the list of diamonds
                    mapObj[x-1][y+1] = 'd'
                    diamond_fx.play()    
                         
                ind = element.index((x, y))
                element[ind] = (x-1,y+1)
                return True
            
            # The rock move to x+1 and y+1 if this space is empty and rocks or diamonds are at x,y+1 and x-1,y+1
            if (mapObj[x+1][y+1] == 's') and (mapObj[x][y+1] in rockOrDiamonds) and (mapObj[x-1][y+1] in rockOrDiamonds) and (mapObj[x-1][y] == 's') and (x-1 != Rockford[0] and y+1 != Rockford[1]):
                mapObj[x][y] = 's'
                if element == rocks : # update the rocks position in the list of rocks
                    mapObj[x+1][y+1] = 'o'
                    fallingRock_fx.play() 
                
                elif element == diamonds : # update the diamond position in the list of diamonds
                    mapObj[x+1][y+1] = 'd'
                    diamond_fx.play() 
                
                ind = element.index((x, y))
                element[ind] = (x+1,y+1)
                return True
            
            # The rock move to x+1,y+1 if this space is empty a rock or diamond is at x,y+1 and not a space at x-1,y
            if (mapObj[x+1][y+1] == 's') and (mapObj[x][y+1] in rockOrDiamonds) and (mapObj[x-1][y] != 's') and (mapObj[x+1][y] == 's'):
                mapObj[x][y] = 's'
                if element == rocks : # update the rocks position in the list of rocks
                    mapObj[x+1][y+1] = 'o'
                    fallingRock_fx.play() 
                
                elif element == diamonds : # update the diamond position in the list of diamonds
                    mapObj[x+1][y+1] = 'd'
                    diamond_fx.play()                    
                    
                ind = element.index((x, y))
                element[ind] = (x+1,y+1)
                return True  
            
    return False
 
def updateScoreBoard(gameStateObj):
    global old_seconds, COUNTER, currentLevelIndex, lives

    diamonds = gameStateObj['diamonds']
    font_score = pygame.font.SysFont('Bauhaus 93', 60)
    sprite_sheet_image = pygame.image.load('images/sprites_sheet.png')
    
    # Display the level number
    draw_text(f'Level {currentLevelIndex+1}', font_score, WHITE, 10, 710)
      
    # Display the number of diamonds collected
    diamond = sprite_sheet_image.subsurface(0, 320, 32, 32)
    rect = diamond.get_rect()
    rect.x = 600
    rect.y = 712
    DISPLAYSURF.blit(diamond, rect)
    
    d_number = f"{len(diamonds):02d}"
    draw_text(str(d_number), font_score, YELLOW, 640, 710)
    
    # Display the number of Rockford lives
    static_Rockford = sprite_sheet_image.subsurface(0, 0, 32, 32)
    rect = static_Rockford.get_rect()
    rect.x = 820
    rect.y = 710
    DISPLAYSURF.blit(static_Rockford, rect)
    
    draw_text(str(lives), font_score, WHITE, 860, 710)
    
    # Display the countdown counter
    current_time = datetime.datetime.now()
    current_seconds = current_time.second
    
    if (old_seconds != current_seconds) :
        old_seconds = current_seconds
        COUNTER -= 1
    draw_text(str(COUNTER), font_score, WHITE, 1200, 710)
    

    
        
        
def runLevel(levels, levelNum):
    global currentImage, diamondsCatched, COUNTER, lives, deadRockford, diamonds_group
    COUNTER = 150
    levelObj = levels[levelNum]
    mapObj = levelObj['mapObj']
    gameStateObj = levelObj['startState']
    mapNeedsRedraw = True # set to True to call drawMap()
    levelIsComplete = False
    last_update = pygame.time.get_ticks()
    animation_cooldown = 50
    diamondsCatched = 0
    deadRockford = False
    diamonds_group = pygame.sprite.Group()
    
    
    while True: # main game loop
        # Reset these variables:
        playerMoveTo = None
        keyPressed = False
        
        
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                # Player clicked the "X" at the corner of the window.
                terminate()
                  
            elif event.type == KEYDOWN:
                # Handle key presses
                keyPressed = True
                if event.key == K_LEFT:
                    playerMoveTo = LEFT
                elif event.key == K_RIGHT:
                    playerMoveTo = RIGHT
                elif event.key == K_UP:
                    playerMoveTo = UP
                elif event.key == K_DOWN:
                    playerMoveTo = DOWN
                
        if playerMoveTo != None and not levelIsComplete:
            # If the player pushed a key to move, make the move
            # (if possible) and push any stars that are pushable.
            moved = makeMove(mapObj, gameStateObj, playerMoveTo)

            if moved:
                # increment the step counter.
                gameStateObj['stepCounter'] += 1
                mapNeedsRedraw = True
                
            if isLevelFinished(levelObj, gameStateObj):
                # level is solved, we should show the "Solved!" image.
                levelIsComplete = True
                keyPressed = False
        
        # Create a cool down period for the animations of the falling rocks        
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            last_update = current_time
                    
            # Check if there is a space below a rock. In that case, the rock has to fall.
            spaceBelowRock = rockHasToFall(mapObj, gameStateObj)   
            if spaceBelowRock:
                mapNeedsRedraw = True
                
        # Manage the aliens' moves
        
                                
        DISPLAYSURF.fill(BGCOLOR)
        
        updateScoreBoard(gameStateObj)
          
        if mapNeedsRedraw:
            mapSurf = drawMap(mapObj, gameStateObj)
            mapNeedsRedraw = False
        
        
        mapSurfRect = mapSurf.get_rect()
        # Draw mapSurf to the DISPLAYSURF Surface object.
        DISPLAYSURF.blit(mapSurf, mapSurfRect)
        
        
        if levelIsComplete:
            # is solved, show the "Solved!" image until the player
            # has pressed a key.
            time.sleep(4)
            return 'solved'
        
        # Restart the level and substract a Rockford live if the counter reaches 0
        if (COUNTER == 0) :
            lives -=1
            finish_fx.play()
            time.sleep(4) 
            return 'counter0'
                       
        pygame.display.update() # draw DISPLAYSURF to the screen.
        
        # Restart the level if Rockford has been crushed
        if deadRockford :
            lives -=1
            time.sleep(4) 
            return 'deadRockford'
        
        FPSCLOCK.tick()

        
    
    
def main():
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, BASICFONT, PLAYERIMAGES, currentImage, diamondsCatched, old_seconds
    global currentLevelIndex, lives

     # Pygame initialization and basic set up of the global variables.
   
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    currentImage = 0
    old_seconds = 70
    lives = 5

    pygame.display.set_caption('Boulder Dash')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 38)
       
    # Load Pygame Surface objects
    sprite_sheet_image = pygame.image.load('images/sprites_sheet.png')
    static_Rockford = sprite_sheet_image.subsurface(0, 0, 32, 32)
    wall = sprite_sheet_image.subsurface(32, 192, 32, 32)
    brick = sprite_sheet_image.subsurface(96, 192, 32, 32)
    rock = sprite_sheet_image.subsurface(0, 224, 32, 32)
    dirt = sprite_sheet_image.subsurface(32, 224, 32, 32)
    space = sprite_sheet_image.subsurface(0, 192, 32, 32)
    diamond = sprite_sheet_image.subsurface(0, 320, 32, 32)
    alien = sprite_sheet_image.subsurface(224, 288, 32, 32)
    exit = sprite_sheet_image.subsurface(64, 192, 32, 32)
    explosion = sprite_sheet_image.subsurface(96, 0, 32, 32)
    intro_title = pygame.image.load('star_title.png')
    
    # A global dict value that will contain all the Pygame
    # Surface objects returned by pygame.image.load().
    IMAGESDICT = {'Rockford': static_Rockford,
                  'wall': wall,
                  'brick': brick,
                  'rock': rock,
                  'dirt': dirt,
                  'space': space,
                  'diamond': diamond,
                  'exit': exit,
                  'explosion': explosion,
                  'alien' : alien,
                  'title': intro_title}
    
    # These dict values are global, and map the character that appears
    # in the level file to the Surface object it represents.
    TILEMAPPING = {'x': IMAGESDICT['dirt'],
                   '#': IMAGESDICT['wall'],
                   '=': IMAGESDICT['brick'],
                   's': IMAGESDICT['space'],
                   'd': IMAGESDICT['diamond'],
                   'e': IMAGESDICT['exit'],
                   'b': IMAGESDICT['explosion'],
                   'a': IMAGESDICT['alien'],
                   'o': IMAGESDICT['rock']}
    
    PLAYERIMAGES = [IMAGESDICT['Rockford']]
    
    #startScreen() # show the title screen until the user presses a key
    
    # Read in the levels from the text file. See the readLevelsFile() for
    # details on the format of this file and how to make your own levels.
    levels = readLevelsFile('BoulderLevels.txt')
    currentLevelIndex = 1
        
    # The main game loop. This loop runs a single level, when the user
    # finishes that level, the next/previous level is loaded.
    while True: # main game loop
        # Run the level to actually start playing the game:
        result = runLevel(levels, currentLevelIndex)

        if result in ('solved', 'next'):
            # Go to the next level.
            currentLevelIndex += 1
            if currentLevelIndex >= len(levels):
                # If there are no more levels, go back to the first one.
                currentLevelIndex = 0
                levels = readLevelsFile('BoulderLevels.txt')
                print('restart first level')
        elif result in ('counter0', 'deadRockford'):
            levels = readLevelsFile('BoulderLevels.txt')
            
        elif result == 'back':
            # Go to the previous level.
            currentLevelIndex -= 1
            if currentLevelIndex < 0:
                # If there are no previous levels, go to the last one.
                currentLevelIndex = len(levels)-1
        elif result == 'reset':
            pass # Do nothing. Loop re-calls runLevel() to reset the level
     

if __name__ == '__main__':
    main()