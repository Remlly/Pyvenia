#
# Developed by Remon Verbraak
# Date: 7-11-2025
#   


#%%imports
import pygame
import pymunk
from PhysicsHandler import *
from debug_drawer import debugscreen
from Player import *

#%%initialize
pygame.init()
pygame.font.init()

#%%Helper variables
screenx,screeny = 800,600   #screen dimensions
cx,cy = screenx/2,screeny/2 #screen center
center = (cx,cy)
dummy = 38

#Set up the game window
screen = pygame.display.set_mode((screenx, screeny))
screen.fill((255,255,255))
pygame.display.flip()
pygame.display.set_caption("An undefined platformer")


clock = pygame.time.Clock()   # Pygame clock for FPS limiting
space = pymunk.Space()        # The 'space' where pymunk simulates
space.gravity = 0   ,981      # Set gravity
space.damping = 1             # Global dampening variable from 0 (full) to 1 (none)
fps = 50                      # Max fps

debug_loc = (10*screenx/12, screeny/6)
debug_size  = (2*screenx/12, 2*screeny/3)
debug = debugscreen(debug_loc,debug_size)


img = [

    "       ",

    " xxx   ",

    "  xx   ",
 
    "  xx   ",

    "  xx   ",

    "  xxxx ",

    "       ",
]


#%% Game loop
def main():
    running = True
    PhysicsManager = Manager()

    ball = Object(center, 10)
    ball.add_shape(pymunk.Circle(ball.body,10))

    floor = Object((0,cy+200),10,body_type=pymunk.Body.STATIC)
    floor.add_shape(pymunk.Segment(floor.body, (0,0),(screenx,0),10))

    shape1 = Object((cx+100,cy), 10)
    shape1.autogeometry(img)

    cam = camera(ball,PhysicsManager,center)

    while running: 
        PhysicsManager.add_objects(space)

        #Get mouse information 
        mouse_pos = pygame.mouse.get_pos() #Get mouse position
        keys = pygame.key.get_pressed()

        debug.set_text('fps',clock.get_fps())
        debug.set_text('mouse pos', mouse_pos)


        
        #%%
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Quit Pygame
                pygame.quit()
    

        screen.fill((255,255,255))
        PhysicsManager.debug_draw(screen,space)
        cam.update(ball, space)
        #PhysicsManager.Translate(space,(1,0))

        pygame.display.update()
        clock.tick(fps)
        space.step(1/fps)
      
if __name__ == "__main__":
    main()


# %%
