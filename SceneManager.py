from pymunk import Body
from pymunk import Shape
from pymunk import Space
from pymunk import pygame_util
from pygame import sprite
from pygame import image

object_list = []                            # List to keep track of objects
queue = []                                  # List to keep for when adding more than 1 shape.
sprite_group = sprite.Group()               # sprite group for drawing images

class SceneManager():
    def __init__(self):
        
        self.camera = camera(object_list[0],self,(800/2,400/2))
        self.space = Space()                # The 'space' where pymunk simulates
        self.space.gravity = 0 ,981       # Set gravity
        self.damping = 1                    # Global dampening variable from 0 (full) to 1 (none)

    def translate_all(self,dxy):
        """This will translate all bodies with xy"""
        for obj in object_list:    
            obj.translate(dxy)
            self.space.reindex_shapes_for_body(obj.body)

    def add_objects(self):
        """This method will add all objects to the given physics space and clear the queue"""
        
        if queue != []: #if list is not empty
            for Obj in queue:
                self.space.add(Obj)
            queue.clear()

    def update(self,screen):
        self.space.step(1/FPS)              #step the physics world
        self.camera.update(object_list[0])  #update the camera
        sprite_group.draw(screen)           #draw the sprites
        sprite_group.update()               #run the custom update function
        self.add_objects()                  #add any objects to the physics world

    def debug_draw(self,surface):
        """Draws objects in defined space to the pygame surface. """
        options = pygame_util.DrawOptions(surface)
        self.space.debug_draw(options)


class Object(sprite.Sprite):
    def __init__(self, body_type = Body.DYNAMIC, shape = None):
        sprite.Sprite.__init__(self)
        self.image = image.load("textures\Sirius.png")
        self.rect = self.image.get_rect()
    

        self.body = Body(body_type=body_type)
        self.shape = shape

        
        object_list.append(self)
        sprite_group.add(self)
        queue.append(self.body)
        if shape is not None:
            queue.append(self.shape)
        

    def translate(self,dxy):
        """This method translates the body by an x and a y coordinate. """
        self.body.position += dxy

    def add_shape(self,shape : Shape, mass: int,collision_type : int):
        self.shape = shape
        self.shape.collision_type = collision_type
        self.shape.mass = mass
        queue.append(self.shape)

    def get_cog(self):
        return self.body.local_to_world(self.body.center_of_gravity)
    
    def update(self):
        self.rect.center = self.get_cog()


class camera():

    def __init__(self,object, manager, location):
        self.object = object
        self.manager = manager 
        self.location = location 
        self.dxy = 0

    def update(self,object):
        """Updates camera based on previous location"""

        self.current = object.get_cog()                   #get a new current position
        self.dxy = self.location - self.current             #calculate the changed position to the set position
        self.manager.translate_all(self.dxy)

if __name__ == "__main__":
    # Initialize Pygame
    import pygame
    import pymunk
    import sys

    pygame.init()
    WIDTH, HEIGHT = 800, 600
    FPS = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Project")
    clock = pygame.time.Clock()

    # Main loop
    
    obj = Object()
    obj.body.position = WIDTH/2, HEIGHT/2
    obj.add_shape(pymunk.Circle(obj.body,10),10,1)

    group = sprite.Group()
    group.add(obj)

    scene = SceneManager()
    cam = camera(obj,scene,(WIDTH/2,HEIGHT/2))

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game logic here

        # Draw
        screen.fill((255, 255, 255))
        scene.debug_draw(screen)
        scene.update(screen)  

        pygame.display.flip()        # Update display
        clock.tick(FPS)              # Update clock
               
        
    

    # Cleanup
    pygame.quit()
    sys.exit()