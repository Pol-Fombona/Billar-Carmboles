import glm
import moderngl as mgl
import numpy as np
import pygame as pg

from MovementManagement import movement
import copy
from MoveCue import displace_cue, rotate_cue, reset_displace_cue, points_distance, cue_hit_ball, change_objective


class Object:
    def __init__(self, app, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program()
        self.vao = self.get_vao()
        self.vaoa = self.get_vao()
        self.vaop = self.get_vao()
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
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
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def update(self):
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
        self.vaop.release()
        self.vaoa.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, "3f 3f", "in_color", "in_position")]
        )
        return vao

    def get_vertex_data(self):

        # vertices = [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]

        vertices = [
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
        ]

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
        vertex_data = self.get_data(vertices, indices)
        return vertex_data

    @staticmethod
    def get_data(vertices, indices, colour):
        # data = [vertices[ind] for triangle in indices for ind in triangle]
        data = [
            (colour[i], vertices[ind])
            for i, triangle in enumerate(indices)
            for ind in triangle
        ]
        return np.array(data, dtype="f4")

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self):
        program = self.ctx.program(
            vertex_shader="""
                #version 330
                layout (location = 0) in vec3 in_color;
                layout (location = 1) in vec3 in_position;
                out vec3 color;
                uniform mat4 m_proj;
                uniform mat4 m_view;
                uniform mat4 m_model;
                void main() {
                    color = in_color;
                    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                layout (location = 0) out vec4 fragColor;
                in vec3 color;
                void main() { 
                    //vec3 color = vec3(1,1,0);
                    fragColor = vec4(color,1.0);
                }
            """,
        )
        return program


class Axis:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program()
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.on_init()
        self.a = True

    def get_model_matrix(self):
        m_model = glm.mat4()
        # m_model = glm.rotate(glm.mat4(),glm.radians(45),glm.vec3(0,1,0))
        return m_model

    def on_init(self):
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def update(self):
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def render(self):
        self.update()
        if self.a:
            self.vao.render(mgl.LINES)

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, "3f 3f", "in_color", "in_position")]
        )
        return vao

    def get_vertex_data(self):

        vertices = [
            (0, 0, 0),
            (100, 0, 0),
            (0, 100, 0),
            (0, 0, 100),
            (0, 0, 0),
            (0, 0, 0),
        ]
        indices = [(0, 1), (2, 4), (3, 5)]
        indices_colours = [0, 0, 1, 1, 2, 2]
        colours = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

        vertex_data = self.get_data(vertices, indices, colours, indices_colours)
        return vertex_data

    @staticmethod
    def get_data(vertices, indices, color, indices_colours):
        #        data = [("", vertices[ind]) for triangle in indices for ind in triangle]

        data = [
            (color[i], vertices[ind])
            for i, triangle in enumerate(indices)
            for ind in triangle
        ]
        return np.array(data, dtype="f4")

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self):
        program = self.ctx.program(
            vertex_shader="""
                #version 330
                layout (location = 0) in vec3 in_color;
                layout (location = 1) in vec3 in_position;
                out vec3 color;
                uniform mat4 m_proj;
                uniform mat4 m_view;
                uniform mat4 m_model;
                void main() {
                    color = in_color;
                    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                layout (location = 0) out vec4 fragColor;
                in vec3 color;
                void main() { 
                    //vec3 color = vec3(1,1,1);
                    fragColor = vec4(color,1.0);
                }
            """,
        )
        return program


