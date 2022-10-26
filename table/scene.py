from model2 import *
from positions import *

# All the positions are set form here


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        add(Legs(app, pos=LEG_1))
        add(Legs(app, pos=LEG_2))
        add(Legs(app, pos=LEG_3))
        add(Legs(app, pos=LEG_4))
        add(Table(app, pos=TABLE_POSITION))
        add(TableFloor(app, pos=(0, 0, 0), tex_id=0))

    def render(self):
        for obj in self.objects:
            obj.render()
