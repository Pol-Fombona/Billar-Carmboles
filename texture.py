from numpy import size
import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}

        self.textures[5] = self.get_texture(path="textures/cue.png")
        self.textures[6] = self.get_texture(path="textures/TexturesCom_Grass_1K_albedo.jpg")
        self.textures[7] = self.get_texture(path="textures/brixton_finish.jpg")
        self.textures[8] = self.get_texture(path="textures/terra2.jpeg")
        self.textures[9] = self.get_texture(path="textures/ceiling-min.jpg")
        self.textures[10] = self.get_texture(path="textures/wall-new-compress-min.jpg")
        self.textures[11] = self.get_texture(path="textures/black.jpg")
        self.textures[12] = self.get_texture(path="textures/jukebox.jpg")
        self.textures[13] = self.get_texture(path="textures/counter.png")
        self.textures[14] = self.get_texture(path="textures/barchair.png")
        self.textures['skybox'] = self.get_texture_cube(dir_path = 'textures/', ext='png')

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

    def get_texture_cube(self,dir_path,ext = "png"):
        faces = ["right", "left", "top", "bottom", "front", "back"]
        textures = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces]
        
        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size = size, components = 3, data= None)
        
        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face = i, data = texture_data)
            
        return texture_cube

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