class Sphere:
    def __init__(
        self,
        app,
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        scale=(1, 1, 1),
        color=(0,0,0),
        radi=1,
        slices=10,
        stacks=10,
    ):
        self.app = app
        self.ctx = app.ctx
        self.radi = radi
        self.color = color

        self.last_rotation = (0, 1, 1)
        self.collisions = {"vX":False, "vZ":False}
        
        ## velocity and friction
        self.velocityX = 0
        self.velocityZ = 0

        self.slices = slices
        self.stacks = stacks
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program()
        self.vao = self.get_vao()
        self.vaoa = self.get_vao()
        self.vaop = self.get_vao()

        # Position intial, useful when resseting position
        self.initial_position = pos
        
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
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
        self.shader_program["light.position"].write(self.app.light.position)
        self.shader_program["light.Ia"].write(self.app.light.Ia)
        self.shader_program["light.Id"].write(self.app.light.Id)

        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def update(self):
        # self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)

        m_model = self.m_model

        m_model = movement(self, m_model)
        self.shader_program["m_model"].write(m_model)

    def render(self):
        self.update()

        self.vao.render()
        #self.vaoa.render(mgl.LINE_LOOP)

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
        self.vaoa.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(
            self.shader_program,
            [(self.vbo, "3f 3f 3f", "in_color", "in_normal", "in_position")],
        )
        return vao

    def get_vertex_data(self):

        vertex_data = []
        color = self.color
        slices = self.slices
        stacks = self.stacks
        radius = self.radi

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

        start = 0
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
                v2 = (sintemp1 * sinCache1a[i], sintemp1 * cosCache1a[i], zLow)
                v3 = (sintemp1 * sinCache1a[i + 1], sintemp1 * cosCache1a[i + 1], zLow)
                v4 = (sintemp1 * sinCache1a[i + 1], sintemp1 * cosCache1a[i + 1], zLow)
                v5 = (sintemp2 * sinCache1a[i + 1], sintemp2 * cosCache1a[i + 1], zHigh)
                v6 = (sintemp2 * sinCache1a[i], sintemp2 * cosCache1a[i], zHigh)
                vertex_data.append((color, v1, v1))
                vertex_data.append((color, v2, v2))
                vertex_data.append((color, v3, v3))
                vertex_data.append((color, v4, v4))
                vertex_data.append((color, v5, v5))
                vertex_data.append((color, v6, v6))

        vertex_data = np.array(vertex_data, dtype="f4")
        return vertex_data

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self):
        program = self.ctx.program(
            vertex_shader="""
                #version 330 core
                layout (location = 0) in vec3 in_color;
                layout (location = 1) in vec3 in_normal;
                layout (location = 2) in vec3 in_position;
                out vec3 color;
                
                struct Light {
                    vec3 position;
                    vec3 Ia;
                    vec3 Id;
                    vec3 Is;
                };
                
                uniform Light light;
                uniform mat4 m_proj;
                uniform mat4 m_view;
                uniform mat4 m_model;
                
                void main() {
                    vec3 normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
                    vec3 ambient = light.Ia;
                    vec3 diffuse = light.Id * max(0,dot(normalize(light.position-in_position),normalize(normal)));
                    color = in_color * (ambient + diffuse);
                    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
                }
            """,
            fragment_shader="""
                #version 330 core
                layout (location = 0) out vec4 fragColor;
                in vec3 color;
                void main() {
                    fragColor = vec4(color,1);
                }
            """,
        )
        return program

