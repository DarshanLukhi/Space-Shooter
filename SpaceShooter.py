import pygame
import random
from os import path

WIDTH = 480
HEIGHT = 600
FPS = 60

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# initialization
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'sound')

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def new_enemy():
    m = Enemy()
    all_sprite.add(m)
    enemy.add(m)


def draw_shield_bar(surf, x, y, shield):
    if shield < 0:
        shield = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    FILL = (shield / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, FILL, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def show_go_screen():
    draw_text(screen, "Space Shooter", 64, WIDTH / 2, HEIGHT / 4 , YELLOW)
    draw_text(screen, "Arrow key to move, Space to fire", 22, WIDTH / 2, HEIGHT / 2 , YELLOW)
    draw_text(screen, "Press a key to start", 22, WIDTH / 2, HEIGHT * 3/4 , YELLOW)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False





def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 21
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.top = HEIGHT - 60
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 5000:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.top = HEIGHT - 60
        self.speedx = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.speedx = -5
        if key[pygame.K_RIGHT]:
            self.speedx = 5
        if key[pygame.K_SPACE]:
            self.shoot()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.x += self.speedx

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprite.add(bullet)
                bullets.add(bullet)
                bullet_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprite.add(bullet1)
                all_sprite.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullet_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(enemy_img)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()

        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-3, 3)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.x < -150 or self.rect.right > WIDTH + 150:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -8

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Blast(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = blast_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(blast_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = blast_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['gun', 'shield', 'life'])
        self.image = powerup_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


# Image Section
background = pygame.image.load(path.join(img_dir, 'space.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'player.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 20))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, 'laser.png')).convert()
enemy_img = []
# 'big1.png',
enemy_list = ['big2.png', 'big3.png', 'big4.png', 'med1.png', 'med2.png',
              'small1.png', 'small2.png', 'tiny1.png']

for img in enemy_list:
    enemy_img.append(pygame.image.load(path.join(img_dir, img)).convert())

blast_anim = {}
blast_anim['lg'] = []
blast_anim['sm'] = []
blast_anim['player'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, 'blast', filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    blast_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    blast_anim['sm'].append(img_sm)
    img = pygame.image.load(path.join(img_dir, 'player blast', filename)).convert()
    img.set_colorkey(BLACK)
    blast_anim['player'].append(img)

powerup_img = {}
powerup_img['gun'] = pygame.image.load(path.join(img_dir, 'power', 'bolt.png')).convert()
powerup_img['shield'] = pygame.image.load(path.join(img_dir, 'power', 'shield.png')).convert()
powerup_img['life'] = player_mini_img
# sound section
bullet_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser.wav'))
blast_sound = []
blast_list = ['explosion1.wav', 'explosion2.wav']
for snd in blast_list:
    blast_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_death_sound = pygame.mixer.Sound(path.join(snd_dir, 'death.ogg'))
pygame.mixer.music.load(path.join(snd_dir, 'background.ogg'))
pygame.mixer.music.set_volume(0.4)


pygame.mixer.music.play(loops=-1)

game_over = True
running = True
while running:

    if game_over:
        show_go_screen()
        game_over = False
        all_sprite = pygame.sprite.Group()
        enemy = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        power = pygame.sprite.Group()
        player = Player()
        all_sprite.add(player)
        for i in range(5):
            new_enemy()
        score = 0

    clock.tick(FPS)
    # INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # UPDATE
    all_sprite.update()
    hits = pygame.sprite.groupcollide(enemy, bullets, True, True)
    for hit in hits:
        score += 60 - hit.radius
        random.choice(blast_sound).play()
        blast = Blast(hit.rect.center, 'lg')
        all_sprite.add(blast)
        new_enemy()
        if random.random() > 0.93:
            p = Power(hit.rect.center)
            all_sprite.add(p)
            power.add(p)

    over = pygame.sprite.spritecollide(player, enemy, True, pygame.sprite.collide_circle)

    for i in over:
        player.shield -= i.radius
        blast = Blast(i.rect.center, 'sm')
        all_sprite.add(blast)
        new_enemy()
        if player.shield <= 0:
            player_death_sound.play()
            player_blast = Blast(player.rect.center, 'player')
            all_sprite.add(player_blast)
            player.lives -= 1
            player.shield = 100
            player.hide()

    hits = pygame.sprite.spritecollide(player, power, True)

    for hit in hits:
        if hit.type == 'shield':
            player.shield += 30
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
        if hit.type == 'life':
            player.lives += 1
            if player.lives >= 3:
                player.lives = 3
    if player.lives == 0 and not player_blast.alive():
        game_over = True
    # DISPLAY
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    draw_text(screen, str(score), 18, WIDTH / 2, 10, WHITE)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    all_sprite.draw(screen)
    pygame.display.flip()

