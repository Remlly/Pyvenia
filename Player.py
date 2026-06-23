from object import Object
from pygame import key
from pymunk import Arbiter
import pygame


class player(Object):
    def __init__(self):
        Object.__init__(self)

        self.Jump_allowed = False
        self.on_wall = False
        self.speed = 50
        self.max_velocity = 250
        self.max_velocity_y = 250
        self.fm = 0 
        self.fb = 0
        self.fj = 0
        self.onPlatform = False
        self.idle_velocity = 0
        self.current = self.body.position
        
        #self.body.mass = 100

    def calculate_controls(self, acceleration_time, decceleration_time,jumping_time):
        self.fm = self.shape.mass * (self.max_velocity/acceleration_time)
        self.fb = self.shape.mass * (self.max_velocity/decceleration_time)
        self.fj = self.shape.mass * (self.max_velocity_y/jumping_time)

    def brake(self):
        if -15 < self.body.velocity.x < 15:
            self.body.velocity = (self.idle_velocity,self.body.velocity.y) 
        elif self.body.velocity.x < self.idle_velocity:
                #apply brakeforce left
                self.body.apply_force_at_local_point((self.fb,0),self.get_cog())
        elif self.body.velocity.x > self.idle_velocity:
                self.body.apply_force_at_local_point((-self.fb,0),self.get_cog())
        
        
    def ground_controller(self):
        keys = key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            
            if self.body.velocity.x > -self.max_velocity:
                self.body.apply_force_at_local_point((-self.fm,0),self.get_cog())
            else:
                self.brake()
        
        elif keys[pygame.K_RIGHT]:

            if self.body.velocity.x < self.max_velocity:
                self.body.apply_force_at_local_point((self.fm,0),self.get_cog())
            else:
                self.brake()

        else:
            self.brake()
        
        if keys[pygame.K_SPACE] and self.Jump_allowed:
        
            self.Jump_allowed = False
            self.body.apply_impulse_at_local_point((0,-self.fj),self.get_cog())
        
       

    def on_platform(self,arbiter:Arbiter,space,data):
        if arbiter.normal.y > 0.9 and not self.onPlatform:
            arbiter.bodies[0].position += arbiter.bodies[1].velocity/25
            
            self.onPlatform = True
            self.Jump_allowed = True

        else:
            self.onPlatform = False
            
               
    def on_ground(self,arbiter: Arbiter,space,data):
        if arbiter.normal.y > 0.9:

            self.Jump_allowed = True
            self.on_wall = False

        if arbiter.normal.x < -0.9 or arbiter.normal.x > 0.9:
            self.on_wall = True