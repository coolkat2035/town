import pygame
pygame.init()

class Node:
    WINDOW_SIZE = (1080, 720)
    WINDOW_AREA = pygame.Rect(0,0,WINDOW_SIZE[0], WINDOW_SIZE[1])
    FPS = 60
    
    #base node, might add in things
    def __init__(self):
        self.win = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Bro?")
        pygame.display.set_icon(pygame.image.load("icon.ico"))
    
    def ProcessInput(self, events, pressed_keys):
        print("handles events and pressed keys.")

    def Update(self):
        print("actual logic")

    def Render(self, screen):
        print("draw stuff")

    