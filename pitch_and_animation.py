import crepe
from scipy.io import wavfile
import pygame
from pygame.locals import *
import numpy as np

class Game():
    def __init__(self):
        self.time = 30
        self.gameInit = 0

    def decTime(self):
        self.time = self.time - 1

    def resetTime(self):
        self.time = 30


sr, audio = wavfile.read('sounds\parabens.wav')
time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)


pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 32, 2, 4096)

font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 72)
info_font = pygame.font.SysFont(font_name, 24)
menu_font = pygame.font.SysFont(font_name, 36)

screen = pygame.display.set_mode((800,600), 0, 32)

background_filename = 'images\\background.png'
background = pygame.image.load(background_filename).convert()

track1_filename = 'images\\track1.png'
track1 = pygame.image.load(track1_filename).convert()

pygame.display.set_caption('Pitch and Animation')
clock = pygame.time.Clock()

class Object():
    def __init__(self,position,sprite):
        self.sprite = sprite
        self.position = position

    def draw(self):
        screen.blit(self.sprite,(self.position))

    def rect(self):
        return Rect(self.position[0],self.position[1],self.sprite.get_width(),self.sprite.get_height())

class Track(Object):
    def __init__(self,position,sprite_enemy,way,factor):
        self.sprite = track1
        self.position = position
        self.way = way
        self.factor = factor

    def move(self,speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed * self.factor
        elif self.way == "left":
            self.position[0] = self.position[0] - speed * self.factor

#Funções gerais
def drawList(list):
    for i in list:
        i.draw()

def moveList(list,speed):
    for i in list:
        i.move(speed)

def destroyTracks(list):
    for i in list:
        if i.position[0] < -10:
            list.remove(i)
        elif i.position[0] > 800:
            list.remove(i)

def createTrack(tracks, frequency):
    position_init = [450, frequency]
    track = Track(position_init, track1,"left", 1)
    tracks.append(track)

trilha_sound = pygame.mixer.Sound('sounds\parabens.wav')

screen.blit(background, (0, 0))
text_info = menu_font.render(('Press any button to start!'), 1,(255,255,255))
gameInit = 0


while gameInit == 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            gameInit = 1

    screen.blit(background, (0, 0))
    screen.blit(text_info,(300,400))
    pygame.display.update()

tracks = []
time_counter = 0
ticks_time = 30
trilha_sound.play(1)

while True:
    gameInit = 1

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    
    if not ticks_time:
        ticks_time = 100
        time_counter = time_counter + 1
        
        
    else:
        ticks_time = ticks_time - 1

    if len(frequency) != 0:
        createTrack(tracks, int(frequency[0]))
        frequency = np.delete(frequency, 0)
            
    screen.blit(background, (0, 0))
    moveList(tracks, 3)
    drawList(tracks)
    text_info2 = info_font.render(('Time: {0}'.format(time_counter,)),1,(255,255,255))
    screen.blit(text_info2,(150,50))
    
    #destroyTracks(tracks)

    pygame.display.update()
    time_passed = clock.tick(100)