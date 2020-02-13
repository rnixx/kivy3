from kivy3.extras.geometries import ConeGeometry, CylinderGeometry
from kivy3 import Object3D, Mesh, Material

class ArrowObject(Object3D):
    def __init__(self, material,**kw):

        length = kw.pop('length', 1.)
        radius = kw.pop('radius', length/10.)
        super(ArrowObject, self).__init__(**kw)
        cone = ConeGeometry(radius *2,length/5)
        cone_mesh = Mesh(cone, material)

        cylinder = CylinderGeometry(radius, 4.*length/5.)
        cylinder_mesh = Mesh(cylinder, material)

        cone_mesh.position.z = 4*length/5
        cylinder_mesh.position.z = 2.*length/5

        self.add(cone_mesh)
        self.add(cylinder_mesh)
        pass

class AxisObject(Object3D):
    #Red is X, Green is Y Blue is Z
    def __init__(self, **kw):
        length=kw.pop('length', 0.1)
        alpha=kw.pop('alpha', 1)
        super(AxisObject, self).__init__(**kw)
        red_mat = Material(color=(1,0,0), diffuse=(1,0,0), specular=(0.3,0.3,0.3), transparency=alpha)
        green_mat = Material(color=(0,1,0), diffuse=(0,1,0), specular=(0.3,0.3,0.3), transparency=alpha)
        blue_mat = Material(color=(0,0,1), diffuse=(0,0,1), specular=(0.3,0.3,0.3), transparency=alpha)
        x_axis = ArrowObject(red_mat, length=length)
        y_axis = ArrowObject(green_mat, length=length)
        z_axis = ArrowObject(blue_mat, length=length)

        x_axis.rot.y = 90
        y_axis.rot.x = -90

        self.add(x_axis)
        self.add(y_axis)
        self.add(z_axis)
