# -*- coding: utf-8 -*-

__author__ = 'Gang.Wang'

import numpy as np
import pygame
import pygame.gfxdraw
import time
import threading
from Queue import Queue
from threading import Thread

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
                       order='F').T
        return mat.reshape(shape + (3, 3))

    def rotate(self, points):
        M = self.as_rotation_matrix()
        return np.dot(points, M.T)


def project_points(points, q, view, vertical=[0, 1, 0]):
    """Project points using a quaternion q and a view v

    Parameters
    ----------
    points : array_like
        array of last-dimension 3
    q : Quaternion
        quaternion representation of the rotation
    view : array_like
        length-3 vector giving the point of view
    vertical : array_like
        direction of y-axis for view.  An error will be raised if it
        is parallel to the view.

    Returns
    -------
    proj: array_like
        array of projected points: same shape as points.
    """
    points = np.asarray(points)
    view = np.asarray(view)

    xdir = np.cross(vertical, view).astype(float)

    if np.all(xdir == 0):
        raise ValueError("vertical is parallel to v")

    xdir /= np.sqrt(np.dot(xdir, xdir))

    # get the unit vector corresponing to vertical
    ydir = np.cross(view, xdir)
    ydir /= np.sqrt(np.dot(ydir, ydir))

    # normalize the viewer location: this is the z-axis
    v2 = np.dot(view, view)
    zdir = view / np.sqrt(v2)

    # rotate the points
    R = q.as_rotation_matrix()
    Rpts = np.dot(points, R.T)

    # project the points onto the view
    dpoint = Rpts - view
    dpoint_view = np.dot(dpoint, view).reshape(dpoint.shape[:-1] + (1,))
    dproj = -dpoint * v2 / dpoint_view

    trans = range(1, dproj.ndim) + [0]
    return np.array([np.dot(dproj, xdir),
                     np.dot(dproj, ydir),
                     -np.dot(dpoint, zdir)]).transpose(trans)

Black = pygame.Color(0, 0, 0)
White = pygame.Color(255, 255, 255)
Blue = pygame.Color(0, 0, 143)
Orange = pygame.Color(255, 111, 0)
Yellow = pygame.Color(255, 207, 0)
Green = pygame.Color(0, 159, 15)
Red = pygame.Color(207, 0, 0)
Gray = pygame.Color(128, 128, 128)
No_Color = pygame.Color(255, 255, 255, 0)

