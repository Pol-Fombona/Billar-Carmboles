from model import *
from positions import *

# All the positions are set form here


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.ball_objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def add_ball(self, obj):
        self.ball_objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object
        add_ball = self.add_ball

        add(Legs(app, pos=LEG_1))
        add(Legs(app, pos=LEG_2))
        add(Legs(app, pos=LEG_3))
        add(Legs(app, pos=LEG_4))
        add(Table(app, pos=TABLE_POSITION))
        add(TableFloor(app, pos=(0, 0, 0), tex_id=0))

        #add_ball(Sphere(app, pos=(20,1,10), tex_id=3))
        add_ball(SubdivisionSphere(app, pos=(20,1,10), tex_id=3))

        #add_ball(Sphere(app, pos=(20,1,60), tex_id=3))
        add_ball(Sphere(app, pos=(21,1,60), tex_id=3))
        add_ball(Sphere(app, pos=(19,1,60), tex_id=3))

        add_ball(Sphere(app, pos=(26,1,65), tex_id=3))
        add_ball(Sphere(app, pos=(23,1,65), tex_id=3))
        add_ball(Sphere(app, pos=(20,1,65), tex_id=3))
        add_ball(Sphere(app, pos=(17,1,65), tex_id=3))
        add_ball(Sphere(app, pos=(14,1,65), tex_id=3))

        add_ball(Sphere(app, pos=(29,1,75), tex_id=3))
        add_ball(Sphere(app, pos=(26,1,75), tex_id=3))
        add_ball(Sphere(app, pos=(23,1,75), tex_id=3))
        add_ball(Sphere(app, pos=(20,1,75), tex_id=3))
        add_ball(Sphere(app, pos=(17,1,75), tex_id=3))
        add_ball(Sphere(app, pos=(14,1,75), tex_id=3))
        add_ball(Sphere(app, pos=(11,1,75), tex_id=3))

        add_ball(Sphere(app, pos=(20,1,80), tex_id=3))

        self.objects = self.objects + self.ball_objects

    def render(self):
        for obj in self.objects:
            obj.render()
