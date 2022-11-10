import numpy as np
import moderngl as mgl
from positions import *
import glm


class VBO:
    def __init__(self, app):
        self.vbos = {}
        self.vbos["legs"] = LegsVBO(app)
        self.vbos["table"] = TableVBO(app)
        self.vbos["table_floor"] = TableFloorVBO(app)
        self.vbos["balls"] = BallVBO(app)
        self.vbos["subdivision_balls"] = SubdivisionBallVBO(app)
        self.vbos["cue"] = CueVBO(app)

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
        size = LEGS_SIZE
        height = LEGS_HEIGHT
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
            # First
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (2, 3, 0),
            (2, 0, 1),
            (2, 3, 0),
            (2, 0, 1),
            (0, 1, 2),
            (0, 2, 3),
            # Second
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (2, 3, 0),
            (2, 0, 1),
            (2, 3, 0),
            (2, 0, 1),
            (0, 1, 2),
            (0, 2, 3),
            # Third
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (2, 3, 0),
            (2, 0, 1),
            (2, 3, 0),
            (2, 0, 1),
            (0, 1, 2),
            (0, 2, 3),
            # Fourth
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (2, 3, 0),
            (2, 0, 1),
            (2, 3, 0),
            (2, 0, 1),
            (0, 1, 2),
            (0, 2, 3),
            # Under
            (0, 1, 2),
            (0, 2, 3),
        ]

        vertex_data = self.get_data(vertices, indices)

        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data


class TableFloorVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app.ctx)
        self.format = "2f 3f 3f"
        self.attrib = ["in_texcoord_0", "in_normal", "in_position"]

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
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (2, 3, 0),
            (2, 0, 1),
            (2, 3, 0),
            (2, 0, 1),
            (0, 1, 2),
            (0, 2, 3),
        ]

        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        normals = [
            (0, 0, 1) * 6,
            (1, 0, 0) * 6,
            (0, 0, -1) * 6,
            (-1, 0, 0) * 6,
            (0, 1, 0) * 6,
        ]

        normals = np.array(normals, dtype="f4").reshape(30, 3)

        vertex_data = np.hstack([normals, vertex_data])

        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data


class BallVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app.ctx)
        self.format = "2f 3f 3f"
        self.attrib = ["in_texcoord_0", "in_normal", "in_position"]

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vertex_data(self):

        vertex_data = []
        normal_data = []
        tex_data = []
        """
        color = self.color
        slices = self.slices
        stacks = self.stacks
        radius = self.radi
        """
        color = BALL_COLOR
        slices = SLICES
        stacks = STACKS
        radius = RADIUS

        sinCache1a = []
        cosCache1a = []
        sinCache2a = []
        cosCache2a = []

        sinCache1b = []
        cosCache1b = []
        sinCache2b = []
        cosCache2b = []

        for i in range(slices):
            angle = 2 * np.pi * i / slices
            sinCache1a.append(np.sin(angle))
            cosCache1a.append(np.cos(angle))
            sinCache2a.append(sinCache1a[i])
            cosCache2a.append(cosCache1a[i])

        for j in range(stacks + 1):
            angle = np.pi * j / stacks
            sinCache2b.append(np.sin(angle))
            cosCache2b.append(np.cos(angle))
            sinCache1b.append(radius * np.sin(angle))
            cosCache1b.append(radius * np.cos(angle))

        sinCache1b[0] = 0
        sinCache1b.append(0)

        sinCache1a.append(sinCache1a[0])
        cosCache1a.append(cosCache1a[0])

        sinCache2a.append(sinCache2a[0])
        cosCache2a.append(cosCache2a[0])

        finish = stacks

        for j in range(finish):
            zLow = cosCache1b[j]
            zHigh = cosCache1b[j + 1]
            sintemp1 = sinCache1b[j]
            sintemp2 = sinCache1b[j + 1]
            sintemp3 = sinCache2b[j + 1]
            costemp3 = cosCache2b[j + 1]
            sintemp4 = sinCache2b[j]
            costemp4 = cosCache2b[j]

            for i in range(slices):
                v1 = (sintemp2 * sinCache1a[i], sintemp2 * cosCache1a[i], zHigh)
                n1 = (sinCache2a[i] * sintemp3, cosCache2a[i] * sintemp3, costemp3)

                v2 = (sintemp1 * sinCache1a[i], sintemp1 * cosCache1a[i], zLow)
                n2 = (sinCache2a[i] * sintemp4, cosCache2a[i] * sintemp4, costemp4)

                v3 = (sintemp1 * sinCache1a[i + 1], sintemp1 * cosCache1a[i + 1], zLow)
                n3 = (sinCache2a[i+1] * sintemp4, cosCache2a[i+1] * sintemp4, costemp4)

                v4 = (sintemp1 * sinCache1a[i + 1], sintemp1 * cosCache1a[i + 1], zLow)
                n4 = (sinCache2a[i+1] * sintemp4, cosCache2a[i+1] * sintemp4, costemp4)

                v5 = (sintemp2 * sinCache1a[i + 1], sintemp2 * cosCache1a[i + 1], zHigh)
                n5 = (sinCache2a[i+1] * sintemp3, cosCache2a[i+1]*sintemp3, costemp3)

                v6 = (sintemp2 * sinCache1a[i], sintemp2 * cosCache1a[i], zHigh)
                n6 = (sinCache2a[i] * sintemp3, cosCache2a[i] * sintemp3, costemp3)

                texture1 = (float(i)/slices, float(j+1) / stacks)
                texture2 = (float(i)/slices, float(j) / stacks)
                texture3 = (float(i+1)/slices, float(j) / stacks)
                texture4 = (float(i+1)/slices, float(j) / stacks)
                texture5 = (float(i+1)/slices, float(j+1) / stacks)
                texture6 = (float(i)/slices, float(j+1) / stacks)

                normal_data.append(n1), vertex_data.append(v1), tex_data.append(texture1)
                normal_data.append(n2), vertex_data.append(v2), tex_data.append(texture2)
                normal_data.append(n3), vertex_data.append(v3), tex_data.append(texture3)
                normal_data.append(n4), vertex_data.append(v4), tex_data.append(texture4)
                normal_data.append(n5), vertex_data.append(v5), tex_data.append(texture5)
                normal_data.append(n6), vertex_data.append(v6), tex_data.append(texture6)


        vertex_data = np.array(vertex_data, dtype="f4")
        normal_data = np.array(normal_data, dtype="f4")
        tex_data = np.array(tex_data, dtype="f4")

        vertex_data = np.hstack([normal_data, vertex_data])
        vertex_data = np.hstack([tex_data, vertex_data])

        return vertex_data


class SubdivisionBallVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app.ctx)
        self.format = "3f 3f 3f"
        self.attrib = ["in_color", "in_normal", "in_position"]

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vertex_data(self):

        data = []
        v1 = np.array([0.0, 0.0, 0.0])
        v2 = np.array([1.0, 0.0, 0.0])
        v3 = np.array([1.0, 0.0, 1.0])
        v4 = np.array([0.0, 0.0, 1.0])
        v5 = np.array([0.5, 1.0, 0.5])
        v6 = np.array([0.5, -1.0, 0.5])

        c = (
            v1 + v2 + v3 + v4 + v5 + v6
        ) / 6.0  # calculo el centre per treure'l i centrar la figura
        v1 -= c
        v2 -= c
        v3 -= c
        v4 -= c
        v5 -= c
        v6 -= c

        color = (
            (1, 0, 0),
            (1, 1, 0),
            (0, 1, 1),
            (0, 1, 0),
            (0, 0, 1),
            (1, 0, 1),
            (0.5, 0.5, 0.5),
            (1, 0.5, 0.3),
        )

        color = (
            SDCOLOR1,
            SDCOLOR1,
            SDCOLOR1,
            SDCOLOR1,
            SDCOLOR2,
            SDCOLOR2,
            SDCOLOR2,
            SDCOLOR2,
        )

        # Part superior
        data.append(
            (color[0], glm.normalize(v1), glm.normalize(v1))
        )  # primer triangle (cara) : color, normal, position
        data.append(
            (color[0], glm.normalize(v5), glm.normalize(v5))
        )  # primer triangle (cara)
        data.append(
            (color[0], glm.normalize(v2), glm.normalize(v2))
        )  # primer triangle (cara)

        data.append((color[1], glm.normalize(v2), glm.normalize(v2)))
        data.append((color[1], glm.normalize(v5), glm.normalize(v5)))
        data.append((color[1], glm.normalize(v3), glm.normalize(v3)))

        data.append((color[2], glm.normalize(v3), glm.normalize(v3)))
        data.append((color[2], glm.normalize(v5), glm.normalize(v5)))
        data.append((color[2], glm.normalize(v4), glm.normalize(v4)))

        data.append((color[3], glm.normalize(v4), glm.normalize(v4)))
        data.append((color[3], glm.normalize(v5), glm.normalize(v5)))
        data.append((color[3], glm.normalize(v1), glm.normalize(v1)))

        ###Part inferior
        data.append((color[4], glm.normalize(v6), glm.normalize(v6)))
        data.append((color[4], glm.normalize(v1), glm.normalize(v1)))
        data.append((color[4], glm.normalize(v2), glm.normalize(v2)))

        data.append((color[5], glm.normalize(v6), glm.normalize(v6)))
        data.append((color[5], glm.normalize(v2), glm.normalize(v2)))
        data.append((color[5], glm.normalize(v3), glm.normalize(v3)))

        data.append((color[6], glm.normalize(v6), glm.normalize(v6)))
        data.append((color[6], glm.normalize(v3), glm.normalize(v3)))
        data.append((color[6], glm.normalize(v4), glm.normalize(v4)))

        data.append((color[7], glm.normalize(v6), glm.normalize(v6)))
        data.append((color[7], glm.normalize(v4), glm.normalize(v4)))
        data.append((color[7], glm.normalize(v1), glm.normalize(v1)))

        data = self.tessel(data, SDDEPTH)

        return np.array(data, dtype="f4")

    def tessel(self, data, depth):

        if depth == 0:
            return data

        else:
            depth -= 1
            new_data = []

            for i in range(0, len(data), 3):

                v12 = glm.normalize((data[i][1] + data[i + 1][1]) / 2)
                v13 = glm.normalize((data[i][1] + data[i + 2][1]) / 2)
                v23 = glm.normalize((data[i + 1][1] + data[i + 2][1]) / 2)

                new_data.append((data[i][0], v12, v12))
                new_data.append((data[i][0], v13, v13))
                new_data.append((data[i][0], data[i][1], data[i][2]))

                new_data.append((data[i + 2][0], v23, v23))
                new_data.append((data[i + 2][0], data[i + 2][1], data[i + 2][2]))
                new_data.append((data[i + 2][0], v13, v13))

                new_data.append((data[i + 1][0], data[i + 1][1], data[i + 1][2]))
                new_data.append((data[i + 1][0], v23, v23))
                new_data.append((data[i + 1][0], v12, v12))

                new_data.append((data[i][0], v12, v12))
                new_data.append((data[i + 2][0], v23, v23))
                new_data.append((data[i + 1][0], v13, v13))

            new_data = self.tessel(new_data, depth)

            return new_data


class CueVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app.ctx)
        self.format = "2f 3f"
        self.attrib = ["in_texcoord_0", "in_position"]

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vertex_data(self):
        vertices = [
            (1.2, 4.47035e-08, 4.47035e-08),
            (19.2, 4.47035e-08, 4.47035e-08),
            (19.2, -0.6, -0.6),
            (19.2, 0.6, -0.6),
            (1.2, -0.1, -0.1),
            (1.2, -0.1, 0.1),
            (19.2, -0.6, 0.6),
            (19.2, 0.6, 0.6),
            (1.2, 0.1, 0.1),
            (1.2, 0.1, -0.1),
            (1.2, -0.0667, -0.126),
            (1.2, -0.0333, -0.136),
            (1.2, 4.47035e-08, -0.1414),
            (1.2, 0.0333, -0.136),
            (1.2, 0.0667, -0.126),
            (19.2, -0.4, -0.756),
            (19.2, -0.2, -0.816),
            (19.2, 4.47035e-08, -0.8485),
            (19.2, 0.2, -0.816),
            (19.2, 0.4, -0.756),
            (1.2, -0.126, -0.0667),
            (1.2, -0.136, -0.0333),
            (1.2, -0.1414, 4.47035e-08),
            (1.2, -0.136, 0.0333),
            (1.2, -0.126, 0.0667),
            (19.2, -0.756, -0.4),
            (19.2, -0.816, -0.2),
            (19.2, -0.8485, 4.47035e-08),
            (19.2, -0.816, 0.2),
            (19.2, -0.756, 0.4),
            (1.2, -0.0667, 0.126),
            (1.2, -0.0333, 0.136),
            (1.2, 4.47035e-08, 0.1414),
            (1.2, 0.0333, 0.136),
            (1.2, 0.0667, 0.126),
            (19.2, -0.4, 0.756),
            (19.2, -0.2, 0.816),
            (19.2, 4.47035e-08, 0.8485),
            (19.2, 0.2, 0.816),
            (19.2, 0.4, 0.756),
            (1.2, 0.126, -0.0667),
            (1.2, 0.136, -0.0333),
            (1.2, 0.1414, 4.47035e-08),
            (1.2, 0.136, 0.0333),
            (1.2, 0.126, 0.0667),
            (19.2, 0.756, -0.4),
            (19.2, 0.816, -0.2),
            (19.2, 0.8485, 4.47035e-08),
            (19.2, 0.816, 0.2),
            (19.2, 0.756, 0.4),
        ]

        indices = [
            (0, 9, 40),
            (0, 41, 40),
            (0, 41, 42),
            (0, 42, 43),
            (0, 43, 44),
            (0, 44, 8),
            (0, 5, 30),
            (0, 30, 31),
            (0, 31, 32),
            (0, 32, 33),
            (0, 33, 34),
            (0, 34, 8),
            (0, 4, 20),
            (0, 20, 21),
            (0, 21, 22),
            (0, 22, 23),
            (0, 23, 24),
            (0, 24, 5),
            (0, 9, 14),
            (0, 14, 13),
            (0, 13, 12),
            (0, 12, 11),
            (0, 11, 10),
            (0, 10, 4),
            (1, 6, 35),
            (1, 35, 36),
            (1, 36, 37),
            (1, 37, 38),
            (1, 38, 39),
            (1, 39, 7),
            (1, 2, 25),
            (1, 25, 26),
            (1, 26, 27),
            (1, 27, 28),
            (1, 28, 29),
            (1, 29, 6),
            (1, 3, 19),
            (1, 19, 18),
            (1, 18, 17),
            (1, 17, 16),
            (1, 16, 15),
            (1, 15, 2),
            (1, 7, 49),
            (1, 49, 48),
            (1, 48, 47),
            (1, 47, 46),
            (1, 46, 45),
            (1, 45, 3),
            (4, 2, 10),
            (10, 2, 15),
            (10, 15, 11),
            (11, 15, 16),
            (11, 16, 12),
            (12, 16, 17),
            (12, 17, 13),
            (13, 17, 18),
            (13, 18, 14),
            (14, 18, 19),
            (14, 19, 9),
            (9, 19, 3),
            (9, 3, 40),
            (40, 3, 45),
            (40, 45, 41),
            (41, 45, 46),
            (41, 46, 42),
            (42, 46, 47),
            (42, 47, 43),
            (43, 47, 48),
            (43, 48, 44),
            (44, 48, 49),
            (44, 49, 8),
            (8, 49, 7),
            (8, 7, 30),
            (30, 7, 39),
            (30, 35, 31),
            (31, 35, 36),
            (31, 36, 32),
            (32, 36, 37),
            (32, 37, 33),
            (33, 37, 38),
            (33, 38, 34),
            (34, 38, 39),
            (34, 35, 5),
            (5, 35, 6),
            (5, 6, 20),
            (20, 6, 29),
            (20, 25, 21),
            (21, 25, 26),
            (21, 26, 22),
            (22, 26, 27),
            (22, 27, 23),
            (23, 27, 28),
            (23, 28, 24),
            (24, 28, 29),
            (24, 25, 4),
            (4, 25, 2),
        ]

        vertex_data = self.get_data(vertices, indices)

        tex_coord = [
            (1 / 2, 1 / 2),
            (1 / 2, 1 / 2),
            (-1, -1),
            (2, -1),
            (0.25, 0.25),
            (0.25, 0.75),
            (-1, 2),
            (2, 2),
            (0.75, 0.75),
            (0.75, 0.25),
            (1 / 3, 0.185),
            (5 / 12, 0.16),
            (3 / 6, 0.1465),
            (7 / 12, 0.16),
            (2 / 3, 0.185),
            (-0.5, -1.39),
            (0, -1.54),
            (0.5, -1.6213),
            (1, -1.54),
            (1.5, -1.39),
            (0.185, 1 / 3),
            (0.16, 5 / 12),
            (0.1465, 3 / 6),
            (0.16, 7 / 12),
            (0.185, 2 / 3),
            (-1.39, -0.5),
            (-1.54, 0),
            (-1.6213, 3 / 6),
            (-1.54, 1),
            (-1.39, 1.5),
            (1 / 3, 0.815),
            (5 / 12, 0.84),
            (3 / 6, 0.8535),
            (7 / 12, 0.84),
            (2 / 3, 0.815),
            (-0.5, 2.39),
            (0, 2.54),
            (3 / 6, 2.6213),
            (1, 2.54),
            (1.5, 2.39),
            (0.815, 1 / 3),
            (0.84, 5 / 12),
            (0.8535, 3 / 6),
            (0.84, 7 / 12),
            (0.815, 2 / 3),
            (2.39, -0.5),
            (2.54, 0),
            (2.6213, 3 / 6),
            (2.54, 1),
            (2.39, 1.5),
        ]

        tex_coord_indices = [
            (0, 9, 40),
            (0, 41, 40),
            (0, 41, 42),
            (0, 42, 43),
            (0, 43, 44),
            (0, 44, 8),
            (0, 5, 30),
            (0, 30, 31),
            (0, 31, 32),
            (0, 32, 33),
            (0, 33, 34),
            (0, 34, 8),
            (0, 4, 20),
            (0, 20, 21),
            (0, 21, 22),
            (0, 22, 23),
            (0, 23, 24),
            (0, 24, 5),
            (0, 9, 14),
            (0, 14, 13),
            (0, 13, 12),
            (0, 12, 11),
            (0, 11, 10),
            (0, 10, 4),
            (1, 6, 35),
            (1, 35, 36),
            (1, 36, 37),
            (1, 37, 38),
            (1, 38, 39),
            (1, 39, 7),
            (1, 2, 25),
            (1, 25, 26),
            (1, 26, 27),
            (1, 27, 28),
            (1, 28, 29),
            (1, 29, 6),
            (1, 3, 19),
            (1, 19, 18),
            (1, 18, 17),
            (1, 17, 16),
            (1, 16, 15),
            (1, 15, 2),
            (1, 7, 49),
            (1, 49, 48),
            (1, 48, 47),
            (1, 47, 46),
            (1, 46, 45),
            (1, 45, 3),
            (4, 2, 10),
            (10, 2, 15),
            (10, 15, 11),
            (11, 15, 16),
            (11, 16, 12),
            (12, 16, 17),
            (12, 17, 13),
            (13, 17, 18),
            (13, 18, 14),
            (14, 18, 19),
            (14, 19, 9),
            (9, 19, 3),
            (9, 3, 40),
            (40, 3, 45),
            (40, 45, 41),
            (41, 45, 46),
            (41, 46, 42),
            (42, 46, 47),
            (42, 47, 43),
            (43, 47, 48),
            (43, 48, 44),
            (44, 48, 49),
            (44, 49, 8),
            (8, 49, 7),
            (8, 7, 30),
            (30, 7, 39),
            (30, 35, 31),
            (31, 35, 36),
            (31, 36, 32),
            (32, 36, 37),
            (32, 37, 33),
            (33, 37, 38),
            (33, 38, 34),
            (34, 38, 39),
            (34, 35, 5),
            (5, 35, 6),
            (5, 6, 20),
            (20, 6, 29),
            (20, 25, 21),
            (21, 25, 26),
            (21, 26, 22),
            (22, 26, 27),
            (22, 27, 23),
            (23, 27, 28),
            (23, 28, 24),
            (24, 28, 29),
            (24, 25, 4),
            (4, 25, 2),
        ]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data
