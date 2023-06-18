#My first bullet hell game
#By Cameron Davies
#Huahui Mo
#
#I pulled some pictures and sound files from the pygame examples
#Music from UN Squadron (It should be playing faster, but I don't know why it's not)
#Font from https://www.dafont.com
#Plane pictures taken from wikipedia

import pygame, random, time, os
from pygame.locals import *

#create all the groups of game objects
all_sprites = pygame.sprite.Group()
player_shots = pygame.sprite.Group()
enemy_shots = pygame.sprite.Group()
enemies = pygame.sprite.Group()

#a function to load images for sprites
def load_image(filename):
    image = pygame.image.load(os.path.join("data", filename))
    return image.convert_alpha()

#a function to load sound effects
def load_sound(filename, volume=0.2):
    snd = pygame.mixer.Sound(os.path.join("data", filename))
    snd.set_volume(volume)
    return snd

#a function to load background music
def load_music(filename, volume=0.2):
    pygame.mixer_music.load(os.path.join("data", filename))
    pygame.mixer_music.set_volume(volume)
    return

#This class defines flight patterns for the enemies
#You get the data directly from spawns, start, x, y, and shoot
#I love python for this ^
class Pattern():
    #reads 2 files as input for the patterns
    def __init__(self, filename, filename2):
        #load file
        openfile = open(filename2, 'r')
        self.start = []
        self.spawns = int(openfile.readline())
        for i in range(self.spawns):
            self.start.append(int(openfile.readline()))
        openfile.close()
        openfile = open(filename, 'r')
        self.x = []
        self.y = []
        self.shoot = []
        for line in openfile:
            self.x.append(int(line[0] + line[1]))
            self.y.append(int(line[3] + line[4]))
            if int(line[6]) == 0:
                self.shoot.append(False)
            else:
                self.shoot.append(True)
        openfile.close()

#A flight of enemies following a certain pattern
class Flight():
    #The flight follows the specified pattern
    def __init__(self, pattern):
        self.pattern = pattern
        self.spawns = self.pattern.spawns
    
    #Returns the enemy to spawn
    def spawn(self):
        self.spawns -= 1
        return Enemy(self.pattern, self.pattern.spawns - self.spawns - 1)

#The hero of this game
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('F14.png')
        self.area = pygame.display.get_surface().get_rect()
        start_x = self.area.width/2
        start_y = self.area.height - 100
        self.rect = self.image.get_rect(center = (start_x, start_y))
        self.pos_x = 0
        self.pos_y = 0
        self.cooldown = 0
        self.health = 10
        self.explosion = load_sound('boom.wav')

    def update(self):
        key = pygame.key.get_pressed()
        if self.cooldown > 0:
            self.cooldown -= 1

        if key[K_LEFT] and (self.rect.x + self.rect.width) > 100:
            self.pos_x = -10
        if key[K_RIGHT] and self.rect.x < self.area.width - 100:
            self.pos_x = 10
        if key[K_UP] and self.rect.y + self.rect.height > 100:
            self.pos_y = -10
        if key[K_DOWN] and self.rect.y < self.area.height - 100:
            self.pos_y = 8
        if key[K_SPACE] and self.cooldown == 0:
            shot = Shot(self.rect.center)
            player_shots.add(shot)
            all_sprites.add(shot)
            self.cooldown = 7

        self.rect.move_ip(self.pos_x, self.pos_y)
        self.pos_x = 0
        self.pos_y = 0

    def kill(self):
        if self.health > 0:
            self.health -= 1
        elif self.health == 0:
            pygame.sprite.Sprite.kill(self)
            boom = Explosion(self.rect.center)
            all_sprites.add(boom)
            self.explosion.play()
		
#Your bullets
class Shot(pygame.sprite.Sprite):
    def __init__(self, position):
        self.velocity = -15
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('Bullet.png')
        self.image = self.base_image
        self.area = pygame.display.get_surface().get_rect()
        self.rect = self.image.get_rect(center=position)
        self.rect.move_ip(0, -50)

    def update(self):
        self.rect.move_ip(0, self.velocity)
        if not self.area.contains(self.rect):
            self.kill()

