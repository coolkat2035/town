import os, pygame
pygame.init()
win = pygame.display.set_mode((1080,720))

run = True

png = pygame.image.load(os.path.join("C:\Python\Works\ktlms\stuff", "bg_1a.png"))

while run:
    for a in pygame.event.get():
        if a.type == pygame.QUIT:
            run = False

    win.blit(png,(0,0))
    pygame.display.update()

pygame.quit()
