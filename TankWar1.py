
################### importing ###########################
import pygame
from pygame.locals import *
import random
import math
pygame.init()
######################## functions and classes ##############################
def render_text(text, font,size, color,x,y):
    aprx_font=pygame.font.match_font(font)
    font = pygame.font.Font(aprx_font, size)
    textsurface = font.render(text, False, color)
    text_rect=textsurface.get_rect()
    text_rect.top=y
    text_rect.left=x
    return textsurface, (x,y)
class LSS():
    def __init__(self, x, next):
        self.x=x
        self.next=next
def Turn_order(player_count):
    first=None
    last=None
    for i in range(1,player_count+1):
        p=LSS(int(i),None)
        if first==None:
            first=p
        else:
            last.next=p
        last=p
    last.next=first
    return first
class Player(pygame.sprite.Sprite):
    def __init__(self, position, skin,player):
        pygame.sprite.Sprite.__init__(self)
        global Whose_Turn
        self.image=pygame.transform.scale(skin,(30,10))
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.mask.clear()
        self.mask.set_at((self.rect.midbottom[0]-self.rect.topleft[0],-self.rect.topleft[1]+self.rect.midbottom[1]-1))
        self.rect.x=random.randrange(40,60)+position
        self.rect.bottom=200
        self.health=100
        self.player=player
        self.power=20
        if self.player ==2:
            self.angle=135
        else:
            self.angle=45
        self.fuel=100
        self.time=pygame.time.get_ticks()
    def fire(self):
        self.fuel-=self.fuel*2+1
        projectiles.add(Projectile((self.rect.centerx,self.rect.centery), self.power,self.angle))
        sprites.add(Projectile((self.rect.centerx,self.rect.centery), self.power,self.angle))
    def changeturn(self):
        global Whose_Turn
        global delay_time
        global delay
        if Whose_Turn.x==self.player and self.fuel<=0:
            delay_time=pygame.time.get_ticks()
            delay=True
            Whose_Turn=Whose_Turn.next
            self.fuel=100
    def update(self):
        global delay_time
        global delay
        terrain=world.sprites()[0]
        Player.changeturn(self)
        key_state=pygame.key.get_pressed()
        now=pygame.time.get_ticks()
        if delay==True and now-delay_time>=1000:
            delay=False
        if self.health<=0 or self.rect.bottom+5>=display_dimentions[1]:
            Loss(self.player)
        ####### Vertical movement
        if terrain.mask.get_at((self.rect.midbottom[0],self.rect.midbottom[1]))==0:
            self.rect.bottom+=self.speed_fall
        ####### Controls
        if Whose_Turn.x==self.player and self.fuel>0 and delay==False:
            if key_state[pygame.K_a] and self.rect.left>2:
                Player.move(self, "left")
            elif key_state[pygame.K_d] and self.rect.right<display_dimentions[0]-2:
                Player.move(self,"right")
            elif key_state[pygame.K_SPACE]:
                Player.fire(self)  
            elif key_state[pygame.K_q]:
                if self.angle<180:
                    self.angle+=1
            elif key_state[pygame.K_e]:
                if self.angle>0:
                    self.angle-=1
            elif key_state[pygame.K_s]:
                if  self.power>1:
                    self.power-=1
            elif key_state[pygame.K_w]:
                if self.power<=100:
                    self.power+=1
    ######### Horizontal controled movement                     
    def move(self, direction):
        immidiate_terrain=[]
        terrain=world.sprites()[0]
        for x in range(self.rect.topleft[0]-2,self.rect.topright[0]+2):
            for y in range(self.rect.topleft[1]-4, self.rect.bottom+1):
                terrain_block=terrain.mask.get_at((x,y))
                if terrain_block==1:
                    immidiate_terrain.append((x,y))
                    break
                elif y==self.rect.bottom:
                    immidiate_terrain.append((x,y))
        self.rect.bottom=immidiate_terrain[17][1]
        index=immidiate_terrain.index((self.rect.midbottom[0],self.rect.midbottom[1]))
        if direction=="right" and immidiate_terrain[index][1]-immidiate_terrain[index+1][1]<=3:
            self.fuel-=1
            self.rect.bottom=immidiate_terrain[index+1][1]
            self.rect.centerx=immidiate_terrain[index+1][0]
        if direction=="left" and immidiate_terrain[index][1]-immidiate_terrain[index-1][1]<=3:
            self.fuel-=1   
            self.rect.bottom=immidiate_terrain[index-1][1]
            self.rect.centerx=immidiate_terrain[index-1][0]
