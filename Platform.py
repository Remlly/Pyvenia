from object import Object
from pymunk import Body
from pymunk import Shape

class platform(Object):
    def __init__(self, body_type=Body.DYNAMIC, shape=None):
        super().__init__(body_type, shape)
        self.body.position = (0,0)
        self.End_x = 0
        self.End_y = 0
        self.Begin_x = 0
        self.Begin_y = 0
        self.forward = True
        self.body.velocity = (25,0)
        
        
    def move(self):

        
        if self.body.position.x < self.Begin_x:
            self.body.velocity = (25,0)
            self.shape.surface_velocity = (25,0)
        if self.body.position.x > self.End_x:
            self.body.velocity = (-25,0)
            self.shape.surface_velocity = (-25,0)

    def translate(self,dxy):
        """Platforms need a morphed translation because of the extra coordinates"""
        self.body.position += dxy
        self.End_x += dxy.x
        self.Begin_x +=dxy.x