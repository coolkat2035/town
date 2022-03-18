import pygame, os
import _spritesheet
from _node import Node
from _objects import *

#TODO: add spritesheet system
#Might need to find a better place to manage files
#switch rooms
#hitbox
#hitbox per room
#find somewhere else to place the player intop the roompesd


class Room(Node):
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

class Title(Room):
    def __init__(self):
        Room.__init__(self)
    
    def ProcessInput(self, events, keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(Game())
    
    def Update(self):
        pass
    
    def Render(self, screen):
        #work on this later
        screen.fill((255, 0, 0))

class Game(Room):
    def __init__(self, startPos, startD, size, spr, player:Player, objs = None):
        """Position (tuple) the room starts with. 
        Need to find ways to config starting player inforamtion.
        Use json files?"""
        super().__init__()

        #Should probably haul these to player class idk, esp vel and count
        #Add exit points? position, size, destination (prob need a function for that)
        #player's movable bound too
        
        self.x = startPos[0]
        self.y = startPos[1]
        self.dir = startD
        self.vel = 5
        self.w = size[0]
        self.h = size[1]
        self.sprite = pygame.image.load(spr)
        self.player_info = player

    def ProcessInput(self, events, keys):
        self.player_info.ProcessInput(events, keys)
    
    def Update(self):
        self.player_info.Update()
        
    def Render(self, screen):   
        screen.blit(self.sprite, (0, 0))
        self.player_info.Render(screen)


class StaticRoom(Game):
    #Same params except the size is fixed
    def __init__(self, startPos, startD, spr, player):
        super().__init__(startPos, startD, self.WINDOW_SIZE, spr, player)
    


class ScrollRoom(Game):
    #Possible to do both h and v?
    #how to take hitbox into account too?
    def __init__(self, startPos, startD, size, spr, player, obj_gp = None):
        super().__init__(startPos, startD, size, spr, player)
        self.initX = startPos[0]

    def scrollScreen(self, dx):
        #move the objects too
        self.x += dx
        self.y += 0

    def Update(self):
        #print(self.x, self.y)
        if self.player_info.x < 300 and self.x < 0:
            self.scrollScreen(5)
            self.player_info.x = 300

        if self.player_info.x > 800 and self.x > self.initX:
            self.scrollScreen(-5)
            self.player_info.x = 800

        self.player_info.Update()

