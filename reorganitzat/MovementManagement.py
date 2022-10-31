import itertools
import glm
import numpy as np

friction = 0.01
edge_collision_loss = 0.99
ball_collision_loss = 0.9
radius = 1
width_table = 41.64 # X-edge
lenght_table = 83.28 # Z-edge

# Perfect Elastic Colision Residual
# If True, add a residual force when a perfect colision happens
# to make the colision look more "natural"
PECR = True


def checkBallsCollisions(objects):
    #Si la suma dels dos radis es superior a la distancia entre les dues esferes (punt central), col·lisio

    for ball_1, ball_2 in itertools.combinations(objects, 2):

        v1 = np.array((ball_1.velocityX, 0, ball_1.velocityZ))
        v2 = np.array((ball_2.velocityX, 0, ball_2.velocityZ))
        
        if np.sum(abs(v1)) != 0 or np.sum(abs(v2)) != 0:
            

            x1 = np.array(ball_1.pos)
            x2 = np.array(ball_2.pos)
            dist = np.linalg.norm(x1 - x2)

            if (dist <= (radius * 2)):

                ballCollision(ball_1, ball_2, v1, v2)
                correctOverlap(ball_1, ball_2, dist, x1, x2)


def correctOverlap(ball_1, ball_2, dist, x1, x2):
    # Correct ball position if there is overlap from the frame movement

    overlap = (dist - radius - radius) / -2
    distance = x1 - x2
    distX, distZ = distance[0], distance[2]

    b1X = ball_1.pos[0] + (overlap * distX) / dist
    b1Z = ball_1.pos[2] + (overlap * distZ) / dist

    b2X = ball_2.pos[0] - (overlap * distX) / dist
    b2Z = ball_2.pos[2] - (overlap * distZ) / dist
 
    ball_1.pos = (b1X, ball_1.pos[1], b1Z)
    ball_2.pos = (b2X, ball_2.pos[1], b2Z)

    return

def ballCollision(ball_1, ball_2, v1, v2):
    
    x1 = np.array(ball_1.pos)
    x2 = np.array(ball_2.pos)

    temp = np.sum(abs(v1)+abs(v2))
    if np.sum(abs(v1)) != 0 and np.sum(abs(v2)) != 0:
        v1f = getImpactVelocityTwoMovingObjects(v1, v2, 1, 1, x1, x2)
        v2f = getImpactVelocityTwoMovingObjects(v2, v1, 1, 1, x2, x1)

    else:
        #  Quan una bola està en repós
        ####  
        v1f, v2f = getImpactVelocityOneMovingObject(x1, x2, v1, v2)


    if (PECR == True):
        if np.sum(abs(v1f)) == 0:
            if np.sum(abs(v1)) * 0.1 < 0.01:
                v1f = v1 * 0.2
            else:
                v1f = v1 * 0.1
        elif np.sum(abs(v2f)) == 0:
            
            if np.sum(abs(v2)) * 0.1 < 0.01:
                v2f = v2 * 0.2
            else:
                v2f = v2 * 0.1


    v1f *= ball_collision_loss
    v2f *= ball_collision_loss

    ball_1.velocityX, ball_1.velocityZ = v1f[0], v1f[2]
    ball_2.velocityX, ball_2.velocityZ = v2f[0], v2f[2]


def getImpactVelocityTwoMovingObjects(v1, v2, m1, m2, x1, x2):
    # https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects

    v = v1 - (2 * m2 / (m1 + m2)) * np.dot(v1 - v2, x1 - x2) / (np.linalg.norm(x1 - x2) ** 2) * (x1 - x2)
    
    return v

def getImpactVelocityOneMovingObject(x1, x2, v1, v2):
    # https://github.com/OneLoneCoder/Javidx9/blob/master/ConsoleGameEngine/BiggerProjects/Balls/OneLoneCoder_Balls1.cpp

    distance =  np.linalg.norm(x1 - x2)
    nx = (x2[0]-x1[0])/distance
    ny = (x2[2]-x1[2])/distance

    kx = v1[0] - v2[0]
    ky = v1[2] - v2[2]

    p = 2.0 * (nx * kx + ny * ky) / 2

    v1f = np.array((v1[0] - p * 1 * nx, 0, v1[2] - p * 1 * ny))
    v2f = np.array((v2[0] + p * 1 * nx, 0, v2[2] + p * 1 * ny))

    return v1f, v2f


def checkEdgeCollisions(objects):

    for ball in objects:

        # X-edges of table
        if (ball.pos[0] - 1) <= 0:
            ball.velocityX = abs(ball.velocityX) * edge_collision_loss

        elif (ball.pos[0] + 1 ) >= width_table:
            ball.velocityX = -abs(ball.velocityX) * edge_collision_loss

        # Z-edges of table
        elif (ball.pos[2] - 1) <= 0:
            ball.velocityZ = abs(ball.velocityZ) * edge_collision_loss

        elif (ball.pos[2] + 1) >= lenght_table:
            ball.velocityZ = -abs(ball.velocityZ) * edge_collision_loss
 

def movement(ball):
    # Controls the movement of the balls adding friction and rotation

    if abs(ball.velocityX) < 0.001:
        ball.velocityX = 0

        if abs(ball.velocityZ) < 0.01:
            ball.velocityZ = 0


    elif abs(ball.velocityZ) < 0.001:
        ball.velocityZ = 0

        if abs(ball.velocityX) < 0.01:
            ball.velocityX = 0

    ball.velocityX = ball.velocityX * (1 - friction)
    ball.velocityZ = ball.velocityZ * (1 - friction)
    ball.pos = (ball.pos[0]+ball.velocityX, ball.pos[1], ball.pos[2] + ball.velocityZ)

    translation = glm.mat4()   
    translation = glm.translate(translation, ball.pos)

    ### Ball Rotation
    rotation = ballRotation(ball)

    return translation, rotation


def ballRotation(ball):

    radi = 1
    perimeter = 2*np.pi*radi
    vX, vZ = ball.velocityX, ball.velocityZ
    velocity = np.sqrt(vX**2 + vZ**2)

    if velocity != 0:

        angle_to_rotate = 360 * (velocity / perimeter)
        coords = np.cross(np.array((vX, 0, vZ)), np.array((0,1,0)))
        rotation = glm.mat4()
        return glm.rotate(rotation, glm.radians(-angle_to_rotate), (coords[0], coords[1], coords[2]))

    else:
        return None
