import pygame,sys,spritesheet
from pygame.locals import *
player_y, player_x=0,0
move_left, move_right, move_up, move_down, sprint=False, False, False, False, False
pygame.init()

g=pygame.display.set_mode([1280,720])
pygame.display.set_caption("Tilemap")
clock=pygame.time.Clock()

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


tilemap=[[1,3,0],[2,2,1],[3,1,2],[0,2,3],[1,2,0]]
colours = {
    0:(153,76,0),
    1:(0,255,0),
    2:(0,0,255),
    3:(0,0,0)}
tilesize=40
mapwidth=len(tilemap[0])
mapheight=len(tilemap)

while True:
    if move_right == True:
        player_x -= 5
    if move_left == True:
        player_x += 5
    if move_up == True:
        player_y -= 5
    if move_down == True:
        player_y += 5
    events()
    clock.tick(60)
    pygame.draw.rect(g, (255,255,255), [0,0,1280,720],0 )       #temp Background
    for row in range(mapheight):
        for column in range(mapwidth):
            pygame.draw.rect(g,colours[tilemap[row][column]],(column*tilesize+player_x,row*tilesize+player_y, tilesize,tilesize))
    pygame.display.flip()

