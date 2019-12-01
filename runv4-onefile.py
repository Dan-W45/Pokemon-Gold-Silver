#movement variables fixed
#Collision fixed
#GET TILE BASED MOVEMENT

import contextlib
with contextlib.redirect_stdout(None):
    import pygame,sys,os,var##,spritesheet
    from pygame.locals import *
player_y, player_x=0,0
move_left, move_right, move_up, move_down, sprint=False, False, False, False, False
os.environ['SDL_VIDEO_CENTERED'] = '1'
##os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
pygame.init()
g=pygame.display.set_mode([1280,720])
pygame.display.set_caption("Tilemap")
clock=pygame.time.Clock()
tilesize = 100

class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error:
            print ('Unable to load spritesheet image:'), filename
            raise SystemExit
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        image = pygame.transform.scale(image, (tilesize, tilesize))
        return image

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
def col(player_x,player_y):
    if player_x<0:
            player_x+=5
    if player_y<0:
            player_y+=5
    if (tilemap[int(player_y/tilesize)][int(player_x/tilesize)] not in whitelist) and (tilemap[int(player_y/tilesize)][int((player_x+99)/tilesize)] not in whitelist):
            ##print("You done goofed (TOP)")
            player_y+=5
    if (tilemap[int(player_y/tilesize)][int(player_x/tilesize)] not in whitelist) and (tilemap[int((player_y+99)/tilesize)][int(player_x/tilesize)] not in whitelist):
            ##print("You done goofed (LEFT)")
            player_x+=5
    if (tilemap[int((player_y+99)/tilesize)][int(player_x/tilesize)] not in whitelist) and (tilemap[int((player_y+99)/tilesize)][int((player_x+99)/tilesize)] not in whitelist):
            ##print("You done goofed (Bottom)")
            player_y-=5
    if (tilemap[int((player_y+99)/tilesize)][int((player_x+99)/tilesize)] not in whitelist) and (tilemap[int(player_y/tilesize)][int((player_x+99)/tilesize)] not in whitelist):
            ##print("You done goofed (Right)")
            player_x-=5
    return player_x,player_y
tilemap=[[000,000,4,000,2,3,41,83,82],
         [15,15,19,20,32,18,15,15,82],
         [15,15,45,46,15,15,15,15,82],             #Convert this to use a txt or we're gonna have a problem
         [15,15,15,15,15,15,15,15,82],
         [40,15,15,15,30,31,15,15,82],
         [55,15,15,15,45,46,15,15,82],
         [82,82,82,82,82,82,82,82,82]]

whitelist=[15,83,45,46]

ss = spritesheet('spritesheet.png')

colours = {}
i=0
for img_row in range(0,10):
    for img_column in range(0,15):
##        print(img_row*16, img_column*16)
        colours[i]=ss.image_at((img_column*16, img_row*16, 16, 16))
        i+=1


colours[1]=ss.image_at((0, 16, 32, 32))

##colours = {
##    0:ss.image_at((0, 0, 16, 16)),
##    1:ss.image_at((16, 0, 16, 16)),
##    2:ss.image_at((32, 0, 16, 16)),
##    3:ss.image_at((48, 0, 16, 16)),           #old stuff i dont want to get rid of
##    4:ss.image_at((64, 0, 16, 16)),
##    5:ss.image_at((0, 16, 16, 16))}
mapwidth=len(tilemap[0])
mapheight=len(tilemap)

while True:
    if move_right == True:
        player_x += 5
    if move_left == True:
        player_x -= 5
    if move_up == True:
        player_y -= 5
    if move_down == True:
        player_y += 5
    events()
    clock.tick(75)
##    print(int(player_y/var.tilesize), int(player_x/var.tilesize), int((player_y+99)/var.tilesize), int((player_x+99)/var.tilesize))
##    print(tilemap[int(player_y/var.tilesize)][int(player_x/var.tilesize)],tilemap[int((player_y+99)/var.tilesize)][int((player_x+99)/var.tilesize)])
    player_x,player_y=col(player_x,player_y)
    framerate = str(int(clock.get_fps()))
    pygame.draw.rect(g, (80,80,80), [0,0,1280,720],0 )       #not so temp Background
    for row in range(mapheight):
        for column in range(mapwidth):
            g.blit(colours[tilemap[row][column]],((column*tilesize+(player_x*-1))+640-(tilesize/2),(row*tilesize+(player_y*-1))+360-(tilesize/2)))
    pygame.draw.rect(g, (225,50,50),[640-(tilesize/2),360-(tilesize/2),tilesize,tilesize])
    font=pygame.font.SysFont("Sans MS", 30)
    text = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('green'))
    g.blit(text, (0,0))
    pygame.display.flip()



















