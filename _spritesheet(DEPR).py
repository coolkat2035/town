#should make a list of animatins, just return when neeeded [is it really needed]

#identify different animations for same chara[done]

#Stolen from https://www.pygame.org/wiki/Spritesheet

import json
from json.decoder import JSONDecodeError
import pygame
import os

class AnimNotFoundError(Exception):
    pass

class AnimSprite(pygame.sprite.Sprite):
    """An animation controller with multiple """
    def __init__(self, charname:str, filename:str, fps):
        try:
            self.filename = filename
            self.fps = fps

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

if __name__ == "__main__":
    if True:
        #DEBUBGGIBNG PURPOSE OBNLY
        #SETTINGS
        pygame.init()
        win = pygame.display.set_mode((720,540))
        pygame.display.set_caption("sad")

        person = spritesheet("player","player.png")
        animation = person.getAnimByKey("left")
        anim_counter = 0

        print(animation)
        run = True
        while run:
            for event in pygame.event.get():#single button presses
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    anim_counter = 0
                    match event.key:
                        case pygame.K_LEFT:
                            animation = person.getAnimByKey("left")
                            print("left")

                        case pygame.K_RIGHT:
                            animation = person.getAnimByKey("right")
                            print("right")

                        case pygame.K_UP:
                            animation = person.getAnimByKey("back")
                            print("up")
                        
                        case pygame.K_DOWN:
                            animation = person.getAnimByKey("front")
                            print("down")

            anim_counter = round(pygame.time.get_ticks() / (1000/12)) % len(animation)
            win.fill((0,255,0))
            win.blit(animation[anim_counter], (0,0))
            pygame.display.flip()

        pygame.quit()
    print("\nHey! You should be running your main program, not this one!!!")
