from pygame import *
from random import randint
from time import time as timer


win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("Шутер от ilya346565")

img_back = "galaxy.jpg"  
img_player1 = "new2.jpg"  
img_player2 = "new.jpg"   
img_bullet = "Bullet.png" 

mixer.init()
mixer.music.load('track.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Constantia', 80)
font2 = font.SysFont('Constantia', 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x = size_x
        self.size_y = size_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, direction):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.direction = direction  
    
    def update(self):
        self.rect.y -= self.speed * self.direction
        
        if self.rect.y < 0 or self.rect.y > win_height:
            self.kill()

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, player_num):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.player_num = player_num  
        self.health = 100
        self.reload_time = 0
        self.last_shot = 0
    
    def update(self):
        keys = key.get_pressed()
        if self.player_num == 1:
            if keys[K_LEFT] and self.rect.x > 5:
                self.rect.x -= self.speed
            if keys[K_RIGHT] and self.rect.x < win_width - self.size_x:
                self.rect.x += self.speed
            if keys[K_UP] and self.rect.y > 5:
                self.rect.y -= self.speed
            if keys[K_DOWN] and self.rect.y < win_height - self.size_y:
                self.rect.y += self.speed
        else:
            if keys[K_a] and self.rect.x > 5:
                self.rect.x -= self.speed
            if keys[K_d] and self.rect.x < win_width - self.size_x:
                self.rect.x += self.speed
            if keys[K_w] and self.rect.y > 5:
                self.rect.y -= self.speed
            if keys[K_s] and self.rect.y < win_height - self.size_y:
                self.rect.y += self.speed
    
    def fire(self):
        now = timer()
        if now - self.last_shot > self.reload_time:
            self.last_shot = now

            bullets.add(bullet)
            fire_sound.play()
            return True
        return False

player1 = Player(img_player1, win_width//4, win_height//2, 80, 80, 5, 1)
player2 = Player(img_player2, 3*win_width//4, win_height//2, 80, 80, 5, 2)

bullets = sprite.Group()

background = transform.scale(image.load(img_back), (win_width, win_height))

run = True
finish = False
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player1.fire()
            if e.key == K_f:
                player2.fire()
            if e.key == K_r and finish:
                finish = False
                player1.health = 100
                player2.health = 100
                for bullet in bullets:
                    bullet.kill()
    
    if not finish:
        window.blit(background, (0, 0))
        player1.update()
        player2.update()
        player1.reset()
        player2.reset()
        bullets.update()
        bullets.draw(window)
        
        for bullet in bullets:
     
        
        if player1.health <= 0 or player2.health <= 0:
            finish = True
            if player1.health <= 0 and player2.health <= 0:
                result_text = font1.render("никто не  победил", True, (255, 255, 255))
            elif player1.health <= 0:
                result_text = font1.render("А4 победил", True, (32, 3, 252))
            else:
                result_text = font1.render("Глент победил", True, (252, 148, 3))
 
 
    
    display.update()
    clock.tick(60)