import glm
import pygame as pg

class Camera:
    def __init__(self, app, position=(0,0,4), yaw=-90, pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0]/app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0,1,0)
        self.right = glm.vec3(1,0,0)
        self.forward = glm.vec3(0,0,-1)
        self.yaw = yaw
        self.pitch = pitch

        self.FOV = 50
        self.near = 0.1
        self.far = 500
        self.speed = 0.05
        self.sensivity = 0.15

        self.bird_camera = True
        
        # view_matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()
        
    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * self.sensivity
        self.pitch -= rel_y * self.sensivity
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def set_bird_camera(self):
        #self.m_view = glm.lookAt(glm.vec3(0,50,0), glm.vec3(0), glm.vec3(-1,0,0))

        pos = glm.vec3(      23.0077,      54.1003,       42.303 )
        forw = glm.vec3(   -0.0174524,    -0.999848,  -8.7392e-17 )
        up = glm.vec3(    -0.999848,    0.0174524, -5.00668e-15 )
        self.m_view = glm.lookAt(pos, pos+forw, up)
        

    def move(self):

        velocity = self.speed * self.app.delta_time
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_q]:
            self.position += self.up * velocity
        if keys[pg.K_e]:
            self.position -= self.up * velocity


    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)
    
    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.FOV), self.aspect_ratio, self.near, self.far)

    def update(self):
        if self.bird_camera:
            self.set_bird_camera()
        else:
            self.move()
            self.rotate()
            self.update_camera_vectors()
            self.m_view = self.get_view_matrix()
