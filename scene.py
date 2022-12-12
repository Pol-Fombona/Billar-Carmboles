from model import *
from positions import *

# All the positions are set form here


class Scene:
    def __init__(self, app):
        self.app = app
        self.mesh = app.mesh
        self.ctx = app.ctx
        self.table_objects = []
        self.ball_objects = []
        self.cue = None
        self.line = None
        # depth buffer
        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)
        if self.app.game_started:
            self.load()
        else:
            self.load_decision_starting() 

    def add_object(self, obj):
        self.table_objects.append(obj)

    def add_ball(self, obj):
        self.ball_objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object
        add_ball = self.add_ball

        add(Legs(app, pos=LEG_1, tex_id=7))
        add(Legs(app, pos=LEG_2, tex_id=7))
        add(Legs(app, pos=LEG_3, tex_id=7))
        add(Legs(app, pos=LEG_4, tex_id=7))
        add(Table(app, pos=TABLE_POSITION, tex_id=7))
        add(TableFloor(app, pos=(0, 0, 0), tex_id=6))

        # add_ball(Sphere(app, pos=(20,1,10), tex_id=3))
        #add_ball(SubdivisionSphere(app, pos=(20, 1, 10), tex_id=3,id = 1))

        # add_ball(Sphere(app, pos=(20,1,60), tex_id=3))
        first_sphere_position = (30, 1, 10)
        second_sphere_position = (10, 1, 10)
        third_sphere_position = (20, 1, 60)
        add_ball(Sphere(app, pos=first_sphere_position, tex_id="sphere1",id = 1))
        add_ball(Sphere(app, pos=second_sphere_position, tex_id="sphere2",id = 2))
        add_ball(Sphere(app, pos=third_sphere_position, tex_id="sphere3",id = 3))
        '''
        add_ball(Sphere(app, pos=(23, 1, 65), tex_id="sphere4",id = 5))
        add_ball(Sphere(app, pos=(20, 1, 65), tex_id="sphere5",id = 6))
        add_ball(Sphere(app, pos=(17, 1, 65), tex_id="sphere6",id = 7))
        add_ball(Sphere(app, pos=(14, 1, 65), tex_id="sphere7",id = 8))

        add_ball(Sphere(app, pos=(29, 1, 75), tex_id="sphere8",id = 9))
        add_ball(Sphere(app, pos=(26, 1, 75), tex_id="sphere9",id = 10))
        add_ball(Sphere(app, pos=(23, 1, 75), tex_id="sphere10",id = 11))
        add_ball(Sphere(app, pos=(20, 1, 75), tex_id="sphere11",id = 12))
        add_ball(Sphere(app, pos=(17, 1, 75), tex_id="sphere12",id = 13))
        add_ball(Sphere(app, pos=(14, 1, 75), tex_id="sphere13",id = 14))
        add_ball(Sphere(app, pos=(11, 1, 75), tex_id="sphere14",id = 15))

        add_ball(Sphere(app, pos=(20, 1, 80), tex_id="sphere15",id = 16))
        '''

        self.cue = Cue(app, axis=glm.vec3(first_sphere_position), tex_id=5)

        add(Terra(app, pos=(0,0,0),tex_id = 8))
        add(Sostre(app, pos=(0,0,0),tex_id = 9))

        self.line = Line(app, axis = glm.vec3(first_sphere_position))

        add(Parets(app, pos=(0,0,0),tex_id = 10))

        self.all_objects = self.table_objects + self.ball_objects + [self.cue,self.line]

    def load_decision_starting(self):
        app = self.app
        add = self.add_object
        add_ball = self.add_ball

        add(Legs(app, pos=LEG_1, tex_id=7))
        add(Legs(app, pos=LEG_2, tex_id=7))
        add(Legs(app, pos=LEG_3, tex_id=7))
        add(Legs(app, pos=LEG_4, tex_id=7))
        add(Table(app, pos=TABLE_POSITION, tex_id=7))
        add(TableFloor(app, pos=(0, 0, 0), tex_id=6))

        pos_sphere_1 = FIRST_BALLS_POSITION[0]
        pos_sphere_2 = FIRST_BALLS_POSITION[1]
        pos_sphere_3 = FIRST_BALLS_POSITION[2]

        add_ball(Sphere(app, pos=pos_sphere_1, tex_id="sphere1",id = 1))
        add_ball(Sphere(app, pos=pos_sphere_2, tex_id="sphere2",id = 2))

        add_ball(Sphere(app, pos=pos_sphere_3, tex_id="sphere3", id = 3))

        self.cue = Cue(app, axis=glm.vec3(pos_sphere_1), tex_id=5)

        add(Terra(app, pos=(0,0,0),tex_id = 8))
        add(Sostre(app, pos=(0,0,0),tex_id = 9))

        # self.line = Line(app, axis = glm.vec3(pos_sphere_1))
        # Per a que no doni error
        self.line = Cue(app, axis=glm.vec3(pos_sphere_1), tex_id=5)

        add(Parets(app, pos=(0,0,0),tex_id = 10))

        self.all_objects = self.table_objects + self.ball_objects + [self.cue,self.line]