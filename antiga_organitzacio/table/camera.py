import glm
import pygame as pg

SPEED = 0.01
SENSITIVITY = 0.05


class Camera:
    def __init__(
        self,
        app,
        position=(0, 0, 4),
        yaw=-90,
        pitch=0,
        table_information=((0, 0, 0), 0, 0, 0),
    ):
        self.app = app
        self.table_information = table_information
        self.aspec_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.first_position = position
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, 0)
        self.yaw = yaw
        self.pitch = pitch
        self.pinfo = "Camera: Free"
        self.camera_type = "Free"
        # view_matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()

    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = min(90, max(-90, self.pitch))

    def update_camera_vector(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def get_view_matrix(self):
        if self.camera_type == "Blocked":
            return glm.lookAt(self.position, (0, 0, 0), self.up)
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(45), self.aspec_ratio, 0.1, 100)

    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vector()
        self.changeCamera()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
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

    def setCamera(self, pos, up=(0, 1, 0)):
        self.position = pos
        self.up = up

    def changeCamera(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_b]:
            self.pinfo = "Camera: Blocked"
            if self.camera_type == "Free":
                self.setCamera(self.first_position)
                self.camera_type = "Blocked"
            else:
                self.camera_type = "Free"
        if keys[pg.K_t]:
            self.pinfo = "Camera: Top"
            self.setCamera(
                (
                    self.table_information[0][0] + self.table_information[1] / 2,
                    self.table_information[0][1] + self.table_information[2] + 3,
                    self.table_information[0][2] + self.table_information[3] / 2,
                ),
                (1, 0, 0),
            )
        if keys[pg.K_m]:
            self.pinfo = "Camera: Right"
            self.setCamera((0, 0, 5))
        if keys[pg.K_v]:
            self.pinfo = "Camera: Prespective"
            self.setCamera((4, 3, 0))
