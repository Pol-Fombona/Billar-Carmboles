from turtle import pos
import glm
import numpy as np

friction = 0.99

def checkBallsCollisions(objects):
    #Si la suma dels dos radis es superior a la distancia entre les dues esferes (punt central), col·lisio
    
    ball_1 = objects[0]
    ball_2 = objects[1]

    # Distancies
    dist_X = (ball_1.pos[0] - ball_2.pos[0])**2
    dist_Z = (ball_1.pos[2] - ball_2.pos[2])**2

    dist = (dist_X + dist_Z) ** (1/2)

    # radi (els dos radis seràn iguals) (de moment es 1)
    radi = 1

    if (dist <= (radi * 2)):
        ballCollision(ball_1, ball_2)




def ballCollision(ball_1, ball_2):
    # Temporal
    # Set inverted velocity for the one moving
    # Transfer velocity to the one stopped
    velocity_loss = 0.6

    ball_2.velocityX, ball_2.velocityZ = ball_1.velocityX * velocity_loss, ball_1.velocityZ * velocity_loss

    ball_1.velocityX *= -velocity_loss
    ball_1.velocityZ *= -velocity_loss

def checkEdgeCollisions(objects):

    for ball in objects:

        # X-edges of table
        if (((ball.pos[0] - 1) <= 0 or (ball.pos[0] + 1) >= 41.64) and not ball.collisions["vX"]):
        
            ball.velocityX *= -1
            ball.collisions["vX"] = True
            

        # Z-edges of table
        elif (((ball.pos[2] - 1) <= 0 or (ball.pos[2] + 1) >= 83.28) and not ball.collisions["vX"]):
            
            ball.velocityZ *= -1
            ball.collisions["vZ"] = True

        else:
            ball.collisions["vX"], ball.collisions["vZ"] = False, False



def movement(ball, m_model):

    if abs(ball.velocityX) < 0.001:
        ball.velocityX = 0

        ### No se si funciona, es per evitar que quan s'acaba la velocitat
        ### d'un eix, no vagi en linia recta a l'altre
        if abs(ball.velocityZ) < 0.01:
            ball.velocityZ = 0


    elif abs(ball.velocityZ) < 0.001:
        ball.velocityZ = 0

        ### No se si funciona, es per evitar que quan s'acaba la velocitat
        ### d'un eix, no vagi en linia recta a l'altre
        if abs(ball.velocityX) < 0.01:
            ball.velocityX = 0

    #if ball.velocityX != 0 or ball.velocityZ != 0:

    ball.velocityX = ball.velocityX * friction
    ball.velocityZ = ball.velocityZ * friction
    ball.pos = (ball.pos[0]+ball.velocityX, ball.pos[1], ball.pos[2] + ball.velocityZ)

    m_model = glm.mat4()
    m_model = glm.translate(m_model, ball.pos)

    ### Ball Rotation
    m_model = ballRotation(ball, m_model)

    return m_model


def ballRotation(ball, m_model):

    # TODO: Quan col·lisiona amb la taula no fa el canvi de rotació suaument

    radi = 1
    perimeter = 2*np.pi*radi
    last_rotation = ball.last_rotation
    vX, vZ = ball.velocityX, ball.velocityZ
    velocity = np.sqrt(vX**2 + vZ**2)

    if velocity != 0:
        angle_to_rotate = 360 * (velocity / perimeter)

        if (last_rotation[1] * vX) >= 0 and (last_rotation[2] * vZ) >= 0:
            angle_to_rotate += ball.last_rotation[0]

        else:
            angle_to_rotate = ball.last_rotation[0] - angle_to_rotate
            
        m_model = glm.rotate(m_model, glm.radians(angle_to_rotate), (vZ, 0, -vX))
        ball.last_rotation = (angle_to_rotate%360, vX, vZ)

    else:
        m_model = glm.rotate(m_model, glm.radians(ball.last_rotation[0]), (ball.last_rotation[2], 0, -ball.last_rotation[1]))
    
    return m_model