class Cue:
    def __init__(self, app, axis=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), length = 0, width = 0, heigth = 0, dist_ball = 0):
        self.app = app
        self.ctx = app.ctx
        self.length = length
        self.width = width
        self.heigth = heigth
        self.dist_ball = dist_ball
        self.rotate_flag = False
        self.rotate_direction = 0
        self.angle = 0
        self.displace_cue = False
        self.reset_pos = True
        self.turn = 1
        self.moving = False
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program()
        self.vao = self.get_vao()
        self.axis = axis
        self.pos = copy.deepcopy(self.axis)
        self.pos[0]+=copy.deepcopy(self.dist_ball)
        self.pos_orig = glm.vec3(self.dist_ball,0,0)
        #self.pos_reset = copy.deepcopy(self.pos)
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(path = "textures/cue.PNG")
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
        self.shader_program['u_texture_0']=0
        self.texture.use()

        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x= False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components = 3, data = pg.image.tostring(texture, "RGB"))
        return texture

    def update(self):
        if self.app.ball_1.velocityX==self.app.ball_1.velocityZ==0:
            if self.app.ball_2.velocityX==self.app.ball_2.velocityZ==0:
                if self.moving == True:
                    if self.turn == 1:
                        change_objective(self, self.app.ball_1)
                    else:
                        change_objective(self, self.app.ball_2)
                    self.moving=False
                if self.rotate_flag == True:
                    rotate_cue(self)
                if self.displace_cue == True and points_distance(self.axis,self.pos)<=20:
                    displace_cue(self)
                if self.displace_cue == False and self.reset_pos==False:
                    reset_displace_cue(self)
                    self.reset_pos=True
                    if self.turn == 1:
                        cue_hit_ball(self,self.app.ball_1)
                    else:
                        cue_hit_ball(self,self.app.ball_2)
                    self.turn*=-1
                    self.pos = copy.deepcopy(self.axis)
                    self.pos[0] = self.dist_ball
                    self.pos_orig = glm.vec3(self.dist_ball,0,0)
                    self.moving = True
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f', 'in_texcoord_0', 'in_position')])
        return vao

    def get_vertex_data(self):
        vertices = [( 1.2, 4.47035e-08, 4.47035e-08 ), ( 19.2, 4.47035e-08, 4.47035e-08 ), ( 19.2, -0.6, -0.6 ), ( 19.2, 0.6, -0.6 ), ( 1.2, -0.1, -0.1 ), 
                    ( 1.2, -0.1, 0.1 ), ( 19.2, -0.6, 0.6 ), ( 19.2, 0.6, 0.6 ), ( 1.2, 0.1, 0.1 ), ( 1.2, 0.1, -0.1 ), ( 1.2, -0.0667, -0.126 ), 
                    ( 1.2, -0.0333, -0.136 ), ( 1.2, 4.47035e-08, -0.1414 ), ( 1.2, 0.0333, -0.136 ), ( 1.2, 0.0667, -0.126 ), ( 19.2, -0.4, -0.756 ),
                    ( 19.2, -0.2, -0.816 ), ( 19.2, 4.47035e-08, -0.8485 ), ( 19.2, 0.2, -0.816 ), ( 19.2, 0.4, -0.756 ), ( 1.2, -0.126, -0.0667 ), 
                    ( 1.2, -0.136, -0.0333 ), ( 1.2, -0.1414, 4.47035e-08 ), ( 1.2, -0.136, 0.0333 ), ( 1.2, -0.126, 0.0667 ), ( 19.2, -0.756, -0.4 ), 
                    ( 19.2, -0.816, -0.2 ), ( 19.2, -0.8485, 4.47035e-08 ), ( 19.2, -0.816, 0.2 ), ( 19.2, -0.756, 0.4 ), ( 1.2, -0.0667, 0.126 ), 
                    ( 1.2, -0.0333, 0.136 ), ( 1.2, 4.47035e-08, 0.1414 ), ( 1.2, 0.0333, 0.136 ), ( 1.2, 0.0667, 0.126 ), ( 19.2, -0.4, 0.756 ), 
                    ( 19.2, -0.2, 0.816 ), ( 19.2, 4.47035e-08, 0.8485 ), ( 19.2, 0.2, 0.816 ), ( 19.2, 0.4, 0.756 ), ( 1.2, 0.126, -0.0667 ), 
                    ( 1.2, 0.136, -0.0333 ), ( 1.2, 0.1414, 4.47035e-08 ), ( 1.2, 0.136, 0.0333 ), ( 1.2, 0.126, 0.0667 ), ( 19.2, 0.756, -0.4 ), 
                    ( 19.2, 0.816, -0.2 ), ( 19.2, 0.8485, 4.47035e-08 ), ( 19.2, 0.816, 0.2 ), ( 19.2, 0.756, 0.4 )]

        indices =[(0,9,40),(0,41,40),(0,41,42),(0,42,43),(0,43,44),(0,44,8),(0,5,30),(0,30,31),(0,31,32),(0,32,33),
                   (0,33,34),(0,34,8),(0,4,20),(0,20,21),(0,21,22),(0,22,23),(0,23,24),(0,24,5),(0,9,14),(0,14,13),
                   (0,13,12),(0,12,11),(0,11,10),(0,10,4),(1,6,35),(1,35,36),(1,36,37),(1,37,38),(1,38,39),(1,39,7),
                   (1,2,25),(1,25,26),(1,26,27),(1,27,28),(1,28,29),(1,29,6),(1,3,19),(1,19,18),(1,18,17),(1,17,16),
                   (1,16,15),(1,15,2),(1,7,49),(1,49,48),(1,48,47),(1,47,46),(1,46,45),(1,45,3),
                    (4,2,10),(10,2,15),(10,15,11),(11,15,16),(11,16,12),(12,16,17),(12,17,13),(13,17,18),(13,18,14),(14,18,19),(14,19,9),(9,19,3),
                    (9,3,40),(40,3,45),(40,45,41),(41,45,46),(41,46,42),(42,46,47),(42,47,43),(43,47,48),(43,48,44),(44,48,49),(44,49,8),(8,49,7),
                    (8,7,30),(30,7,39),(30,35,31),(31,35,36),(31,36,32),(32,36,37),(32,37,33),(33,37,38),(33,38,34),(34,38,39),(34,35,5),(5,35,6),
                    (5,6,20),(20,6,29),(20,25,21),(21,25,26),(21,26,22),(22,26,27),(22,27,23),(23,27,28),(23,28,24),(24,28,29),(24,25,4),(4,25,2)]
                    
        
        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(1/2,1/2),(1/2,1/2),(-1,-1),(2,-1),(0.25,0.25),(0.25,0.75),(-1,2),(2,2),(0.75,0.75),(0.75,0.25),(1/3,0.185),(5/12,0.16),
                    (3/6,0.1465),(7/12,0.16),(2/3,0.185),(-0.5,-1.39),(0,-1.54),(0.5,-1.6213),(1,-1.54),(1.5,-1.39),
                    (0.185,1/3),(0.16,5/12),(0.1465,3/6),(0.16,7/12),(0.185,2/3),(-1.39,-0.5),(-1.54,0),(-1.6213,3/6),
                    (-1.54,1),(-1.39,1.5),(1/3,0.815),(5/12,0.84),(3/6,0.8535),(7/12,0.84),(2/3,0.815),(-0.5,2.39),(0,2.54),
                    (3/6,2.6213),(1,2.54),(1.5,2.39),(0.815,1/3),(0.84,5/12),(0.8535,3/6),(0.84,7/12),(0.815,2/3),(2.39,-0.5),
                    (2.54,0),(2.6213,3/6),(2.54,1),(2.39,1.5)]
        
        tex_coord_indices = [(0,9,40),(0,41,40),(0,41,42),(0,42,43),(0,43,44),(0,44,8),(0,5,30),(0,30,31),(0,31,32),(0,32,33),
                   (0,33,34),(0,34,8),(0,4,20),(0,20,21),(0,21,22),(0,22,23),(0,23,24),(0,24,5),(0,9,14),(0,14,13),
                   (0,13,12),(0,12,11),(0,11,10),(0,10,4),(1,6,35),(1,35,36),(1,36,37),(1,37,38),(1,38,39),(1,39,7),
                   (1,2,25),(1,25,26),(1,26,27),(1,27,28),(1,28,29),(1,29,6),(1,3,19),(1,19,18),(1,18,17),(1,17,16),
                   (1,16,15),(1,15,2),(1,7,49),(1,49,48),(1,48,47),(1,47,46),(1,46,45),(1,45,3),
                    (4,2,10),(10,2,15),(10,15,11),(11,15,16),(11,16,12),(12,16,17),(12,17,13),(13,17,18),(13,18,14),(14,18,19),(14,19,9),(9,19,3),
                    (9,3,40),(40,3,45),(40,45,41),(41,45,46),(41,46,42),(42,46,47),(42,47,43),(43,47,48),(43,48,44),(44,48,49),(44,49,8),(8,49,7),
                    (8,7,30),(30,7,39),(30,35,31),(31,35,36),(31,36,32),(32,36,37),(32,37,33),(33,37,38),(33,38,34),(34,38,39),(34,35,5),(5,35,6),
                    (5,6,20),(20,6,29),(20,25,21),(21,25,26),(21,26,22),(22,26,27),(22,27,23),(23,27,28),(23,28,24),(24,28,29),(24,25,4),(4,25,2)]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)
        
        vertex_data = np.hstack([tex_coord_data,vertex_data])
        return vertex_data

    @staticmethod
    def get_data(vertices, indices): 
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self):
        program = self.ctx.program(    
            vertex_shader='''
                #version 330
                layout (location = 0) in vec2 in_texcoord_0;
                layout (location = 1) in vec3 in_position;
                out vec2 uv_0;
                uniform mat4 m_proj;
                uniform mat4 m_view;
                uniform mat4 m_model;
                void main() {
                    uv_0 = in_texcoord_0;
                    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330
                layout (location = 0) out vec4 fragColor;
                in vec2 uv_0;
                uniform sampler2D u_texture_0;
                void main() { 
                    vec3 color = texture(u_texture_0, uv_0).rgb;
                    fragColor = vec4(color,1.0);
                }
            ''',
        )
        return program


