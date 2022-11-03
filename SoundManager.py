import pygame as pg
import os
import numpy as np


class Sound:
    def __init__(self,id,path):
        self.id = id
        self.path = path
        self.sound = pg.mixer.Sound(self.path)
        self.sound.set_volume(0.05)

    def play(self,times):
        self.sound.play(times)

    def stop(self):
        self.sound.stop()

class SoundManager:
    def __init__(self):
        self.dict_songs = {}
        self.song_playing = True
        self.dict_sounds = {}
        pg.mixer.init()

    def loadSongs(self):
        songs = os.listdir("sounds/songs/")
        for x in range(len(songs)):
            self.dict_songs[x]=Sound(x,"sounds/songs/"+songs[x])

    def playSong(self,id,times):
        self.dict_songs[id].play(times)

    def stopSong(self,id):
        self.dict_songs[id].stop()

    def loadSounds(self):
        sounds = os.listdir("sounds/effects/")
        for x in range(len(sounds)):
            self.dict_sounds[x]=Sound(x,"sounds/effects/"+sounds[x])
            
    def playSound(self,id,times):
        self.dict_sounds[id].play(times)

    def changeIntensity(self,id,val):
        self.dict_sounds[id].sound.set_volume(val) 

    def intensityBall(self,lvel):
        cnt = 0.45
        intensity = np.sqrt((lvel[0][0]-lvel[1][0])**2+(lvel[0][2]-lvel[1][2])**2)*cnt
        self.changeIntensity(0,intensity)

    def intensityEdge(self,elvel):
        cnt = 0.45
        intensity = np.sqrt(elvel[0]**2+elvel[1]**2)*cnt
        self.changeIntensity(2,intensity)

    def intensityCue(self,clvel):
        cnt = 0.45
        intensity = np.sqrt(clvel[0]**2+clvel[1]**2)*cnt
        self.changeIntensity(3,intensity)

