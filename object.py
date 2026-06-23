from pygame import sprite
from pygame import image
from pygame import transform
from pymunk import Shape
from pymunk import Body
from pymunk import Poly

import math
import SceneManager
import pymunk



class Object(sprite.Sprite):
    
    def __init__(self, body_type = Body.DYNAMIC, shape = None):
        sprite.Sprite.__init__(self)
        self.org_image = image.load("Game\Textures\Sirius.png")
        self.image = self.org_image
        self.rect = self.image.get_rect()
    

        self.body = Body(body_type=body_type)
        self.shape = shape
    
    def from_tiled(self,tileSize: tuple,position : tuple, image):
        
        self.shape = self.add_shape(Poly.create_box(self.body,(tileSize[0],tileSize[1])),10,1)
        self.body.position = position
        self.org_image = image 
        self.image = image
       

        
    def add_image(self,image_path : str):
        self.org_image = image.load(image_path)
        self.image = self.org_image

    def add_from_tileset(self, image):
        self.org_image = image
        self.image = self.org_image

    def translate(self,dxy):
        """This method translates the body by an x and a y coordinate. """
        self.body.position += dxy

    def add_shape(self,shape : Shape, mass: int,collision_type : int):
        self.shape = shape
        self.shape.collision_type = collision_type
        self.shape.mass = mass

    def get_cog(self):
        return self.body.local_to_world(self.body.center_of_gravity)
    
    def update(self):
        self.rect.topleft = self.body.position.x-16, self.body.position.y-16

        if self.body.body_type == Body.DYNAMIC and isinstance(self.shape, pymunk.Poly):
            rot_image =  transform.rotate(self.org_image,math.degrees(-self.body.angle))
            self.rect = rot_image.get_rect(center = self.get_cog())
            self.image = rot_image
