from pymunk import Body
from pymunk import Shape
from pymunk import Space
from pymunk import pygame_util
from pymunk import Arbiter

from pygame import sprite
from pygame import image
from pygame import key


class SceneManager():
    def __init__(self):
        
        self.camera = None
        self.space = Space()                # The 'space' where pymunk simulates
        self.space.gravity = 0 ,981         # Set gravity
        self.damping = 1                    # Global dampening variable from 0 (full) to 1 (none)
        self.data = 1

        self.object_list = []               #lists for keeping track of objects
        self.platform_list = []             #lists for keeping track of platforms 
        self.statics_list = []              #lists  for keeping track of statics
        self.sprite_group = sprite.Group()  #sprite group for drawing images
        self.queue = []                     #queue for holding pymunk bodies and shapes

    def load_base(self,tiled_map):
        pass

    def translate_all(self,dxy):
        """This will translate all bodies with xy"""
        for obj in self.object_list + self.statics_list + self.platform_list:    
            obj.translate(dxy)
            self.space.reindex_shapes_for_body(obj.body)

    def add_objects(self):
        """This method will add all objects to the given physics space and clear the queue"""
        
        if self.queue != []: #if list is not empty
            for Obj in self.queue:
                self.space.add(Obj)
            self.queue.clear()

    def update(self,screen,FPS):
        self.space.step(1/FPS)              #step the physics world
        self.camera.update()                #update the camera
        self.sprite_group.draw(screen)      #draw the sprites
        self.sprite_group.update()          #run the custom update function
        self.add_objects()                  #add any objects to the physics world

    def debug_draw(self,surface):
        """Draws objects in defined space to the pygame surface. """
        options = pygame_util.DrawOptions(surface)
        self.space.debug_draw(options)



class camera():

    def __init__(self,object, manager, location):
        self.object = object
        self.manager = manager 
        self.location = location 
        self.dxy = 0

    def update(self):
        """Updates camera based on previous location"""

        self.current = self.object.get_cog()                   #get a new current position
        self.dxy = self.location - self.current             #calculate the changed position to the set position
        self.manager.translate_all(self.dxy)



         
        

    
            
    
if __name__ == "__main__":
    pass
