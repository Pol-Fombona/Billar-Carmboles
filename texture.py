from numpy import size
import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path="textures/pool_table_texture.jpg")
        self.textures[1] = self.get_texture(
            path="textures/wooden-textured-background.jpg"
        )
        self.textures[2] = self.get_texture(path="textures/test_mantel.png")
        #self.textures[3] = None # Falta per crear les textures de les boles
        #self.textures[4] = None # Falta per crear les textures de les boles subdivisions
        self.textures[5] = self.get_texture(path="textures/cue.png")


    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(
            size=texture.get_size(),
            components=3,
            data=pg.image.tostring(texture, "RGB"),
        )
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
