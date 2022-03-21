from _modules import *

#TODO: 

#bg sprites? how to group them
#switch rooms

#hitbox per room [ongoing]
#animation fps

#add readme

#fix animation problem, anim counter doesnt increment [done]
#add spritesheet system [done]
#hitbox[done]

root = Node()#change window size in node.py
clock = pygame.time.Clock()

player = Player(
    "me",
    (0,0, 80, 150),
    AnimSprite("player", "stuff/player.png", 4),
    Hitbox((0,90), (80,60)),
    Checker((80,60))
    )

objects = (
    Object("wall1", (0,0,1080,220), StaticSprite(None), Hitbox((0,150), (1080, 70))),
    Object("bed1", (0,140,205,430), StaticSprite("stuff/obj_bed.png"), Hitbox((0,0), (205,430)))
    )

yee = StaticRoom((0, 0),"stuff/bg_normal.png", player, (540, 360), 3, objects)

long = ScrollRoom((-500,0), "stuff/bg_hscroll.png", player, (200, 300), 0)
tall = ScrollRoom((0, -1480), "stuff/bg_vscroll.png", player, (540, 600), 2)
chung = ScrollRoom((-350, -215), "stuff/bg_big.png", player, (540, 360), 1)

def run_game(fps, starting_scene:Room):
    global win
    active_scene = starting_scene

    while active_scene != None:
        keys = pygame.key.get_pressed()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and (keys[pygame.K_LALT] or keys[pygame.K_RALT]):
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, keys)
        active_scene.Update()
        active_scene.Render(root.win)

        active_scene = active_scene.next
        
        pygame.display.flip()
        clock.tick(fps)


run_game(root.FPS,yee)
