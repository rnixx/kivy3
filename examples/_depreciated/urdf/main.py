import os
import math
from kivy.app import App
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

from kivy3 import Scene, Renderer, PerspectiveCamera, Mesh, Material
from kivy3.controls.orbitcontrols import OrbitControls
from kivy3.extras.geometries import BoxGeometry
from kivy3.extras.stlgeometry import STLGeometry
from urdf_parser_py.urdf import URDF
from stl import mesh

# Resources paths
from kivy3.objects.stlmesh import STLMesh

_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "./blinnphong.glsl")


class BaseBox(BoxLayout):
    theta = ListProperty([0, 0, 0, 0, 0, 0, 0, 0])
    joints = []
    renderer = ObjectProperty()
    control_box = ObjectProperty()
    control_widgets = []

    def on_parent(self, inst, renderer):
        for widg in reversed(self.control_widgets):
            self.control_box.add_widget(widg)


class JointControl(BoxLayout):
    name = StringProperty('Joint Name')
    value = NumericProperty(0)
    min = NumericProperty(0)
    max = NumericProperty(360)
    joint = ObjectProperty()

    def on_value(self, inst, value):
        self.joint.rotation.x = self.joint.rot_offset[0] + value * self.joint.axis[0] if self.joint.axis[0] else self.joint.rotation.x
        self.joint.rotation.y = self.joint.rot_offset[0] + value * self.joint.axis[1] if self.joint.axis[1] else self.joint.rotation.y
        self.joint.rotation.z = self.joint.rot_offset[0] + value * self.joint.axis[2] if self.joint.axis[2] else self.joint.rotation.z


class MainApp(App):

    def build(self):
        self.renderer = Renderer(shader_file=shader_file)
        self.renderer.set_clear_color((.6, .6, .6, 1.))
        scene = Scene()

        camera = PerspectiveCamera(90, 1, 0.1, 2500)
        self.camera = camera

        root = BaseBox()
        trackball = OrbitControls(camera, 1)

        # robot = URDF.from_xml_file('./RS2-1032-segmented-def.SLDASM/urdf/RS2-1032-segmented-def.SLDASM.urdf')
        # robot = URDF.from_xml_file('./RS2-1021-segmented-def-urdf/urdf/RS2-1021-segmented-def-urdf.urdf')
        robot = URDF.from_xml_file('RS2-7FN-Def-URDF-Exp/urdf/RS2-7FN-Def-URDF-Exp.urdf')
        link_dict = {}

        for link in robot.links:

            # get geometry each link
            filename = link.visual.geometry.filename
            filename = filename.replace('package:/', '.')
            print(filename)
            stl = mesh.Mesh.from_file(filename)
            # geo = STLGeometry(stl)

            # if len(geo.vertices) == 0:
            #     geo = BoxGeometry(0.1, 0.1, 0.1)

            material = Material(color=link.visual.material.color.rgba,
                                diffuse=link.visual.material.color.rgba,
                                specular=(.01, .01, .01),
                                shininess=4)

            obj = STLMesh(stl, material, name=link.name)

            # store in dictionary
            link_dict[link.name] = obj

        self.joints = []
        self.child_joints = []

        for joint in robot.joints:
            parent_link = link_dict[joint.parent]
            child_link = link_dict[joint.child]
            parent_link.add(child_link)
            child_link.pos.x = joint.origin.position[0]
            child_link.pos.y = joint.origin.position[1]
            child_link.pos.z = joint.origin.position[2]
            child_link.rot.x = math.degrees(joint.origin.rotation[0])
            child_link.rot.z = math.degrees(joint.origin.rotation[1])
            child_link.rot.y = math.degrees(joint.origin.rotation[2])
            child_link.rot_offset = [child_link.rot.x, child_link.rot.y, child_link.rot.z]
            child_link.axis = joint.axis
            self.joints.append(parent_link)
            self.child_joints.append(child_link)

            ctrl = JointControl()
            ctrl.name = child_link.name
            ctrl.joint = child_link
            root.control_widgets.append(ctrl)

        scene.add(self.joints[0])

        self.renderer.render(scene, camera)
        self.renderer.main_light.intensity = 2000

        trackball.add_widget(self.renderer)
        root.renderer_box.add_widget(trackball)
        root.joints = self.child_joints

        self.renderer.bind(size=self._adjust_aspect)
        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect


if __name__ == '__main__':
    # Disable the orange dot that appears on right clicks.
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse,disable_multitouch')

    MainApp().run()
