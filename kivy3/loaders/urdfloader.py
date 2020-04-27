from .loader import BaseLoader
from kivy3 import Object3D, Mesh, Material, Vector3
from urdf_parser_py.urdf import URDF
from kivy3.extras.geometries import BoxGeometry, CylinderGeometry, SphereGeometry
from kivy3.loaders import STLLoader
import math
import numpy as np
from scipy.spatial.transform import Rotation as R


class LinkError(Exception):
    pass


class Link(Object3D):
    pass


class Joint():
    def __init__(self, joint, child, parent, mode="Normal"):
        self.joint = joint
        self.child = child
        self.mode = mode
        self.parent = parent
        if joint.axis is not None:
            self.axis = Vector3(*joint.axis)
            self.axis.normalize()
        pass
        self.mimic_joints = []
        self.current_value = 0.
        self.global_position = (0, 0, 0)

    def set_position(self, value):
        if self.joint.joint_type == "revolute":
            angle = min([self.joint.limit.upper, value])
            angle = max([self.joint.limit.lower, angle])
            self.current_value = angle
            rot_origin = self.joint.origin.rotation

            new_rot = [rot_origin[0] + angle * self.axis[0],
                       rot_origin[1] + angle * self.axis[1],
                       rot_origin[2] + angle * self.axis[2]]
            r = R.from_euler('xyz', new_rot)
            a = r.as_euler('zyx')

            self.child.rot.x = math.degrees(a[2])
            self.child.rot.y = math.degrees(a[1])
            self.child.rot.z = math.degrees(a[0])
        elif self.joint.joint_type == "prismatic":
            value = min([self.joint.limit.upper, value])
            value = max([self.joint.limit.lower, value])
            self.current_value = value
            pos_origin = self.joint.origin.position
            new_pos = [float(self.axis[0]) * value + pos_origin[0],
                       float(self.axis[1]) * value + pos_origin[1],
                       float(self.axis[2]) * value + pos_origin[2]]
            self.child.pos.x = new_pos[0]
            self.child.pos.y = new_pos[1]
            self.child.pos.z = new_pos[2]
        elif self.joint.joint_type == "continious":
            # TODO
            pass
        else:
            # print("No position possible to set")
            return

        for m_joint in self.mimic_joints:
            m_joint[0].set_position(m_joint[1] * self.current_value + m_joint[2])

        if self.mode == "joint_color":
            color_g = self.current_value/self.joint.limit.upper
            color_r = 1. - color_g
            color = (color_r, color_g, 0)
            mat = Material(color=color, diffuse=color, specular=(0.3, 0.3, 0.3))
            self.child.children[0].set_material(mat)
            # self.child.children[0].children[1].set_material(mat)
            # self.parent.set_material(mat)

    def connect_mimic(self, mimic_joint, a, b):
        self.mimic_joints.append([mimic_joint, a, b])

    def get_rotation_matrix(self, angle):
        u_x = self.axis.x
        u_y = self.axis.y
        u_z = self.axis.z
        a = angle
        # Rotation matrix from :
        # https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
        matrix = np.array[[math.cos(a) + u_x**2*(1-math.cos(a)),
                           u_x * u_y * (1-math.cos(a)) - u_z * math.sin(a),
                           u_x * u_z * (1-math.cos(a)) + u_y * math.sin(a)],
                           \
                          [u_y * u_x * (1-math.cos(a)) + u_z * math.sin(a),
                           math.cos(a) + u_y**2*(1-math.cos(a)),
                           u_y * u_z * (1-math.cos(a)) - u_x * math.sin(a)]
                           \
                          [u_z * u_x * (1-math.cos(a)) - u_y * math.sin(a),
                           u_z * u_y * (1-math.cos(a)) + u_x * math.sin(a),
                           math.cos(a) + u_z**2*(1-math.cos(a))]]
        return matrix

    def get_global_coordinate(self, offset=[0,0,0]):
        # joint_offset = [self.joint.origin.position[0],
        #           self.joint.origin.position[1],
        #           self.joint.origin.position[2]]
        return self.child.get_global_coordinate(offset=offset)
        pass