class Cube:
    def __init__(self, app, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program()
        self.vao = self.get_vao()
        self.vaoa = self.get_vao()
        self.vaop = self.get_vao()
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
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
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def update(self):
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        # self.shader_program['m_model'].write(self.m_model)
        # m_model = glm.rotate(self.m_model, 3*self.app.time, glm.vec3(0,1,0))
        self.shader_program["m_model"].write(self.m_model)

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
        self.vaop.release()
        self.vaoa.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, "3f 3f", "in_color", "in_position")]
        )
        return vao

    def get_vertex_data(self):

        # vertices = [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]

        vertices = [
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
        ]

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

        colours = [
            (1, 0, 0),
            (0, 1, 0),
            (1, 0, 0),
            (0, 1, 0),
            (1, 0, 0),
            (0, 1, 0),
            (1, 0, 0),
            (0, 1, 0),
            (1, 0, 0),
            (0, 1, 0),
            (1, 0, 0),
            (0, 1, 0),
        ]
        vertex_data = self.get_data(vertices, indices, colours)
        return vertex_data

    @staticmethod
    def get_data(vertices, indices, colours):
        # data = [vertices[ind] for triangle in indices for ind in triangle]
        data = [
            (colours[i], vertices[ind])
            for i, triangle in enumerate(indices)
            for ind in triangle
        ]
        return np.array(data, dtype="f4")

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self):
        program = self.ctx.program(
            vertex_shader="""
                #version 330
                layout (location = 0) in vec3 in_color;
                layout (location = 1) in vec3 in_position;
                out vec3 color;
                uniform mat4 m_proj;
                uniform mat4 m_view;
                uniform mat4 m_model;
                void main() {
                    color = in_color;
                    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                layout (location = 0) out vec4 fragColor;
                in vec3 color;
                void main() { 
                    //vec3 color = vec3(1,1,0);
                    fragColor = vec4(color,1.0);
                }
            """,
        )
        return program


