import pygame
from statemachine import StateMachine, State
from PhysicsHandler import Object

#%%
class Player(StateMachine, Object):

    """A player is an object that can handle inputs, and follows a statemachine"""
    idle = State(initial=True)
    moving_left = State()
    moving_right = State()


    go_left = idle.to(moving_left)
    go_right = idle.to(moving_right)
    go_idle = idle.to.itself()
    go_idle = (moving_left.to(idle) | moving_right.to(idle))

    def on_enter_idle(self):
        print("Entering idle state")

    def on_enter_moving_left(self):
        print("Moving left")

 

    def on_enter_moving_right(self):
        print("Moving right")

PlayerSm = Player()        
#PlayerSm._graph().write_png("PlayerMachine.png")
# %%
