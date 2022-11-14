from openal import * #pip install PyOpenAL
import numpy as np

class Sound:
    def __init__(self,path,position=[0,0,0]):
        self.path = path
        self.source = oalOpen(self.path)
        self.source.set_position(position)
        #self.sound.set_volume(0.05)

    def play(self,looping, pos, rolloff, ref_dist):
        self.source.set_looping(looping)
        self.source.set_position(pos)
        self.source.set_rolloff_factor(rolloff)
        self.source.set_reference_distance(ref_dist)
        self.source.play()

    def stop(self):
        self.source.stop()
    
    def set_position(self,position):
        self.source.set_position(position)
    
    """
    def set_volume(self,dist):
        self.source.set_reference_distance(1/dist)
    """

class SoundManager:
    def __init__(self,app,pos = [0,0,0]):
        self.app = app
        self.listener = oalGetListener()
        #alDistanceModel(AL_INVERSE_DISTANCE_CLAMPED)
        self.listener.set_position(list(self.app.camera.position))
        forward = self.app.camera.forward
        up = self.app.camera.up
        self.listener.set_orientation([forward[0],forward[1],forward[2],up[0],up[1],up[2]])
        self.dict_songs = {}
        self.song_playing = True
        self.dict_sounds = {}
        self.on_init(pos)
    
    def on_init(self,pos=[0,0,0]):
        self.loadSongs(pos)
        self.loadSounds()
        alDistanceModel(AL_INVERSE_DISTANCE_CLAMPED)
    def update(self):
        if not self.app.camera.bird_camera:
            self.listener.set_position(list(self.app.camera.position))
            forward = self.app.camera.forward
            up = self.app.camera.up
            #self.listener.set_orientation([forward[0],forward[1],forward[2],up[0],up[1],up[2]])
            self.listener.set_orientation(list(forward)+list(up))
        else:
            self.listener.set_position([23.0077,54.1003,42.303])        
            self.listener.set_orientation([ -0.0174524, -0.999848, -8.7392e-17,-0.999848,0.0174524,-5.00668e-15])
    def destroy(self):
        oalQuit()

    def loadSongs(self, position = [0,0,0]):
        songs = os.listdir("sounds/songs/")
        for x in range(len(songs)):
            self.dict_songs[x]=Sound("sounds/songs/"+songs[x],position)
        alDistanceModel(AL_INVERSE_DISTANCE_CLAMPED)

    def playSong(self,id=0,looping=True,pos=[0,0,0],rolloff=.25, ref_dist = 5):
        self.dict_songs[id].play(looping, pos, rolloff, ref_dist)

    def stopSong(self,id=0):
        self.dict_songs[id].stop()

    def loadSounds(self):
        sounds = os.listdir("sounds/effects/")
        for ball in self.app.scene.ball_objects:
            self.dict_sounds[ball.id] = []
            for x in range(len(sounds)):
                self.dict_sounds[ball.id].append(Sound("sounds/effects/"+sounds[x]))
            
    def playSound(self,balls=[],effect=0):
        looping = False
        if effect == 0:
            pos = list(ti/2 for ti in balls[0].pos+balls[1].pos)
            ref_dist = float(np.sqrt((balls[1].velocity[0]-balls[0].velocity[0])**2 +
            (balls[1].velocity[2]-balls[0].velocity[2])**2))+0.4
        elif effect == 2:
            pos = balls[1]
            ref_dist  = float(np.sqrt(balls[0].velocity[0]**2+balls[0].velocity[2]**2))+0.5
        looping = False
        rolloff = 0.25
        self.dict_sounds[balls[0].id][effect].play(looping,pos,rolloff, ref_dist)
