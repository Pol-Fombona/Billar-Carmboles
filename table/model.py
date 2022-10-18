import glm
import numpy as np
import moderngl as mgl
import pygame as pg


class Table:
    def __init__(
        self, app, initial_pos=(0, 0, 0), width=0, height=0, prof=0, margin_width=0
    ):
        self.app = app
        self.ctx = app.ctx
        self.initial_pos = initial_pos
        self.width = width
        self.height = height
        self.prof = prof
        self.margin_width = margin_width
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program("table")
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture("table/textures/wooden-textured-background.jpg")
        self.on_init()

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(
            size=texture.get_size(),
            components=3,
            data=pg.image.tostring(texture, "RGB"),
        )

        return texture

    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model

    def on_init(self):
        # texture
        self.shader_program["u_texture_0"] = 0
        self.texture.use()
        # mvp
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def update(self):
        self.shader_program["m_view"].write(self.app.camera.m_view)

    def render(self):
        self.vao.render()
        self.update()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, "2f 3f", "in_texcoord_0", "in_position")]
        )
        return vao

    def get_vertex_data(self):
        x, y, z = self.initial_pos
        w = self.width
        h = self.height
        p = self.prof
        width_table = self.margin_width
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

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f"table/shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"table/shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )

        return program


class TableFloor:
    def __init__(self, app, pos=(1, 0, 1), w=0, h=0, p=0):
        self.app = app
        self.ctx = app.ctx
        self.pos = pos
        self.w = w
        self.h = h
        self.p = p
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program("table_floor")
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        # self.texture = self.get_texture("textures/pool_table_texture.jpg")
        self.on_init()

    def get_texture(self, path):
        texture2 = pg.image.load(path).convert()
        texture2 = pg.transform.flip(texture2, flip_x=False, flip_y=True)
        texture2 = self.ctx.texture(
            size=texture2.get_size(),
            components=3,
            data=pg.image.tostring(texture2, "RGB"),
        )

        return texture2

    def get_model_matrix(self):
        m_model = glm.mat4()
        # m_model = glm.rotate(glm.mat4(), glm.radians(45), glm.vec3(0, 1, 0))
        return m_model

    def on_init(self):
        # texture
        # self.shader_program["u_texture_1"] = 0
        # self.texture.use()
        # mvp
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def update(self):
        self.shader_program["m_view"].write(self.app.camera.m_view)

    def render(self):
        self.vao.render()
        self.update()
        # self.vaoa.render(mgl.LINE_LOOP)
        # self.vaop.render(mgl.POINTS)

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, "3f", "in_position")]
        )
        return vao

    def get_vertex_data(self):
        x, y, z = self.pos
        h = self.h
        w = self.w
        p = self.p
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
        """
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
        """

        return vertex_data

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f"table/shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"table/shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )

        return program


class Legs:
    def __init__(self, app, posx=0, posz=0, size=1, height=2):
        self.app = app
        self.ctx = app.ctx
        self.size = size
        self.height = height
        self.vbo = self.get_vbo(posx, posz)
        self.shader_program = self.get_shader_program("legs")
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture("table/textures/wooden-textured-background.jpg")
        self.on_init()

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(
            size=texture.get_size(),
            components=3,
            data=pg.image.tostring(texture, "RGB"),
        )

        return texture

    def get_model_matrix(self):
        m_model = glm.mat4()
        # m_model = glm.rotate(glm.mat4(), glm.radians(45), glm.vec3(0, 1, 0))
        return m_model

    def on_init(self):
        # texture
        self.shader_program["u_texture_0"] = 0
        self.texture.use()
        # mvp
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def update(self):
        self.shader_program["m_view"].write(self.app.camera.m_view)

    def render(self):
        self.vao.render()
        self.update()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, "2f 3f", "in_texcoord_0", "in_position")]
        )
        return vao

    def get_vertex_data(self, posx, posz):
        vertices = [
            (0, 0, 0),
            (self.size, 0, 0),
            (self.size, self.height, 0),
            (0, self.height, 0),
            (0, 0, self.size),
            (self.size, 0, self.size),
            (self.size, self.height, self.size),
            (0, self.height, self.size),
        ]
        vertices_end = []
        for (x, y, z) in vertices:
            vertices_end.append((x + posx, y, z + posz))

        indices = [
            (0, 2, 1),
            (0, 3, 2),
            (4, 5, 6),
            (4, 6, 7),
            (0, 1, 4),
            (1, 4, 5),
            (2, 3, 7),
            (2, 7, 6),
            (1, 2, 6),
            (1, 6, 5),
            (0, 4, 7),
            (0, 7, 3),
        ]
        vertex_data = self.get_data(vertices_end, indices)

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

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vbo(self, posx, posz):
        vertex_data = self.get_vertex_data(posx, posz)
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f"table/shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"table/shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )

        return program


class Axis:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program("axis")
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.on_init()

    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model

    def on_init(self):
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def update(self):
        self.shader_program["m_view"].write(self.app.camera.m_view)

    def render(self):
        self.vao.render(mgl.LINES)
        self.update()

    def get_vao(self):
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, "3f 3f", "in_color", "in_position")]
        )
        return vao

    def get_vertex_data(self):
        vertices = [(0, 0, 0), (2.54, 0, 0), (0, 2.54, 0), (0, 0, 2.54)]
        indices = [(0, 1), (0, 2), (0, 3)]
        vertex_data = self.get_data(vertices, indices)

        colors = [(1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1)]
        colors = np.array(colors, dtype="f4")

        vertex_data = np.hstack([colors, vertex_data])

        return vertex_data

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f"table/shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"table/shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )

        return program
