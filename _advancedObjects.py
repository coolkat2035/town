from _basicObjects import *

class Object(Node):
    """A thing with a sprite and hitbox"""
    def __init__(self, name, startRect:tuple, spr, hitbox:Hitbox):
        #general container
        self.x = startRect[0]
        self.y = startRect[1]
        self.w = startRect[2]
        self.h = startRect[3]

        self.name = name #prolly used for debugs

        self.sprite = spr #load the static image / entire anim controller for updating

        self.hitbox = hitbox
        self.hitbox.rect = pygame.Rect(self.x + self.hitbox.oX, self.y + self.hitbox.oY, self.hitbox.w, self.hitbox.h)

    def Update(self):
        if isinstance(self.sprite, AnimSprite):#static sprites doesnt update lol
            self.sprite.Update()

    def Render(self, screen):   
        if isinstance(self.sprite, AnimSprite):
            screen.blit(self.sprite.curFrame, (self.x, self.y))#animated
        else:
            cropped = pygame.Surface((self.w, self.h))
            cropped.blit(self.sprite.image, (0,0)) #crop le huge green rectangle
            screen.blit(cropped, (self.x, self.y))

        self.hitbox.Render(screen)

class Interactable(Object):
    #flavor text, yaddda yadda
    pass

class RoomExit(Object):
    """Invisible thing that switches rooms."""
    def __init__(self, dest):
        """Which room does this transport you to?"""
        pass
