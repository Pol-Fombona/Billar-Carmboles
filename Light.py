
import glm

from positions import LIGHT_POSITION

class Light():

    def __init__(self, position=LIGHT_POSITION, color=(1,1,1)):
        self.position = glm.vec3(position)
        # self.position2 = glm.vec3(position2)
        self.color = glm.vec3(color)
        self.direction = glm.vec3(0, 0, 0)
        # intensities
        self.Ia = 0.1 * self.color # ambient
        self.Id = 0.8 * self.color # diffuse
        self.Is = 1.0 * self.color # specular
        #view matrix
        self.m_view_light = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.direction, glm.vec3(0, 1, 0))
    
