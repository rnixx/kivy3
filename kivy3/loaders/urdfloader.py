from .loader import BaseLoader
from os.path import abspath, dirname, join, exists
from kivy.core.image import Image
from kivy.graphics import Mesh as KivyMesh
from kivy.logger import Logger
from kivy3 import Object3D, Mesh, Material, Vector2, Vector3
from kivy3.core.geometry import Geometry
from kivy3.core.face3 import Face3
from urdf_parser_py.urdf import URDF
from kivy3.extras.geometries import BoxGeometry, CylinderGeometry, SphereGeometry
from kivy3.loaders import OBJLoader, STLLoader
import math
import numpy as np


class LinkError(Exception):
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
            # rotation_matrix = self.get_rotation_matrix(value)
            # rotation_matrix.dot()
            angle = min([self.joint.limit.upper, value])
            angle = max([self.joint.limit.lower, angle])
            self.current_value= angle
            rot_origin = self.joint.origin.rotation
            new_rot = [rot_origin[0] + angle * self.axis[0],
                       rot_origin[1] + angle * self.axis[1],
                       rot_origin[2] + angle * self.axis[2]]
            self.child.rot.x = math.degrees(new_rot[0])
            self.child.rot.y = math.degrees(new_rot[1])
            self.child.rot.z = math.degrees(new_rot[2])
        elif self.joint.joint_type == "prismatic":
            #TODO
            pass
        elif self.joint.joint_type == "continious":
            pass
        else:
            print("No position possible to set")
            return

        for m_joint in self.mimic_joints:
            m_joint[0].set_position(m_joint[1] * angle + m_joint[2])

        if self.mode == "joint_color":
            color_g = self.current_value/self.joint.limit.upper
            color_r = 1. - color_g
            color = (color_r, color_g, 0)
            mat = Material(color=color, diffuse=color, specular=(0.3, 0.3, 0.3))
            self.child.children[0].children[0].set_material(mat)
            self.child.children[0].children[1].set_material(mat)
            #self.parent.set_material(mat)

    def connect_mimic(self, mimic_joint, a, b):
        self.mimic_joints.append([mimic_joint, a, b])

    def get_rotation_matrix(self, angle):
        u_x = self.axis.x
        u_y = self.axis.y
        u_z = self.axis.z
        a = angle
        #Rotation matrix from :
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
    def __init__(self, urdf, package_path, base_link="base_link", **kw):
        super(URDFObject, self).__init__(**kw)
        self.urdf = urdf
        self.package_path = package_path
        self.stlloader = STLLoader()

        self.default_material = \
            Material(color=(0.3, 0, 0), diffuse=(0.3, 0, 0),
                     specular=(0.3, 0, 0))

        # Create material dictionary
        self.materials = {}
        for material in urdf.materials:
            color = material.color.rgba
            self.materials[material.name] = Material(color=color[0:3],
                                                     diffuse=color[0:3],
                                                     specular=(0.1, 0.1, 0.1))
        self.link_dict = {}
        self.joint_dict = {}

        self.create_link_objects()

        self.link_joints()

        self.add(self.link_dict[base_link])
        self.link_dict[base_link].rot.x = -90
        # self.base_link = base_link

    def create_link_objects(self):
        for link in self.urdf.links:
            if link.name in self.link_dict:
                raise LinkError("Found duplicate link")
            kw = dict(name=link.name)
            self.link_dict[link.name] = Object3D(**kw)
            # Add visuals to the list
            for visual in link.visuals:
                # Add visual to the object
                if hasattr(visual, "material"):
                    pass
                    if visual.material.color is None:
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

                    print(material)
                    mesh = self.stlloader.load(filename, material)

                elif visual.geometry.XML_REFL.tag == "cylinder":
                    geometry = CylinderGeometry(visual.geometry.radius,
                                                visual.geometry.length)
                    mesh = Mesh(geometry, material)
                elif visual.geometry.XML_REFL.tag == "box":
                    geometry = BoxGeometry(*visual.geometry.size)
                    mesh = Mesh(geometry, material)
                elif visual.geometry.XML_REFL.tag == "sphere":
                    geometry = SphereGeometry(radius=visual.geometry.radius)
                    mesh = Mesh(geometry, material)

                # Adjust origin of geometry
                if visual.origin is not None:
                    # mesh.
                    # TODO: Implement origin offset
                    pass
                self.link_dict[link.name].add(mesh)

    def link_joints(self):
        # Go through the joints and connect them as objects.
        for joint in self.urdf.joints:
            parent_link = self.link_dict[joint.parent]
            child_link = self.link_dict[joint.child]
            parent_link.add(child_link)
            child_link.pos.x = joint.origin.position[0]
            child_link.pos.y = joint.origin.position[1]
            child_link.pos.z = joint.origin.position[2]
            child_link.rot.x = math.degrees(joint.origin.rotation[0])
            child_link.rot.z = math.degrees(joint.origin.rotation[1])
            child_link.rot.y = math.degrees(joint.origin.rotation[2])
            if joint.name in self.joint_dict:
                raise LinkError("Found duplicate joint")
            self.joint_dict[joint.name] = Joint(joint, child_link, parent_link)

        for joint in self.urdf.joints:
            if joint.mimic is not None:
                self.joint_dict[joint.mimic.joint].\
                    connect_mimic(self.joint_dict[joint.name],
                                  joint.mimic.multiplier,
                                  joint.mimic.offset)

    def calculate_joint_positions(self, base_joint=None):
        if base_joint is None:
            root = self.joint_dict["base_link"]

        pass


class URDFLoader(BaseLoader):
    def __init__(self, package_path=".", **kw):
        super(URDFLoader, self).__init__(**kw)
        self.package_path = package_path

    def load(self, source):
        robot = URDF.from_xml_file(source)
        urdf = URDFObject(robot, self.package_path)
        return urdf
