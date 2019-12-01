#Working spritesheet map

import contextlib
with contextlib.redirect_stdout(None):
    import pygame,sys,os,spritesheet,var
    from pygame.locals import *
ss = spritesheet.spritesheet('spritesheet.png')
player_y, player_x=0,0
move_left, move_right, move_up, move_down, sprint=False, False, False, False, False
os.environ['SDL_VIDEO_CENTERED'] = '1'
##os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
pygame.init()
g=pygame.display.set_mode([1280,720])
pygame.display.set_caption("Tilemap")
clock=pygame.time.Clock()
speed = 1
def events():
        global move_left, move_right, move_up, move_down, sprint
        for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT or event.key == ord('a'):
                                move_right=True
                        if event.key == pygame.K_RIGHT or event.key == ord('d'):
                                move_left=True
                        if event.key == pygame.K_UP or event.key == ord('w'):
                                move_up = True
                        if event.key == pygame.K_DOWN or event.key == ord('s'):
                                move_down=True
                        if event.key == pygame.K_LSHIFT:
                                sprint=True

                elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == ord('a'):
                                move_right=False
                        if event.key == pygame.K_RIGHT or event.key == ord('d'):
                                move_left=False
                        if event.key == pygame.K_UP or event.key == ord('w'):
                                move_up=False
                        if event.key == pygame.K_DOWN or event.key == ord('s'):
                                move_down=False
                        if event.key == pygame.K_LSHIFT:
                                sprint=False

tilemap=[[000,000,4,000,2,3,41,83],
         [15,15,19,20,32,18,15,15],
         [15,15,45,46,15,15,15,15],             #Convert this to use a txt or we're gonna have a problem
         [15,15,15,15,15,15,15,15],
         [40,15,15,15,30,31,15,15],             #save to legacy_map.py once confirmed working
         [55,15,15,15,45,46,15,15]]


colours = {}
i=0
for img_row in range(0,10):
    for img_column in range(0,15):
##        print(img_row*16, img_column*16)
        colours[i]=ss.image_at((img_column*16, img_row*16, 16, 16))
        i+=1




mapwidth=len(tilemap[0])
mapheight=len(tilemap)
##print(colours)

while True:
    if sprint == True:
        speed = 2
    else:
        speed = 1
    if move_right == True:
        player_x += 5*speed
    if move_left == True:
        player_x -= 5*speed
    if move_up == True:
        player_y += 5*speed
    if move_down == True:
        player_y -= 5*speed
    events()
    clock.tick(75)
    pygame.draw.rect(g, (50,50,50), [0,0,1280,720],0 )       #temp Background
    for row in range(mapheight):
        for column in range(mapwidth):
            g.blit(colours[tilemap[row][column]],((column*var.tilesize+player_x)+640-(var.tilesize/2),(row*var.tilesize+player_y)+360-(var.tilesize/2)))
    pygame.draw.rect(g, (225,50,50),[640-(var.tilesize/2),360-(var.tilesize/2),var.tilesize,var.tilesize])
    font=pygame.font.SysFont("Sans MS", 30)
    text = font.render(str(int(clock.get_fps())), True, pygame.Color('green'))
    g.blit(text, (0,0))
    pygame.display.flip()



















