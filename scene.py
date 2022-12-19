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

    def render_shadow(self):
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.table_objects:
            obj.render_shadow()

        for sphere in self.ball_objects:
            sphere.render_shadow()
        

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

        ombra1 = OmbresEsferes(app, pos=(first_sphere_position[0], first_sphere_position[1] - 0.9, first_sphere_position[2]))
        ombra2 = OmbresEsferes(app, pos=(second_sphere_position[0], second_sphere_position[1] - 0.9, second_sphere_position[2]))
        ombra3 = OmbresEsferes(app, pos=(third_sphere_position[0], third_sphere_position[1] - 0.9, third_sphere_position[2]))

        add_ball(Sphere(app, pos=first_sphere_position, tex_id="sphere1",id = 1, ombra=ombra1))
        add_ball(Sphere(app, pos=second_sphere_position, tex_id="sphere2",id = 2, ombra=ombra2))
        add_ball(Sphere(app, pos=third_sphere_position, tex_id="sphere3",id = 3, ombra=ombra3))
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

        add(Jukebox(app, pos=(-20,-5,-35.5),scale = (4,4,4), tex_id = 12))
        add(Counter(app, pos=(-10,-2,12.16),scale = (10,10,10), tex_id = 13))
        add(Barchair(app, pos=(-14,-4,12),scale = (5,5,5), tex_id = 14))
        add(Barchair(app, pos=(-14,-4,24),scale = (5,5,5), tex_id = 14))
        add(Barchair(app, pos=(-14,-4,36),scale = (5,5,5), tex_id = 14))

        # Han de ser els ultims objectes
        add(ombra1)
        add(ombra2)
        add(ombra3)

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

        ombra1 = OmbresEsferes(app, pos=(pos_sphere_1[0], pos_sphere_1[1] - 0.9, pos_sphere_1[2]))
        ombra2 = OmbresEsferes(app, pos=(pos_sphere_2[0], pos_sphere_2[1] - 0.9, pos_sphere_2[2]))
        ombra3 = OmbresEsferes(app, pos=(pos_sphere_3[0], pos_sphere_3[1] - 0.9, pos_sphere_3[2]))

        add_ball(Sphere(app, pos=pos_sphere_1, tex_id="sphere1",id = 1, ombra=ombra1))
        add_ball(Sphere(app, pos=pos_sphere_2, tex_id="sphere2",id = 2, ombra=ombra2))

        add_ball(Sphere(app, pos=pos_sphere_3, tex_id="sphere3", id = 3, ombra=ombra3))

        self.cue = Cue(app, axis=glm.vec3(pos_sphere_1), tex_id=5)

        add(Terra(app, pos=(0,0,0),tex_id = 8))
        add(Sostre(app, pos=(0,0,0),tex_id = 9))

        self.line = Line(app, axis = glm.vec3(pos_sphere_1))

        add(Parets(app, pos=(0,0,0),tex_id = 10))

        add(Jukebox(app, pos=(-20,-5,-35.5),scale = (4,4,4), tex_id = 12))
        add(Counter(app, pos=(-10,-2,12.16),scale = (10,10,10), tex_id = 13))
        add(Barchair(app, pos=(-14,-4,12),scale = (5,5,5), tex_id = 14))
        add(Barchair(app, pos=(-14,-4,24),scale = (5,5,5), tex_id = 14))
        add(Barchair(app, pos=(-14,-4,36),scale = (5,5,5), tex_id = 14))

        # Han de ser els ultims objectes
        add(ombra1)
        add(ombra2)
        add(ombra3)

        self.all_objects = self.table_objects + self.ball_objects + [self.cue,self.line]



    def render(self):
        self.ctx.screen.use()
        # Render table + spheres

        # self.render_shadow()

        for obj in self.table_objects:
            obj.render()

        for sphere in self.ball_objects:
            sphere.render()


    def render_with_cue(self):
        # Render table + spheres + cue

        for obj in self.all_objects:
            obj.render()


    def replay_render(self):
        # Render table + special render spheres

        for obj in self.table_objects[:-3]:
            obj.render()

        for sphere in self.ball_objects:
            sphere.replay_render()
        