class Cube:
    """Magic Cube Representation"""
    # define some attribues
    default_plastic_color = Black
    default_face_colors = [White, Yellow, Blue, Green,
                           Orange, Red, Gray, No_Color]

    base_face = np.array([[1, 1, 1],
                          [1, -1, 1],
                          [-1, -1, 1],
                          [-1, 1, 1],
                          [1, 1, 1]], dtype=float)
    stickerwidth = 0.9
    stickermargin = 0.5 * (1. - stickerwidth)
    stickerthickness = 0.001
    (d1, d2, d3) = (1 - stickermargin,
                    1 - 2 * stickermargin,
                    1 + stickerthickness)
    base_sticker = np.array([[d1, d2, d3], [d2, d1, d3],
                             [-d2, d1, d3], [-d1, d2, d3],
                             [-d1, -d2, d3], [-d2, -d1, d3],
                             [d2, -d1, d3], [d1, -d2, d3],
                             [d1, d2, d3]], dtype=float)

    base_face_centroid = np.array([[0, 0, 1]])
    base_sticker_centroid = np.array([[0, 0, 1 + stickerthickness]])

    # Define rotation angles and axes for the six sides of the cube
    x, y, z = np.eye(3)
    rots = [Quaternion.from_v_theta(x, theta)
            for theta in (np.pi / 2, -np.pi / 2)]
    rots += [Quaternion.from_v_theta(y, theta)
             for theta in (np.pi / 2, -np.pi / 2, np.pi, 2 * np.pi)]

    # define face movements
    facesdict = dict(F=z, B=-z,
                     R=x, L=-x,
                     U=y, D=-y)

    def __init__(self, N=3, plastic_color=None, face_colors=None):
        self.N = N
        if plastic_color is None:
            self.plastic_color = self.default_plastic_color
        else:
            self.plastic_color = plastic_color

        if face_colors is None:
            self.face_colors = self.default_face_colors
        else:
            self.face_colors = face_colors

        self._move_list = []
        self._initialize_arrays()

    def _initialize_arrays(self):
        # initialize centroids, faces, and stickers.  We start with a
        # base for each one, and then translate & rotate them into position.

        # Define N^2 translations for each face of the cube
        cubie_width = 2. / self.N
        translations = np.array([[[-1 + (i + 0.5) * cubie_width,
                                   -1 + (j + 0.5) * cubie_width, 0]]
                                 for i in range(self.N)
                                 for j in range(self.N)])

        # Create arrays for centroids, faces, stickers, and colors
        face_centroids = []
        faces = []
        sticker_centroids = []
        stickers = []
        colors = []

        factor = np.array([1. / self.N, 1. / self.N, 1])

        for i in range(6):
            M = self.rots[i].as_rotation_matrix()
            faces_t = np.dot(factor * self.base_face
                             + translations, M.T)
            stickers_t = np.dot(factor * self.base_sticker
                                + translations, M.T)
            face_centroids_t = np.dot(self.base_face_centroid
                                      + translations, M.T)
            sticker_centroids_t = np.dot(self.base_sticker_centroid
                                         + translations, M.T)
            colors_i = i + np.zeros(face_centroids_t.shape[0], dtype=int)

            # append face ID to the face centroids for lex-sorting
            face_centroids_t = np.hstack([face_centroids_t.reshape(-1, 3),
                                          colors_i[:, None]])
            sticker_centroids_t = sticker_centroids_t.reshape((-1, 3))

            faces.append(faces_t)
            face_centroids.append(face_centroids_t)
            stickers.append(stickers_t)
            sticker_centroids.append(sticker_centroids_t)
            colors.append(colors_i)

        self._face_centroids = np.vstack(face_centroids)
        self._faces = np.vstack(faces)
        self._sticker_centroids = np.vstack(sticker_centroids)
        self._stickers = np.vstack(stickers)
        self._colors = np.concatenate(colors)

        self._sort_faces()

    def _sort_faces(self):
        # use lexsort on the centroids to put faces in a standard order.
        ind = np.lexsort(self._face_centroids.T)
        self._face_centroids = self._face_centroids[ind]
        self._sticker_centroids = self._sticker_centroids[ind]
        self._stickers = self._stickers[ind]
        self._colors = self._colors[ind]
        self._faces = self._faces[ind]

    def rotate_face(self, f, n=1, layer=0):
        """Rotate Face"""
        if layer < 0 or layer >= self.N:
            raise ValueError('layer should be between 0 and N-1')

        try:
            f_last, n_last, layer_last = self._move_list[-1]
        except:
            f_last, n_last, layer_last = None, None, None

        if (f == f_last) and (layer == layer_last):
            ntot = (n_last + n) % 4
            if abs(ntot - 4) < abs(ntot):
                ntot = ntot - 4
            if np.allclose(ntot, 0):
                self._move_list = self._move_list[:-1]
            else:
                self._move_list[-1] = (f, ntot, layer)
        else:
            self._move_list.append((f, n, layer))

        v = self.facesdict[f]
        r = Quaternion.from_v_theta(v, n * np.pi / 2)
        M = r.as_rotation_matrix()

        proj = np.dot(self._face_centroids[:, :3], v)
        cubie_width = 2. / self.N
        flag = ((proj > 0.9 - (layer + 1) * cubie_width) &
                (proj < 1.1 - layer * cubie_width))

        for x in [self._stickers, self._sticker_centroids,
                  self._faces]:
            x[flag] = np.dot(x[flag], M.T)
        self._face_centroids[flag, :3] = np.dot(self._face_centroids[flag, :3],
                                                M.T)

class cube_polygon(object):
    def __init__(self, xy, color, zorder):
        self.xy = np.asarray(xy)
        self.zorder = zorder
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

