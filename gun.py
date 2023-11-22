import math
from random import choice
from random import randint
import pygame
import sys


FPS = 30
point=0

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600




class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0   #сила трения
        self.vy = 0
        self.ax=0
        self.ay=-1
        self.kx=-0.02
        self.ky=-0.02
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.livetimer = 200

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.vy+=self.ay+self.ky*self.vy
        self.vx+=self.ax+self.kx*self.vx
        self.x += self.vx
        self.y -= self.vy
        self.livetimer-=1
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx *= -1
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy *= -1
        if self.x + self.r >= 800:
            self.x = 800 - self.r
            self.vx *= -1
        if self.y + self.r >= 600:
            self.y = 600 - self.r
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x-obj.x)**2+(self.y-obj.y)**2)**0.5<=(self.r+obj.r):
            return True
        return False
class NewBall(Ball):
    def __init__(self, *args, **kwargs):
        Ball.__init__(self, *args, **kwargs)
        self.livetimer = 90
    def move(self):
        self.vy+=0
        self.vx+=0
        self.x += self.vx
        self.y -= self.vy
        self.livetimer-=1

    def draw(self):
        target_surf = pygame.image.load('ball2.png')
        DEFAULT_IMAGE_SIZE = (2 * self.r, 2 * self.r)
        target_surf = pygame.transform.scale(target_surf, DEFAULT_IMAGE_SIZE)
        screen.blit(target_surf, (self.x-self.r, self.y-self.r))




class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.y=440
        self.x=0
        self.height=30
        self.width=30

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        if ball_type:
            new_ball = Ball(self.screen, y=self.y)
        else:
            new_ball = NewBall(self.screen, y=self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.pos[0]-20)!=0:
                self.an = math.atan((event.pos[1]-self.y) / (event.pos[0]-20))
            elif (event.pos[1]-self.y)>0:
                self.an = math.pi/2
            else:
                self.an = -math.pi/2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def move_up(self):
        if self.y>20:
            self.y-=5

    def move_down(self):
        if self.y<580:
            self.y+=5

    def draw(self):
        if pygame.key.get_pressed()[pygame.K_q]:
            Gun.move_down(self)
        if pygame.key.get_pressed()[pygame.K_e]:
            Gun.move_up(self)


        cos = math.cos(self.an)
        sin = math.sin(self.an)
        c1 = [self.x - self.height / 2 * sin, self.y + self.height / 2 * cos]
        c4 = [self.x + self.height / 2 * sin, self.y - self.height / 2 * cos]
        c2 = [self.width * cos + c1[0], self.width * sin + c1[1]]
        c3 = [self.width * cos + c4[0], self.width * sin + c4[1]]
        pygame.draw.polygon(self.screen, self.color, [c1, c2, c3, c4])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                self.color = (self.f2_power * 1.44 + 110, 138.8 - 1.38 * self.f2_power, 138.8 - 1.38 * self.f2_power)
        else:
            self.color = GREY




class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()
    def __init__(self, screen):
        """ Конструктор класса Target

        Args:
        x,y - начальное положение мяча по горизонтали задатся случайно

        """
        self.screen = screen
        self.points = 0
        self.miss=0
        self.live = 1
        self.x = randint(500, 780)
        self.y = randint(300, 550)
        self.kx=-0.2
        self.ky=-0.2
        self.vx = 0
        self.vy = 0
        self.k = -0.002
        self.r = randint(10, 50)
        self.color = choice([RED, CYAN])

    def move(self):
        """Переместить target по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.vy += randint(-1,1)
        self.vx += randint(-1,1)+self.k*self.vx
        self.x += self.vx
        self.y += self.vy
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx *= -1
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy *= -1
        if self.x + self.r >= 800:
            self.x = 800 - self.r
            self.vx *= -1
        if self.y + self.r >= 600:
            self.y = 600 - self.r
            self.vy *= -1


    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points
    #def nothit(self,miss=1):
        #self.miss+=miss

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
class Target2(Target):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.w=0.1
        self.R=randint(30,100)
        self.x0=randint(100, WIDTH - 180)
        self.y0=randint(100, HEIGHT-180)
        self.r=randint(10, 30)
        self.color = BLUE
        self.a=0
        self.x = self.x0 + self.R * math.cos(self.a)
        self.y = self.y0 + self.R * math.sin(self.a)
        self.points = 0
    def move2(self):
        self.a += self.w
        self.x = self.x0 + self.R * math.cos(self.a)
        self.y = self.y0 + self.R * math.sin(self.a)




    def draw(self):
        target_surf = pygame.image.load('boom.png')
        DEFAULT_IMAGE_SIZE = (2 * self.r, 2 * self.r)
        target_surf = pygame.transform.scale(target_surf, DEFAULT_IMAGE_SIZE)
        self.screen.blit(target_surf, (self.x - self.r, self.y - self.r))








pygame.init()
ball_type = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
window = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("bg.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
target2=Target2(screen)

finished = False
font=pygame.font.Font(None,36)

while not finished:
    window.blit(background, (0, 0))  # !!!
    all_sprites.draw(window)  # !!!
    #pygame.display.update()
    score_text = font.render("Очки: " + str(point), True, BLACK)
    screen.blit(score_text, (10, 10))
    gun.draw()
    target.draw()
    target.move()
    target2.draw()
    target2.move2()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                ball_type = not ball_type



    for b in balls:
        b.move()
        if b.hittest(target):
            target.hit()
            target = Target(screen)
            b.live = 0
            point+=1
            balls.remove(b)
        elif b.hittest(target2):
            target2.hit()
            target2=Target2(screen)
            b.live = 0
            point+=1
            balls.remove(b)
        if len(balls) > 5:
            balls.pop(0)
        if b.livetimer<0:
            balls.remove(b)
    gun.power_up()




pygame.quit()