#The no good Reds
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pattern, start):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('Mig29.png')
        self.area = pygame.display.get_surface().get_rect()
        self.pos_x = 0
        self.pos_y = 0
        self.count = 0
        self.pattern = pattern
        start_x = self.pattern.start[start]
        start_y = -50
        self.rect = self.image.get_rect(center = (start_x, start_y))
        self.curr_y = start_y
        self.health = 4
        self.explosion = load_sound('boom.wav')
        self.alive = True

    def update(self):
        self.pos_x = self.pattern.x[self.count]
        self.pos_y = self.pattern.y[self.count]
        self.curr_y += self.pos_y
        if self.pattern.shoot[self.count]:
            shot = EnemyShot(self.rect.center)
            enemy_shots.add(shot)
            all_sprites.add(shot)

        self.rect.move_ip(self.pos_x, self.pos_y)
        if self.curr_y >= 1000:
            pygame.sprite.Sprite.kill(self)
        self.count += 1

    def kill(self):
        if self.health > 1:
            self.health -= 1
        else:
            pygame.sprite.Sprite.kill(self)
            boom = Explosion(self.rect.center)
            all_sprites.add(boom)
            self.explosion.play()
            self.alive = False
        
#Do not let these touch the hero
class EnemyShot(pygame.sprite.Sprite):
    def __init__(self, position):
        self.velocity = 15
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('Enemy_Bullet.png')
        self.image = self.base_image
        self.area = pygame.display.get_surface().get_rect()
        self.rect = self.image.get_rect(center=position)
        self.rect.move_ip(0, 50)

    def update(self):
        self.rect.move_ip(0, self.velocity)
        if not self.area.contains(self.rect):
            self.kill()

#Something that follows the destruction of a vehicle
class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('explosion1.gif')
        self.image = self.base_image
        self.area = pygame.display.get_surface().get_rect()
        self.rect = self.image.get_rect(center=position)
        self.rect.move_ip(0, 0)
        self.alive = 200

    def update(self):
        self.rect.move_ip(0, 0)
        self.alive -= 10
        if self.alive <= 0:
            self.kill()

