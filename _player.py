import pygame
from _basicObjects import *
from _advancedObjects import *

class Checker(Hitbox):
    """Used to interact with other things. Has variable offset"""
    def __init__(self, size):
        super().__init__((0,0), size)
    
    def Render(self, screen):
        pygame.draw.rect(screen, (255,255,0), self.rect, 2)
    #update position in
        
class Player(Object):
    """Can be moved around. Has a special checking box to interact with other things"""
    def __init__(self, name, startRect:tuple, spr:AnimSprite, hitbox:Hitbox, check:Checker):
        super().__init__(name, startRect, spr, hitbox)

        self.name = name

        self.sprite = spr
        
        self.vel = 5 #hitbox

        self.check = check #the check box object itself
        self.isChecking = False
        self.dir = 0

        match self.dir:#set initial checkbox
            case 0:#l
                self.check.oX = 0 - self.check.rect.w
                self.check.oY = self.hitbox.oY
                self.sprite.setAnim("left")
            case 1:#up
                self.check.oX = self.hitbox.oX
                self.check.oY = self.hitbox.oY - self.check.h
                self.sprite.setAnim("back")
            case 2:#r
                self.check.oX = self.w
                self.check.oY = self.hitbox.oY
                self.sprite.setAnim("right")
            case 3:#down
                self.check.oX = 0
                self.check.oY = self.h
                self.sprite.setAnim("front")

        self.sprite.curFrame = self.sprite.curAnim[0]
    
    def ProcessInput(self, events, keys):
        #animation
        if any((keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN])):
            if keys[pygame.K_LEFT] and self.x + self.hitbox.oX> 0:
                self.dir = 0
                self.x -= self.vel
                self.sprite.setAnim("left")
                
            if keys[pygame.K_RIGHT] and self.x + self.hitbox.oX + self.hitbox.w < self.WINDOW_SIZE[0]:
                self.dir = 2
                self.x += self.vel
                self.sprite.setAnim("right")
                
            if keys[pygame.K_UP] and self.y + self.hitbox.oY> 0:
                self.dir = 1
                self.y -= self.vel
                self.sprite.setAnim("back")
            
            if keys[pygame.K_DOWN] and self.y + self.hitbox.oY + self.hitbox.h < self.WINDOW_SIZE[1]:
                self.dir = 3
                self.y += self.vel
                self.sprite.setAnim("front")

            self.sprite.frame_count += 1
        else:
            self.sprite.frame_count = 0
        self.sprite.frame_count %= self.FPS

        #checkbox
        for e in events:
            if e.type == pygame.KEYDOWN:
                if (e.key == pygame.K_z or e.key == pygame.K_SPACE):
                    self.isChecking = True
                    match self.dir:
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
        print("Player info:", self.sprite.curAnimName, self.sprite.frame_count, self.dir, self.isChecking)
        self.hitbox.rect = pygame.Rect(self.x + self.hitbox.oX, self.y + self.hitbox.oY, self.hitbox.w, self.hitbox.h)
        self.check.rect = pygame.Rect(self.x + self.check.oX, self.y + self.check.oY, self.check.w, self.check.h)
        self.sprite.curFrame = self.sprite.curAnim[(self.sprite.frame_count // (self.FPS//self.sprite.fps)) % len(self.sprite.curAnim)]

        self.isChecking = False

    def Render(self, screen):   
        screen.blit(self.sprite.curFrame, (self.x, self.y))#spr
        self.hitbox.Render(screen)
        self.check.Render(screen)
        


