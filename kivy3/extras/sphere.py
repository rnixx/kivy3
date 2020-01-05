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


class SphereGeometry(Geometry):

    def __init__(self, radius=1, sectors=36, stacks=18, **kw):
        """

        :param radius:
        :param height:
        :param segments:
        :param radius_top:
        :param kw:
        """
        name = kw.pop('name', '')
        super(SphereGeometry, self).__init__(name)

        self.build_sphere(radius, sectors, stacks)

    def build_sphere(self, radius, sectors, stacks):

        for i in range(stacks):
            stack_angle = math.pi * ((1 / 2) - (i / stacks))
            xy = radius * math.cos(stack_angle)
            z = radius * math.sin(stack_angle)

            # add(sectorCount + 1) vertices per stack
            # the first and last vertices have same position and normal, but different tex coords
            for j in range(sectors):
                sector_angle = j * 2 * math.pi / sectors

                # vertex position x y z
                x = xy * math.cos(sector_angle)
                y = xy * math.sin(sector_angle)
                vec = Vector3(x, y, z)
                self.vertices.append(vec)

                # normals
                # length_inv = 1 / radius
                # nx = x * length_inv
                # ny = y * length_inv
                # nz = z * length_inv
                # normal = Vector3(nx, ny, nz)
                # self.normals.append(normal)

                # tex coords (s, t) range between [0, 1]
                # TODO: https://www.songho.ca/opengl/gl_sphere.html

        for i in range(stacks):
            k_1 = i * (sectors)  # beginning of current stack
            k_2 = k_1 + sectors  # beginning of next stack

            for j in range(sectors):
                # faces
                #
                # if i = 0:
                #     face = Face3(0, k_2)
                #
                if i != 0:
                    face = Face3(k_1, k_2, k_1 + 1)
                    # normal = self.calculate_normal(face)
                    # face.vertex_normals = [normal, normal, normal]
                    self.faces.append(face)

                if i != (stacks - 1):
                    face = Face3(k_1 + 1, k_2, k_2 + 1)
                    # normal = self.calculate_normal(face)
                    # face.vertex_normals = [normal, normal, normal]
                    self.faces.append(face)

                k_1 += 1
                k_2 += 1

        for face in self.faces:
            if face.a > len(self.vertices) \
                    or face.b > len(self.vertices) \
                    or face.c > len(self.vertices):
                print(face)


    # def _build_cylinder(self):
    #     """
    #     Generate faces between top and bottom faces
    #     :return:
    #     """
    #     top_circle_vertex_start_index = len(self.vertices) // 2
    #
    #     for i in range(top_circle_vertex_start_index):
    #         base_v0 = i
    #         base_v1 = i + 1
    #         top_v0 = i + top_circle_vertex_start_index
    #         top_v1 = top_v0 + 1
    #         if base_v1 == top_circle_vertex_start_index:
    #             base_v1 = 0
    #             top_v1 = top_circle_vertex_start_index
    #
    #         # two points on first circle, one on second circle
    #         face = Face3(base_v0, base_v1, top_v0)
    #         normal = self.calculate_normal(face)
    #         face.vertex_normals = [normal, normal, normal]
    #         self.faces.append(face)
    #
    #         # one point on first circle, two on second circle
    #         face = Face3(base_v1, top_v1, top_v0)
    #         normal = self.calculate_normal(face)
    #         face.vertex_normals = [normal, normal, normal]
    #         self.faces.append(face)
    #
    # def _build_polygon(self, radius, z, segments=32, reverse_vertex_order=False):
    #     """
    #     Generate a polygon given number of segments and radius
    #
    #     :param radius:
    #     :param z:
    #     :param segments:
    #     :param reverse_vertex_order:
    #     :return:
    #     """
    #     vertex_start_index = len(self.vertices)
    #
    #     for i in range(segments):
    #         angle = (math.pi / 2) + (i  / segments) * 2 * math.pi
    #
    #         x = radius * math.cos(angle)
    #         y = radius * math.sin(angle)
    #
    #         vertex = Vector3(x, y, z)
    #         self.vertices.append(vertex)
    #
    #         if i >= 2:
    #             if reverse_vertex_order:
    #                 face = Face3(vertex_start_index + i,
    #                              vertex_start_index + i-1,
    #                              vertex_start_index)
    #             else:
    #                 face = Face3(vertex_start_index,
    #                              vertex_start_index + i - 1,
    #                              vertex_start_index + i)
    #
    #             normal = self.calculate_normal(face)
    #             face.vertex_normals = [normal, normal, normal]
    #             self.faces.append(face)
