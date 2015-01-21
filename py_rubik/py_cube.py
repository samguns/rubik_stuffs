# -*- coding: utf-8 -*-

__author__ = 'Gang.Wang'

import pygame
import pygame.gfxdraw
import numpy as np

class cube_polygon(object):
    def __init__(self, xy, color):
        self.xy = np.asarray(xy)
        self.zorder = 0
        self.color = color

    def set_xy(self, xy):
        self.xy = np.asarray(xy)

    def get_xy(self):
        return self.xy

    def set_zorder(self, zorder):
        self.zorder = zorder

    def get_zorder(self):
        return self.zorder

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

class Quaternion:
    """Quaternion Rotation:

    Class to aid in representing 3D rotations via quaternions.
    """
    @classmethod
    def from_v_theta(cls, v, theta):
        """
        Construct quaternions from unit vectors v and rotation angles theta

        Parameters
        ----------
        v : array_like
            array of vectors, last dimension 3. Vectors will be normalized.
        theta : array_like
            array of rotation angles in radians, shape = v.shape[:-1].

        Returns
        -------
        q : quaternion object
            quaternion representing the rotations
        """
        theta = np.asarray(theta)
        v = np.asarray(v)
        s = np.sin(0.5 * theta)
        c = np.cos(0.5 * theta)

        v = v * s / np.sqrt(np.sum(v * v, -1))
        x_shape = v.shape[:-1] + (4,)

        x = np.ones(x_shape).reshape(-1, 4)
        x[:, 0] = c.ravel()
        x[:, 1:] = v.reshape(-1, 3)
        x = x.reshape(x_shape)

        return cls(x)

    def __init__(self, x):
        self.x = np.asarray(x, dtype=float)

    def __repr__(self):
        return "Quaternion:\n" + self.x.__repr__()

    def __mul__(self, other):
        # multiplication of two quaternions.
        # we don't implement multiplication by a scalar
        sxr = self.x.reshape(self.x.shape[:-1] + (4, 1))
        oxr = other.x.reshape(other.x.shape[:-1] + (1, 4))

        prod = sxr * oxr
        return_shape = prod.shape[:-1]
        prod = prod.reshape((-1, 4, 4)).transpose((1, 2, 0))

        ret = np.array([(prod[0, 0] - prod[1, 1]
                         - prod[2, 2] - prod[3, 3]),
                        (prod[0, 1] + prod[1, 0]
                         + prod[2, 3] - prod[3, 2]),
                        (prod[0, 2] - prod[1, 3]
                         + prod[2, 0] + prod[3, 1]),
                        (prod[0, 3] + prod[1, 2]
                         - prod[2, 1] + prod[3, 0])],
                       dtype=np.float,
                       order='F').T
        return self.__class__(ret.reshape(return_shape))

    def as_v_theta(self):
        """Return the v, theta equivalent of the (normalized) quaternion"""
        x = self.x.reshape((-1, 4)).T

        # compute theta
        norm = np.sqrt((x ** 2).sum(0))
        theta = 2 * np.arccos(x[0] / norm)

        # compute the unit vector
        v = np.array(x[1:], order='F', copy=True)
        v /= np.sqrt(np.sum(v ** 2, 0))

        # reshape the results
        v = v.T.reshape(self.x.shape[:-1] + (3,))
        theta = theta.reshape(self.x.shape[:-1])

        return v, theta

    def as_rotation_matrix(self):
        """Return the rotation matrix of the (normalized) quaternion"""
        v, theta = self.as_v_theta()

        shape = theta.shape
        theta = theta.reshape(-1)
        v = v.reshape(-1, 3).T
        c = np.cos(theta)
        s = np.sin(theta)

        mat = np.array([[v[0] * v[0] * (1. - c) + c,
                         v[0] * v[1] * (1. - c) - v[2] * s,
                         v[0] * v[2] * (1. - c) + v[1] * s],
                        [v[1] * v[0] * (1. - c) + v[2] * s,
                         v[1] * v[1] * (1. - c) + c,
                         v[1] * v[2] * (1. - c) - v[0] * s],
                        [v[2] * v[0] * (1. - c) - v[1] * s,
                         v[2] * v[1] * (1. - c) + v[0] * s,
                         v[2] * v[2] * (1. - c) + c]],
                       order='F')
        return mat.T.reshape(shape + (3, 3))

White = pygame.Color(255, 255, 255, 220)
Blue = pygame.Color(0, 0, 143, 220)
Orange = pygame.Color(255, 111, 0, 220)
Yellow = pygame.Color(255, 207, 0, 220)
Green = pygame.Color(0, 159, 15, 220)
Red = pygame.Color(207, 0, 0, 220)

