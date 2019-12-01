##Holding keys down broken
##Colision not implemented
##Colision & holding keys fixed

import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, os, spritesheet, var, legacy_map
    from pygame.locals import *
ss=spritesheet.spritesheet('spritesheet.png')
player_x, player_y,player_goto_x,player_goto_y,key_delay=300,300,300,300,0
move_left, move_right, move_up, move_down = False, False, False, False
face_left, face_right, face_up, face_down = False, False, False, True
tilemap = legacy_map.bedroom
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
g=pygame.display.set_mode([1280,720])
pygame.display.set_caption("Tilemap")
clock=pygame.time.Clock()

colours = {}
i=0
for img_row in range(10):
    for img_column in range(15):
        colours[i]=ss.image_at((img_column*16, img_row*16, 16, 16))
        i+=1

def events(legacy_map):
    global move_up, move_down, move_left, move_right, player_goto_x, face_left, face_right, face_up, face_down, tilemap
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                move_up = True
                face_left, face_right, face_up, face_down = False, False, True, False
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                move_down = True
                face_left, face_right, face_up, face_down = False, False, False, True
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                move_left = True
                face_left, face_right, face_up, face_down = True, False, False, False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                move_right = True
                face_left, face_right, face_up, face_down = False, True, False, False
            if event.key == ord('q'):
                tilemap = legacy_map.downstairs
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == ord('w'):
                move_up = False
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                move_down = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                move_left = False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                move_right = False

def col(player_x, player_y, player_goto_x, player_goto_y):
    whitelist=[15,16,83,45,46,21,22]
    global key_delay
    if player_goto_x<0:
        key_delay=0
        player_goto_x+=100
    if player_goto_y<0:
        key_delay=0
        player_goto_y+=100
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] not in whitelist) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist):                  #Collision Top
        key_delay=0
        player_y += 5
        player_goto_y += 100
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] not in whitelist) and (tilemap[int((player_y+99)/var.tilesize)][int(player_x/var.tilesize)] not in whitelist):                  #Collision Left
        key_delay=0
        player_x += 5
        player_goto_x += 100
    if (tilemap[int((player_y+99)/var.tilesize)][int(player_x/var.tilesize)] not in whitelist) and (tilemap[int((player_y+99)/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist):        #Collision Botom
        key_delay=0
        player_y -= 5
        player_goto_y -= 100
    if (tilemap[int((player_y+99)/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist):        #Collision Right
        key_delay=0
        player_x -= 5
        player_goto_x -= 100
    return player_x, player_y, player_goto_x, player_goto_y

def event_tile(player_x,player_y,player_goto_x,player_goto_y):
    global tilemap, legacy_map
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] == 83) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] == 83) and player_goto_x == player_x and player_goto_y == player_y:
        player_goto_y+=100
        player_x = 900
        player_goto_x = 900
        tilemap = legacy_map.downstairs
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] == 22) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] == 22) and player_goto_x == player_x and player_goto_y == player_y:
        player_goto_y+=100
        player_x = 700
        player_goto_x = 700
        tilemap = legacy_map.bedroom
    return player_x,player_y,player_goto_x,player_goto_y

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

    key_delay+=1
    events(legacy_map)
    clock.tick(75)
    pygame.draw.rect(g, (80,80,80), [0,0,1280,720],0 )       #Grey Background
    player_x, player_y, player_goto_x, player_goto_y=col(player_x, player_y, player_goto_x, player_goto_y)                                                              #Calls collision detection
    player_x,player_y,player_goto_x,player_goto_y = event_tile(player_x,player_y,player_goto_x,player_goto_y)
    mapwidth=len(tilemap[0])
    mapheight=len(tilemap)
    for row in range(mapheight):
        for column in range(mapwidth):
            g.blit(colours[tilemap[row][column]],((column*var.tilesize+(player_x*-1))+640-(var.tilesize/2),(row*var.tilesize+(player_y*-1))+360-(var.tilesize/2)))      #Draw tiles
    pygame.draw.rect(g, (225,50,50),[640-(var.tilesize/2),360-(var.tilesize/2),var.tilesize,var.tilesize])                                                              #Draw "player" ####Change to image####
    font=pygame.font.SysFont("Sans MS", 30)
    text = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('green'))                                                                                   #Framerate counter
    g.blit(text, (0,0))
    pygame.display.flip()



















