
import glm

from positions import LIGHT_POSITION

class Light():

    def __init__(self, position=LIGHT_POSITION, position2=(0, 5, 0), color=(1,1,1)):
        self.position = glm.vec3(position)
        # self.position2 = glm.vec3(position2)
        self.color = glm.vec3(color)
        # intensities
        self.Ia = 0.1 * self.color # ambient
        self.Id = 0.8 * self.color # diffuse
        self.Is = 1.0 * self.color # specular
    
