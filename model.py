import moderngl as mgl
import numpy as np
import glm
from MovementManagement import movement, IA_movement
from MoveCue import *
import MoveLine
import copy


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0)):
        self.app = app
        self.pos = pos
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)

        return m_model

    def update(self):
        self.texture.use()
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def render(self):
        self.update()
        self.vao.render()


class Legs(BaseModel):
    def __init__(self, app, vao_name="legs", tex_id=1, pos=(0, 0, 0)):
        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()

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
        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()

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
        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()

    def on_init(self):
        # light
        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia)
        self.program["light.Id"].write(self.app.light.Id)
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
                    radi=1, slices=10, stacks=10, vao_name="balls", 
                    tex_id="sphere1",id = 0):

        super().__init__(app, vao_name, tex_id, pos)

        # Initial position, useful when resseting position        
        self.initial_position = pos
        self.id = id
        self.translation = glm.mat4()
        self.rotation = glm.mat4()

        self.radi = radi
        self.velocity = np.array((0, 0, 0), dtype=float)

        self.slices = slices
        self.stacks = stacks

        self.on_init()

    def on_init(self):
        # light
        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia)
        self.program["light.Id"].write(self.app.light.Id)
        self.program["light.Is"].write(self.app.light.Is)
        self.program["light2.position"].write(self.app.light2.position)
        self.program["light2.Ia"].write(self.app.light2.Ia)
        self.program["light2.Id"].write(self.app.light2.Id)
        self.program["light2.Is"].write(self.app.light2.Is)
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_0"] = 0
        self.texture.use()
        # mvp
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def replay_render(self):
        self.replay_update()
        self.vao.render()

    def update(self):
        # self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.texture.use()
        self.program["m_view"].write(self.app.camera.m_view)
        self.program['camPos'].write(self.app.camera.position)

        self.translation, new_rotation = movement(self)

        if new_rotation != None:
            self.rotation = new_rotation * self.rotation

        m_model = self.translation * self.rotation
        self.m_model = m_model
        self.program["m_model"].write(m_model)

    def replay_update(self):
        # self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.texture.use()
        self.program["m_view"].write(self.app.camera.m_view)
        self.program['camPos'].write(self.app.camera.position)

        self.program["m_model"].write(self.m_model)

        self.vao.render()


    def IA_update(self):
        IA_movement(self)


class SubdivisionSphere(BaseModel):
    def __init__(
        self, app, pos=(0, 0, 0), radi=1, vao_name="subdivision_balls", tex_id=4,id = 0
    ):

        # Position intial, useful when resseting position
        self.initial_position = pos
        self.pos = pos
        self.id = id
        super().__init__(app, vao_name, tex_id, pos)

        self.translation = glm.mat4()
        self.rotation = glm.mat4()

        self.radi = radi
        # self.color = color

        ## velocity and friction
        self.velocity = np.array((0, 0, 0), dtype=float)
        # self.velocityX = 0
        # self.velocityZ = 0

        # self.rot = glm.vec3([glm.radians(a) for a in rot])
        # self.scale = scale
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
        self.m_model = m_model
        self.program["m_model"].write(m_model)
        self.program["camPos"].write(self.app.camera.position)

    def replay_render(self):
        self.replay_update()
        self.vao.render()

    def replay_update(self):
        # self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)
        self.program["m_model"].write(self.m_model)
        self.program["camPos"].write(self.app.camera.position)

class Cue(BaseModel):
    def __init__(
        self,
        app,
        tex_id=5,
        axis=glm.vec3((0, 0, 0)),
        rot=(0, 0, 0),
        scale=(1, 1, 1),
        length=0,
        width=0,
        heigth=0,
        dist_ball=0,
        vao_name="cue",
        max_distance = 20
    ):
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.axis = axis

        super().__init__(app, vao_name, tex_id, axis)

        self.length = length
        self.width = width
        self.heigth = heigth
        self.dist_ball = dist_ball
        self.max_distance = max_distance
        self.state = "stop"
        self.rotate_flag = False
        self.rotate_direction = 0
        self.angle = 0
        self.displace_cue = False
        self.reset_pos = True
        self.turn = 1
        self.moving = False
        self.pos = copy.deepcopy(self.axis)
        self.pos[0] += copy.deepcopy(self.dist_ball)
        self.pos_orig = glm.vec3(self.dist_ball, 0, 0)
        self.on_init()

    def get_model_matrix(self):

        m_model = glm.mat4()

        # translate (origen)
        m_model = glm.translate(m_model, (0, 0, 0))

        # rotation
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))

        # scale
        m_model = glm.scale(m_model, self.scale)

        # translate
        m_model = glm.translate(m_model, self.axis)

        return m_model

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_0"] = 0
        self.texture.use()

        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def update(self):
        self.texture.use()
        manage_move(self)
        
        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)
        self.program["m_model"].write(self.m_model)

