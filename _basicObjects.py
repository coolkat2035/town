import pygame, json, os
from _node import Node
from json.decoder import JSONDecodeError
import pygame

#immovables, interactable, npc, player
#how to set player starring position per room
#dialogue box? how to make interactables

#add placeholder greenbox if sprite is none: how to decide size? [done]

#add testing furniture: clock, table, bed, desk (your room)

#moving bg: clouds?
#player diagonal direction?

class AnimNotFoundError(Exception):
    #lol
    pass

class Hitbox(Node):
    """Collision controller"""
    def __init__(self, offset, size, tang:bool):
        """name?, offset from the player object, width and height"""
        self.oX = offset[0]
        self.oY = offset[1]
        self.w = size[0]
        self.h = size[1]
        self.rect = pygame.Rect(self.oX, self.oY, size[0], size[1]) #the object, if anyone wants
        self.isTangible = tang

    def Render(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.rect, 2)

    def isCollide(self, other):
        return pygame.Rect.colliderect(self.rect, other.rect)

    '''def __repr__(self):
        return str(self.__dict__)
        return f"{self.name}, at ({self.oX}, {self.oY}, {self.w}, {self.h})"'''
    #do update in player, easier to calc position

class StaticSprite(pygame.sprite.Sprite, Node):
    def __init__(self, spr:str, group = None):
        """Makes a sprite from the given filename"""
        super().__init__()

        #placeholder setup, a green rectangle if there is no image
        if spr == None:
            self.image = pygame.Surface(self.WINDOW_SIZE)# should be cropped in obj class
            self.image.fill((0,255,0))
        else:
            self.image = pygame.image.load(spr) #Surface object
           
class AnimSprite(pygame.sprite.Sprite):
    """An animation controller with multiple animations."""
    def __init__(self, charname:str, filename:str, fps):
        super().__init__()
        try:
            #meta
            self.filename = filename
            self.fps = fps

            #data
            self.image = pygame.image.load(self.filename) #image sprite sheet
            self.charname = charname #character name (name_walk0001.png)
            self.sheet = None #json sprite sheet

            self.curAnim = [] #current pygame surface obj list
            self.curAnimName = None #string
            self.frame_count = 0
            self.curFrame = None #surface object to blit lol

            with open(f"{os.path.splitext(self.filename)[0]}.json",'r', encoding = 'utf-8-sig') as s:
                self.sheet = json.loads(s.read())
            self.rect = () #what's this

        except pygame.error:
            print(f"{filename} doesn't exist.")
            raise SystemExit

        except JSONDecodeError:#a weird code at the beginning
            print("Is this JSON???")

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle:tuple, colorkey = None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)#here is very importatent
        image.blit(self.image, (0, 0), rect)
        if colorkey != None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def getAnimByKey(self, key:str):
        "returns a list of surface objects made by image_at, sets my rectangle to frame size"
        _wrong_counter = 0
        self.curAnim = [] #clear everything

        for frame in self.sheet["frames"]:
            #very efficient way to check if animation exists
            if frame.startswith(f"{self.charname}_{key}"):
                #print(f"adding: {frame}")
                self.curAnim.append(self.image_at((
                    self.sheet["frames"][frame]["frame"]['x'],
                    self.sheet["frames"][frame]["frame"]['y'],
                    self.sheet["frames"][frame]["frame"]['w'],
                    self.sheet["frames"][frame]["frame"]['h']))
                    )
                    #json parsing epic!!!!
            else:
                _wrong_counter += 1
        if _wrong_counter == len(self.sheet["frames"]):
            #nothing is found
            raise AnimNotFoundError(f"""
            $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            ANIMATION [{key}] NOT [[Found]]!!!!!
            $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$""")
        
        self.rect = pygame.Rect(self.sheet["frames"][f"{self.charname}_{key}0000"]["spriteSourceSize"]['x'],
                                self.sheet["frames"][f"{self.charname}_{key}0000"]["spriteSourceSize"]['y'],
                                self.sheet["frames"][f"{self.charname}_{key}0000"]["spriteSourceSize"]['w'],
                                self.sheet["frames"][f"{self.charname}_{key}0000"]["spriteSourceSize"]['h'])

        return self.curAnim

    def setAnim(self, name):
        self.curAnim = self.getAnimByKey(name)
        self.curAnimName = name


