import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, os, ast, spritesheet, var
    from pygame.locals import *
ss=spritesheet.spritesheet('spritesheet.png')
player_x, player_y,player_goto_x,player_goto_y,key_delay=300,300,300,300,0
move_left, move_right, move_up, move_down, sprint = False, False, False, False, 1
display_fps = True
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mouse.set_visible(True)                                                  #Show/Hide the mouse in the pygame window
pygame.init()
g=pygame.display.set_mode([1280,720])
pygame.display.set_caption("Tilemap")
clock=pygame.time.Clock()
colours = {}

def change_map(savename,room_data_name):
    searchfile = open("maps.txt", "r")
    for line in searchfile:
        if savename in line:
            to_tilemap=line.replace(savename,"")
            to_tilemap=to_tilemap.replace(" ","")
            to_tilemap=to_tilemap.replace("\n","")
            to_tilemap=to_tilemap.replace("=","")
            tilemap=ast.literal_eval(to_tilemap)
    searchfile.close()

    datafile = open("maps_data.txt", "r")
    for line in datafile:
        if room_data_name in line:
            to_data=line.replace(room_data_name,"")
            to_data=to_data.replace(" ","")
            to_data=to_data.replace("\n","")
            to_data=to_data.replace("=","")
            map_data=ast.literal_eval(to_data)
    datafile.close()
    return tilemap, map_data
tilemap, map_data = change_map("bedroom","bedroom_data")

def spritesheet_divider(map_data):
    global colours
    i=0
    for img_row in range(map_data[3], map_data[4]):
        for img_column in range(map_data[5], map_data[6]):
            colours[i]=ss.image_at((img_column*16, img_row*16, 16, 16))
            i+=1

spritesheet_divider(('bedroom',700,0, 0,10, 0,15))

def events():
    global move_up, move_down, move_left, move_right, player_goto_x,sprint
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                move_up = True
            elif event.key == pygame.K_DOWN or event.key == ord('s'):
                move_down = True
            elif event.key == pygame.K_LEFT or event.key == ord('a'):
                move_left = True
            elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                move_right = True
            if event.key == pygame.K_LSHIFT:
                sprint=2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == ord('w'):
                move_up = False
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                move_down = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                move_left = False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                move_right = False
            if event.key == pygame.K_LSHIFT:
                sprint=1

def col(player_x, player_y, player_goto_x, player_goto_y,sprint):
    whitelist=[15,16,83,45,46,21,22]
    global key_delay
    if player_goto_x<0:
        key_delay=0
        player_x+=5
        player_goto_x+=100/sprint
    if player_goto_y<0:
        key_delay=0
        player_y+=5
        player_goto_y+=100/sprint
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] not in whitelist) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist):                  #Collision Top
        key_delay=0
        player_y += 5
        player_goto_y += 100/sprint
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] not in whitelist) and (tilemap[int((player_y+99)/var.tilesize)][int(player_x/var.tilesize)] not in whitelist):                  #Collision Left
        key_delay=0
        player_x += 5
        player_goto_x += 100/sprint
    if (tilemap[int((player_y+99)/var.tilesize)][int(player_x/var.tilesize)] not in whitelist) and (tilemap[int((player_y+99)/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist):        #Collision Botom
        key_delay=0
        player_y -= 5
        player_goto_y -= 100/sprint
    if (tilemap[int((player_y+99)/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] not in whitelist):        #Collision Right
        key_delay=0
        player_x -= 5
        player_goto_x -= 100/sprint
    return player_x, player_y, player_goto_x, player_goto_y

def event_tile(player_x,player_y,player_goto_x,player_goto_y):
    global tilemap, legacy_map, key_delay
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] == 83) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] == 83) and player_goto_x == player_x and player_goto_y == player_y:
        tilemap, map_data = change_map("downstairs","downstairs_data")
        spritesheet_divider(map_data)
        player_x = player_goto_x = map_data[1]
        player_y = player_goto_y = map_data[2]
        player_goto_y+=100
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] == 22) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] == 22) and player_goto_x == player_x and player_goto_y == player_y:
        tilemap, map_data = change_map("bedroom","bedroom_data")
        spritesheet_divider(map_data)
        player_x = player_goto_x = map_data[1]
        player_y = player_goto_y = map_data[2]
        spritesheet_divider(map_data)
        player_goto_y+=100
    if (tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)] == 21) and (tilemap[int(player_y/var.tilesize)][int((player_x+99)/var.tilesize)] == 21) and player_goto_x == player_x and player_goto_y == player_y:
        tilemap, map_data = change_map("new_bark_town","new_bark_town_data")
        spritesheet_divider(map_data)
        player_x = player_goto_x = map_data[1]
        player_y = player_goto_y = map_data[2]
        player_goto_y+=100
    return player_x,player_y,player_goto_x,player_goto_y

while True:
    if move_right == True and player_goto_x == player_x and player_goto_y == player_y:
        key_delay=0
        player_goto_x+=100
    if move_left == True and player_goto_x == player_x and player_goto_y == player_y:
        key_delay=0
        player_goto_x -= 100
    if move_up == True and player_goto_x == player_x and player_goto_y == player_y:
        key_delay=0
        player_goto_y -= 100
    if move_down == True and player_goto_x == player_x and player_goto_y == player_y:
        key_delay=0
        player_goto_y += 100

    if player_x!=player_goto_x:
        if player_x>player_goto_x:
            player_x-=5*sprint
        else:
            player_x+=5*sprint
    if player_y!=player_goto_y:
        if player_y>player_goto_y:
            player_y-=5*sprint
        else:
            player_y+=5*sprint

    events()
    clock.tick(75)
    pygame.draw.rect(g, (80,80,80), [0,0,1280,720],0 )       #Grey Background
    player_x, player_y, player_goto_x, player_goto_y=col(player_x, player_y, player_goto_x, player_goto_y,sprint)                                                       #Calls collision detection
    player_x,player_y,player_goto_x,player_goto_y = event_tile(player_x,player_y,player_goto_x,player_goto_y)
    mapwidth=len(tilemap[0])
    mapheight=len(tilemap)

    for row in range(mapheight):
        for column in range(mapwidth):
            g.blit(colours[tilemap[row][column]],((column*var.tilesize+(player_x*-1))+640-(var.tilesize/2),(row*var.tilesize+(player_y*-1))+360-(var.tilesize/2)))      #Draw tiles


    pygame.draw.rect(g, (225,50,50),[640-(var.tilesize/2),360-(var.tilesize/2),var.tilesize,var.tilesize])                                                              #Draw "player" ####Change to image####
    if display_fps == True:
        font=pygame.font.SysFont("Sans MS", 30)
        text = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('green'))                                                                               #Framerate counter
        g.blit(text, (0,0))
    pygame.display.flip()






















