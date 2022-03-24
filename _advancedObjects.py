"""More complex things made of basic objects"""
from _basicObjects import *

class Object(Node):
    """A thing with a sprite and hitbox"""
    def __init__(self, name, startRect:pygame.Rect, spr, hitbox:Hitbox):
        #general container
        self.rect = startRect
        self.name = name #prolly used for debugs

        self.sprite = spr #load the static image / entire anim controller for updating

        self.hitbox = hitbox
        #update position
        self.hitbox.rect = pygame.Rect(self.rect.x + self.hitbox.oX, self.rect.y + self.hitbox.oY, self.hitbox.w, self.hitbox.h)

    def Update(self):
        if isinstance(self.sprite, AnimSprite):#static sprites doesnt update lol
            self.sprite.Update()

    def Render(self, screen):   
        if isinstance(self.sprite, AnimSprite):
            screen.blit(self.sprite.curFrame, (self.rect.x, self.rect.y))#animated
        else:
            cropped = pygame.Surface((self.rect.w, self.rect.h))
            cropped.blit(self.sprite.image, (0,0)) #crop le huge green rectangle
            screen.blit(cropped, (self.rect.x, self.rect.y))

        self.hitbox.Render(screen)

class Interactable(Object):
    #flavor text, yaddda yadda
    pass

class RoomExit(Object):
    """Invisible thing that switches rooms."""
    def __init__(self, dest):
        """Which room does this transport you to?"""
        pass
