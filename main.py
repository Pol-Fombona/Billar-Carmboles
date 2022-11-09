import pygame as pg
import moderngl as mgl
import time
import sys

from model import *
from FreeCamera import *
from mesh import Mesh
from scene import Scene
from MenuManager import pause_manager, progress_manager, format_time

from Light import Light
from MovementManagement import checkCollisions
from GameManager import *
from SoundManager import *



# Table measures
TABLE_WIDTH = 41.64
TABLE_LENGTH = 83.28
TABLE_HEIGHT = 0.5
MARGIN_WIDTH = 1
LEGS_HEIGHT = 500
TABLE_PROF = (
    TABLE_HEIGHT / 2
)  # Aixo es la profunditat de la moqueta a l'interor de la taula
# Per a tenir la moqueta de la taula a 0,0,0 aquestes son les coordenades de la taula => (-MARGIN_WIDTH, -TABLE_PROF, -MARGIN_WIDTH)
TABLE_POSITION = (-MARGIN_WIDTH, -TABLE_PROF, -MARGIN_WIDTH)


class GraphicsEngine:
    #def __init__(self, win_size=(1600, 900)):
    def __init__(self, win_size=(900, 500)):
        # init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = win_size
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # detect and use exixting opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST)
        # self.ctx.viewport(0,0,self.WIN_SIZE[0]/2,self.WIN_SIZE[1]/2)
        self.clock = pg.time.Clock()
        # camera
        '''
        self.camera = Camera(
            self,
            position=(
                TABLE_POSITION[0] + TABLE_WIDTH + 1,
                TABLE_POSITION[1] + TABLE_HEIGHT + 1,
                TABLE_POSITION[2] + TABLE_LENGTH,
            ),
            table_information=(TABLE_POSITION, TABLE_WIDTH, TABLE_HEIGHT, TABLE_LENGTH),
        )
        '''
        self.camera = Camera(self)
        # scene
        self.light = Light()
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.scene.pinfo = "Object: ON"
        self.delta_time = 0
        self.mode_bird_cam = True
        self.pause = False
        self.quit = False
        self.game = None
        self.sound = SoundManager()
        self.sound.loadSongs()
        self.sound.loadSounds()
        self.sound.playSong(0,0)


    def check_events(self):
        if self.quit:
            self.mesh.destroy()
            pg.quit()
            sys.exit()

        for event in pg.event.get():

            if not self.pause:
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.pause = True
        
                elif event.type == pg.KEYDOWN and event.key == pg.K_b:

                    self.mode_bird_cam = not self.mode_bird_cam

                    if self.mode_bird_cam:
                        self.camera.bird_camera = True

                    else:
                        self.camera.bird_camera = False   

                elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    self.scene.ball_objects[0].velocity[0] += -0.5
                elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    self.scene.ball_objects[0].velocity[0] += 0.5
                elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                    self.scene.ball_objects[0].velocity[2] += -0.5
                elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                    self.scene.ball_objects[0].velocity[2] += 0.5

                elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                    ## Reset positions

                    for object in self.scene.ball_objects:
                        object.velocity *= 0
                        object.pos = object.initial_position

                elif (
                    event.type == pg.KEYDOWN
                    and event.key == pg.K_k
                    and not self.scene.cue_objects[0].displace_cue
                ):
                    self.scene.cue_objects[0].rotate_flag = True
                    self.scene.cue_objects[0].rotate_direction = 1
                elif (
                    event.type == pg.KEYDOWN
                    and event.key == pg.K_j
                    and not self.scene.cue_objects[0].displace_cue
                ):
                    self.scene.cue_objects[0].rotate_flag = True
                    self.scene.cue_objects[0].rotate_direction = -1
                elif event.type == pg.KEYUP and event.key == pg.K_k:
                    self.scene.cue_objects[0].rotate_flag = False
                    self.scene.cue_objects[0].rotate_direction = 0
                elif event.type == pg.KEYUP and event.key == pg.K_j:
                    self.scene.cue_objects[0].rotate_flag = False
                    self.scene.cue_objects[0].rotate_direction = 0
                elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and not self.scene.cue_objects[0].rotate_flag:
                    self.scene.cue_objects[0].displace_cue = True
                elif event.type == pg.KEYUP and event.key == pg.K_SPACE and not self.scene.cue_objects[0].rotate_flag:
                    self.scene.cue_objects[0].displace_cue = False
                    self.scene.cue_objects[0].reset_pos = False

                if event.type == pg.KEYDOWN and event.key == pg.K_m:
                    if self.sound.song_playing:
                        self.sound.song_playing = False
                        self.sound.stopSong(0)
                    else:
                        self.sound.song_playing = True
                        self.sound.playSong(0,-1)       

    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.scene.render()

        checkCollisions(self.scene.ball_objects, self.sound)
        '''
        bcollision,blvel = checkBallsCollisions(self.scene.ball_objects)
        ecollision,elvel = checkEdgeCollisions(self.scene.ball_objects)
        if bcollision:
            self.sound.intensityBall(blvel)
            self.sound.playSound(0,0)
        if ecollision:
            self.sound.intensityEdge(elvel)
            self.sound.playSound(2,0)
        '''

        pg.display.set_caption(self.get_info())
        # swap buffers
        pg.display.flip()

    def get_info(self):
        # Returns info text (scores, time...) to show on top of window

        time_info = "Playing time: " + str(format_time(self.game.played_time))
        p1_score_info = "Scores: [" + self.game.player1.name + " - " + str(self.game.player1.score) + "; "
        p2_score_info = self.game.player2.name + " - " + str(self.game.player2.score) + "]"
        
        info = time_info + " | " + p1_score_info + p2_score_info + " | "
        return info


    def unpause(self):
        self.pause = False
        pg.event.clear()
        return time.time()

    def run(self):

        last_timestamp = time.time()
        
        player1 = Player(name = "P1", ball = self.scene.ball_objects[0])
        player2 = Player(name = "P2", ball = self.scene.ball_objects[1])

        self.game = Game(player1, player2, self.scene.ball_objects)
        
        while True:

            self.check_events()

            if self.pause:
                self.quit = pause_manager(self.game)
                last_timestamp = self.unpause()


            else:   

                self.camera.update()
                self.render()
                self.delta_time = self.clock.tick(60)
                self.game.played_time, last_timestamp = progress_manager(self.game.played_time, last_timestamp, time.time())


if __name__ == "__main__":
    app = GraphicsEngine()
    app.run()
