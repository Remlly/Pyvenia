from pymunk import Body
from pymunk import Shape
from pymunk import Space
from pymunk import pygame_util
from pymunk import Arbiter
from pygame import sprite
from pygame import image
from pygame import key
import math

object_list = []                            # List to keep track of objects
queue = []                                  # List to keep for when adding more than 1 shape.
sprite_group = sprite.Group()               # sprite group for drawing images


Jump_allowed = True
def on_ground(arbiter : Arbiter, space, data):
    #print(arbiter.normal)
    global Jump_allowed
    if arbiter.normal > (0,0):
        Jump_allowed = True


class SceneManager():
    def __init__(self):
        
        self.camera = None
        self.space = Space()                # The 'space' where pymunk simulates
        self.space.gravity = 0 ,981         # Set gravity
        self.damping = 1                    # Global dampening variable from 0 (full) to 1 (none)
        self.data = 1

        #self.handler = self.space.on_collision(1,2,post_solve=on_ground)


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
        self.camera.update()                #update the camera
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
        self.org_image = image.load("textures\Sirius.png")
        self.image = self.org_image
        self.rect = self.image.get_rect()
    

        self.body = Body(body_type=body_type)
        self.shape = shape


        object_list.append(self)
        
        queue.append(self.body)
        if shape is not None:
            queue.append(self.shape)
        
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
        queue.append(self.shape)

    def get_cog(self):
        return self.body.local_to_world(self.body.center_of_gravity)
    
    def update(self):
        self.rect.topleft = self.body.position.x, self.body.position.y

        if self.body.body_type == Body.DYNAMIC and isinstance(self.shape, pymunk.Poly):
            rot_image =  pygame.transform.rotate(self.org_image,math.degrees(-self.body.angle))
            self.rect = rot_image.get_rect(center = self.get_cog())
            self.image = rot_image

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


class player(Object):
    def __init__(self):
        Object.__init__(self)

        self.Jump_allowed = False
        self.speed = 50
        self.max_velocity = 250
        self.fm = 2000 
        self.fb = 2*self.fm
        self.db = False
        
        #self.body.mass = 100

    def brake(self):
        if self.body.velocity.x < 0:
                #apply brakeforce left
                self.body.apply_force_at_local_point((self.fb,0),self.get_cog())
        elif self.body.velocity.x > 0:
                self.body.apply_force_at_local_point((-self.fb,0),self.get_cog())

    def control(self):
        "The controller works on if a key is pressed or not pressed."
        "going horizontal sets a velocity. releasing the key sets it to 0"
        "vertical velocity is gained when the spacebar is pressed, but can only be done once. a collision arbiter"
        "handles this part"
        keys = key.get_pressed()



        if keys[pygame.K_LEFT] and self.Jump_allowed:

            if self.body.velocity.x > 0:
                self.brake()

            if self.body.velocity.x > -self.max_velocity:
                self.body.apply_force_at_local_point((-self.fm,0),self.get_cog())
                if self.db:
                    self.body.velocity = (-self.speed,self.body.velocity.y)
                    self.db = False
        elif keys[pygame.K_RIGHT] and self.Jump_allowed:
            if self.body.velocity.x < 0:
                self.brake()

            if self.body.velocity.x < self.max_velocity:
                self.body.apply_force_at_local_point((self.fm,0),self.get_cog())
            
                if self.db:
                    self.body.velocity = (self.speed,self.body.velocity.y)
                    self.db = False
        elif self.Jump_allowed:
            self.db = True
            self.brake()
                #apply brakeforce right
            #self.body.velocity = (0,self.body.velocity.y)

        if keys[pygame.K_SPACE] and self.Jump_allowed:
            self.Jump_allowed = False
            self.body.velocity = (self.body.velocity.x,-500)

       
        
    def on_ground(self,arbiter: Arbiter,space,data):
        if arbiter.normal > (0,0):
            self.Jump_allowed = True


            
    
if __name__ == "__main__":

    # Initialize Pygame
    import pygame
    import pymunk
    import sys
    import Grid
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
    player1.body.position = WIDTH/2, HEIGHT/2
    
    sprite_group.add(player1)
    
    #print (obj.body.moment)
    player1.add_shape(pymunk.Poly(player1.body,[(0,0),(32,0),(32,64),(0,64)],radius=1),10,1)
    player1.add_image("Textures/Sirius.png")
    player1.shape.friction = 0.1
    sprite_group.add(player1)
  
    tileset = image.load("Textures/Tilesheet1.png")
    tilesize = 32
    tiles = dict()
    cols,rows = 3,3
    counter = 0
    for x in range(0,cols):
        for y in range(0,rows):
            counter += 1
            tiles[str(counter)] = tileset.subsurface(pygame.Rect(y*32,x*32,tilesize,tilesize ))

    filename = Path('Maps/tilemap.tmx')
    tile_level = pytiled_parser.parse_map(filename)
    layers = tile_level.layers

    data2 = layers[1]
    for object in data2.tiled_objects:
        if object.name == "player":
            player1.body.position = object.coordinates
        if object.name == "box":
            obj = Object(body_type=Body.DYNAMIC)
            obj.body.position = object.coordinates
            obj.add_shape(pymunk.Poly(obj.body,[(0,0),(30,0),(30,30),(0,30)]),5,2)
            obj.add_image("Textures/doos.png")
            sprite_group.add(obj)
            obj.shape.friction = 0.3

          
    
    for x in range(tile_level.map_size.width):
        for y in range(tile_level.map_size.height):
            data1 = layers[0].data[y][x]
            
            if data1 > 0:
                floor = Object(body_type=pymunk.Body.STATIC)
                floor.body.position = x*32,y*32
                floor.add_shape(pymunk.Poly(floor.body,[(0,0),(32,0),(32,32),(0,32)],radius=1),10,2)
                floor.add_from_tileset(tiles[str(data1)])
                sprite_group.add(floor)
                floor.shape.friction = 0.5


            
        
                


    #obj.body.mass = math.inf

    group = sprite.Group()
    group.add(player1)

    scene = SceneManager()
    scene.space.on_collision(1,2,post_solve=player1.on_ground)
    scene.camera = camera(player1,scene,(WIDTH/2,HEIGHT/2))


    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game logic here
        player1.body.moment = math.inf
        player1.control()

        

        # Draw
        screen.fill((41, 44, 49))
        scene.debug_draw(screen)
        scene.update(screen)  

        pygame.display.flip()        # Update display
        clock.tick(FPS)              # Update clock
               
      
            

            # Cleanup
    pygame.quit()
    sys.exit()