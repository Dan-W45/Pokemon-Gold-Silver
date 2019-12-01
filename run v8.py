import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, os, ast, spritesheet, var, time
    from pygame.locals import *

pygame.mixer.pre_init(buffer=2048)
pygame.mixer.init()
pygame.mixer.music.set_volume(0.15)
##pygame.mixer.music.load("sounds/Load_song.mp3")
##pygame.mixer.music.play(1)
##time.sleep(24)
pygame.mixer.music.load("sounds/12 new bark town.mp3")
pygame.mixer.music.play(-1)

ssm=spritesheet.spritesheet('spritesheet.png')
ssp=spritesheet.spritesheet('playersheet.png')
player_x, player_y,player_goto_x,player_goto_y,key_delay=300,300,300,300,0
ani_stage, frame_cycle = 0, 0
move_left, move_right, move_up, move_down = False, False, False, False
display_fps = True

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

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mouse.set_visible(True)                                                  #Show/Hide the mouse in the pygame window
pygame.init()
g=pygame.display.set_mode([1280,720])
pygame.display.set_caption("Tilemap")
clock=pygame.time.Clock()

colours = {}
player_sheet = {}
def spritesheet_divider(map_data):
    global colours
    i=0
    for img_row in range(map_data[3], map_data[4]):
        for img_column in range(map_data[5], map_data[6]):
            colours[i]=ssm.image_at((img_column*16, img_row*16, 16, 16))
            i+=1

spritesheet_divider(('bedroom',700,0, 0,10, 0,15))

i=0
for player_row in range(4):
    for player_column in range(4):
        player_sheet[i]=ssp.image_at((player_column*16, player_row*16, 16, 16))
        player_sheet[i].set_colorkey((0,255,0))                                 #Sets colour green to transparent
        i+=1
def events():
    global move_up, move_down, move_left, move_right, player_goto_x
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
        player_x+=5
        player_goto_x+=100
    if player_goto_y<0:
        key_delay=0
        player_y+=5
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
        if player_x>player_goto_x:                                      #Going left
            player_x-=5
            if frame_cycle >= 10:
                if ani_stage < 4 or ani_stage >= 8:
                    ani_stage = 4
                ani_stage +=1
                frame_cycle = 0
                if ani_stage >= 8:
                    ani_stage = 4
        else:                                                           #Going right
            player_x+=5
            if frame_cycle >= 10:
                if ani_stage < 8 or ani_stage >= 12:
                    ani_stage = 8
                ani_stage +=1
                frame_cycle = 0
                if ani_stage >= 12:
                    ani_stage = 8
    if player_y!=player_goto_y:                                         #Going up
        if player_y>player_goto_y:
            player_y-=5
            if frame_cycle >= 10:
                if ani_stage < 12 or ani_stage >= 16:
                    ani_stage = 12
                ani_stage +=1
                frame_cycle = 0
                if ani_stage >= 16:
                    ani_stage = 12
        else:                                                           #Going down
            player_y+=5
            if frame_cycle >= 10:
                if ani_stage >= 4:
                    ani_stage = 0
                ani_stage +=1
                frame_cycle = 0
                if ani_stage >= 4:
                    ani_stage = 0

    frame_cycle += 1
    key_delay+=1
    events()
    clock.tick(75)
    pygame.draw.rect(g, (80,80,80), [0,0,1280,720],0 )       #Grey Background
    player_x, player_y, player_goto_x, player_goto_y=col(player_x, player_y, player_goto_x, player_goto_y)                                                              #Calls collision detection
    player_x,player_y,player_goto_x,player_goto_y = event_tile(player_x,player_y,player_goto_x,player_goto_y)
    mapwidth=len(tilemap[0])
    mapheight=len(tilemap)

    for row in range(mapheight):
        for column in range(mapwidth):
            g.blit(colours[tilemap[row][column]],((column*var.tilesize+(player_x*-1))+640-(var.tilesize/2),(row*var.tilesize+(player_y*-1))+360-(var.tilesize/2)))      #Draw tiles

    g.blit(player_sheet[ani_stage], (590,285))                                                                                                                          #Drawer player
    if display_fps == True:
        font=pygame.font.SysFont("Sans MS", 30)
        text = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('green'))                                                                               #Framerate counter
        g.blit(text, (0,0))
    pygame.display.flip()





















