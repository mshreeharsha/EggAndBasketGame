import pygame
import random
pygame.font.init()

WIDTH,HEIGHT= 800,600
BWIDTH,BHEIGHT = 150,70
EWIDTH,EHEIGHT = 30,30
RED=(255,0,0)
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Egg And Basket Game")
FPS=60
VEL=10
E_VEL=7
EGG_CAPTURED = pygame.USEREVENT + 1
EGG_MISSED = pygame.USEREVENT + 2
END_MESSAGE=pygame.font.SysFont("comicsans",25)
SCORELIVES=pygame.font.SysFont("comicsans",20)


SCENARY= pygame.transform.scale(pygame.image.load("background.jpg"),(WIDTH,HEIGHT))
BASKET=pygame.transform.scale(pygame.image.load("basket.jpg"),(BWIDTH,BHEIGHT))
EGG=pygame.transform.scale(pygame.image.load("egg.png"),(EWIDTH,EHEIGHT))

def drawgameendtext(game_text,score):
    text=END_MESSAGE.render(game_text,1,RED)
    WIN.blit(text,(WIDTH/2 - text.get_width()/2,HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def egg_handle(NUMBER,egg,basket):
    for e in NUMBER:
        e.y += E_VEL

        if basket.colliderect(e):
            pygame.event.post(pygame.event.Event(EGG_CAPTURED))
            NUMBER.remove(e)
        elif e.y > HEIGHT:
            pygame.event.post(pygame.event.Event(EGG_MISSED))
            NUMBER.remove(e)
        


def basketmovement(keys,basket):
    if keys[pygame.K_RIGHT] and basket.x + BWIDTH < WIDTH:
        basket.x += VEL
    if keys[pygame.K_LEFT] and basket.x >0:
        basket.x -= VEL

def redrawwindow(basket,NUMBER,score,lives,level):
    WIN.blit(SCENARY,(0,0))
    WIN.blit(BASKET,(basket.x,basket.y))

    for egg in NUMBER:
        WIN.blit(EGG,(egg.x,egg.y))
    SCORE_TEXT=SCORELIVES.render(f"Score : {score}",1, RED)
    LIVES_TEXT=SCORELIVES.render(f"Lives : {lives}",1, RED)
    LEVEL_TEXT=SCORELIVES.render(f"Level : {level}",1, RED)
    WIN.blit(SCORE_TEXT,(10,SCORE_TEXT.get_height()+10))
    WIN.blit(LEVEL_TEXT,(WIDTH/2 - LEVEL_TEXT.get_width()/2,LEVEL_TEXT.get_height()+10))
    WIN.blit(LIVES_TEXT,(WIDTH- 10-LIVES_TEXT.get_width(),SCORE_TEXT.get_height()+10))
    pygame.display.update()

def main():

    basket=pygame.Rect(WIDTH/2 - BWIDTH/2 , HEIGHT- BHEIGHT -10, BWIDTH, BHEIGHT)
    NUMBER=[]
    lives=3
    score=0
    level=1

    running =True
    clock=pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == EGG_CAPTURED:
                score+=1

            if event.type == EGG_MISSED:
                lives-=1
        
        clock.tick(FPS)
        if len(NUMBER)<level:
            x_coor=random.randint(10, WIDTH-EWIDTH-10)
            egg = pygame.Rect(x_coor, 50,EWIDTH,EHEIGHT)
            NUMBER.append(egg)
        

        keys=pygame.key.get_pressed()
        basketmovement(keys, basket)
        egg_handle(NUMBER,egg,basket)
        redrawwindow(basket,NUMBER,score,lives,level)
        
        if score > level*(15):
            level+=1
            lives+=3

        if lives <=0:
            drawgameendtext(f"You LOST !! Your SCORE : {score}",score)
            break

    main()
        
if __name__=="__main__":
    main()