class URDFObject(Object3D):
    """ This is a 3d Object to hold information about a urdf """
    def __init__(self, urdf, package_path, base_link="base_link", **kw):
        super(URDFObject, self).__init__(**kw)
        self.urdf = urdf
        self.package_path = package_path
        self.stlloader = STLLoader()

        self.default_material = \
            Material(color=(0.1, 0.1, 0.1), diffuse=(0.1, 0.1, 0.1),
                     specular=(0.1, 0.1, 0.1))

        # Create material dictionary
        self.materials = {}
        for material in urdf.materials:
            color = material.color.rgba
            self.materials[material.name] = Material(color=color[0:3],
                                                     diffuse=color[0:3],
                                                     specular=(0.1, 0.1, 0.1))
        self.link_dict = {}
        self.joint_dict = {}

        # Creates Objects for all links in the urdfs
        self.create_link_objects()

        # Attaches objects to each parent/child via joints for each link.
        self.link_joints()

        self.add(self.link_dict[base_link])
        #This ofset changes z up to the opengl y up.
        # self.link_dict[base_link].rot.x = -90

    def create_link_objects(self):
        for link in self.urdf.links:
            if link.name in self.link_dict:
                raise LinkError("Found duplicate link")
            kw = dict(name=link.name)
            self.link_dict[link.name] = Link(**kw)
            # Add visuals to the list
            for visual in link.visuals:
                # Add visual to the object
                if hasattr(visual, "material"):
                    if visual.material is None:
                        material = self.default_material
                    elif visual.material.color is None:
                        if visual.material.name in self.materials:
                            material = self.materials[visual.material.name]
                        else:
                            material = self.default_material
                    else:
                        color = visual.material.color.rgba
                        material = Material(color=color[0:3],
                                            diffuse=color[0:3],
                                            specular=(0.1, 0.1, 0.1))
                else:
                    material = self.default_material

                if visual.geometry.XML_REFL.tag == "mesh":
                    filename = \
                        visual.geometry.filename.replace('package:/',
                                                         self.package_path)

                    mesh = self.stlloader.load(filename, material)

                elif visual.geometry.XML_REFL.tag == "cylinder":
                    geometry = CylinderGeometry(visual.geometry.radius,
                                                visual.geometry.length)
                    mesh = Mesh(geometry, material, swap_xz=False)
                elif visual.geometry.XML_REFL.tag == "box":
                    geometry = BoxGeometry(*visual.geometry.size)
                    mesh = Mesh(geometry, material, swap_xz=False)
                elif visual.geometry.XML_REFL.tag == "sphere":
                    geometry = SphereGeometry(radius=visual.geometry.radius)
                    mesh = Mesh(geometry, material, swap_xz=False)

                # Adjust origin of geometry
                if visual.origin is not None:
                    mesh.pos.x = visual.origin.position[0]
                    mesh.pos.y = visual.origin.position[1]
                    mesh.pos.z = visual.origin.position[2]
                    r = R.from_euler('xyz', visual.origin.rotation)
                    a = r.as_euler('zyx')
                    mesh.rot.x = math.degrees(a[2])
                    mesh.rot.y = math.degrees(a[1])
                    mesh.rot.z = math.degrees(a[0])
                self.link_dict[link.name].add(mesh)

    def link_joints(self):
        # Go through the joints and connect them as objects and their children
        for joint in self.urdf.joints:
            parent_link = self.link_dict[joint.parent]
            child_link = self.link_dict[joint.child]
            child_link.pos.x = joint.origin.position[0]
            child_link.pos.y = joint.origin.position[1]
            child_link.pos.z = joint.origin.position[2]

            r = R.from_euler('xyz', joint.origin.rotation)
            a = r.as_euler('zyx')

            child_link.rot.x = math.degrees(a[2])
            child_link.rot.y = math.degrees(a[1])
            child_link.rot.z = math.degrees(a[0])

            parent_link.add(child_link)

            if joint.name in self.joint_dict:
                raise LinkError("Found duplicate joint")
            self.joint_dict[joint.name] = Joint(joint, child_link, parent_link)

        # After all the joints, link the mimics to a joint.
        for joint in self.urdf.joints:
            if joint.mimic is not None:
                self.joint_dict[joint.mimic.joint].\
                    connect_mimic(self.joint_dict[joint.name],
                                  joint.mimic.multiplier,
                                  joint.mimic.offset)


class URDFLoader(BaseLoader):
    def __init__(self, package_path=".", **kw):
        super(URDFLoader, self).__init__(**kw)
        self.package_path = package_path

    def load(self, source):
        robot = URDF.from_xml_file(source)
        urdf = URDFObject(robot, self.package_path)
        return urdf
