import crepe
from scipy.io import wavfile
import pygame
from pygame.locals import *
import numpy as np

str_sound = 'Beethoven_-_Diabelli_Variations_-_00.wav'

class Game():
    def __init__(self):
        self.time = 30
        self.gameInit = 0

    def decTime(self):
        self.time = self.time - 1

    def resetTime(self):
        self.time = 30

#text_info = menu_font.render(('Press any button to start!'), 1,(255,255,255))

def getMaxFreq(freq):
    division = 1
    str_1 = ''
    str_2 = ''
    str_3 = ''
    str_4 = ''
    str_5 = ''
    max_freq = frequency.max()
    if max_freq <= 500:
        division = 1
        max_freq_s = 500
    elif max_freq <= 1000:
        division = 2
        max_freq_s = 1000
    elif max_freq <= 1500:
        division = 3
        max_freq_s = 1500
    elif max_freq <= 2000:
        division = 4
        max_freq_s = 2000
    elif max_freq <= 2500:
        division = 5
        max_freq_s = 2500
    elif max_freq <= 3000:
        division = 6
        max_freq_s = 3000
    elif max_freq <= 3500:
        division = 7
        max_freq_s = 3500
    else:
        division = 8
        max_freq_s = 4000
    
    str_1 = str(max_freq_s) + 'Hz'
    str_2 = str(int(max_freq_s*0.8)) + 'Hz'
    str_3 = str(int(max_freq_s*0.6)) + 'Hz'
    str_4 = str(int(max_freq_s*0.4)) + 'Hz'
    str_5 = str(int(max_freq_s*0.2)) + 'Hz'

    return division, str_1, str_2, str_3, str_4, str_5



pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 32, 2, 4096)

font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 72)
info_font = pygame.font.SysFont(font_name, 24)
menu_font = pygame.font.SysFont(font_name, 36)

screen = pygame.display.set_mode((800,600), 0, 32)

background_filename = 'images\\background2.png'
background = pygame.image.load(background_filename).convert()

track1_filename = 'images\\track2.png'
track1 = pygame.image.load(track1_filename).convert()

marker_filename = 'images\\s_marker.png'
marker1 = pygame.image.load(marker_filename).convert()

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

class Marker(Object):
    def __init__(self,position,sprite_enemy,way,factor):
        self.sprite = marker1
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
        if i.position[0] < 60:
            list.remove(i)

def createTrack(tracks, frequency):
    position_init = [700, frequency]
    track = Track(position_init, track1,"left", 1)
    tracks.append(track)

def createMarker(markers):
    position_init = [700, 50]
    #position_init = [300, 400]
    marker = Marker(position_init, marker1, "left", 1)
    markers.append(marker)

trilha_sound = pygame.mixer.Sound('sounds/' + str_sound)

screen.blit(background, (0, 0))
text_music = info_font.render(('Musica: ' + str_sound), 1,(255,255,255))
text_info = info_font.render(('Realizando pitch tracking...'), 1,(255,255,255))
gameInit = 0

screen.blit(background, (0, 0))
screen.blit(text_info,(65,30))
screen.blit(text_music,(65,10))
pygame.display.update()

sr, audio = wavfile.read('sounds/' + str_sound)
time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)
division, str1, str2, str3, str4, str5 = getMaxFreq(frequency)

text_division1 = info_font.render((str1), 1,(255,255,255))
text_division2 = info_font.render((str2), 1,(255,255,255))
text_division3 = info_font.render((str3), 1,(255,255,255))
text_division4 = info_font.render((str4), 1,(255,255,255))
text_division5 = info_font.render((str5), 1,(255,255,255))

screen.blit(background, (0, 0))
text_info = info_font.render(('Pressione qualquer tecla para continuar'), 1,(255,255,255))
screen.blit(text_info,(65,30))
screen.blit(text_music,(65,10))
pygame.display.update()

while gameInit == 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            gameInit = 1

    screen.blit(background, (0, 0))
    screen.blit(text_info,(65,30))
    pygame.display.update()

tracks = []
marker = []
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
        createMarker(marker)
        
    else:
        ticks_time = ticks_time - 1

    if len(frequency) != 0:
        createTrack(tracks, int(600 - frequency[0]/division))
        frequency = np.delete(frequency, 0)
    
    # Acabou o pitch tracking
    else:
        trilha_sound.stop()
            
    screen.blit(background, (0, 0))
    moveList(tracks, 3)
    moveList(marker, 3)
    drawList(tracks)
    drawList(marker)
    text_info2 = info_font.render(('Tempo: {0}'.format(time_counter,)),1,(255,255,255))
    screen.blit(text_music,(65,10))
    screen.blit(text_info2,(65,30))
    screen.blit(text_division1,(10,85))
    screen.blit(text_division2,(10,185))
    screen.blit(text_division3,(10,285))
    screen.blit(text_division4,(10,385))
    screen.blit(text_division5,(10,485))
    
    destroyTracks(tracks)
    destroyTracks(marker)

    pygame.display.update()
    time_passed = clock.tick(100)