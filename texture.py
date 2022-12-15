from numpy import size
import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}

        self.textures[5] = self.get_texture(path="textures/cue.png")
        self.textures[6] = self.get_texture(path="textures/pool_table2.jpg")
        self.textures[7] = self.get_texture(path="textures/brixton_finish.jpg")
        self.textures[8] = self.get_texture(path="textures/floor-texture-refactor.jfif")
        self.textures[9] = self.get_texture(path="textures/ceiling.jpg")
        self.textures[10] = self.get_texture(path="textures/wall-new-compress.jpg")

        # Spheres  [https://sharecg.com/v/12975/view/6/Texture/Billiard-Ball-N%B0-10]
        self.textures["sphere1"] = self.get_texture(path="textures/spheres/sphere (1).jpg")
        self.textures["sphere2"] = self.get_texture(path="textures/spheres/sphere (2).jpg")
        self.textures["sphere3"] = self.get_texture(path="textures/spheres/sphere (3).jpg")
        
        self.textures["depth_texture"] = self.get_depth_texture()


    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        return depth_texture

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
