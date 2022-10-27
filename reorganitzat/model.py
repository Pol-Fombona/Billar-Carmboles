import moderngl as mgl
import numpy as np
import glm
from MovementManagement import movement


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0)):
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


class Sphere(BaseModel):
    def __init__(self, app, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1),
        color=(0, 0, 0), radi=1, slices=10, stacks=10, vao_name="balls", tex_id=3):

        # Position intial, useful when resseting position
        self.initial_position = pos
        self.pos = pos

        super().__init__(app, vao_name, tex_id, pos)

        self.translation = glm.mat4()
        self.rotation = glm.mat4()

        self.radi = radi
        #self.color = color

        ## velocity and friction
        self.velocityX = 0
        self.velocityZ = 0

        self.slices = slices
        self.stacks = stacks

        #self.rot = glm.vec3([glm.radians(a) for a in rot])
        #self.scale = scale
        self.on_init()

    def on_init(self):
        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia)
        self.program["light.Id"].write(self.app.light.Id)

        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def update(self):
        # self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)

        self.translation, new_rotation = movement(self)

        if new_rotation != None:
            self.rotation = new_rotation * self.rotation

        m_model = self.translation * self.rotation

        self.program["m_model"].write(m_model)


class SubdivisionSphere(BaseModel):
    def __init__(self, app, pos=(0, 0, 0), radi=1, 
        vao_name="subdivision_balls", tex_id=4):

        # Position intial, useful when resseting position
        self.initial_position = pos
        self.pos = pos

        super().__init__(app, vao_name, tex_id, pos)

        self.translation = glm.mat4()
        self.rotation = glm.mat4()

        self.radi = radi
        #self.color = color

        ## velocity and friction
        self.velocityX = 0
        self.velocityZ = 0

        #self.rot = glm.vec3([glm.radians(a) for a in rot])
        #self.scale = scale
        self.on_init()

    def on_init(self):
        # Light
        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia)
        self.program["light.Id"].write(self.app.light.Id)
        self.program["light.Is"].write(self.app.light.Is)

        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def update(self):
        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)

        self.translation, new_rotation = movement(self)

        if new_rotation != None:
            self.rotation = new_rotation * self.rotation

        m_model = self.translation * self.rotation
        self.program["m_model"].write(m_model)
        self.program["camPos"].write(self.app.camera.position)