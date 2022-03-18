from _modules import *

#TODO: 

#bg sprites? how to group them
#switch rooms

#hitbox per room
#animation fps

#fix animation problem, anim counter doesnt increment [done]
#add spritesheet system [done]
#hitbox[done]

root = Node()#change window size in node.py
clock = pygame.time.Clock()

player = Player("me",
                (0,0, 80, 150),
                Sprite("player", (0,0), 0, spritesheet("player", "player.png")),
                Hitbox("player", (0,90), (80,60)))
#name, starting xywh, sprite(name, offset, sheet(id, file)), hitbox(name, offset, size)

yee = StaticRoom((0, 0), 1, "stuff/bg_gate.png", player)
quack = ScrollRoom((0,0), 2, (2000,720), "stuff/bg_hscroll.png", player)
bruh = ScrollRoom((0, -1480), 3, (1080,2200), "stuff/bg_vscroll.png", player)

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
                alt_pressed = keys[pygame.K_LALT] or keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
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


run_game(root.FPS, quack)
