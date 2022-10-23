import itertools
import glm
import numpy as np

friction = 0.99
edge_collision_loss = 0.99
radius = 1

def checkBallsCollisions(objects):
    #Si la suma dels dos radis es superior a la distancia entre les dues esferes (punt central), col·lisio

    for ball_1, ball_2 in itertools.combinations(objects, 2):

        # radi (els dos radis seràn iguals) (de moment es 1)
        radi = 1
        x1 = np.array(ball_1.pos)
        x2 = np.array(ball_2.pos)
        dist = np.linalg.norm(x1 - x2)
        
        if (dist <= (radi * 2)):

            # overlap
            correctOverlap(ball_1, ball_2, dist, x1, x2)
            ballCollision(ball_1, ball_2)


def correctOverlap(ball_1, ball_2, dist, x1, x2):
    # Correct ball pos if there is overlap from the movement
    
    overlap = (dist - radius - radius) / -2

    distance = x1 - x2
    distX, distZ = distance[0], distance[1]

    b1X = ball_1.pos[0] + (overlap * distX) / dist
    b1Z = ball_1.pos[2] + (overlap * distZ) / dist

    b2X = ball_2.pos[0] - (overlap * distX) / dist
    b2Z = ball_2.pos[2] - (overlap * distZ) / dist

    ball_1.pos = (b1X, ball_1.pos[1], b1Z)
    ball_2.pos = (b2X, ball_2.pos[1], b2Z)

    return

def ballCollision(ball_1, ball_2):
    
    v1 = np.array((ball_1.velocityX, 0, ball_1.velocityZ))
    v2 = np.array((ball_2.velocityX, 0, ball_2.velocityZ))
    x1 = np.array(ball_1.pos)
    x2 = np.array(ball_2.pos)

    temp = np.sum(abs(v1)+abs(v2))
    if np.sum(abs(v1)) != 0 and np.sum(abs(v2)) != 0:
        v1f = getImpactVelocity(v1, v2, 1, 1, x1, x2)
        v2f = getImpactVelocity(v2, v1, 1, 1, x2, x1)

        ball_1.velocityX, ball_1.velocityZ = v1f[0], v1f[2]
        ball_2.velocityX, ball_2.velocityZ = v2f[0], v2f[2]

    else:
        #  Quan una bola està en repós
        #### https://github.com/OneLoneCoder/Javidx9/blob/master/ConsoleGameEngine/BiggerProjects/Balls/OneLoneCoder_Balls1.cpp 
        distance =  np.linalg.norm(x1 - x2)
        nx = (x2[0]-x1[0])/distance
        ny = (x2[2]-x1[2])/distance

        kx = ball_1.velocityX - ball_2.velocityX
        ky = ball_1.velocityZ - ball_2.velocityZ

        p = 2.0 * (nx * kx + ny * ky) / 2

        ball_1.velocityX = ball_1.velocityX - p * 1 * nx
        ball_1.velocityZ = ball_1.velocityZ - p * 1 * ny

        ball_2.velocityX = ball_2.velocityX + p * 1 * nx
        ball_2.velocityZ = ball_2.velocityZ + p * 1 * ny

    ball_1.velocityX *= 0.9
    ball_1.velocityZ *= 0.9

    ball_2.velocityX *= 0.9
    ball_2.velocityZ *= 0.9


    ## No important, només per mirar l'elasticitat 
    v1f = np.array((ball_1.velocityX, 0, ball_1.velocityZ))
    v2f = np.array((ball_2.velocityX, 0, ball_2.velocityZ))
    temp2 = np.sum(abs(v1f)+abs(v2f))

    if (temp < temp2):
        print("bola1", v1, "final", v1f)
        print("bola2", v2, "final", v2f)
        print("v1",temp, "v2", temp2)
        #exit()


def getImpactVelocity(v1, v2, m1, m2, x1, x2):
    # https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects

    v = v1 - (2 * m2 / (m1 + m2)) * np.dot(v1 - v2, x1 - x2) / (np.linalg.norm(x1 - x2) ** 2) * (x1 - x2)
    
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