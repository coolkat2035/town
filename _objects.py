import pygame
from _spritesheet import spritesheet
from _node import Node

#immovables, interactable, npc, player
#how to set player starring position per room    

class Hitbox(Node):
    """Collision controller"""
    def __init__(self, name, offset:tuple, size:tuple):
        """The offset is a rectangle!!"""
        self.oX = offset[0]
        self.oY = offset[1]
        self.w = size[0]
        self.h = size[1]
        self.rect = pygame.Rect(self.oX, self.oY, size[0], size[1]) #the object, if anyone wants

    def isCollide(self, other):
        return pygame.Rect.colliderect(self.hitbox, other)
    #do update in player, easier to calc position

class Sprite(Node):
    """Animation controller"""
    def __init__(self, name, offset:tuple, startD:int, spr:spritesheet):
        self.name = name #whats the use of this tho
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
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    #make checker box
                    print("check")
                    pass


        if any(keys):
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
    def __init__(self, name, startRect:tuple, spr:Sprite, hitbox:Hitbox):
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

class Player(Object):
    def __init__(self, name, startRect:tuple, spr:Sprite, hitbox:Hitbox):
        super().__init__(name, startRect, spr, hitbox)

        self.vel = 5
    
    def ProcessInput(self, events, keys):
        if any(keys):
            #if held down and is in the window
            if keys[pygame.K_LEFT] and self.x > 0:
                self.x -= self.vel
                
            if keys[pygame.K_RIGHT] and self.x + self.hitbox.oX + self.hitbox.w < self.WINDOW_SIZE[0]:
                self.x += self.vel
                
            if keys[pygame.K_UP] and self.y > 0:
                self.y -= self.vel
            
            if keys[pygame.K_DOWN] and self.y + self.hitbox.oY + self.hitbox.h < self.WINDOW_SIZE[1]:
                self.y += self.vel

        self.sprite.ProcessInput(events, keys)

    def Update(self):
        #print(self.x, self.y)
        self.hitbox.rect = pygame.Rect(self.x + self.hitbox.oX, self.y + self.hitbox.oY, self.hitbox.w, self.hitbox.h)
        self.sprite.Update()

    def Render(self, screen):   
        screen.blit(self.sprite.curFrame, (self.x + self.sprite.oX, self.y + self.sprite.oY))#spr
        pygame.draw.rect(screen, (255,0,0), self.hitbox.rect, 2)

