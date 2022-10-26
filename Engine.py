import pygame as pg
import moderngl as mgl
import sys
import glm

from FreeCamera import Camera
from Object import Axis, Legs, Sphere, TableFloor, Table, Cue

from Light import Light
from MovementManagement import checkBallsCollisions, checkEdgeCollisions


class GraphicsEngine:
    def __init__(self, win_size=(900, 900)):
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
        # detect and use exixting opengl context

        # mouse grab
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx = mgl.create_context()
        # self.ctx.enable_only(mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.ctx.enable_only(mgl.DEPTH_TEST)

        ## clock
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0
        # Light
        self.light = Light()
        # camera
        self.camera = Camera(self)

        # scene
        # self.scene = Cube(self, pos=(10,1,0), rot=(0,0,0), scale = (0.1,0.4,0.1))

        # Esfera per particions horitzontals i verticals
        self.ball_1 = Sphere(
            self, pos=(20, 3, 10), radi=1, slices=20, stacks=20, color=(1, 1, 1)
        )

        self.ball_2 = Sphere(
            self, pos=(20, 3, 60), radi=1, slices=20, stacks=20, color=(1, 1, 0)
        )
        self.ball_3 = Sphere(
            self, pos=(23, 3, 60), radi=1, slices=20, stacks=20, color=(1, 1, 0)
        )
        self.ball_4 = Sphere(
            self, pos=(17, 3, 60), radi=1, slices=20, stacks=20, color=(1, 1, 0)
        )

        self.ball_5 = Sphere(
            self, pos=(26, 3, 65), radi=1, slices=20, stacks=20, color=(1, 0, 1)
        )
        self.ball_6 = Sphere(
            self, pos=(23, 3, 65), radi=1, slices=20, stacks=20, color=(1, 0, 1)
        )
        self.ball_7 = Sphere(
            self, pos=(20, 3, 65), radi=1, slices=20, stacks=20, color=(1, 0, 1)
        )
        self.ball_8 = Sphere(
            self, pos=(17, 3, 65), radi=1, slices=20, stacks=20, color=(1, 0, 1)
        )
        self.ball_9 = Sphere(
            self, pos=(14, 3, 65), radi=1, slices=20, stacks=20, color=(1, 0, 1)
        )

        self.ball_10 = Sphere(
            self, pos=(29, 3, 75), radi=1, slices=20, stacks=20, color=(0.8, 0.1, 1)
        )
        self.ball_11 = Sphere(
            self, pos=(26, 3, 75), radi=1, slices=20, stacks=20, color=(0.8, 0.1, 1)
        )
        self.ball_12 = Sphere(
            self, pos=(23, 3, 75), radi=1, slices=20, stacks=20, color=(0.8, 0.1, 1)
        )
        self.ball_13 = Sphere(
            self, pos=(20, 3, 75), radi=1, slices=20, stacks=20, color=(0.8, 0.1, 1)
        )
        self.ball_14 = Sphere(
            self, pos=(17, 3, 75), radi=1, slices=20, stacks=20, color=(0.8, 0.1, 1)
        )
        self.ball_15 = Sphere(
            self, pos=(14, 3, 75), radi=1, slices=20, stacks=20, color=(0.8, 0.1, 1)
        )
        self.ball_16 = Sphere(
            self, pos=(11, 3, 75), radi=1, slices=20, stacks=20, color=(0.8, 0.1, 1)
        )

        self.ball_17 = Sphere(
            self, pos=(20, 3, 80), radi=1, slices=20, stacks=20, color=(0.8, 0.1, 1)
        )

        # Esfera per subdivisions de triangles
        # from Object import SphereSubdivision
        # self.ball_1 = SphereSubdivision(self, depth = 3, pos=(5,3,10), color1=(1,0,0), color2=(1,1,0))
        # self.ball_2 = SphereSubdivision(self, depth = 3, pos=(10,3,10), color1=(0.5,0.5,0), color2=(0,1,1))
        # self.ball_3 = SphereSubdivision(self, depth = 3, pos=(15,3,10), color1=(0,0,1), color2=(1,0,1))

        self.objects = [
            self.ball_1,
            self.ball_2,
            self.ball_3,
            self.ball_4,
            self.ball_5,
            self.ball_6,
            self.ball_7,
            self.ball_8,
            self.ball_9,
            self.ball_10,
            self.ball_11,
            self.ball_12,
            self.ball_13,
            self.ball_14,
            self.ball_15,
            self.ball_16,
            self.ball_17,
        ]

        # Pal
        # CUE_LENGTH = 20
        # CUE_WIDTH = 1
        # CUE_HEIGTH = 1
        # DIST_BALL = 1.2
        self.cue = Cue(self, axis=glm.vec3(20, 3, 10))
        # self.cue = Cue(self,pos=(5,3,10))

        ###
        # Table
        #
        # Table measures
        # Les boles tnene diametre 61 mm vida real i radi 1 en el joc (-30.5x)
        # La taula 1,27 m de ancho por 2.54 de largo, en el joc 41,64 x 83.28

        TABLE_WIDTH = 41.64
        TABLE_LENGTH = 83.28
        TABLE_HEIGHT = 0.5
        MARGIN_WIDTH = 1
        LEGS_HEIGHT = 2
        TABLE_PROF = TABLE_HEIGHT / 2
        TABLE_POSITION = (-MARGIN_WIDTH, -TABLE_PROF, -MARGIN_WIDTH)

        self.leg1 = Legs(
            self,
            (TABLE_POSITION[0], TABLE_POSITION[1], TABLE_POSITION[2]),
            MARGIN_WIDTH,
            LEGS_HEIGHT,
            TABLE_HEIGHT,
        )
        self.leg2 = Legs(
            self,
            (
                TABLE_POSITION[0] + TABLE_WIDTH + MARGIN_WIDTH,
                TABLE_POSITION[1],
                TABLE_POSITION[2],
            ),
            MARGIN_WIDTH,
            LEGS_HEIGHT,
            TABLE_HEIGHT,
        )
        self.leg3 = Legs(
            self,
            (
                TABLE_POSITION[0] + TABLE_WIDTH + MARGIN_WIDTH,
                TABLE_POSITION[1],
                TABLE_POSITION[2] + TABLE_LENGTH + MARGIN_WIDTH,
            ),
            MARGIN_WIDTH,
            LEGS_HEIGHT,
            TABLE_HEIGHT,
        )
        self.leg4 = Legs(
            self,
            (
                TABLE_POSITION[0],
                TABLE_POSITION[1],
                TABLE_POSITION[2] + TABLE_LENGTH + MARGIN_WIDTH,
            ),
            MARGIN_WIDTH,
            LEGS_HEIGHT,
            TABLE_HEIGHT,
        )
        self.floor = TableFloor(
            self,
            (
                TABLE_POSITION[0] + MARGIN_WIDTH,
                TABLE_POSITION[1] + TABLE_PROF,
                TABLE_POSITION[2] + +MARGIN_WIDTH,
            ),
            TABLE_WIDTH,
            TABLE_HEIGHT / 2,
            TABLE_LENGTH,
        )
        self.table = Table(
            self,
            TABLE_POSITION,
            TABLE_WIDTH,
            TABLE_HEIGHT,
            TABLE_LENGTH,
            MARGIN_WIDTH,
        )

        self.table_objects = [
            self.leg1,
            self.leg2,
            self.leg3,
            self.leg4,
            self.floor,
            self.table,
        ]
        ###

        # axis
        self.axis = Axis(self)

        self.mode_rotate = False
        self.mode_object = True
        self.mode_birc_cam = True

        self.temp = (0, 0, 0)

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                for object in self.objects:
                    object.destroy()

                for objecte in self.table_objects:
                    objecte.destroy()

                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN and event.key == pg.K_b:

                self.mode_birc_cam = not self.mode_birc_cam

                if self.mode_birc_cam:
                    self.camera.bird_camera = True

                else:
                    self.camera.bird_camera = False

            elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                ## Reset positions

                for object in self.objects:
                    object.velocityX, object.velocityZ = 0, 0
                    object.pos = object.initial_position

            elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.ball_1.velocityX += -0.5
            elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.ball_1.velocityX += 0.5
            elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.ball_1.velocityZ += -0.5
            elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.ball_1.velocityZ += 0.5

            elif (
                event.type == pg.KEYDOWN
                and event.key == pg.K_k
                and not self.cue.displace_cue
            ):
                self.cue.rotate_flag = True
                self.cue.rotate_direction = 1
            elif (
                event.type == pg.KEYDOWN
                and event.key == pg.K_j
                and not self.cue.displace_cue
            ):
                self.cue.rotate_flag = True
                self.cue.rotate_direction = -1
            elif event.type == pg.KEYUP and event.key == pg.K_k:
                self.cue.rotate_flag = False
                self.cue.rotate_direction = 0
            elif event.type == pg.KEYUP and event.key == pg.K_j:
                self.cue.rotate_flag = False
                self.cue.rotate_direction = 0
            elif event.type == pg.MOUSEBUTTONDOWN and not self.cue.rotate_flag:
                self.cue.displace_cue = True
            elif event.type == pg.MOUSEBUTTONUP and not self.cue.rotate_flag:
                self.cue.displace_cue = False
                self.cue.reset_pos = False

    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.ctx.viewport = (0, 0, self.WIN_SIZE[0], self.WIN_SIZE[1])
        self.axis.render()

        for objecte in self.objects:
            objecte.render()

        self.cue.render()

        for objecte in self.table_objects:
            objecte.render()

        # Check balls collisions
        checkBallsCollisions(self.objects)
        checkEdgeCollisions(self.objects)

        pg.display.flip()

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)