class Terra(BaseModel):
    def __init__(
        self, 
        app, 
        vao_name="terra", 
        tex_id = 8, 
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        scale=(1, 1, 1),
    ):
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()

    def get_model_matrix(self):

        m_model = glm.mat4()

        # translate (origen)
        m_model = glm.translate(m_model, (0, 0, 0))

        # rotation
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))

        # scale
        m_model = glm.scale(m_model, self.scale)

        # translate
        m_model = glm.translate(m_model, self.pos)

        return m_model
    
    def on_init(self):
        
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_0"] = 0
        self.texture.use()
        
        self.program['m_proj'].write(self.app.camera.m_proj)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_model'].write(self.m_model)

class Sostre(BaseModel):
    def __init__(
        self, 
        app, 
        vao_name = "sostre", 
        tex_id = 9, 
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        scale=(1, 1, 1),
    ):
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale

        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()

    def get_model_matrix(self):

        m_model = glm.mat4()

        # translate (origen)
        m_model = glm.translate(m_model, (0, 0, 0))

        # rotation
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))

        # scale
        m_model = glm.scale(m_model, self.scale)

        # translate
        m_model = glm.translate(m_model, self.pos)

        return m_model
    
    def on_init(self):
        
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_0"] = 0
        self.texture.use()
        
        self.program['m_proj'].write(self.app.camera.m_proj)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_model'].write(self.m_model)

class Line(BaseModel):
    def __init__(
        self,
        app, 
        tex_id=None,
        vao_name = "line",
        axis = glm.vec3((0, 0, 0)),
        rot=(0, 0, 0),
        scale=(1, 1, 1),
        ):
        self.app = app
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.axis = glm.vec3(axis)
        self.angle = 0
        self.dist_ball = 0
        self.pos = copy.deepcopy(self.axis)
        self.pos[0] += copy.deepcopy(self.dist_ball)
        self.pos_orig = glm.vec3(self.dist_ball, 0, 0)
        self.moving = False
        self.perc = 1

        super().__init__(app, vao_name, tex_id, self.axis)
        self.on_init()
    
    def get_model_matrix(self):

        m_model = glm.mat4()

        # translate (origen)
        m_model = glm.translate(m_model, (0, 0, 0))

        # rotation
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))

        # scale
        m_model = glm.scale(m_model, self.scale)

        # translate
        m_model = glm.translate(m_model, self.axis)

        return m_model

    def on_init(self):
        MoveLine.scale_line(self)
        self.m_model = glm.scale(self.m_model,(self.perc,1,1))
        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def update(self):
        MoveLine.manage_move(self)
        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)
        self.program["m_model"].write(self.m_model)
    def render(self):
        self.update()
        self.vao.render(mgl.LINE_LOOP)

class Parets(BaseModel):
    def __init__(
        self, 
        app, 
        vao_name = "parets", 
        tex_id = 10, 
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        scale=(1, 1, 1),
    ):
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale

        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()

    def get_model_matrix(self):

        m_model = glm.mat4()

        # translate (origen)
        m_model = glm.translate(m_model, (0, 0, 0))

        # rotation
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))

        # scale
        m_model = glm.scale(m_model, self.scale)

        # translate
        m_model = glm.translate(m_model, self.pos)

        return m_model
    
    def on_init(self):
        
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_0"] = 0
        self.texture.use()
        
        self.program['m_proj'].write(self.app.camera.m_proj)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_model'].write(self.m_model)