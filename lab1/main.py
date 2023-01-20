import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
from curve import P
import math
import numpy as np

# controlPoints = (
#     (0,0,0),
#     (0, 10, 5),
#     (10, 10, 10),
#     (10, 0, 15),
#     (0, 0, 20),
#     (0, 10, 25),
#     (10, 10, 30),
#     (10, 0, 35),
#     (0, 0, 40),
#     (0, 10, 45),
#     (10, 10, 50),
#     (10, 0, 55))

f = open("controlPoints.txt", "r")

controlPoints = [[float(j) for j in i.split(" ")] for i in f.read().splitlines()]


# scene = pywavefront.Wavefront('objects/tetrahedron.obj', collect_faces=True)
scene = pywavefront.Wavefront('objects/kocka.obj', collect_faces=True)

orientationPoint = scene.vertices[0]


centroid    = [0 for i in range(3)]

scale    = 3
for vertex in scene.vertices:
    centroid = [centroid[i] + vertex[i]*scale for i in range(3)]

centroid = [centroid[i]/(len(scene.vertices)) for i in range(3)]
# print(centroid)
default_orientation = [-centroid[i] + orientationPoint[i] for i in range(3)]




def OrientationVector(default_vector, goal_vector):
    s = np.array(default_vector)
    e = np.array(goal_vector)
    phi = math.degrees(math.acos(np.dot(s,e)/(np.linalg.norm(s)*np.linalg.norm(e))))
    return [phi, (s[1]*e[2]-e[1]*s[2]), -(s[0]*e[2]-e[0]*s[2]), (s[0]*e[1]-s[1]*e[0])]


def Tangent(point, tangent):
    scale_tangent=0.3
    point_end = [point[i]+scale_tangent*tangent[i] for i in range(3)]
    glColor3f(0, 1, 1)
    glBegin(GL_LINES)
    glVertex3fv(point)
    glVertex3fv(point_end)
    glEnd()


def Curve():

    pi = P(controlPoints)

    glPointSize(2)
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_STRIP)
    for j in range(1, len(controlPoints)-2):
        for point in pi(j):
            glVertex3fv(point)
    glEnd()

    # glPointSize(2)
    # glColor3f(0, 1, 1)
    # glBegin(GL_POINTS)
    # glVertex3fv([0, 0, 0])
    # glEnd()
    # glFlush()
    # glColor3f(0, 1, 1)
    # glBegin(GL_LINES)
    # glVertex3fv([0, 0, 0])
    # glVertex3fv([5, 0, 0])
    # glEnd()

def Model(translate, rotate):


    glPushMatrix()

    glTranslatef(*translate)
    glRotatef(*rotate)
    glRotatef(*OrientationVector(default_orientation, [1,0,0]))
    glTranslatef(*[-centroid[i] for i in range(3)])

    glColor3f(1, 1, 1)
    for mesh in scene.mesh_list:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex in face:
                glVertex3f(*[scene.vertices[vertex][i]*scale for i in range(3)])
        glEnd()
    # glPointSize(2)
    glColor3f(1, 0, 0)
    for mesh in scene.mesh_list:
        glBegin(GL_LINE_STRIP)
        for face in mesh.faces:
            for vertex in face:
                glVertex3f(*[scene.vertices[vertex][i]*scale for i in range(3)])
        glEnd()

    glPopMatrix()


def main():
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (display[0] / display[1]), 1, 500.0)
        glTranslatef(-5, 5, -75)
        glRotatef (20, 1, 0, 0)
        # x = 20
        # y = 20
        # z = 60
        # glOrtho(-x, x, -y, y, -z, z)

        pi = P(controlPoints)
        i = 0
        j = 0
        t_num = 30
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            if i%t_num == 0:
                j+=1
                if j%(len(controlPoints)-2)==0:
                    j = 1
                pj = pi(j, t_num)
                pj_tan = pi.tangent(j, t_num)

            k = i%t_num

            translate = [(pj[k][p]) for p in range(3)]
            rotate = OrientationVector([1,0,0], pj_tan[k])
            Curve()
            Model(translate, rotate)
            Tangent(pj[k],pj_tan[k])


            pygame.display.flip()
            pygame.time.wait(20)

            i +=1

main()