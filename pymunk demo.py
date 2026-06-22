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
import numpy as np
import Grid

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

Jump_allowed = True
def on_ground(arbiter : pymunk.Arbiter, space, data):
    #print(arbiter.normal)
    global Jump_allowed
    if arbiter.normal > (0,0):
        Jump_allowed = True



handler = space.on_collision(1,2,post_solve=on_ground)


def Player_controller(key, body : pymunk.Body, type):
        """Prototype"""
        global Jump_allowed
        
        if key == pygame.K_RIGHT:
            body.velocity = (200,body.velocity.y)
        elif key == pygame.K_LEFT: 
            body.velocity = (-200,body.velocity.y)
        elif key == pygame.K_SPACE and Jump_allowed:
            body.velocity = (body.velocity.x,-500) 
     
            print('jumping')
            Jump_allowed = False
        if (key == pygame.K_LEFT or key == pygame.K_RIGHT) and type:
            print(key)
            body.velocity = (body.velocity.x,body.velocity.y) 


pilaar_img = pygame.image.load("textures\pilaar.png")
doos_img = pygame.image.load("textures\doos.png")
sirius = pygame.image.load("textures\Sirius.png")

#alpha_array = pygame.surfarray.pixels_alpha(pilaar_img)

#np.savetxt("alpha_values.csv", alpha_array, fmt="%d", delimiter=",")
#%% Game loop

def grid2obj(map):
    for x in range(map.statics.get_width()):
        for y in range(map.statics.get_height()):
            data = map.statics.get_at((x,y))
            if data == (255,255,255):
                floor = Object((x*32,y*32),10,body_type=pymunk.Body.STATIC)
                floor.add_shape(pymunk.Poly(floor.body,[(0,0),(32,0),(32,32),(0,32)]),2,10)
            if data == (255,00,00):
                obj = Object((x*32,y*32),80,body_type=pymunk.Body.DYNAMIC)
                obj.add_shape(pymunk.Poly(obj.body,[(0,0),(32,0),(32,32),(0,32)]),2,10)
                obj.shape.friction = 0.9


def main():
    running = True
    PhysicsManager = Manager()

    ball = Object((screenx/2,-screeny), 80)
    ball.add_shape(pymunk.Circle(ball.body,10), 1,80)

    #sirius_torso = Object((screenx/2,-screeny+1200),80,body_type=pymunk.Body.DYNAMIC)
    #sirius_head = Object((screenx/2,-screeny+90),80)
    #shape for sirius 
    #head as a circle #radius 8 #location 16,16
    
    #sirius_torso.add_shape(pymunk.Poly(sirius_torso.body,[(0,0),(32,0),(16,32),(16,32)],radius=10),1,10)
    #sirius_torso.add_shape(pymunk.Segment(sirius_torso.body,(8,32),(24,32),3),1,10)
    #sirius_torso.add_shape(pymunk.Circle(sirius_torso.body,8,(16,-16)),1,10)
    #sirius_torso.body.moment = pymunk.inf
    #j = pymunk.PinJoint(sirius_head.body,sirius_torso.body,(16,-16),(16,0))
    #j.distance = 16
    #Pymunk_queue.append(j)

    #body as a triangle # 1,17 16,1
    #a flat base

    #ball.from_image(sirius)
    #ball.shape.elasticity = 0.0

    map = Grid.grid()
    map.load_layer()
    grid2obj(map)



    cam = camera(ball,PhysicsManager,center)

    PlayerSm = Player()

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
            if event.type == pygame.KEYDOWN: 

                Player_controller(event.key, ball.body, 0)
            if event.type == pygame.KEYUP:
                Player_controller(event.key, ball.body, 1) #the player should stop moving left or right when a key is released, but not when jumping
                print('test')


        screen.fill((255,255,255))
        PhysicsManager.debug_draw(screen,space)
        cam.update(ball, space)
        #PhysicsManager.Translate(space,(1,0))

        for obj in Object_list:
            obj

        pygame.display.update()
        clock.tick(fps)
        space.step(1/fps)
      
if __name__ == "__main__":
    main()


# %%
