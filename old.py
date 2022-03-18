import os
import pygame as pygame

#TODO: add spritesheet system
#switch rooms
#hitbox
#hitbox per room

#initalize
pygame.init()

win = pygame.display.set_mode((1080,720))

icon = pygame.image.load(os.path.join("stuff","icon.png"))

pygame.display.set_icon(icon)
pygame.display.set_caption("KTLS")

clock = pygame.time.Clock()

#photos    
chr_WalkRight = [pygame.image.load(os.path.join("stuff","chr_R1.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_R2.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_R3.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_R4.png")).convert_alpha()]
chr_WalkLeft = [pygame.image.load(os.path.join("stuff","chr_L1.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_L2.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_L3.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_L4.png")).convert_alpha()]
chr_WalkFront = [pygame.image.load(os.path.join("stuff","chr_F1.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_F2.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_F3.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_F4.png")).convert_alpha()]
chr_WalkBack = [pygame.image.load(os.path.join("stuff","chr_B1.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_B2.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_B3.png")).convert_alpha(), pygame.image.load(os.path.join("stuff","chr_B4.png")).convert_alpha()]
bg = pygame.image.load(os.path.join("stuff","bg_gate.png"))

#Character apperance
x = 400
y = 400
vel = 5

#Character Direction
dir = 0
walkCount = 0

pygame.font.init()
def Update():
    '''Redraws the game window and {left0 back1 right2 front3}'''
    global walkCount
    
    win.blit(bg, (0, 0))

    walkCount = walkCount % 12
    print(walkCount)

    if dir == 0:
        win.blit(chr_WalkLeft[walkCount//3], (x,y))
        
    elif dir == 2:
        win.blit(chr_WalkRight[walkCount//3], (x,y))
        
    elif dir == 1:
        win.blit(chr_WalkBack[walkCount//3], (x,y))

    elif dir == 3:
        win.blit(chr_WalkFront[walkCount//3], (x,y))
        
    pygame.display.update()


#################################################################################################################################################
# mainloop

run = True
while run:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    modkeys = pygame.key.get_mods()

    if modkeys & pygame.KMOD_SHIFT:
        vel = 30
    else:
        vel = 10
        
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        dir = 0
        walkCount += 1
        
    if keys[pygame.K_RIGHT] and x < 995:
        x += vel
        dir = 2
        walkCount += 1
        
    if keys[pygame.K_UP] and y > vel:
        y -= vel
        dir = 1
        walkCount += 1
    
    if keys[pygame.K_DOWN] and y < 565:
        y += vel
        dir = 3
        walkCount += 1

    else:
        walkCount = 0


    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    Update()
#------------------------------------------------------------------real thing------------------------------------------------------#

    
    
    
pygame.quit()


