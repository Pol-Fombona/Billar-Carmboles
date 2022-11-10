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


def checkCollisions(objects, sound):
    # Checks collisions between spheres and between spheres and table
    
    # Between spheres
    checkBallsCollisions(objects)

    # Between table and sphere
    checkEdgeCollisions(objects)

    return


def checkBallsCollisions(objects):
    # If the distance between the spheres is less than the sum of radius
    # there is a collision
    
    collision = False
    lvel = []

    for ball_1, ball_2 in itertools.combinations(objects, 2):
        # Iterates over every pair of spheres

        v1 = ball_1.velocity 
        v2 = ball_2.velocity
        
        if np.sum(abs(v1)) != 0 or np.sum(abs(v2)) != 0:
            # If atleast one of the two spheres in the pair is moving

            x1 = np.array(ball_1.pos)
            x2 = np.array(ball_2.pos)
            dist = np.linalg.norm(x1 - x2)

            if (dist <= (radius * 2)):

                ballCollision(ball_1, ball_2, v1, v2, x1, x2)
                correctOverlap(ball_1, ball_2, dist, x1, x2)
                
                collision = True 
                lvel = [v1,v2]

    return collision,lvel


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


def ballCollision(ball_1, ball_2, v1, v2, x1, x2):
    # Returns velocity after colision

    if np.sum(abs(v1)) != 0 and np.sum(abs(v2)) != 0:
        # If the two spheres are moving
        v1f = getImpactVelocityTwoMovingObjects(v1, v2, 1, 1, x1, x2)
        v2f = getImpactVelocityTwoMovingObjects(v2, v1, 1, 1, x2, x1)

    else:
        # If one sphere is resting
        v1f, v2f = getImpactVelocityOneMovingObject(x1, x2, v1, v2)

    if (PECR == True):
       v1f, v2f = addPECR(v1, v1f, v2, v2f)

    ball_1.velocity = v1f * ball_collision_loss
    ball_2.velocity = v2f * ball_collision_loss  

    return 


def addPECR(v1, v1f, v2, v2f):
    # Add residual velocity if perfect colision happens
    # to the sphere moving initially

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

    return v1f, v2f


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
    # Checks collisions between the edges of the table
    # and a sphere

    collision = False
    lvel = [0,0,0]
    
    for sphere in objects:

        if sum(abs(sphere.velocity)) > 0:
            overlap_x, overlap_z = 0, 0

            # X-edges of table
            if (sphere.pos[0] - 1) <= 0:
                lvel[0] = sphere.velocity[0]
                sphere.velocity[0] *=  -edge_collision_loss
                overlap_x = sphere.pos[0] - 1
                collision = True

            elif (sphere.pos[0] + 1 ) >= width_table:
                lvel[0] = sphere.velocity[0]
                sphere.velocity[0] *= -edge_collision_loss
                overlap_x = (sphere.pos[0] + 1) - width_table
                collision = True

            # Z-edges of table
            elif (sphere.pos[2] - 1) <= 0:
                lvel[2] = sphere.velocity[2]
                sphere.velocity[2] *= -edge_collision_loss
                overlap_z = sphere.pos[2] - 1
                collision = True

            elif (sphere.pos[2] + 1) >= lenght_table:
                lvel[2] = sphere.velocity[2]
                sphere.velocity[2] *= -edge_collision_loss
                overlap_z = (sphere.pos[2] + 1) - lenght_table
                collision = True

            # Corrects overlap with table edge
            sphere.pos = (sphere.pos[0] - overlap_x, sphere.pos[1], sphere.pos[2] - overlap_z)        
    
    return collision, lvel


def movement(ball):
    # Controls the movement of the balls adding friction and rotation

    if abs(ball.velocity[0]) < 0.001:
        ball.velocity[0] = 0

        if abs(ball.velocity[2]) < 0.01:
            ball.velocity[2] = 0


    elif abs(ball.velocity[2]) < 0.001:
        ball.velocity[2] = 0

        if abs(ball.velocity[0]) < 0.01:
            ball.velocity[0] = 0

    ball.velocity *= 1 - friction
    ball.pos = tuple(ball.pos + ball.velocity)

    translation = glm.translate(glm.mat4(), ball.pos)

    ### Ball Rotation
    rotation = ballRotation(ball)

    return translation, rotation


def ballRotation(ball):
    # Returns rotation matrix

    radi = 1
    perimeter = 2*np.pi*radi
    vX, vZ = ball.velocity[0], ball.velocity[2]
    velocity = np.sqrt(vX**2 + vZ**2)

    if velocity != 0:

        angle_to_rotate = 360 * (velocity / perimeter)
        coords = np.cross(np.array((vX, 0, vZ)), np.array((0,1,0)))
        rotation = glm.rotate(glm.mat4(), glm.radians(-angle_to_rotate), (coords[0], coords[1], coords[2]))

    else:
        rotation = None

    return rotation
