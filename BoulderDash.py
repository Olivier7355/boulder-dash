# Boulder Dash clone
# This module is in development
# By Olivier Charles olivier7355@gmail.com
# Released under a GNU GPL 3.0 license

import pygame, sys
from pygame.locals import *

FPS = 30 # frames per second to update the screen
WINWIDTH = 800 # width of the program's window, in pixels
WINHEIGHT = 800 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# The total width and height of each tile in pixels.
TILEWIDTH = 32
TILEHEIGHT = 32

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = BLACK
TEXTCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def terminate():
    pygame.quit()
    sys.exit()

    
def startScreen():
    """Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None."""

    # Position the title image.
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 0 # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    instructionText = ['Push the stars over the marks.',
                       'Arrow keys to move, WASD for camera control, P to change character.',
                       'Backspace to reset level, Esc to quit.',
                       'N for next level, B to go back a level.']

    # Start with drawing a blank color to the entire window:
    DISPLAYSURF.fill(BGCOLOR)

    # Draw the title image to the window:
    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

    # Position and draw the text.
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10 # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    while True: # Main loop for the start screen.
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
    pass


def runLevel(levels, levelNum):
    pass    
    
    
def main():
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, BASICFONT

     # Pygame initialization and basic set up of the global variables.
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption('Boulder Dash')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 28)
    
    # A global dict value that will contain all the Pygame
    # Surface objects returned by pygame.image.load().
    IMAGESDICT = {'uncovered goal': pygame.image.load('star_title.png'),
                  'covered goal': pygame.image.load('star_title.png'),
                  'star': pygame.image.load('star_title.png'),
                  'title': pygame.image.load('star_title.png')}
    
    # These dict values are global, and map the character that appears
    # in the level file to the Surface object it represents.
    """TILEMAPPING = {'x': IMAGESDICT['corner'],
                   '#': IMAGESDICT['wall'],
                   'o': IMAGESDICT['inside floor'],
                   ' ': IMAGESDICT['outside floor']}
    """
    startScreen() # show the title screen until the user presses a key
    
    # Read in the levels from the text file. See the readLevelsFile() for
    # details on the format of this file and how to make your own levels.
    levels = readLevelsFile('starPusherLevels.txt')
    currentLevelIndex = 0
    
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