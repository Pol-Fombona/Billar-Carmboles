import moderngl as mgl
import numpy as np
import glm

cont = 0


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0)):
        global cont
        # TODO jugar amb el contador per a les posicions dels objectes
        self.app = app
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.pos = pos
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self):
        ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)

        return m_model

    def render(self):
        self.update()
        self.vao.render()


class Legs(BaseModel):
    def __init__(self, app, vao_name="legs", tex_id=1, pos=(0, 0, 0)):
        self.pos = pos
        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()

    def update(self):
        self.texture.use()
        # self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_0"] = 0
        self.texture.use()
        # mvp
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)


class Table(BaseModel):
    def __init__(self, app, vao_name="table", tex_id=1, pos=(0, 0, 0)):
        self.pos = pos
        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program["m_view"].write(self.camera.m_view)
        # self.program["m_model"].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_0"] = 0
        self.texture.use()
        # mvp
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)


class TableFloor(BaseModel):
    def __init__(self, app, vao_name="table_floor", tex_id=0, pos=(0, 0, 0)):
        self.pos = pos
        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program["m_view"].write(self.camera.m_view)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_0"] = 0
        self.texture.use()
        # mvp
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)
