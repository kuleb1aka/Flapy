from pygame import *
from random import *
init()


window = display.set_mode((1200,800))
display.set_caption("Flapy")
running = True
FPS = 120
clock = time.Clock()

class bird():
    def __init__(self,x,y,img=None):
        self.x = x
        self.y = y
        self.img = img
        if self.img:
            self.rect = self.img.get_rect()
        else:
            self.rect = Rect(x,y,100,100)

    def move(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y -= 5
        if keys[K_s]:
            self.rect.y += 5
    def update(self,screen):
        if self.img:
            screen.blit(self.img, (self.rect.x,self.rect.y,))
        else:
            draw.rect(screen,(255,255,0),self.rect)

class tube:
    def __init__(self,x,y,width=120,height = 800, img = None):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.img = img
        if self.img:
            self.rect = self.img.get_rect()
        else:
            self.rect = Rect(x,y,width,height)
    def update(self,screen):
        if self.img:
            screen.blit(self.img, (self.rect.x,self.rect.y,))
        else:
            draw.rect(screen,(255,255,0),self.rect)
    def move(self):
        self.rect.x -= 4
def generate_tubes(count):
    xcor = 1200
    tubes = list()
    for i in range(count):
        ycor = randint(-600,-300)
        
        top_tube = tube(xcor,ycor)
        bottom_tube = tube(xcor,ycor+800+250)
        
        tubes.extend([top_tube,bottom_tube])
        
        xcor +=400
    return tubes
tubes= generate_tubes(150)
player = bird(100,100)
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    window.fill("skyblue")
    
    player.move()
    player.update(window)
    
    for t in tubes:
        t.update(window)
        t.move()
    
    display.update()
    clock.tick(FPS)