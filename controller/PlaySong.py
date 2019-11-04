import pygame
import time

# class로 정리할 것

def playsound(soundfile):
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(soundfile)
    clock = pygame.time.Clock()
    sound.play()
    while pygame.mixer.get_busy():
        print("playsound")
        clock.tick(1000)
        
def playmusic(soundfile):
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        print("playingmusic")
        clock.tick(1000)
        
def stopmusic():
    pygame.mixer.music.stop()
    
def getmixerargs():
    pygame.mixer.init()
    freq, size, chan = pygame.mixer.get_init()
    return freq, size, chan

def initMixer():
    BUFFER = 3072
    FREQ, SIZE, CHAN = getmixerargs()
    pygame.mixer.init(FREQ, SIZE, CHAN, BUFFER)
    
try: 
    initMixer()
    filename = "./song.midi"
    playmusic(filename)
except KeyboardInterrupt:
    stopmusic()
    print("stop by user")
except Exception:
    print("unkown error")
    

  
