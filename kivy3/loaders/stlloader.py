from .loader import BaseLoader
from os.path import abspath, dirname, join, exists
from kivy.core.image import Image
from kivy.graphics import Mesh as KivyMesh
from kivy.logger import Logger
from kivy3 import Object3D, Mesh, Material, Vector2
from kivy3.core.geometry import Geometry
from kivy3.core.face3 import Face3
import numpy as np
from stl import mesh

DEFAULT_VERTEX_FORMAT = [
    (b'v_pos', 3, 'float'),
    (b'v_normal', 3, 'float'),
    (b'v_tc0', 2, 'float')
]
DEFAULT_MESH_MODE = 'triangles'


class STLMesh(Object3D):
    def __init__(self, v0, v1, v2, normals, material, **kw):
        super(STLMesh, self).__init__(**kw)
        self.vertex_format = kw.pop('vertex_format', DEFAULT_VERTEX_FORMAT)
        self.mesh_mode = kw.pop('mesh_mode', DEFAULT_MESH_MODE)
        self.material = material
        self.normals = normals
        indices = list(range(0, len(v0)*3))
        uvs = np.zeros((len(v0), 2)).astype(np.float32)
        vertices = list(np.block([v0.astype(np.float32),normals.astype(np.float32),uvs,v1.astype(np.float32),normals.astype(np.float32),uvs,v2.astype(np.float32),normals.astype(np.float32),uvs]).flatten())
        kw2=dict(vertices=vertices,
                indices=indices,
                fmt=self.vertex_format,
                mode=self.mesh_mode)

        # if self.material.map:
        #     kw2['texture'] = self.material.map
        self._mesh = KivyMesh(**kw2)

    def custom_instructions(self):
        yield self.material
        yield self._mesh

    def set_material(self, mat):
        idx = 0
        for instr in self._instructions.children:
            if instr.__class__.__name__ == "Material":
                self._instructions.children[idx] = mat
                return
            idx += 1

    def get_material(self):
        idx = 0
        for instr in self._instructions.children:
            if instr.__class__.__name__ == "Material":
                return self._instructions.children[idx]
            idx += 1


class STLObject(Object3D):
    def __init__(self, stl_mesh, material, **kw):
        super(STLObject, self).__init__(**kw)
        self.stl_mesh = stl_mesh
        self.material = material
        self.mtl = self.material  # shortcut for material property

        self.meshes = []

        self.create_mesh()

    def create_mesh(self):
        """ Create real mesh object from the geometry and material """
        max_faces = 65530//3
        #geometries = []
        start = 0

        while(True):
            _faces=[]
            _vertices = []
            if (len(self.stl_mesh.v0)-start) >= max_faces:
                length = max_faces

                mesh = STLMesh(self.stl_mesh.v0[start:start+length], self.stl_mesh.v1[start:start+length], self.stl_mesh.v2[start:start+length], self.stl_mesh.normals[start:start+length],
                self.material)
                self.add(mesh)
                start = start+length
                self.meshes.append(mesh)

            else:
                mesh = STLMesh(self.stl_mesh.v0[start:], self.stl_mesh.v1[start:], self.stl_mesh.v2[start:], self.stl_mesh.normals[start:],
                self.material)

                self.add(mesh)
                self.meshes.append(mesh)
                break

        return self

    # def custom_instructions(self):
        #yield self.material
        #yield self._mesh

    def set_material(self,mat):
        for stl_mesh in self.meshes:
            stl_mesh.set_material(mat)




class STLLoader(BaseLoader):
    def __init__(self, **kw):
        super(STLLoader, self).__init__(**kw)

    def load(self, source, material, **kw):
        self.material = material
        return super(STLLoader, self).load(source, **kw)


    def parse(self):

        stl = mesh.Mesh.from_file(self.source)



        stl_object = STLObject(stl,self.material)
        # stl_object.scale=[0.5,1,1]



        return stl_object
