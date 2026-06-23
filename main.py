#
# Developed by Remon Verbraak
# Date: 7-11-2025
#   


#%%imports
import pygame
import pymunk
import pytmx
from object import Object
from SceneManager import SceneManager
from SceneManager import camera
from Platform import platform
from Player import player
from pymunk import Body
from pymunk import Poly



if __name__ == "__main__":
        # Initialize Pygame
    import pygame
    import pymunk
    import sys
    import math
    import pytiled_parser
    from pathlib import Path
    
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    FPS = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Project")
    clock = pygame.time.Clock()

    # Main loop
    #print(level)
    #to_obj(map,tiles)
    
    player1 = player()
    shape = pymunk.Poly(player1.body,((0,0),(0,64),(32,64),(32,0)))
    player1.add_shape(shape,10,1)
    player1.calculate_controls(0.3,0.3,0.5)
    


    scene = SceneManager()
    scene.camera = camera(player1,scene,(WIDTH/2,HEIGHT/2))

    scene.sprite_group.add(player1)
    scene.space.add(player1.body,player1.shape)
    scene.space.on_collision(1,2, post_solve=player1.on_ground)

    scene.object_list.append(player1)

    tiled_map = pytmx.load_pygame("Game/Maps/Tilemap.tmx")

    base_layer = tiled_map.get_layer_by_name('Tilelaag 1')
    tile_size = (tiled_map.tilewidth,tiled_map.tileheight)

    for x, y, image in base_layer.tiles():
            obj = Object(Body.STATIC)
            obj.body.position = (x*32,y*32)
            shape = Poly.create_box(obj.body,tile_size)
            obj.add_shape(shape,10,2)
            obj.image = image
            obj.org_image = image

            scene.sprite_group.add(obj)
            scene.space.add(obj.body,obj.shape)
            scene.statics_list.append(obj)

    
    print(tiled_map.tilewidth)

    running = True
    while running:
        #dt = clock.tick(FPS)/1000
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game logic here
        player1.body.moment = math.inf
        player1.ground_controller()
        print(player1.fj)
        #platform1.move()

        

        # Draw
        screen.fill((41, 44, 49))
        scene.debug_draw(screen)
        scene.update(screen,60)  

        pygame.display.flip()        # Update display
        clock.tick(FPS)              # Update clock
               
      
            

            # Cleanup
    pygame.quit()
    sys.exit()


# %%
