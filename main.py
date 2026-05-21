from pygame import *
from random import *
import numpy
import sounddevice as sd
init()



display.set_caption("Flapy")
running = True
lose = False
FPS = 120

sr = 16000
block = 256
mic_level = 0.0

window = display.set_mode((1200,800))
clock = time.Clock()

class bird():
    def __init__(self,x,y,img=None):
        self.x = x
        self.y = y
        self.img = img
        if self.img:
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
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
def audio_cb(indata,frames,time,status):
    global mic_level
    if status:
        return
    rms = float(numpy.sqrt(numpy.mean(indata**2)))
    mic_level = 0.85 * mic_level + 0.15 * rms

birdimg =  image.load("bird.png")
tubes= generate_tubes(150)
player = bird(100,450-100,birdimg)

y_vel = 0.0
gravity = 0.6
THRESH = 0.001
IMPULSE = -8.0 

with sd.InputStream(samplerate=sr, channels=1, blocksize=block, callback=audio_cb):
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        window.fill("skyblue")
    
        player.move()
        player.update(window)
    
        if mic_level > THRESH:
            y_vel = IMPULSE
        y_vel += gravity
        player.rect.y += int(y_vel)
        for t in tubes:
            if not lose:
                t.move()
            t.update(window)
            
            if t.rect.right < 0:
                tubes.remove(t)
            if player.rect.colliderect(t.rect):
                lose = True
            if len(tubes) < 8:
                tubes += generate_tubes(150)
        display.update()
        clock.tick(FPS)