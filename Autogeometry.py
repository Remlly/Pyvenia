
#%%
import pymunk
import pygame

from pymunk.autogeometry import march_soft
from pymunk.autogeometry import march_hard
img = [

    "xxxxx  ",

    "xxxxx  ",

    "   xx  ",
 
    "   xx  ",

    "   xx  ",

    "   xxxx",

    "   xxxx",

]

pilaar_img = pygame.image.load("art\pilaar.png")
alphas = pygame.surfarray.array_alpha(pilaar_img)

def sample_func(point, img):

    x = int(point[0])

    y = int(point[1])
   
    if img[y][x] == " ":
        return 1
    else:
        return 0
    #return 1 if img[y][x] == "x" else 0

def sample_alpha(point, img):
    x = int(point[0])

    y = int(point[1])

    if img[y][x] == 255:
        return 1
    else:
        return 0

def from_image( img : pygame.surface):

        bb = img.get_bounding_rect()
        width = img.get_width()
        height = img.get_height()

        alpha_data = pygame.surfarray.pixels_alpha(img)
        print(width,height)

        pl_set = march_soft(pymunk.BB(0,0,height-1,width-1), height, width, 0, lambda p: sample_func_alphas(p, alpha_data))
        for poly_line in pl_set:
            for i in range(len(poly_line) - 1):
                a = poly_line[i]
                b = poly_line[i + 1]

def autogeometry(img):
    pl_set = march_soft(pymunk.BB(0,0,6,6), 7, 7, .5, lambda p: sample_func(p, img))
    for poly_line in pl_set:
        for i in range(len(poly_line) - 1):
            a = poly_line[i]
            b = poly_line[i + 1]
    return a,b

if __name__ == "__main__":
    a,b = autogeometry(img)
    print(a,b)