class InteractiveCube:
    def __init__(self, surface, cube=None,
                 interactive=True,
                 view=(0, 0, 10)):
        if cube is None:
            self.cube = Cube(3)
        elif isinstance(cube, Cube):
            self.cube = cube
        else:
            self.cube = Cube(cube)

        self._view = view
        self._start_rot = Quaternion.from_v_theta((1, -1, 0),
                                                  -np.pi / 6)

        self._surface = surface
        self._start_xlim = 0
        self._start_ylim = 0

        # Define movement for up/down arrows or up/down mouse movement
        self._ax_UD = (1, 0, 0)
        self._step_UD = 0.01

        # Define movement for left/right arrows or left/right mouse movement
        self._ax_LR = (0, -1, 0)
        self._step_LR = 0.01

        self._ax_LR_alt = (0, 0, 1)

        # Internal state variable
        self._active = False  # true when mouse is over axes
        self._button1 = False  # true when button 1 is pressed
        self._button2 = False  # true when button 2 is pressed
        self._event_xy = None  # store xy position of mouse event
        self._shift = False  # shift key pressed
        self._digit_flags = np.zeros(10, dtype=bool)  # digits 0-9 pressed

        self._current_rot = self._start_rot  #current rotation state
        self._face_polys = None
        self._sticker_polys = None

        self._draw_cube()


    def _project(self, pts):
        return project_points(pts, self._current_rot, self._view, [0, 1, 0])

    def axes_to_position(self, x, y):
        pos_x = 300 + (x * 130)
        pos_y = 300 - (y * 130)

        return pos_x, pos_y

    def _draw_cube(self):
        stickers = self._project(self.cube._stickers)[:, :, :2]
        faces = self._project(self.cube._faces)[:, :, :2]
        face_centroids = self._project(self.cube._face_centroids[:, :3])
        sticker_centroids = self._project(self.cube._sticker_centroids[:, :3])

        plastic_color = self.cube.plastic_color
        colors = np.asarray(self.cube.face_colors)[self.cube._colors]
        face_zorders = -face_centroids[:, 2]
        sticker_zorders = -sticker_centroids[:, 2]

        self._surface.fill((128, 128, 128))

        if self._face_polys is None:
            self._face_polys = []
            self._sticker_polys = []

            for i in range(len(colors)):
                fp = cube_polygon(faces[i], plastic_color,
                                 face_zorders[i])
                sp = cube_polygon(stickers[i], colors[i],
                                 sticker_zorders[i])

                self._face_polys.append(fp)
                self._sticker_polys.append(sp)
        else:
            # subsequent call: update the polygon objects
            for i in range(len(colors)):
                self._face_polys[i].set_xy(faces[i])
                self._face_polys[i].set_zorder(face_zorders[i])
                self._face_polys[i].set_color(plastic_color)

                self._sticker_polys[i].set_xy(stickers[i])
                self._sticker_polys[i].set_zorder(sticker_zorders[i])
                self._sticker_polys[i].set_color(colors[i])

        plastic_zindex = {}
        sticker_zindex = {}
        for i in range(len(colors)):
            plastic_zindex.setdefault(face_zorders[i], []).append(self._face_polys[i])
            sticker_zindex.setdefault(sticker_zorders[i], []).append(self._sticker_polys[i])

        for plastic_zindex_key in plastic_zindex.keys():
            for plastic in plastic_zindex[plastic_zindex_key]:
                plastic_point_list = plastic.get_xy().tolist()
                plastic_polygon_list = []

                for j in range(len(plastic_point_list)):
                    px = plastic_point_list[j][0]
                    py = plastic_point_list[j][1]
                    fact_x, fact_y = self.axes_to_position(px, py)
                    plastic_polygon_list.append((fact_x, fact_y))

                #pygame.gfxdraw.filled_polygon(self._surface, plastic_polygon_list, plastic.get_color())
                pygame.draw.polygon(self._surface, plastic.get_color(), plastic_point_list, 10)
                #pygame.draw.aalines(surface, plastic.get_color(), True, plastic_polygon_list, 100)

        for sticker_zindex_key in sorted(sticker_zindex.keys()):
            for sticker in sticker_zindex[sticker_zindex_key]:
                sticker_point_list = sticker.get_xy().tolist()
                sticker_polygon_list = []

                for j in range(len(sticker_point_list)):
                    px = sticker_point_list[j][0]
                    py = sticker_point_list[j][1]
                    fact_x, fact_y = self.axes_to_position(px, py)
                    sticker_polygon_list.append((fact_x, fact_y))

                pygame.gfxdraw.filled_polygon(self._surface, sticker_polygon_list, sticker.get_color())

    def rotate(self, rot):
        self._current_rot = self._current_rot * rot

    def rotate_face(self, face, steps, turns=1, layer=0):
        if not np.allclose(turns, 0):
            #for i in range(steps):
            self.cube.rotate_face(face, turns * 1. / steps,
                                  layer=layer)
            self._draw_cube()

    def _reset_view(self, *args):
        #self.set_xlim(self._start_xlim)
        #self.set_ylim(self._start_ylim)
        self._current_rot = self._start_rot
        self._draw_cube()

    def _solve_cube(self, *args):
        move_list = self.cube._move_list[:]
        for (face, n, layer) in move_list[::-1]:
            self.rotate_face(face, -n, layer, steps=3)
        self.cube._move_list = []

    def _key_press(self, event):
        """Handler for key press events"""
        if event.key == 'shift':
            self._shift = True
        elif event.key.isdigit():
            self._digit_flags[int(event.key)] = 1
        elif event.key == 'right':
            if self._shift:
                ax_LR = self._ax_LR_alt
            else:
                ax_LR = self._ax_LR
            self.rotate(Quaternion.from_v_theta(ax_LR,
                                                5 * self._step_LR))
        elif event.key == 'left':
            if self._shift:
                ax_LR = self._ax_LR_alt
            else:
                ax_LR = self._ax_LR
            self.rotate(Quaternion.from_v_theta(ax_LR,
                                                -5 * self._step_LR))
        elif event.key == 'up':
            self.rotate(Quaternion.from_v_theta(self._ax_UD,
                                                5 * self._step_UD))
        elif event.key == 'down':
            self.rotate(Quaternion.from_v_theta(self._ax_UD,
                                                -5 * self._step_UD))
        elif event.key.upper() in 'LRUDBF':
            if self._shift:
                direction = -1
            else:
                direction = 1

            if np.any(self._digit_flags[:N]):
                for d in np.arange(N)[self._digit_flags[:N]]:
                    self.rotate_face(event.key.upper(), direction, layer=d)
            else:
                self.rotate_face(event.key.upper(), direction)

        self._draw_cube()

    def rotate_demo(self):
        rot1 = Quaternion.from_v_theta(self._ax_UD,
                                       self._step_UD * -0)
        rot2 = Quaternion.from_v_theta(self._ax_LR,
                                       self._step_LR * -0.3)
        self.rotate(rot1 * rot2)
        self._draw_cube()

