"""Building blocks"""
import pygame, os
from _node import Node
from _basicObjects import *
from _advancedObjects import *
from PIL import Image
from _player import *

#TODO: 

#Might need to find a better place to manage room data (json?)
#switch rooms

#layering: move player in front of the object if its Y is larger than its
#hitbox per room

#debug mode: add groups to sprite and hitbox seperately
#find somewhere else to place the player intop the room [done]
#add spritesheet system? [done]
#scrolling [done]

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
    def __init__(self, startPos, spr, player:Player, player_startPos:tuple, player_startD:int, objs:tuple[Object] = None):
        """Position (tuple) the room starts with. 
        Need to find ways to config starting player inforamtion.
        Use json files?"""
        super().__init__()

        #Add exit points? position, size, destination (prob need a function for that)
        #player's movable bound too
        
        self.x = startPos[0]
        self.y = startPos[1]
        self.vel = 5

        with Image.open(spr) as spruh:
            self.w, self.h = spruh.size

        self.sprite = pygame.image.load(spr)

        self.player_info = player
        self.player_info.hitbox.rect.x = player_startPos[0]
        self.player_info.hitbox.rect.y = player_startPos[1]
        self.player_info.sprite.dir = player_startD

        self.obj_info = objs

    def ProcessInput(self, events, keys):
        self.player_info.ProcessInput(events, keys, self.obj_info)

    def Update(self):
        self.player_info.Update()
        
    def Render(self, screen):   
        screen.blit(self.sprite, (self.x, self.y))
        if self.obj_info != None:
            for o in self.obj_info:
                o.Render(screen) 
        self.player_info.Render(screen)

class StaticRoom(Game):
    #Same params except the size is fixed
    #Kinda useless tbh
    def __init__(self, startPos, spr, player, player_startPos, player_startD, objs = None):
        super().__init__(startPos,spr, player, player_startPos, player_startD, objs)
    
class ScrollRoom(Game):
    #Possible to do both h and v?
    #how to take hitbox into account too?
    def __init__(self, startPos, spr, player, player_startPos, player_startD, objs = None):
        super().__init__(startPos, spr, player, player_startPos, player_startD, objs)
        self.initX = startPos[0]

    def scrollScreen(self, dx, dy):
        #move the objects too
        self.x += dx
        self.y += dy

    def Update(self):
        #print(self.x, self.y)
        if (self.player_info.x + self.player_info.hitbox.oX < 432) and self.x < 0: #collision checked using hitbox ONLY
            #camera to the left
            self.scrollScreen(self.player_info.vel, 0)
            self.player_info.x = 432 - self.player_info.hitbox.oX

        elif (self.player_info.x + self.player_info.hitbox.oX + self.player_info.hitbox.w > 648) and (self.x > self.WINDOW_SIZE[0] - self.w):
            #right
            self.scrollScreen(0 - self.player_info.vel, 0)
            self.player_info.x = 648 - self.player_info.hitbox.oX - self.player_info.hitbox.w

        if (self.player_info.y + self.player_info.hitbox.oY < 288) and self.y < 0:
            #up
            self.scrollScreen(0, self.player_info.vel)
            self.player_info.y = 288 - self.player_info.hitbox.oY

        elif (self.player_info.y + self.player_info.hitbox.oY > 432) and (self.y > self.WINDOW_SIZE[1] - self.h):
            #down
            self.scrollScreen(0, 0 - self.player_info.vel)
            self.player_info.y = 432 - self.player_info.hitbox.oY

        self.player_info.Update()

