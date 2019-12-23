from kivy3 import Vector3
from kivy3.core.geometry import Geometry
from kivy3.core.face3 import Face3

#TODO: Implement me. This is copied and pasted from BoxGeometry()
class CylinderGeometry(Geometry):

    _cylinder_vertices = [(-1, 1, -1), (1, 1, -1),
                      (1, -1, -1), (-1, -1, -1),
                      (-1, 1, 1), (1, 1, 1),
                      (1, -1, 1), (-1, -1, 1),
                      ]

    _cylinder_faces = [(0, 1, 2), (0, 2, 3), (3, 2, 6),
                   (3, 6, 7), (7, 6, 5), (7, 5, 4),
                   (4, 5, 1), (4, 1, 0), (4, 0, 3),
                   (7, 4, 3), (5, 1, 2), (6, 5, 2)
                   ]

    _cylinder_normals = [(0, 0, 1), (-1, 0, 0), (0, 0, -1),
                     (1, 0, 0), (0, 1, 0), (0, -1, 0)
                     ]

    def __init__(self, radius, height, segments=32, **kw):
        name = kw.pop('name', '')
        super(CylinderGeometry, self).__init__(name)
        self.width_segment = kw.pop('width_segment', 1)
        self.height_segment = kw.pop('height_segment', 1)
        self.depth_segment = kw.pop('depth_segment', 1)

        self.r = radius
        self.h = height
        self.segments = segments

        self._build_cylinder()

    def _build_cylinder(self):

        for i in range(self.segments):


        for v in self._cube_vertices:
            v = Vector3(0.5 * v[0] * self.w,
                        0.5 * v[1] * self.h,
                        0.5 * v[2] * self.d)
            self.vertices.append(v)

        n_idx = 0
        for f in self._cube_faces:
            face3 = Face3(*f)
            normal = self._cube_normals[int(n_idx / 2)]
            face3.vertex_normals = [normal, normal, normal]
            n_idx += 1
            self.faces.append(face3)

    def _build_circle(self, segments):
        """ """