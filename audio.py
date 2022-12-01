import pygame
import time
import os
import glob
import string
import re
import random

pygame.mixer.init()
pygame.mixer.music.load('sounds/ost/gasgasgas.ogg')
#pygame.mixer.music.play()

def is_explosion(filename):     # see line 76
    return "explosion" in filename

class sound_library:
    def __init__(self, path):
        self.sounds=[]
        self.table=self.createTable(path)
        # print(self.table)
    
    def playsound(self, ID):
        sfx = pygame.mixer.Sound(self.table[ID])
        pygame.mixer.Sound.play(sfx)

    def addsound(self, name, location):
        self.sounds[name]=location

    def find_audio_files(self):     # returns all locations of .wav, .ogg & .mp3 files in "sounds" folder
        res = []

        for root, dirs, files in os.walk(r"./sounds"):
            for file in files:
                if file.endswith(".wav"):
                    res.append(os.path.join(root, file))
                elif file.endswith(".ogg"):
                    res.append(os.path.join(root, file))
                elif file.endswith(".mp3"):
                    res.append(os.path.join(root, file))

        res = [e.replace("\\", "/") for e in res]

        # print(res)
        return res    

    def derive_id(self):     # returns only the parent directory and filename of all .wav, .ogg & .mp3 files in "sounds" folder
        res = []

        for root, dirs, files in os.walk(r"./sounds"):
            for file in files:
                if file.endswith(".wav"):
                    res.append(os.path.join(root, file))
                elif file.endswith(".ogg"):
                    res.append(os.path.join(root, file))
                elif file.endswith(".mp3"):
                    res.append(os.path.join(root, file))

        res = [e.replace("\\", "/") for e in res]
        res = [e.replace("/sounds", "") for e in res]
        res = [e.replace("./", "") for e in res]
        res = [e.replace(".wav", "") for e in res]
        res = [e.replace(".ogg", "") for e in res]
        res = [e.replace(".mp3", "") for e in res]

        # print(res)
        return res

    def createTable(self, path):
        table={}

        for (path, ID) in zip(self.find_audio_files(),self.derive_id()):
            table[ID]=path
        return table

    def play_random_explosion(self):     # creates a list with all "explosion.wav" files and randomly selects one for availability
        res = []

        for root, dirs, files in os.walk(r"./sounds"):
            for file in files:
                if file.endswith(".wav"):
                    res.append(os.path.join(root, file))
                elif file.endswith(".ogg"):
                    res.append(os.path.join(root, file))
                elif file.endswith(".mp3"):
                    res.append(os.path.join(root, file))

        res = [e.replace("\\", "/") for e in res]
        res = list(filter(is_explosion, res))
        # print(res)
        random_index = random.randint(0, len(res)-1)
        
        sfx = pygame.mixer.Sound(res[random_index])
        pygame.mixer.Sound.play(sfx)


# for testing:

# sfx1 = sound_library(r"./sounds")
# sfx1.playsound("sfx/bullet_sfx")
# expl2 = sound_library(r"./sounds")
# expl2.playsound("sfx/explosion2")
# expl2.play_random_explosion()
# sfx2 = sound_library(r"./sounds")
# sfx2.playsound("sfx/splashBig")

# time.sleep(1)