class Cube():
    face = np.array([[1, 1], [1, -1], [-1, -1], [-1, 1], [1, 1]])
    faces = np.array([np.hstack([face[:, :i],
                                 np.ones((5, 1)),
                                 face[:, i:]]) for i in range(3)] +
                     [np.hstack([face[:, :i],
                                 -np.ones((5, 1)),
                                 face[:, i:]]) for i in range(3)])
    stickercolors = [White, Blue, Orange, Yellow, Green, Red]

    def __init__(self, surface):
        self.start_rot = Quaternion.from_v_theta((1, -1, 0), -np.pi / 6)
        self.current_rot = self.start_rot

        self.start_zloc = 10.
        self.current_zloc = 10.

        # Define movement for up/down arrows or up/down mouse movement
        self._ax_UD = (1, 0, 0)
        self._step_UD = 0.01

        # Define movement for left/right arrows or left/right mouse movement
        self._ax_LR = (0, -1, 0)
        self._step_LR = 0.01

        # Internal variables.  These store states and data
        self._active = False
        self._xy = None
        self._cubes = None
        self._surface = surface

        self.draw()

    @staticmethod
    def project_points(pts, rot, zloc):
        """Project points to 2D given a rotation and a view

        pts is an ndarray, last dimension 3
        rot is a Quaternion object, containing a single quaternion
        zloc is a distance along the z-axis from which the cube is being viewed
        """
        R = rot.as_rotation_matrix()
        Rpts = np.dot(pts, R.T)

        xdir = np.array([1., 0, 0])
        ydir = np.array([0, 1., 0])
        zdir = np.array([0, 0, 1.])

        view = zloc * zdir
        v2 = zloc ** 2

        result = []
        for p in Rpts.reshape((-1, 3)):
            dpoint = p - view
            dproj = 0.5 * dpoint * v2 / np.dot(dpoint, -1. * view)
            result += [np.array([np.dot(xdir, dproj),
                                 np.dot(ydir, dproj),
                                 np.dot(zdir, dpoint / np.sqrt(v2))])]
        return np.asarray(result).reshape(pts.shape)

    def draw(self, rot=None, zloc=None):
        if rot is None:
            rot = self.current_rot
        if zloc is None:
            zloc = self.current_zloc

        self.current_rot = rot
        self.current_zloc = zloc

        if self._cubes is None:
            self._cubes = [cube_polygon(self.faces[i, :, :2],
                                        self.stickercolors[i]) for i in range(6)]

        faces = self.project_points(self.faces, rot, zloc)
        zorder = np.argsort(np.argsort(faces[:, :4, 2].sum(1)))

        self._surface.fill((128, 128, 128))

        [self._cubes[i].set_xy(faces[i, :, :2]) for i in range(6)]
        [self._cubes[i].set_zorder(10 * zorder[i]) for i in range(6)]

        zindex = {}
        for i in range(6):
            zindex[zorder[i]] = self._cubes[i]

        for i in range(6):
            point_list = zindex[i].get_xy().tolist()
            polygon_list = []
            for j in range(len(point_list)):
                px = point_list[j][0]
                py = point_list[j][1]
                fact_x, fact_y = self.axes_to_position(px, py)
                polygon_list.append((fact_x, fact_y))

            pygame.gfxdraw.filled_polygon(self._surface, polygon_list, zindex[i].get_color())
            #pygame.draw.polygon(self._surface, zindex[i].get_color(), polygon_list)
            pygame.draw.aalines(surface, (50, 50, 50), False, polygon_list, 100)

        '''
        for i in range(6):
            print "zorder ", i, " ", repr(zorder[i])

            point_list = self._cubes[zorder[i]].get_xy().tolist()
            #print point_list, len(point_list)
            polygon_list = []
            for j in range(len(point_list)):
                px = point_list[j][0]
                py = point_list[j][1]
                fact_x, fact_y = self.axes_to_position(px, py)
                polygon_list.append((fact_x, fact_y))

            #pygame.draw.lines(surface, (50, 50, 50, 100), False, polygon_list, 5)
            #pygame.draw.aalines(surface, (50, 50, 50), False, polygon_list, 30)
            #pygame.draw.polygon(self._surface, self._cubes[zorder[i]].get_color(), polygon_list)
            pygame.gfxdraw.filled_polygon(self._surface, polygon_list, self._cubes[zorder[i]].get_color())
            pygame.draw.aalines(surface, (50, 50, 50), False, polygon_list, 50)
            #pygame.draw.lines(surface, (50, 50, 50, 200), False, polygon_list, 3)

        print "####\n"
        '''

    def rotate_left(self):
        self.current_rot = (self.current_rot
                            * Quaternion.from_v_theta(self._ax_LR,
                                                      -self._step_LR))
        self.draw()

    def rotate_right(self):
        self.current_rot = (self.current_rot
                            * Quaternion.from_v_theta(self._ax_LR,
                                                      self._step_LR))
        self.draw()

    def axes_to_position(self, x, y):
        pos_x = 300 + (x * 300)
        pos_y = 300 - (y * 300)

        return pos_x, pos_y

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.SRCALPHA, 32)
    pygame.display.set_caption('My PyGame Cube demo')

    surface = pygame.Surface((600, 600)).convert_alpha()
    c = Cube(surface)
    clock = pygame.time.Clock()
    screen.fill((128, 128, 128))

    try:
        while (1):
            screen.fill((128, 128, 128), surface.get_rect(center=(400, 300)))
            clock.tick(60)
            c.rotate_left()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise KeyboardInterrupt

                if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_SPACE:
                    c.rotate_left()

                if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_LEFT:
                    c.rotate_left()

                if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_RIGHT:
                    c.rotate_right()

            screen.blit(surface, surface.get_rect(center=(400, 300)))
            pygame.display.flip()

    except KeyboardInterrupt:
        pass