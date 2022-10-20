from msilib import Table
import pygame as pg
import moderngl as mgl
import sys
import glm

from FreeCamera import Camera
from Object import Cube, Axis, Legs, Sphere, TableFloor, Table

from Light import Light
from MovementManagement import checkBallsCollisions, checkEdgeCollisions

class GraphicsEngine:
    def __init__(self, win_size=(900,900)):
        # init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = win_size
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # detect and use exixting opengl context

        # mouse grab
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx = mgl.create_context()
        #self.ctx.enable_only(mgl.DEPTH_TEST | mgl.CULL_FACE)
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
        #self.scene = Cube(self, pos=(10,1,0), rot=(0,0,0), scale = (0.1,0.4,0.1))

        # Esfera per particions horitzontals i verticals
        self.ball_1 = Sphere(self, pos =(5,3,10), radi = 1, slices= 20, stacks = 20)
        self.ball_2 = Sphere(self, pos =(5,3,15), radi = 1, slices= 20, stacks = 20)
        # Esfera per subdivisions de triangles
        #self.ball_1 = SphereSubdivision(self, depth = 3, pos=(5,3,10))
        #self.ball_2 = SphereSubdivision(self, depth = 3, pos=(5,3,15))

        self.objects = [self.ball_1, self.ball_2]

        ###
        # Table
        # 
        # Table measures
        # Les boles tnene diametre 61 mm vida real i radi 1 en el joc (-30.5x)
        # La taula 1,27 m de ancho por 2.54 de largo, en el joc 41,64 x 83.28

        TABLE_POSITION = (0, 2, 0)
        TABLE_WIDTH = 41.64
        TABLE_LENGTH = 83.28
        TABLE_HEIGHT = 0.5
        MARGIN_WIDTH = 1

        self.leg1 = Legs(self, TABLE_POSITION[0], TABLE_POSITION[2], MARGIN_WIDTH, 2)
        self.leg2 = Legs(self, TABLE_WIDTH + MARGIN_WIDTH, 0, MARGIN_WIDTH, 2)
        self.leg3 = Legs(
            self,
            TABLE_WIDTH + MARGIN_WIDTH,
            TABLE_LENGTH + MARGIN_WIDTH,
            MARGIN_WIDTH,
            2,
        )
        self.leg4 = Legs(
            self, TABLE_POSITION[0], TABLE_LENGTH + MARGIN_WIDTH, MARGIN_WIDTH, 2
        )
        self.floor = TableFloor(
            self,
            (MARGIN_WIDTH, TABLE_POSITION[1] + TABLE_HEIGHT / 2, MARGIN_WIDTH),
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

        self.table_objects = [self.leg1, self.leg2, self.leg3, self.leg4,
                                self.floor, self.table]
        ###

        # axis
        self.axis = Axis(self)

        self.mode_rotate = False
        self.mode_object = True
        self.mode_birc_cam = True

        self.temp = (0,0,0)



    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
         
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.ball_1.destroy()
                self.ball_2.destroy()

                for objecte in self.table_objects:
                    objecte.destroy()

                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.mode_rotate = not self.mode_rotate

                if self.mode_rotate:
                    self.ball_1.rotate = True

                else:
                    self.ball_1.rotate = False

            elif event.type == pg.KEYDOWN and event.key == pg.K_o:
                self.mode_object = not self.mode_object

                if self.mode_object:
                    self.ball_1.object = True

                else:
                    self.ball_1.object = False
   
            elif event.type == pg.KEYDOWN and event.key == pg.K_b:

                self.mode_birc_cam = not self.mode_birc_cam

                if self.mode_birc_cam:
                    self.camera.bird_camera = True

                else:
                    self.camera.bird_camera = False


            elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                ##reset positions

                self.ball_1.velocityX, self.ball_1.velocityZ = 0, 0
                self.ball_1.pos = (5,3,10)
                self.ball_2.velocityX, self.ball_2.velocityZ = 0, 0
                self.ball_2.pos = (5,3,15)


            elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.ball_1.velocityX += -0.5
            elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.ball_1.velocityX += 0.5
            elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.ball_1.velocityZ += -0.5
            elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.ball_1.velocityZ += 0.5
                
    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08,0.16,0.18))
        self.ctx.viewport = (0,0,self.WIN_SIZE[0],self.WIN_SIZE[1])
        self.axis.render()

        self.ball_1.render()
        self.ball_2.render()

        for objecte in self.table_objects:
            objecte.render()

        if self.ball_1.pos != self.temp:
            # Check balls collisions
            checkBallsCollisions(self.objects)
            checkEdgeCollisions(self.objects)
            self.temp = self.ball_1.pos


        pg.display.flip()
        
    def run(self):
         while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60) 

