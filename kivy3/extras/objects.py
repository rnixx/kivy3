from kivy3.extras.geometries import ConeGeometry, CylinderGeometry
from kivy3 import Object3D, Mesh, Material

class ArrowObject(Object3D):
    def __init__(self, material,**kw):

        length = kw.pop('length', 1.)
        radius = kw.pop('radius', length/10.)
        cone_radius = kw.pop('cone_radius', radius*2.)
        cone_length = kw.pop('cone_length', radius*3.)
        cylinder_length = kw.pop('cylinder_length', length-(radius*3.))
        super(ArrowObject, self).__init__(**kw)
        cone = ConeGeometry(cone_radius, cone_length)
        cone_mesh = Mesh(cone, material)

        cylinder = CylinderGeometry(radius=radius, length=cylinder_length)
        cylinder_mesh = Mesh(cylinder, material)

        cone_mesh.position.x = cylinder_length
        cone_mesh.rot.y = 90.
        cylinder_mesh.position.x = cylinder_length/2.
        cylinder_mesh.rot.y = 90.
        self.add(cone_mesh)
        self.add(cylinder_mesh)
        pass

class AxisObject(Object3D):
    #Red is X, Green is Y Blue is Z
    def __init__(self, id_color_x = None, id_color_y = None, id_color_z = None, **kw):
        length=kw.pop('length', 0.1)
        radius=kw.pop('radius', length/14.)
        cone_radius = kw.pop('cone_radius', radius*2.)
        alpha=kw.pop('alpha', 1)
        super(AxisObject, self).__init__(**kw)
        red_mat = Material(color=(1,0,0), diffuse=(1,0,0), specular=(0.3,0.3,0.3), transparency=alpha, id_color=id_color_x)
        green_mat = Material(color=(0,1,0), diffuse=(0,1,0), specular=(0.3,0.3,0.3), transparency=alpha, id_color=id_color_y)
        blue_mat = Material(color=(0,0,1), diffuse=(0,0,1), specular=(0.3,0.3,0.3), transparency=alpha, id_color=id_color_z)
        x_axis = ArrowObject(red_mat, length=length, radius=radius, cone_radius=cone_radius, )
        y_axis = ArrowObject(green_mat, length=length, radius=radius, cone_radius=cone_radius)
        z_axis = ArrowObject(blue_mat, length=length, radius=radius, cone_radius=cone_radius)

        z_axis.rot.y = -90
        y_axis.rot.z = +90

        self.add(x_axis)
        self.add(y_axis)
        self.add(z_axis)
