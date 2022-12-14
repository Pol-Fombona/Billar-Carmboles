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
        self.vao_name = vao_name
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def on_init(self):
        # # shadow
        # self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        # self.shadow_program = self.shadow_vao.program
        # self.shadow_program['m_proj'].write(self.camera.m_proj)
        # self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        # self.shadow_program['m_model'].write(self.m_model)
        # light
        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia)
        self.program["light.Id"].write(self.app.light.Id)
        self.program["light.Is"].write(self.app.light.Is)
        self.program["light2.position"].write(self.app.light2.position)
        self.program["light2.Ia"].write(self.app.light2.Ia)
        self.program["light2.Id"].write(self.app.light2.Id)
        self.program["light2.Is"].write(self.app.light2.Is)
        self.program["light3.position"].write(self.app.light3.position)
        self.program["light3.Ia"].write(self.app.light3.Ia)
        self.program["light3.Id"].write(self.app.light3.Id)
        self.program["light3.Is"].write(self.app.light3.Is)
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_0"] = 0
        self.texture.use()
        # mvp
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)

        return m_model

    def update(self):
        self.texture.use()
        self.program["m_view"].write(self.camera.m_view)
        self.program['camPos'].write(self.app.camera.position)
        self.program["m_model"].write(self.m_model)

    def render(self):
        self.update()
        self.vao.render()
    
    def update_shadow(self):
        try:
            self.shadow_program['m_model'].write(self.m_model)
        except:
            pass
    
    def render_shadow(self):
        try:
            self.update_shadow()
            self.shadow_vao.render()
        except:
            pass


class Legs(BaseModel):
    def __init__(self, app, vao_name="legs", tex_id=1, pos=(0, 0, 0)):
        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()


class Table(BaseModel):
    def __init__(self, app, vao_name="table", tex_id=1, pos=(0, 0, 0)):
        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()


class TableFloor(BaseModel):
    def __init__(self, app, vao_name="table_floor", tex_id=0, pos=(0, 0, 0)):
        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()


class Sphere(BaseModel):
    def __init__(self, app, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1),
                    radi=1, slices=10, stacks=10, vao_name="balls", 
                    tex_id="sphere1",id = 0, ombra=None):

        super().__init__(app, vao_name, tex_id, pos)

        # Initial position, useful when resseting position        
        self.initial_position = pos
        self.id = id
        self.translation = glm.mat4()
        self.rotation = glm.mat4()

        self.radi = radi
        self.velocity = np.array((0, 0, 0), dtype=float)
        self.abs_velocity = 0

        self.slices = slices
        self.stacks = stacks

        self.ombra = ombra

        self.on_init()

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
        # Move ombra
        if self.ombra != None:
            self.ombra.pos = (self.pos[0] + 0.6, self.pos[1] - 0.9, self.pos[2] + 0.6)


    def replay_update(self):
        # self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.texture.use()
        self.program["m_view"].write(self.app.camera.m_view)
        self.program['camPos'].write(self.app.camera.position)

        self.program["m_model"].write(self.m_model)

        self.vao.render()


    def IA_update(self):
        IA_movement(self)

    def update_velocity_values(self, new_vel):
        # Updata both velocity values (normal and absolute)
        self.velocity = np.array(new_vel)
        self.abs_velocity = sum(abs(new_vel))

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
        # shadow
        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)
        # light
        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia)
        self.program["light.Id"].write(self.app.light.Id)
    
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

class SkyBox(BaseModel):
    def __init__(self,app, vao_name='skybox',tex_id='skybox', pos=(0,0,0), rot=(0,0,0),scale=(1,1,1)):
        super().__init__(app, vao_name,tex_id, pos)
        self.on_init()
    
    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))
        
        
    def on_init(self):
        self.texture= self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_skybox"] = 0
        self.texture.use(location=0)

        
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
    

class OmbresEsferes(BaseModel):
    def __init__(
        self, 
        app, 
        vao_name = "ombres_esferes", 
        tex_id = 11, 
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

    def update(self):
        self.texture.use()
        self.program["m_view"].write(self.camera.m_view)
        self.program['camPos'].write(self.app.camera.position)
        self.program["m_model"].write(self.get_model_matrix())


class Jukebox(BaseModel):
    def __init__(self, app, vao_name="jukebox", tex_id=12, pos=(0, 0, 0),rot=(0, 0, 0),scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3(rot)
        self.scale = glm.vec3(scale)
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao_name = vao_name
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera
        
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

class Counter(BaseModel):
    def __init__(self, app, vao_name="counter", tex_id=13, pos=(0, 0, 0),rot=(0, 0, 0),scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3(rot)
        self.scale = glm.vec3(scale)
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao_name = vao_name
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera
        
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


class Barchair(BaseModel):
    def __init__(self, app, vao_name="barchair", tex_id=14, pos=(0, 0, 0),rot=(0, 0, 0),scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3(rot)
        self.scale = glm.vec3(scale)
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao_name = vao_name
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera
        
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
