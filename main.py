import pygame as pg
import moderngl as mgl
import time
import sys

from model import *
from FreeCamera import *
from mesh import Mesh
from scene import Scene
from MenuManager import pause_manager, progress_manager

from Light import Light
from MovementManagement import checkBallsCollisions, checkEdgeCollisions



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
    def __init__(self, win_size=(1600, 900)):
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
        self.scene.o = True
        self.delta_time = 0
        self.mode_bird_cam = True
        self.pause = False
        self.quit = False


    def check_events(self):
        if self.quit:
            self.mesh.destroy()
            pg.quit()
            sys.exit()

        for event in pg.event.get():

            if not self.pause:
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.pause = True

                elif event.type == pg.KEYDOWN and event.key == pg.K_o:
                    if not self.scene.o:
                        self.scene.pinfo = "Object: ON"
                        self.scene.o = True
                    else:
                        self.scene.pinfo = "Object: OFF"
                        self.scene.o = False
        
                elif event.type == pg.KEYDOWN and event.key == pg.K_b:

                    self.mode_bird_cam = not self.mode_bird_cam

                    if self.mode_bird_cam:
                        self.camera.bird_camera = True

                    else:
                        self.camera.bird_camera = False   

                elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    self.scene.ball_objects[0].velocityX += -0.5
                elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    self.scene.ball_objects[0].velocityX += 0.5
                elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                    self.scene.ball_objects[0].velocityZ += -0.5
                elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                    self.scene.ball_objects[0].velocityZ += 0.5

                elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                    ## Reset positions

                    for object in self.scene.ball_objects:
                        object.velocityX, object.velocityZ = 0, 0
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
                elif event.type == pg.MOUSEBUTTONDOWN and not self.scene.cue_objects[0].rotate_flag:
                    self.scene.cue_objects[0].displace_cue = True
                elif event.type == pg.MOUSEBUTTONUP and not self.scene.cue_objects[0].rotate_flag:
                    self.scene.cue_objects[0].displace_cue = False
                    self.scene.cue_objects[0].reset_pos = False

            

    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        if self.scene.o:
            self.scene.render()

        checkBallsCollisions(self.scene.ball_objects)
        checkEdgeCollisions(self.scene.ball_objects)

        #pg.display.set_caption(f" | {self.scene.pinfo} | {self.camera.pinfo}")
        # swap buffers
        pg.display.flip()

    def run(self):

        last_timestamp = time.time()
        played_time = 0

        while True:

            self.check_events()

            if self.pause:
                pg.event.set_grab(False)
                self.quit = pause_manager()
                pg.event.set_grab(True)
                self.pause = False
                last_timestamp = time.time()
                pg.event.clear()

            else:
                self.camera.update()
                self.render()

                played_time, last_timestamp = progress_manager(played_time, last_timestamp, time.time())
                self.delta_time = self.clock.tick(60)


if __name__ == "__main__":
    app = GraphicsEngine()
    app.run()
