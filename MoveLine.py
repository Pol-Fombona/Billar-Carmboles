import glm
import numpy as np
import math
import copy
from positions import *
from sympy import symbols, solve

def rotate_line(line):
    line.m_model = glm.scale(line.m_model, (1/line.perc,1,1))
    #line.m_model = glm.scale(line.m_model, (0.95,1,1))
    #line.m_model = glm.scale(line.m_model, (1*1/0.95,1,1))
    line.m_model = glm.rotate(line.m_model,glm.radians(line.app.scene.cue.rotate_direction),glm.vec3(0,1,0))
    line.angle-=line.app.scene.cue.rotate_direction
    line.angle = line.angle%360
    line.pos = Ry(glm.radians(line.angle))*line.pos_orig+line.axis 

    scale_line(line)
    line.m_model = glm.scale(line.m_model, (line.perc,1,1))

def Ry(theta):
  return glm.mat3([[ np.cos(theta), 0, np.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-np.sin(theta), 0, np.cos(theta)]])

def change_objective(line,ball):
    # translate (origen)
    line.m_model = glm.scale(line.m_model, (1/line.perc,1,1))
    #line.perc = 1
    line.m_model = glm.rotate(line.m_model,-glm.radians(-line.angle),glm.vec3(0,1,0))
    line.m_model = glm.translate(line.m_model, -line.axis)
    line.m_model = glm.translate(line.m_model, ball.pos)
    line.angle=0
    line.axis = glm.vec3(ball.pos)
    line.pos = copy.deepcopy(line.axis)
    line.pos[0] += line.dist_ball
    line.pos_orig = glm.vec3(line.dist_ball,0,0)
    scale_line(line)
    print("pos: ",line.pos)
    line.m_model = glm.scale(line.m_model,(line.perc,1,1))

def scale_line(line):
    point = glm.vec3(-30,0,0)
    point = glm.rotate(point,glm.radians(-line.angle),glm.vec3(0,1,0))
    point += line.axis
    vd = (point[0]-line.axis[0],0,point[2]-line.axis[2])

    w = TABLE_WIDTH
    h = TABLE_LENGTH 
    angle = 360-line.angle
    try:
        if angle == 360 or angle == 0:
            line.perc = float(np.roots([vd[0],line.axis[0]])[0])    
        elif 0 <= angle <= 90:
            sol1 = np.roots([vd[0],line.axis[0]])
            sol2 = np.roots([vd[2],line.axis[2]-h])
            a = float(sol1)*glm.vec3(vd)+line.axis
            if a[2]<=h:
                line.perc = float(sol1[0])
            else:
                line.perc = float(sol2[0])

        elif 90 < angle <= 180:
            sol1 = np.roots([vd[2],line.axis[2]-h])
            sol2 = np.roots([vd[0],line.axis[0]-w])
            a = float(sol1)*glm.vec3(vd)+line.axis
            if a[0]<=w:
                line.perc = float(sol1[0])
            else:
                line.perc = float(sol2[0])
        elif 180 < angle <= 270:
            sol1 = np.roots([vd[0],line.axis[0]-w])
            sol2 = np.roots([vd[2],line.axis[2]])
            a = float(sol1)*glm.vec3(vd)+line.axis
            if a[2]>=0:
                line.perc = float(sol1[0])
            else:
                line.perc = float(sol2[0])
        elif 270 < angle < 360:
            sol1 = np.roots([vd[2],line.axis[2]])
            sol2 = np.roots([vd[0],line.axis[0]])
            a = float(sol1)*glm.vec3(vd)+line.axis
            if a[0]>=0:
                line.perc = float(sol1[0])
            else:
                line.perc = float(sol2[0])
    except:
        line.perc+=0.001

def manage_move(line):
    if (
            line.app.game.getTurnStatus() == "initial"
        ):    
            if line.moving:
                change_objective(line, line.app.game.current_player.ball)  
                line.moving = False  
            if line.app.scene.cue.rotate_flag:
                rotate_line(line)

                