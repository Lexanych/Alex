from random import randint
from pygame import *

mixer.init()
fire_sound = mixer.Sound("Fired.ogg")

font.init()
font1 = font.Font(None,80)
font2 = font.Font(None,36)
win = font1.render("Ти переміг!", True, (19, 214, 71))
lose = font1.render("Ти програв!", True, (230, 21, 21))

class GameSprite(sprite.Sprite):
    def __init__(self, image_name, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (width, height))
        self.speed = speed
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def reset(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))



class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.rect.x = 0
        if keys[K_d]:
            self.rect.x += self.speed
            if self.rect.x > 1000 - 70:
                self.rect.x = 1000 - 70
        if keys[K_w]:
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.rect.y = 0
        if keys[K_s]:
            self.rect.y += self.speed
            if self.rect.y > 700 - 70:
                self.rect.y = 700 - 70

    def fire(self):
        bullet = Bullet("bulle.jpg", self.rect.centerx, self.rect.top, 15, 20, 25)
        bullets.add(bullet)

class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= window_height:
            self.rect.x = randint(80, window_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Wall(sprite.Sprite):
    def __init__(self, x, y, width, height, colors):
        super().__init__()
        self.width = width
        self.height = height
        self.colors = colors
        self.image = Surface((self.width, self.height))
        self.image.fill(colors)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drawWall(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):

    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 1000:
            self.kill()
lost = 0

bullets = sprite.Group()
tanks = sprite.Group()

window = display.set_mode((1000, 700))
display.set_caption("Лабіринт")
background = transform.scale(image.load("Back.png"), (1000, 700))

tank1 = Player("Tank1.jpg", 50, 250, 75, 75, 5)
tank2 = GameSprite("Tank2.jpg", 500, 60, 75, 75, 4)
tanks.add(tank2)
tank3 = GameSprite("Tank2.jpg", 400, 570, 75, 75, 4)
tanks.add(tank3)
fuel = Enemy("Fuel.jpg", 200, 160, 75, 75, 0)

wall_color = (7, 18, 79)
walls = [
    Wall(100, 20, 600, 10, wall_color),
    Wall(100, 20, 10, 200, wall_color),
Wall(100, 350, 10, 200, wall_color),
Wall(200, 350, 10, 200, wall_color),
Wall(200, 150, 10, 200, wall_color),
Wall(200, 150, 250, 10, wall_color),
Wall(450, 150, 10, 200, wall_color),
Wall(800, 150, 10, 200, wall_color),
Wall(650, 150, 10, 200, wall_color),
Wall(700, 20, 200, 10, wall_color),
Wall(900, 20, 10, 200, wall_color),

Wall(100, 650, 600, 10, wall_color),
Wall(660, 650, 250, 10, wall_color),
Wall(100, 450, 10, 200, wall_color),
Wall(200, 550, 260, 10, wall_color),
Wall(450, 350, 10, 100, wall_color),
Wall(450, 550, 200, 10, wall_color),
Wall(900, 200, 10, 450, wall_color),

Wall(200, 350, 100, 10, wall_color),
Wall(300, 440, 150, 10, wall_color),
Wall(290, 250, 10, 100, wall_color),
Wall(391, 350, 60, 10, wall_color),
Wall(300, 250, 65, 10, wall_color),

Wall(300, 450, 10, 20, wall_color),
Wall(450, 530, 10, 20, wall_color),
Wall(560, 350, 100, 10, wall_color),
Wall(460, 200, 100, 10, wall_color),
Wall(650, 350, 10, 100, wall_color),

Wall(760, 350, 40, 10, wall_color),
Wall(660, 200, 50, 10, wall_color),

Wall(800, 150, 100, 10, wall_color),
Wall(760, 440, 50, 10, wall_color),
Wall(760, 550, 150, 10, wall_color),




]
font.init()
font = font.Font(None, 70)
win = font.render("Ти переміг", True, (11, 128, 25))
lose = font.render("ти програв", True, (180, 0, 0))

game = True
finish = False
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:  # Проверяем нажатие ЛКМ
            if e.button == 1:
                fire_sound.play()
                tank1.fire()

    if finish != True:
        window.blit(background, (0,0))
        tank1.update()
        tank1.reset(window)
        tanks.draw(window)
        fuel.reset(window)
        bullets.update()
        bullets.draw(window)

        for wall in walls:
            wall.drawWall(window)

        if sprite.spritecollideany(tank1, walls):
            window.blit(lose, (200, 200))
            finish = True

        if sprite.spritecollide(tank1, tanks, True):
            window.blit(lose, (200, 200))
            finish = True

        if sprite.collide_rect(fuel, tank1):
             window.blit(win, (200, 200))
             finish = True

        sprite.groupcollide(tanks, bullets, True, True)


    display.update()
    clock.tick(FPS)