def norm(v):

    length = (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) ** (1 / 2)
    v = v / length

    return v


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
        self.texture = self.get_texture("textures/wooden-textured-background.jpg")
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
        self.shader_program["m_proj"].write(self.app.camera.m_proj)

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
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"shaders/{shader_name}.frag") as file:
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
        self.shader_program["m_proj"].write(self.app.camera.m_proj)

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
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"shaders/{shader_name}.frag") as file:
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
        self.texture = self.get_texture("textures/wooden-textured-background.jpg")
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
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )

        return program



class SphereSubdivision:
    def __init__(self,app, pos=(0,0,0), rot=(0,0,0), scale = (1,1,1), depth = 0, color1 = (0,0,0), color2 = (0,0,0)):
        self.app = app
        self.depth = depth
        self.ctx = app.ctx

        self.color1 = color1
        self.color2 = color2
        self.radi = 1

        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program()

        self.last_rotation = (0, 1, 1)
        self.collisions = {"vX":False, "vZ":False}


        self.vao = self.get_vao()
        self.vaoa = self.get_vao()
        self.vaop = self.get_vao()

        # Position intial, useful when resseting position
        self.initial_position = pos

        self.pos = pos

        self.rotate = False
        self.object = True

        ## velocity and friction
        self.velocityX = 0
        self.velocityZ = 0

        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.on_init()

        
    def get_model_matrix(self):
        
        m_model = glm.mat4()
        
        #translate (origen)
        m_model = glm.translate(m_model, (0,0,0))

        # rotation
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1,0,0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0,1,0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0,0,1))

        # scale 
        m_model = glm.scale(m_model, self.scale)
        
        # translate
        m_model = glm.translate(m_model, self.pos)
        return m_model

                
    def on_init(self):
        # Light
        self.shader_program['light.position'].write(self.app.light.position)
        self.shader_program['light.Ia'].write(self.app.light.Ia)
        self.shader_program['light.Id'].write(self.app.light.Id)
        self.shader_program['light.Is'].write(self.app.light.Is)


        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)

    def update(self):
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
                
        m_model = self.m_model

        m_model = movement(self, m_model)
        
        self.shader_program['m_model'].write(m_model)
        self.shader_program['camPos'].write(self.app.camera.position)

    def render(self):
        self.update()

        self.vao.render()
        #self.vaoa.render(mgl.LINE_LOOP)      
        
    def destroy (self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
        self.vaop.release()
        self.vaoa.release()
    
    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f 3f 3f', 'in_color', 'in_normal', 'in_position')])
        return vao
    
    def get_vertex_data(self):

        data = []
        v1 = np.array([0.,0.,0.])
        v2 = np.array([1.,0.,0.])
        v3 = np.array([1.,0.,1.])
        v4 = np.array([0.,0.,1.])
        v5 = np.array([0.5,1.,0.5])
        v6 = np.array([0.5,-1.,0.5])
        
        c = (v1+v2+v3+v4+v5+v6)/6.0  # calculo el centre per treure'l i centrar la figura
        v1-=c
        v2-=c
        v3-=c
        v4-=c
        v5-=c
        v6-=c
        
        color = ((1,0,0), (1,1,0), (0,1,1), (0,1,0), (0,0,1), 
            (1,0,1), (0.5, 0.5, 0.5), (1,0.5,0.3))

        color = (self.color1, self.color1, self.color1, self.color1,
            self.color2, self.color2, self.color2, self.color2)

        # Part superior
        data.append((color[0], glm.normalize(v1), glm.normalize(v1))) # primer triangle (cara) : color, normal, position
        data.append((color[0], glm.normalize(v5), glm.normalize(v5))) # primer triangle (cara)
        data.append((color[0], glm.normalize(v2), glm.normalize(v2))) # primer triangle (cara)

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

        data = self.tessel(data, self.depth)

        return np.array(data, dtype='f4')

    def tessel(self, data, depth):

        if depth == 0:
            return data

        else:
            depth -= 1
            new_data = []

            for i in range(0, len(data), 3):
                
                v12 = glm.normalize((data[i][1] + data[i+1][1]) / 2 )
                v13 = glm.normalize((data[i][1] + data[i+2][1]) / 2 )
                v23 = glm.normalize((data[i+1][1] + data[i+2][1]) / 2)

                new_data.append((data[i][0], v12, v12))
                new_data.append((data[i][0], v13, v13))
                new_data.append((data[i][0], data[i][1], data[i][2]))

                new_data.append((data[i+2][0], v23, v23))
                new_data.append((data[i+2][0], data[i+2][1], data[i+2][2]))
                new_data.append((data[i+2][0], v13, v13))

                new_data.append((data[i+1][0], data[i+1][1], data[i+1][2]))
                new_data.append((data[i+1][0], v23, v23))
                new_data.append((data[i+1][0], v12, v12))

                new_data.append((data[i][0], v12, v12))
                new_data.append((data[i+2][0], v23, v23))
                new_data.append((data[i+1][0], v13, v13))


            new_data = self.tessel(new_data, depth)

            return new_data
    
    @staticmethod
    def get_data(vertices, indices, colour): 
        #data = [vertices[ind] for triangle in indices for ind in triangle]
        data = [(colour[i],vertices[ind]) for i,triangle in enumerate(indices) for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    
    def get_shader_program(self):
        program = self.ctx.program(    
            vertex_shader='''
                #version 330 core
                layout (location = 0) in vec3 in_color;
                layout (location = 1) in vec3 in_normal;
                layout (location = 2) in vec3 in_position;
                out vec3 color;
                
                struct Light {
                    vec3 position;
                    vec3 Ia;
                    vec3 Id;
                    vec3 Is;
                };
                
                uniform Light light;
                uniform mat4 m_proj;
                uniform mat4 m_view;
                uniform mat4 m_model;
                uniform vec3 camPos;
                
                void main() {
                    vec3 normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
                    vec3 ambient = light.Ia;
                    vec3 lightDir = normalize(light.position-in_position);
                    vec3 diffuse = light.Id * max(0,dot(lightDir,normalize(normal)));
                    
                    //Specular light
                    vec3 viewDir = normalize(camPos-in_position);
                    vec3 reflectDir = reflect(-lightDir, normalize(normal));
                    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
                    vec3 specular = spec * light.Is;

                    //color = ambient + in_color * diffuse;
                    color = in_color * (ambient + diffuse + specular);
                    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330
                layout (location = 0) out vec4 fragColor;
                in vec3 color;
                void main() { 
                    fragColor = vec4(color,1.0);
                }
            ''',
        )
        return program