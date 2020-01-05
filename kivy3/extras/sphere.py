"""
The MIT License (MIT)

Copyright (c) 2020 Shaun Barlow

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
import math

from kivy3 import Vector3
from kivy3.core.geometry import Geometry
from kivy3.core.face3 import Face3


class PrismGeometry(Geometry):

    def __init__(self, radius=1, height=1, segments=32, radius_top=None, **kw):
        """

        :param radius:
        :param height:
        :param segments:
        :param radius_top:
        :param kw:
        """
        name = kw.pop('name', '')
        super(PrismGeometry, self).__init__(name)

        self.r = radius
        self.h = height
        self.segments = segments
        if not radius_top:
            radius_top = radius

        self._build_polygon(radius, 0, segments, reverse_vertex_order=True)
        self._build_polygon(radius_top, height, segments)
        self._build_cylinder()

    def _build_cylinder(self):
        """
        Generate faces between top and bottom faces
        :return:
        """
        top_circle_vertex_start_index = len(self.vertices) // 2

        for i in range(top_circle_vertex_start_index):
            base_v0 = i
            base_v1 = i + 1
            top_v0 = i + top_circle_vertex_start_index
            top_v1 = top_v0 + 1
            if base_v1 == top_circle_vertex_start_index:
                base_v1 = 0
                top_v1 = top_circle_vertex_start_index

            # two points on first circle, one on second circle
            face = Face3(base_v0, base_v1, top_v0)
            normal = self.calculate_normal(face)
            face.vertex_normals = [normal, normal, normal]
            self.faces.append(face)

            # one point on first circle, two on second circle
            face = Face3(base_v1, top_v1, top_v0)
            normal = self.calculate_normal(face)
            face.vertex_normals = [normal, normal, normal]
            self.faces.append(face)

    def _build_polygon(self, radius, z, segments=32, reverse_vertex_order=False):
        """
        Generate a polygon given number of segments and radius
        
        :param radius:
        :param z:
        :param segments:
        :param reverse_vertex_order:
        :return:
        """
        vertex_start_index = len(self.vertices)

        for i in range(segments):
            angle = (math.pi / 2) + (i  / segments) * 2 * math.pi

            x = radius * math.cos(angle)
            y = radius * math.sin(angle)

            vertex = Vector3(x, y, z)
            self.vertices.append(vertex)

            if i >= 2:
                if reverse_vertex_order:
                    face = Face3(vertex_start_index + i,
                                 vertex_start_index + i-1,
                                 vertex_start_index)
                else:
                    face = Face3(vertex_start_index,
                                 vertex_start_index + i - 1,
                                 vertex_start_index + i)

                normal = self.calculate_normal(face)
                face.vertex_normals = [normal, normal, normal]
                self.faces.append(face)
