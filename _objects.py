from msilib.schema import CheckBox
from re import L
import pygame
from _spritesheet import spritesheet
from _node import Node

#immovables, interactable, npc, player
#how to set player starring position per room
#dialogue box? how to make interactables

#add testing furniture: clock, table, bed, desk (your room)

#moving bg: clouds?
#player diagonal direction?

class Hitbox(Node):
    """Collision controller"""
    def __init__(self, name, offset:tuple, size:tuple):
        """name?, offset from the player object, width and height"""
        self.oX = offset[0]
        self.oY = offset[1]
        self.w = size[0]
        self.h = size[1]
        self.rect = pygame.Rect(self.oX, self.oY, size[0], size[1]) #the object, if anyone wants

    def Render(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.rect, 2)

    def isCollide(self, other):
        return pygame.Rect.colliderect(self.hitbox, other)

    #do update in player, easier to calc position

class AnimSprite(Node):
    """Animation controller"""
    def __init__(self, name, offset:tuple, startD:int, spr:spritesheet):
        """name??, offset from the player object, stating direction, spritesheet object"""
        #self.name = name #whats the use of this tho
        self.oX = offset[0]
        self.oY = offset[1]

        self.ANIM_FPS = 4
        self.dir = startD
        self.walk_count = 0
        self.sprite = spr

        match self.dir:
            case 0:
                self.setAnim("left")
            case 1:
                self.setAnim("back")
            case 2:
                self.setAnim("right")
            case 3:
                self.setAnim("front")

        self.curFrame = self.sprite.curAnim[self.walk_count]

    def setAnim(self, name:str):
        self.sprite.curAnim = self.sprite.getAnimByKey(name)

    def ProcessInput(self, events, keys):
        if any((keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN])):
            #if held down and is in the window
            if keys[pygame.K_LEFT]:
                self.dir = 0
                self.setAnim("left")
                
            if keys[pygame.K_RIGHT]:
                self.dir = 2
                self.setAnim("right")
                
            if keys[pygame.K_UP]:
                self.dir = 1
                self.setAnim("back")
            
            if keys[pygame.K_DOWN]:
                self.dir = 3
                self.setAnim("front")

            self.walk_count += 1

        else:
            #key up lol
            self.walk_count = 0
            
        self.walk_count %= self.FPS

    def Update(self):
        #I want to die
        self.curFrame = self.sprite.curAnim[(self.walk_count // (self.FPS//self.ANIM_FPS)) % 4]

class Object(Node):
    """A thing with a hitbox and a sprite."""
    def __init__(self, name, startRect:tuple, spr:AnimSprite, hitbox:Hitbox):
        self.x = startRect[0]
        self.y = startRect[1]
        self.w = startRect[2]
        self.h = startRect[3]

        self.name = name

        self.sprite = spr
        self.hitbox = hitbox        
    
    def Update(self):
        self.hitbox.rect = pygame.Rect(self.x + self.hitbox.oX, self.y + self.hitbox.oY, self.hitbox.w, self.hitbox.h)
        self.sprite.Update()

    def Render(self, screen):   
        screen.blit(self.sprite, (self.x + self.sprite.oX, self.y + self.sprite.oY))#spr
        pygame.draw.rect(screen, (255,0,0), self.hitbox.rect, 2)#hitbox

class Checker(Hitbox):
    """Used to interact with other things. Has variable offset"""
    def __init__(self, name, offset, size):
        super().__init__(name, offset, size)
    
    def Render(self, screen):
        pygame.draw.rect(screen, (255,255,0), self.rect, 2)
        
class Player(Object):
    """Can be moved around. Has a special checking box to interact with other things"""
    def __init__(self, name, startRect:tuple, spr:AnimSprite, hitbox:Hitbox, check:Checker):
        super().__init__(name, startRect, spr, hitbox)

        self.vel = 5
        self.check = check #the object itself
        self.isChecking = False
    
    def ProcessInput(self, events, keys):
        #if held down and is in the window
        if keys[pygame.K_LEFT] and self.x + self.hitbox.oX> 0:
            self.x -= self.vel
            
        if keys[pygame.K_RIGHT] and self.x + self.hitbox.oX + self.hitbox.w < self.WINDOW_SIZE[0]:
            self.x += self.vel
            
        if keys[pygame.K_UP] and self.y + self.hitbox.oY> 0:
            self.y -= self.vel
        
        if keys[pygame.K_DOWN] and self.y + self.hitbox.oY + self.hitbox.h < self.WINDOW_SIZE[1]:
            self.y += self.vel

        self.sprite.ProcessInput(events, keys)

        #checkbox
        for e in events:
            if e.type == pygame.KEYDOWN:
                if (e.key == pygame.K_z or e.key == pygame.K_SPACE):
                    self.isChecking = True
                    match self.sprite.dir:
                        #relative to the entire player object
                        case 0:#l
                            self.check.oX = 0 - self.check.rect.w
                            self.check.oY = self.hitbox.oY
                        case 1:#up
                            self.check.oX = self.hitbox.oX
                            self.check.oY = self.hitbox.oY - self.check.h
                        case 2:#r
                            self.check.oX = self.w
                            self.check.oY = self.hitbox.oY
                        case 3:#down
                            self.check.oX = 0
                            self.check.oY = self.h


    def Update(self):
        print(self.isChecking)
        self.hitbox.rect = pygame.Rect(self.x + self.hitbox.oX, self.y + self.hitbox.oY, self.hitbox.w, self.hitbox.h)
        self.check.rect = pygame.Rect(self.x + self.check.oX, self.y + self.check.oY, self.check.w, self.check.h)
        self.sprite.Update()

        self.isChecking = False

    def Render(self, screen):   
        screen.blit(self.sprite.curFrame, (self.x + self.sprite.oX, self.y + self.sprite.oY))#spr
        self.hitbox.Render(screen)
        self.check.Render(screen)
        

class Interactable(Hitbox):
    pass