class Terrain(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.orgimage=pygame.transform.scale(terrain_surface,display_dimentions)       
        self.mask=pygame.mask.from_surface(self.orgimage)
        self.image=self.mask.to_surface(surface=None, setsurface=None, unsetsurface=None, setcolor=(0, 255, 0, 255), unsetcolor=(0, 0, 250, 0), dest=(0, 0))
        self.rect=self.mask.get_rect()
        self.rect.bottom=display_dimentions[1]
    def update(self):
        if pygame.sprite.spritecollide(self, explosions, False, pygame.sprite.collide_mask):
            for explosion in explosions.sprites():
                self.mask.erase(explosion.mask, (explosion.rect.topleft[0],explosion.rect.topleft[1]))         
        self.image=self.mask.to_surface(surface=None, setsurface=None, unsetsurface=None, setcolor=(0, 255, 0, 255), unsetcolor=(0, 0, 250, 0), dest=(0, 0))

class explosion(pygame.sprite.Sprite):
    def __init__(self, where, size):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(boom,size)
        self.image.set_colorkey((255,255,255))
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.rect.centerx=where[0]
        self.rect.centery=where[1]
        self.time=pygame.time.get_ticks()
        self.size=size
    def update(self):
        now =pygame.time.get_ticks()
        player=players.sprites()       
        if now-self.time>100:
            for p in player:
                hitx= abs(self.rect.centerx-p.rect.centerx)
                hity= abs(self.rect.centery-p.rect.centery)
                if hitx<=self.size[0]-50 and hity<=self.size[1]-50:
                    p.health-=20
            self.kill()
class Projectile(pygame.sprite.Sprite):
    def __init__(self, who, power,angle):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(shell,(20,20))
        self.image.set_colorkey((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.left=who[0]
        self.rect.bottom=who[1]
        self.mask=pygame.mask.from_surface(self.image)
        self.who=who
        self.velocity=power
        self.mass=4
        self.angle=angle
        self.time=pygame.time.get_ticks()//1000
    def update(self):
        terrain=world.sprites()[0]
        self.rect.centerx+=math.cos(math.radians(self.angle))*3
        first_x=self.who[0]
        first_y=self.who[1]
        self.rect.centery+=((self.rect.centerx-first_x)*0.015/(self.velocity/40))**2-4*math.sin(math.radians(self.angle))
        if self.mass>-3:
            self.mass-=1/(self.velocity/4)
        if self.rect.left>display_dimentions[0] or self.rect.top>display_dimentions[1] or self.rect.right<0:
            self.kill()        
        hit=terrain.mask.overlap(self.mask,(-terrain.rect.topleft[0]+self.rect.topleft[0],-terrain.rect.topleft[1]+self.rect.topleft[1]))
        if hit != None:
            sprites.add(explosion((hit[0],hit[1]),(75,75)))
            explosions.add(explosion((hit[0],hit[1]),(75,75)))
            self.kill()
def Loss(who):
    global running
    global loser
    loser=who
    print('Player {} lost'.format(who))  
    sprites.empty()
    running=False
def GUI():
        player1=players.sprites()[0]
        player2=players.sprites()[1]
        to_blit=[]
        health_player1=render_text('Player 1 health: {} '.format(player1.health), "arialblack",16, red,display_dimentions[0]/10,display_dimentions[1]/100)
        to_blit.append(health_player1)
        angle_player1=render_text('Angle: {} '.format(player1.angle), "arialblack",16, black,display_dimentions[0]/10,display_dimentions[1]/100+24)
        to_blit.append(angle_player1)
        power_player1=render_text('Power: {} '.format(player1.power), "arialblack",16, black,display_dimentions[0]/10,display_dimentions[1]/100+48)
        to_blit.append(power_player1)
        fuel_player1=render_text('Fuel: {} '.format(player1.fuel), "arialblack",16, black,display_dimentions[0]/10,display_dimentions[1]/100+72)
        to_blit.append(fuel_player1)
        health_player2=render_text('Player 2 health: {} '.format(player2.health), "arialblack",16,red,display_dimentions[0]-display_dimentions[0]/4,display_dimentions[1]/100)
        to_blit.append(health_player2)
        angle_player2=render_text('Angle: {} '.format(player2.angle), "arialblack",16, black,display_dimentions[0]-display_dimentions[0]/4,display_dimentions[1]/100+24)
        to_blit.append(angle_player2)
        power_player2=render_text('Power: {} '.format(player2.power), "arialblack",16, black,display_dimentions[0]-display_dimentions[0]/4,display_dimentions[1]/100+48)
        to_blit.append(power_player2)
        fuel_player2=render_text('Fuel: {} '.format(player2.fuel), "arialblack",16, black,display_dimentions[0]-display_dimentions[0]/4,display_dimentions[1]/100+72)
        to_blit.append(fuel_player2)
        turn=render_text('Turn of Player {} '.format(Whose_Turn.x), "arial black",16, black,display_dimentions[0]/2-50,display_dimentions[1]/100)
        to_blit.append(turn)
        for text in to_blit:
            display_surface.blit(text[0],text[1])

######################### constants used ##########################
grey=(100,100,100)
light_grey=(200,200,200)
black=(0,0,0)
green=(0,255,0)
red=(255,0,0)
blue=(0,0,255)
white=(255,255,255)
sprites=pygame.sprite.Group()
world=pygame.sprite.Group()
projectiles=pygame.sprite.Group()
explosions=pygame.sprite.Group()
players=pygame.sprite.Group()
display_dimentions=(800,600)
fps=50

turn=1
player_count=2
game_clock=pygame.time.Clock()

display_surface=pygame.display.set_mode(display_dimentions)
boom=pygame.image.load("boom.png").convert_alpha()
game_icon= pygame.image.load("tank.gif")
terrain_surface=pygame.image.load("terrain.gif").convert()
firmament_surface=pygame.transform.scale(pygame.image.load("firmament.gif").convert_alpha(),display_dimentions)
tank1_image=pygame.image.load("tank1.gif").convert_alpha()
tank2_image=pygame.image.load("tank2.gif").convert_alpha()
shell=pygame.image.load("projectile1.png").convert_alpha()
loser=0
Whose_Turn=Turn_order(player_count)
game_over=True
running=True
delay=False
delay_time=0
########################## game loops ############################################
def main_loop():
    ##################### game intialization ########################
    terrain=Terrain()
    sprites.add(terrain)
    world.add(terrain)
    player1_tank=Player( 0, tank1_image,1)
    player2_tank=Player( display_dimentions[0]-200, tank2_image,2)
    sprites.add(player1_tank)
    sprites.add(player2_tank)
    players.add(player1_tank)
    players.add(player2_tank)
    pygame.display.set_caption("Tanky")
    pygame.display.set_icon(game_icon)
    #################################################################
    while running:
        game_clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return      
        sprites.update()
        display_surface.blit(firmament_surface,(0,0))        
        sprites.draw(display_surface) 
        GUI()
        pygame.display.update()
    while game_over:
        game_clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        sprites.empty()
        world.empty()
        players.empty()
        display_surface.fill(black)
        text=render_text('Player {} lost'.format(loser), 'freesansbold.ttf',64, white,display_dimentions[0]/3,display_dimentions[1]/3)
        display_surface.blit(text[0],text[1])
        pygame.display.update()
########### calling the main function #####################################
if __name__=="__main__":    
    main_loop()
    pygame.quit()