from turtle import pos
import glm
import numpy as np
import math
import copy

def rotate_cue(cue):
    cue.m_model = glm.rotate(cue.m_model,glm.radians(cue.rotate_direction),glm.vec3(0,1,0))
    cue.angle-=cue.rotate_direction
    cue.pos = Ry(glm.radians(cue.angle))*cue.pos_orig+cue.axis 

def Ry(theta):
  return glm.mat3([[ np.cos(theta), 0, np.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-np.sin(theta), 0, np.cos(theta)]])
    
def displace_cue(cue,mode):
    if mode == "b":
        displace = glm.vec3(1,0,0)*0.25
    elif mode == "f":
        displace = -glm.vec3(1,0,0)*0.25
    cue.pos_orig +=displace
    cue.pos = Ry(glm.radians(cue.angle))*cue.pos_orig+cue.axis
    cue.m_model =  glm.translate(cue.m_model,displace)
   
def points_distance(point1,point2):
        return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2+(point1[2]-point2[2])**2)


def reset_displace_cue(cue):
    cue.m_model =  glm.translate(cue.m_model,-cue.pos_orig+glm.vec3(cue.dist_ball,0,0))

def cue_hit_ball(cue,ball):
    vel = cue.axis - cue.pos
    #ball.velocity[0] = vel[0]*ball.radi*0.15
    #ball.velocity[2] = vel[2]*ball.radi*0.15
    ball.update_velocity_values(vel*ball.radi*0.15)
    #ball.velocityX = vel[0]*ball.radi*0.15
    #ball.velocityZ = vel[2]*ball.radi*0.15

def change_objective(cue,ball):
    # translate (origen)
    cue.m_model = glm.rotate(cue.m_model,-glm.radians(-cue.angle),glm.vec3(0,1,0))
    cue.m_model = glm.translate(cue.m_model, -cue.axis)
    cue.m_model = glm.translate(cue.m_model, ball.pos)
    cue.angle=0
    cue.axis = glm.vec3(ball.pos)
    cue.pos = copy.deepcopy(cue.axis)
    cue.pos[0] += cue.dist_ball
    cue.pos_orig = glm.vec3(cue.dist_ball,0,0)

def manage_move(cue):
    if (
            cue.app.game.getTurnStatus() == "initial"
        ):    
            if cue.moving:
                change_objective(cue, cue.app.game.current_player.ball)    
                cue.moving = False
                cue.app.scene.line.moving = True
            if cue.rotate_flag:
                rotate_cue(cue)
            if (
                cue.state == "backward"
                #and points_distance(cue.axis, cue.pos) <= cue.max_distance
            ):
                displace_cue(cue,"b")
                if points_distance(cue.axis, cue.pos) >= cue.max_distance:
                    cue.state = "forward"
            elif (
                cue.state == "forward"
            ):
                displace_cue(cue,"f")
                if points_distance(cue.axis, cue.pos) <= cue.dist_ball+0.5:
                    cue.state = "backward"
            elif cue.state == "reset":
                reset_displace_cue(cue)
                cue.state = "stop"
                cue_hit_ball(cue, cue.app.game.current_player.ball)
                cue.moving = True
                cue.app.sound.playSound([cue.app.game.current_player.ball,cue.axis],3)