import pygame
import pymunk
from pymunk.autogeometry import march_soft
from pymunk.autogeometry import march_hard
import pymunk.pygame_util
import math

Object_list = []    #To keep track of all objects
Pymunk_queue = []   #This queue will keep all pymunk items that need to be added to the space. eg all bodies and shapes. 


def to_pygame(p):
    """Small helper to convert Pymunk vec2d to Pygame integers"""
    return round(p.x), round(p.y)


def sample_func(point,img):
    """A function for autogeometry sampling"""
    x = int(point[0])

    y = int(point[1])

    return 1 if img[y][x] == "x" else 0


def sample_func_alphas(point,img):
    """A function for autogeometry sampling using alpha layer?"""
    x = int(point[0])

    y = int(point[1])

    return 1 if img[y][x] == 0 else 0

class PhysicsBody():
    def __init__(self, location : tuple, body_type = pymunk.Body.DYNAMIC):
        """PhysicsBody is a pymunk body. Its responsible for: 
        1. Location
        2. Translation
        3. Rotation"""
        self.body = pymunk.Body(body_type=body_type)

        self.body.position = location
        self.radius = 1
        Pymunk_queue.append(self.body)
        Object_list.append(self)

    def translate(self,dxy):
        """This method translates the body by an x and a y coordinate. """
        self.body.position += dxy

    def rotate (self,angle):
        pass

    def get_cog(self):
        return self.body.local_to_world(self.body.center_of_gravity)


class Object(PhysicsBody, pygame.sprite.Sprite):
    def __init__(self, location : tuple, mass : int, body_type = pymunk.Body.DYNAMIC):
        """An object is a specialized form of a pymunk body. it inherits from PhysicsBody.
        Its responsible for
        1. Defining the shape
            - from autogeometry
            - from user defined pymunk shape
            - from a user defined shape list
        2. The texture attached to this shape"""
        super().__init__(location,body_type)
        self.shape = None
        self.mass = mass
        self.scale = 32
        


    def autogeometry(self, img):
        pl_set = march_soft(pymunk.BB(0,0,6,6), 7, 7, .5, lambda p: sample_func(p, img))
        for poly_line in pl_set:
            for i in range(len(poly_line) - 1):
                a = poly_line[i]
                b = poly_line[i + 1]
                self.shape = pymunk.Segment(self.body, a*self.scale, b*self.scale, self.radius)
                self.shape.mass = self.mass
                Pymunk_queue.append(self.shape)

    def from_image(self, img : pygame.surface, collision_type = 2):

        bb = img.get_bounding_rect()
        width = img.get_width()
        height = img.get_height()

        alpha_data = pygame.surfarray.array_alpha(img)
        print(width,height)

        pl_set = march_soft(pymunk.BB(0,0,height-1,width-1), height, width, 0, lambda p: sample_func_alphas(p, alpha_data))
        for poly_line in pl_set:
            for i in range(len(poly_line) - 1):
                a = poly_line[i]
                b = poly_line[i + 1]
                shape = pymunk.Segment(self.body, a, b, self.radius)
                shape.collision_type = collision_type  
                shape.mass = self.mass
                Pymunk_queue.append(shape)  

                

    def add_shape(self,shape : pymunk.Shape, collision_type : int, mass):
        self.shape = shape
        self.shape.friction = 0.1
        self.shape.elasticity = 0
        self.shape.collision_type = collision_type
        self.shape.mass = mass
        Pymunk_queue.append(self.shape)


    def add_shape_list(self, list : list):
        for shape in list:
            shape.mass = self.mass
            Pymunk_queue.append(shape)

class Player(Object):
    def __init__(self):
        """A player is an object that can handle inputs"""
        pass

class Manager():
    def __init__(self):
        pass
    def debug_draw(self,surface, space):
        """Draws objects in defined space to the pygame surface. """
        options = pymunk.pygame_util.DrawOptions(surface)
        space.debug_draw(options)

    def draw(self):
        pass

    def add_objects(self,space):
        """This method will add all objects to the given physics space and clear the queue"""
        
        if Pymunk_queue != []: #if list is not empty
            for Obj in Pymunk_queue:
                space.add(Obj)
            Pymunk_queue.clear()

    def Translate_all(self,space,dxy):
        """This will translate all bodies with xy"""
        for obj in Object_list:    
            obj.translate(dxy)
            space.reindex_shapes_for_body(obj.body)

class camera:
    def __init__(self,object, manager, location):
        self.object = object
        self.manager = manager 
        self.location = location 
        self.dxy = 0

    def update(self, object : PhysicsBody, space):
        """Updates camera based on previous location"""

        self.current = object.get_cog()                   #get a new current position
        self.dxy = self.location - self.current             #calculate the changed position to the set position
        self.manager.Translate_all(space,self.dxy)

