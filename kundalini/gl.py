import math
from numpy import matrix
from pygame.surface import Surface
from OpenGL.GL import *
from OpenGL.GLU import *
from .vector import Vector

__all__ = ['init', 'resize', 'Matrix']


#-----------------------------------------------------------------------
def init() -> None:
    glEnable(GL_DEPTH_TEST)
    glClearColor(1., 1., 1., 0.)
    glShadeModel(GL_FLAT)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLight(GL_LIGHT0, GL_POSTION, (0, 1, 1, 0))


#-----------------------------------------------------------------------
def resize(screen:Surface, perspective:float=60.) -> None:
    width, height = screen.get_size()
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(perspective, float(width) / height, 1., 10000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


#-----------------------------------------------------------------------
class Matrix(matrix):

    def __new__(cls, data:(list, str)=None, dtype:type=None, copy:bool=True):
        if not data:
            # Default: identity
            data = [
                [1., 0., 0., 0.],
                [0., 1., 0., 0.],
                [0., 0., 1., 0.],
                [0., 0., 0., 1.],
            ]
        return super(Matrix, cls).__new__(cls, data, dtype, copy)


    def transform(self, vector:Vector) -> Vector:
        if len(vector) < 4:
            w = 1
        else:
            w = vector.w
        return Vector([
            vector.x * self[0, 0] + vector.y * self[0, 1] + vector.z * self[0, 2] + w * self[0, 3],
            vector.x * self[1, 0] + vector.y * self[1, 1] + vector.z * self[1, 2] + w * self[1, 3],
            vector.x * self[2, 0] + vector.y * self[2, 1] + vector.z * self[2, 2] + w * self[2, 3],
        ])


    @classmethod
    def make_translation(cls, vector:Vector) -> matrix:
        return cls([
            [1., 0., 0., 0.],
            [0., 1., 0., 0.],
            [0., 0., 1., 0.],
            [vector.x, vector.y, vector.z, 1.],
        ])


    @classmethod
    def make_xyz_rotate(cls, angle_x:float=0., angle_y:float=0., angle_z:float=0.) -> matrix:
        cx = cos(math.radians(angle_x))
        sx = sin(math.radians(angle_x))
        cy = cos(math.radians(angle_y))
        sy = sin(math.radians(angle_y))
        cz = cos(math.radians(angle_z))
        sz = sin(math.radians(angle_z))

        sxsy = sx * sy
        cxcy = cx * cy

        return cls([
            [cy * cz,  sxsy * cz + cx * sz,  -cxsy * cz + sx * sz, 0.],
            [-cy * sz, -sxsy * sz + cx * cz, cxsy * sz + sx * cz, 0.],
            [sy, -sx * cy, cx*cy, 0.],
            [0., 0., 0., 1.],
        ])
