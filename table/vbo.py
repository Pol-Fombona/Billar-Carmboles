import numpy as np
import moderngl as mgl
from positions import *


class VBO:
    def __init__(self, app):
        self.vbos = {}
        self.vbos["legs"] = LegsVBO(app)
        self.vbos["table"] = TableVBO(app)
        self.vbos["table_floor"] = TableFloorVBO(app)

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]


class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attrib: list = None

    def get_vertex_data(self):
        ...

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)

        return vbo

    def destroy(self):
        self.vbo.release()


class LegsVBO(BaseVBO):
    def __init__(self, app):
        ctx = app.ctx
        super().__init__(ctx)
        self.format = "2f 3f"
        self.attrib = ["in_texcoord_0", "in_position"]

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]

        return np.array(data, dtype="f4")

    def get_vertex_data(self):
        size = 0.2
        height = 2
        posx = 0
        posy = 0
        posz = 0
        vertices = [
            (posx, posy, posz),
            (posx + size, posy, posz),
            (posx + size, posy, posz + size),
            (posx, posy, posz + size),
            (posx, posy - height, posz),
            (posx + size, posy - height, posz),
            (posx + size, posy - height, posz + size),
            (posx, posy - height, posz + size),
        ]

        indices = [
            (0, 1, 2),
            (0, 2, 3),
            (4, 5, 6),
            (4, 6, 7),
            (0, 4, 5),
            (0, 5, 1),
            (1, 5, 6),
            (1, 6, 2),
            (2, 6, 7),
            (2, 7, 3),
            (0, 4, 7),
            (0, 7, 3),
        ]

        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (2, 3, 0),
            (2, 0, 1),
            (0, 2, 3),
            (0, 1, 2),
            (3, 1, 2),
            (3, 0, 1),
        ]

        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data


class TableVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app.ctx)
        self.format = "2f 3f"
        self.attrib = ["in_texcoord_0", "in_position"]

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]

        return np.array(data, dtype="f4")

    def get_vertex_data(self):
        x, y, z = (0, 0, 0)
        w = TABLE_WIDTH
        h = TABLE_HEIGHT
        p = TABLE_LENGTH
        width_table = MARGIN_WIDTH
        vertices = [
            # First
            (x, y, z),
            (x + width_table, y, z),
            (x + width_table, y + h, z),
            (x, y + h, z),
            (x, y, z + p + (width_table) * 2),
            (x + width_table, y, z + p + (width_table) * 2),
            (x + width_table, y + h, z + p + (width_table) * 2),
            (x, y + h, z + p + (width_table) * 2),
            # Second
            (x + width_table, y, z),
            (x + w + width_table, y, z),
            (x + w + width_table, y + h, z),
            (x + width_table, y + h, z),
            (x + width_table, y, z + width_table),
            (x + w + width_table, y, z + width_table),
            (x + w + width_table, y + h, z + width_table),
            (x + width_table, y + h, z + width_table),
            # Third
            (x + w + width_table, y, z),
            (x + w + width_table * 2, y, z),
            (x + w + width_table * 2, y + h, z),
            (x + w + width_table, y + h, z),
            (x + w + width_table, y, z + p + width_table * 2),
            (x + w + width_table * 2, y, z + p + width_table * 2),
            (x + w + width_table * 2, y + h, z + p + width_table * 2),
            (x + w + width_table, y + h, z + p + width_table * 2),
            # Fourth
            (x + width_table, y, z + p + width_table),
            (x + w + width_table, y, z + p + width_table),
            (x + w + width_table, y + h, z + p + width_table),
            (x + width_table, y + h, z + p + width_table),
            (x + width_table, y, z + p + width_table * 2),
            (x + w + width_table, y, z + p + width_table * 2),
            (x + w + width_table, y + h, z + p + width_table * 2),
            (x + width_table, y + h, z + p + width_table * 2),
        ]

        indices = [
            # Fist Rectangle
            (0, 1, 2),
            (0, 2, 3),
            (4, 5, 6),
            (4, 6, 7),
            (0, 1, 5),
            (0, 5, 4),
            (3, 2, 6),
            (3, 6, 7),
            (0, 4, 7),
            (0, 7, 3),
            # Second Rectangle
            (8, 9, 10),
            (8, 10, 11),
            (9, 13, 14),
            (9, 14, 10),
            (8, 12, 15),
            (8, 15, 11),
            (8, 9, 13),
            (8, 13, 12),
            (11, 10, 14),
            (11, 14, 15),
            # Third
            (16, 17, 18),
            (16, 18, 19),
            (20, 21, 22),
            (20, 22, 23),
            (17, 21, 22),
            (17, 22, 18),
            (16, 17, 21),
            (16, 21, 20),
            (19, 18, 22),
            (19, 22, 23),
            # Fourth
            (28, 29, 30),
            (28, 30, 31),
            (25, 29, 30),
            (25, 30, 26),
            (24, 28, 31),
            (24, 31, 27),
            (24, 25, 29),
            (24, 29, 28),
            (27, 26, 30),
            (27, 30, 31),
            # Under
            (12, 13, 25),
            (12, 25, 24),
        ]

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (2, 3, 0),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (2, 3, 0),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (2, 3, 0),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (2, 3, 0),
        ]

        vertex_data = self.get_data(vertices, indices)

        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data


class TableFloorVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app.ctx)
        self.format = "2f 3f"
        self.attrib = ["in_texcoord_0", "in_position"]

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vertex_data(self):
        x, y, z = (0, 0, 0)
        h = TABLE_PROF
        w = TABLE_WIDTH
        p = TABLE_LENGTH
        vertices = [
            (x, y, z),
            (x + w, y, z),
            (x + w, y + h, z),
            (x, y + h, z),
            (x, y, z + p),
            (x + w, y, z + p),
            (x + w, y + h, z + p),
            (x, y + h, z + p),
        ]

        indices = [
            (0, 1, 2),
            (0, 2, 3),
            (4, 5, 6),
            (4, 6, 7),
            (0, 4, 7),
            (0, 7, 3),
            (1, 5, 6),
            (1, 6, 2),
            (0, 1, 5),
            (0, 5, 4),
        ]

        vertex_data = self.get_data(vertices, indices)
        
        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (2, 3, 0),
            (2, 0, 1),
            (0, 2, 3),
            (0, 1, 2),
        ]

        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        vertex_data = np.hstack([tex_coord_data, vertex_data])
        

        return vertex_data
