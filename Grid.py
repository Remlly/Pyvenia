import pygame
import json


from pygame import Vector2
from pygame import Surface
from pygame import image
from SceneManager import *
import SceneManager
from pymunk import Poly
from pymunk import Body

#bunch_of_colours
green = (100, 150, 100) 
red   = (100,0,0)
blue  = (0,0,100)
orange = (255, 165, 0)
grey = (128,128,128)

def set_bit(value, index):
    return value | (1<<index)

def clear_bit(value, index):
    return value & ~(1<<index)

def get_bit(value, bit_index):
    return (value >> bit_index) & 1

class grid():
    def __init__(self,x = 32,y = 32,z=1):
        self.data = [[[0 for i in range(x)] for j in range(y)]  for k in range(z)]
        self.statics = Surface((x,y))
        self.dynamics = Surface((x,y))

    def save_layer(self):
        image.save(self.statics,'statics.png')
    
    def load_layer(self):
        self.statics = image.load('statics.png',)
        print('Loading')

    def to_obj(self):
        print('test')
        for x in range(self.statics.get_width()):
            for y in range(self.statics.get_height()):
                
                data = self.statics.get_at((x,y))
                if data == (255,255,255,255):
                    floor = Object(body_type=Body.STATIC)
                    floor.body.position = x*32,y*32
                    floor.add_shape(Poly(floor.body,[(0,0),(32,0),(32,32),(0,32)]),10,2)
                if data == (255,00,00,255):
                    obj = Object(body_type=Body.DYNAMIC)
                    obj.body.position = x*32,y*32
                    obj.add_shape(Poly(obj.body,[(0,0),(32,0),(32,32),(0,32)]),10,2)
                    obj.shape.friction = 0.9

    def world2screen(self):
        pass
    def draw(self):
        pass



if __name__ == "__main__":
    map = grid()
    map.load_layer()
    map.to_obj()

    
    #print (map.data[1])
    
# arena = grid(10,10,20,Vector2(10,10))
# arena.data[3][3] = set_bit(arena.data[3][3],Impassable)
# arena.data[3][3] = set_bit(arena.data[3][3],Enemy)

#   tl = Vector2(0,0).rotate(45)
#   tr = Vector2(20/2,0).rotate(45)
#   bl = Vector2(0,20).rotate(45)
#   br = Vector2(20/2,20).rotate(45)
#   pygame.draw.polygon(screen,green,[tl,tr,br,bl])
