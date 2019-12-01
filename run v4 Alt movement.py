#movement variables fixed
#Collision fixed
#GET TILE BASED MOVEMENT
#Hey look at that, tile based kinda works, now fix the collision/stack issue
#Collision fixed, get changing floors to work / render differnt maps from maps.py -> updated to legacy_map.py
#Tidy up movement variables/if statements

#May require re-writing to enable storing map in a 3D list, also tilemap will no longer work with updated variables

import contextlib
with contextlib.redirect_stdout(None):
    import pygame,sys,os,spritesheet,var,legacy_map
    from pygame.locals import *
ss = spritesheet.spritesheet('spritesheet.png')
player_x, player_y=300,300
move_left, move_right, move_up, move_down, sprint=False, False, False, False, 1
os.environ['SDL_VIDEO_CENTERED'] = '1'
##os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
pygame.init()
g=pygame.display.set_mode([1280,720])
pygame.display.set_caption("Tilemap")
clock=pygame.time.Clock()

player_x, player_y,player_goto_x,player_goto_y,key_delay=300,300,300,300,0

def events():
        global move_left, move_right, move_up, move_down, sprint
        for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT or event.key == ord('a'):
                                move_left=True
                        if event.key == pygame.K_RIGHT or event.key == ord('d'):
                                move_right=True
                        if event.key == pygame.K_UP or event.key == ord('w'):
                                move_up = True
                        if event.key == pygame.K_DOWN or event.key == ord('s'):
                                move_down=True
                        if event.key == pygame.K_LSHIFT:
                                sprint=True

                elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == ord('a'):
                                move_left=False
                        if event.key == pygame.K_RIGHT or event.key == ord('d'):
                                move_right=False
                        if event.key == pygame.K_UP or event.key == ord('w'):
                                move_up=False
                        if event.key == pygame.K_DOWN or event.key == ord('s'):
                                move_down=False
                        if event.key == pygame.K_LSHIFT:
                                sprint=False

def col(player_x,player_y,player_goto_y,player_goto_x):                 #Collision detection
    if player_goto_x<0:
            player_x+=5
            player_goto_x += 100
    if player_goto_y<0:
            player_y+=5
            player_goto_y += 100
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] not in whitelist) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist):                  #Collision Top
            player_y+=5
            player_goto_y += 100
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] not in whitelist) and (tilemap[int((player_y+99)/var.tilesize)][int(player_x/var.tilesize)] not in whitelist):                  #Collision Left
            player_x+=5
            player_goto_x += 100
    if (tilemap[int((player_y+99)/var.tilesize)][int(player_x/var.tilesize)] not in whitelist) and (tilemap[int((player_y+99)/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist):        #Collision Botom
            player_y-=5
            player_goto_y -= 100
    if (tilemap[int((player_y+99)/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist):        #Collision Right
            player_x-=5
            player_goto_x -= 100
    event_tile(player_x,player_y,player_goto_x,player_goto_y)
    return player_x,player_y,player_goto_x,player_goto_y

def event_tile(player_x,player_y,player_goto_x,player_goto_y):          #Stairs/doors etc anything that requires the tileset to be changed
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] in trigger) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] in trigger) and player_goto_x == player_x and player_goto_y == player_y:
        player_goto_y += 100
        #Find door co-ords of new map, then +100 to the y axis to come "Up/Down" the stairs
    return player_x,player_y,player_goto_x,player_goto_y


tilemap = legacy_map.bedroom

whitelist=[15,83,45,46]
trigger=[83]

colours = {}
i=0
for img_row in range(0,10):
    for img_column in range(0,15):
        colours[i]=ss.image_at((img_column*16, img_row*16, 16, 16))
        i+=1


mapwidth=len(tilemap[0])
mapheight=len(tilemap)

while True:
    if move_right == True and player_goto_x == player_x and player_goto_y == player_y and key_delay > 20:
        key_delay=0
        player_goto_x+=100
    if move_left == True and player_goto_x == player_x and player_goto_y == player_y and key_delay > 20:
        key_delay=0
        player_goto_x -= 100
    if move_up == True and player_goto_x == player_x and player_goto_y == player_y and key_delay > 20:
        key_delay=0
        player_goto_y -= 100
    if move_down == True and player_goto_x == player_x and player_goto_y == player_y and key_delay > 20:
        key_delay=0
        player_goto_y += 100

    key_delay+=1
    if player_x!=player_goto_x:
        if player_x>player_goto_x:
            player_x-=5
        else:
            player_x+=5
    if player_y!=player_goto_y:
        if player_y>player_goto_y:
            player_y-=5
        else:
            player_y+=5

    events()                                                                                                                                                            #Calls key presses
    clock.tick(75)
    framerate = str(int(clock.get_fps()))
    player_x,player_y,player_goto_x,player_goto_y=col(player_x,player_y,player_goto_y,player_goto_x)                                                                    #Calls collision detection
    player_x,player_y,player_goto_x,player_goto_y=event_tile(player_x,player_y,player_goto_x,player_goto_y)                                                             #Calls event detection
    pygame.draw.rect(g, (80,80,80), [0,0,1280,720],0 )       #Grey Background
    for row in range(mapheight):
        for column in range(mapwidth):
            g.blit(colours[tilemap[row][column]],((column*var.tilesize+(player_x*-1))+640-(var.tilesize/2),(row*var.tilesize+(player_y*-1))+360-(var.tilesize/2)))      #Draw tiles
    pygame.draw.rect(g, (225,50,50),[640-(var.tilesize/2),360-(var.tilesize/2),var.tilesize,var.tilesize])                                                              #Draw "player" ####Change to image####
    font=pygame.font.SysFont("Sans MS", 30)
    text = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('green'))                                                                                   #Framerate counter
    g.blit(text, (0,0))
    pygame.display.flip()



















