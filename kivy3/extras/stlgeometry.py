from kivy3 import Vector3
from kivy3.core.geometry import Geometry
from kivy3.core.face3 import Face3


class STLGeometry(Geometry):

    def __init__(self, stl_mesh, **kw):
        name = kw.pop('name', '')
        super(STLGeometry, self).__init__(name)

        self._build_mesh(stl_mesh)

    def _build_mesh(self, stl_mesh):

        # min(..., 65534//3) is a hack to keep large meshes from crashing
        # OpenGL restricts number of vertices <= 65535
        for i in range(min(stl_mesh.attr.size, 65534//3)):
            for j in range(3):
                v = Vector3(stl_mesh.vectors[i][j][0],
                            stl_mesh.vectors[i][j][1],
                            stl_mesh.vectors[i][j][2])
                self.vertices.append(v)

            f_index = i * 3
            face3 = Face3(f_index, f_index + 1, f_index + 2)
            face3.normal = Vector3(stl_mesh.normals[i][0],
                                   stl_mesh.normals[i][1],
                                   stl_mesh.normals[i][2])
            face3.vertex_normals = [face3.normal, face3.normal, face3.normal]
            self.faces.append(face3)
