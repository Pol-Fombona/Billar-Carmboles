import itertools
import glm
import numpy as np

friction = 0.99
edge_collision_loss = 0.99

def checkBallsCollisions(objects):
    #Si la suma dels dos radis es superior a la distancia entre les dues esferes (punt central), col·lisio

    for ball_1, ball_2 in itertools.combinations(objects, 2):

        # radi (els dos radis seràn iguals) (de moment es 1)
        radi = 1
        x1 = np.array(ball_1.pos)
        x2 = np.array(ball_2.pos)
        dist = np.linalg.norm(x1 -x2)
        
        if (dist * 0.95 <= (radi * 2)):
            ballCollision(ball_1, ball_2)




def ballCollision(ball_1, ball_2):
    # Temporal
    # Set inverted velocity for the one moving
    # Transfer velocity to the one stopped
    
    v1 = np.array((ball_1.velocityX, 0, ball_1.velocityZ))
    v2 = np.array((ball_2.velocityX, 0, ball_2.velocityZ))
    x1 = np.array(ball_1.pos)
    x2 = np.array(ball_2.pos)

    if np.sum(abs(v1)) == 0: v1 += 0.001
    elif np.sum(abs(v2)) == 0: v2 += 0.001

    # v1 inicial + v2 inicial = v1 final + v2 final
    if np.sum(abs(v1)) != 0 and np.sum(abs(v2)) != 0:
        v1f = getImpactVelocity(v1, v2, 1, 1, x1, x2)
        v2f = getImpactVelocity(v2,v1, 1, 1, x2,x1)

        ball_1.velocityX, ball_1.velocityZ = v1f[0], v1f[2]
        ball_2.velocityX, ball_2.velocityZ = v2f[0], v2f[2] 


def getImpactVelocity(v1, v2, m1, m2, x1, x2):
    # https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects

    v = v1 - (2 * m2 / (m1 + m2)) 
    v = v * np.dot(v1 - v2, x1 - x2) 
    v = v / (np.linalg.norm(x1 - x2) ** 2) 
    v = v * (x1 - x2)
    
    return v

def checkEdgeCollisions(objects):

    for ball in objects:

        # X-edges of table
        if (ball.pos[0] - 1) <= 0:
            ball.velocityX = abs(ball.velocityX) * edge_collision_loss

        elif (ball.pos[0] + 1 ) >= 41.64:
            ball.velocityX = -abs(ball.velocityX) * edge_collision_loss

        elif (ball.pos[2] - 1) <= 0:
            ball.velocityZ = abs(ball.velocityZ) * edge_collision_loss

        elif (ball.pos[2] + 1) >= 83.28:
            ball.velocityZ = -abs(ball.velocityZ) * edge_collision_loss
 

def movement(ball, m_model):

    if abs(ball.velocityX) < 0.001:
        ball.velocityX = 0

        if abs(ball.velocityZ) < 0.01:
            ball.velocityZ = 0


    elif abs(ball.velocityZ) < 0.001:
        ball.velocityZ = 0

        if abs(ball.velocityX) < 0.01:
            ball.velocityX = 0

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