#The main game
def main():
    #The main menu function
    def menu():
        select = 1
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return False
                if e.type == KEYDOWN:
                    if e.key == K_DOWN:
                        select = 2
                    if e.key == K_UP:
                        select = 1
                    if e.key == K_RETURN or e.key == K_SPACE:
                        if select == 1:
                            return True
                        if select == 2:
                            pygame.quit()
                            return False
            screen.blit(background, (0, 0))
            ren = font64.render("Top", 1, (0, 0, 0))
            screen.blit(ren, (450-ren.get_width()/2, 50))                
            ren = font64.render("Gun", 1, (0, 0, 0))
            screen.blit(ren, (450-ren.get_width()/2, 120))  
            ren = font32.render("By Cameron Davies", 1, (0, 0, 0))
            screen.blit(ren, (450-ren.get_width()/2, 220))   
            ren = font32.render("New Game", 1, (0, 0, 0))
            screen.blit(ren, (450-ren.get_width()/2, 360))  
            ren = font32.render("Quit Game", 1, (0, 0, 0))
            screen.blit(ren, (450-ren.get_width()/2, 400))
            if select == 1:
                ren = font32.render("> New Game <", 1, (255, 0, 0))
                screen.blit(ren, (450-ren.get_width()/2, 360)) 
            if select == 2:
                ren = font32.render("> Quit Game <", 1, (255, 0, 0))
                screen.blit(ren, (450-ren.get_width()/2, 400)) 
            pygame.display.flip()
    
    #The pause screen
    def paused():
        pygame.mixer_music.pause()
        select = 1
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        pygame.mixer_music.unpause()
                        return
                    if e.key == K_DOWN:
                        select = 2
                    if e.key == K_UP:
                        select = 1
                    if e.key == K_RETURN or e.key == K_SPACE:
                        if select == 1:
                            pygame.mixer_music.unpause()
                            return
                        if select == 2:
                            pygame.quit()
                            return
            screen.blit(background, (0, 0))
            ren = font64.render("Paused", 1, (0, 0, 0))
            screen.blit(ren, (450-ren.get_width()/2, 120))    
            ren = font32.render("Resume", 1, (0, 0, 0))
            screen.blit(ren, (450-ren.get_width()/2, 360))  
            ren = font32.render("Quit", 1, (0, 0, 0))
            screen.blit(ren, (450-ren.get_width()/2, 400))
            if select == 1:
                ren = font32.render("> Resume <", 1, (255, 0, 0))
                screen.blit(ren, (450-ren.get_width()/2, 360)) 
            if select == 2:
                ren = font32.render("> Quit <", 1, (255, 0, 0))
                screen.blit(ren, (450-ren.get_width()/2, 400)) 
            pygame.display.flip()
    
    pygame.init()
    random.seed()
    score = 0
    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption('Bullet Hell')
    background = load_image('Sky.png')
    screen.blit(background, (0, 0))
    font = pygame.font.Font(os.path.join("data", "font.ttf"), 16)
    font32 = pygame.font.Font(os.path.join("data", "font.ttf"), 32)
    font64 = pygame.font.Font(os.path.join("data", "font.ttf"), 64)
    font128 = pygame.font.Font(os.path.join("data", "font.ttf"), 128)
    load_music('bgmusic.ogg', 0.1)

    player = Player()
    player.add(all_sprites)
    isalive = True
    lives = 5

    pattern = []
    pattern.append(Pattern(os.path.join("data", "enemy_movement1.data"), os.path.join("data", "enemy_spawn1.data")))
    pattern.append(Pattern(os.path.join("data", "enemy_movement2.data"), os.path.join("data", "enemy_spawn2.data")))
    pattern.append(Pattern(os.path.join("data", "enemy_movement3.data"), os.path.join("data", "enemy_spawn3.data")))
    
    select = menu()

    spawntime = 50
    flight = Flight(pattern[random.randint(0, len(pattern)-1)])
    pygame.mixer_music.play(-1)
    while select:
        wait = time.clock()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    paused()
            if event.type == QUIT:
                return
        
        #You died and another plane will sortie to take your place
        if (not isalive):
            if len(enemies.sprites()) == 0 and lives != 0:
                player = Player()
                player.add(all_sprites)
                isalive = True
                spawntime = 50
                lives -= 1
            else:
                for sprite in enemies.sprites():
                    sprite.kill()
                for sprite in enemy_shots.sprites():
                    sprite.kill()
        
        #A new fighter is coming
        if spawntime == 0 and (len(enemies.sprites()) == 0 or flight.spawns > 0):
            spawntime = 20
            if flight.spawns == 0:
                flight = Flight(pattern[random.randint(0, len(pattern)-1)])
            enemy = flight.spawn()
            enemy.add(all_sprites)
            enemy.add(enemies)
        elif spawntime > 0:
            spawntime -= 1
        
        #display the background and other hud stuff
        screen.blit(background, (0, 0))
        ren = font.render("Score: %06d" % score, 1, (0, 0, 0))
        screen.blit(ren, (10, 10))
        ren = font.render("Lives: %d" % lives, 1, (0, 0, 0))
        screen.blit(ren, (800, 10))
        ren = font.render("Health: %d" % player.health, 1, (0, 0, 0))
        screen.blit(ren, (800, 30))
        
        #Game Over
        if (not isalive) and lives == 0:
            ren = font128.render("Game", 1, (0, 0, 0))
            screen.blit(ren, (450-ren.get_width()/2, 300))
            ren = font128.render("Over", 1, (0, 0, 0))
            screen.blit(ren, (450-ren.get_width()/2, 450))
            spawntime = -1
        
        #update sprites and collisions
        all_sprites.update()
        for killed in pygame.sprite.groupcollide(enemies, player_shots, True, True):
            if not killed.alive:
                score += 10
        if isalive and (pygame.sprite.spritecollide(player, enemies, True) or pygame.sprite.spritecollide(player, enemy_shots, True)):
            player.kill()
            if player.health == 0:
                isalive = False
                player.kill()
                spawntime = 10

        all_sprites.clear(screen, background)
        all_sprites.draw(screen)
        pygame.display.flip()
        
        #Limit to 30 fps
        sleeping = 0.033 - (time.clock() - wait)
        if sleeping > 0:
            time.sleep(sleeping)
        #print(1/(time.clock() - wait))

if __name__ == '__main__': main()
pygame.quit()
exit()