PLAYERDEAD = pygame.USEREVENT+2
q = Queue()

def thread_main(stop_event):
    while not stop_event.is_set():
        print "thread_main"
        time.sleep(2)
        q.put(True)

if __name__ == '__main__':
    import sys
    try:
        N = int(sys.argv[1])
    except:
        N = 3

    t_stop = threading.Event()
    t = Thread(target=thread_main, args=(t_stop, ))
    t.daemon = True
    t.start()

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('My PyGame Cube demo')

    surface = pygame.Surface((600, 600)).convert_alpha()
    clock = pygame.time.Clock()
    screen.fill((128, 128, 128))

    ic = InteractiveCube(surface)

    running = True
    face_turning = False
    steps = 40
    counter = 0
    while running is True:
        screen.fill((128, 128, 128), surface.get_rect(center=(400, 300)))
        clock.tick(60)
        ic.rotate_demo()

        try:
            item = q.get(False)
            if item == True:
                face_turning = True
                q.task_done()
        except:
            pass

        if face_turning == True:
            ic.rotate_face('U', steps)
            counter += 1
            if counter == steps:
                counter = 0
                face_turning = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                t_stop.set()

            if face_turning == False:
                if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_u:
                    face_turning = True

            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_SPACE:
                ic._reset_view()

        screen.blit(surface, surface.get_rect(center=(400, 300)))
        pygame.display.flip()

    t.join()