"""
The MIT License (MIT)

Copyright (c) 2013 Niko Skrypnik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from kivy3 import Vector3

"""
Geometry class
=============

"""


class Geometry(object):

    def __init__(self, name=''):
        self.name = name
        self.faces = []
        self.vertices = []
        self.face_vertex_uvs = [[]]
        self.lines = []

    def compute_vertex_normal(self):
        pass

    def calculate_normal(self, face):
        """
        Calculate and return the normal to the plane on a given face.
        Normal points in direction according right-hand rule.
        :param face:
        :return:
        """
        vec_a = self.vertices[face.a]
        vec_b = self.vertices[face.b]
        vec_c = self.vertices[face.c]
        b_minus_a = Vector3((vec_b[0]-vec_a[0],vec_b[1]-vec_a[1], vec_b[2]-vec_a[2]))
        # b_minus_a = Vector3.sub_vectors(vec_b, vec_a)
        c_minus_a = Vector3((vec_c[0] - vec_a[0], vec_c[1] - vec_a[1], vec_c[2] - vec_a[2]))
        # c_minus_a = Vector3.sub_vectors(vec_c, vec_a)
        b_minus_a.cross(c_minus_a)
        normal = b_minus_a
        return normal


    def rotate_geometry(self, axis):
        for v in self.vertices:
            x = v[0]
            y = v[1]
            z = v[2]
            if axis == 'x':
                v[1] = z
                v[2] = -y
            elif axis == '-x':
                v[1] = -z
                v[2] = y
            elif axis == 'y':
                v[2] = x
                v[0] = -z
            elif axis == '-y':
                v[2] = -x
                v[0] = z
            elif axis == 'z':
                v[0] = y
                v[1] = -x
            elif axis == '-z':
                v[0] = -y
                v[1] = x

    def translate_geometry(self, x, y, z):
        for v in self.vertices:
            v[0] += x
            v[1] += y
            v[2] += z
