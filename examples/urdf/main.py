
import os
import math
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

from kivy3 import Scene, Renderer, PerspectiveCamera, Mesh, Material
from kivy3.extras.geometries import BoxGeometry
from kivy3.extras.stlgeometry import STLGeometry
from kivy3.loaders import OBJLoader
from kivy.uix.floatlayout import FloatLayout
from urdf_parser_py.urdf import URDF
from stl import mesh

# Resources paths
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


class ObjectTrackball(BoxLayout):

    def __init__(self, camera, radius, *args, **kw):
        super(ObjectTrackball, self).__init__(*args, **kw)
        self.camera = camera
        self.radius = radius
        self.phi = 90
        self.theta = 0
        self._touches = []
        self.camera.pos.z = radius
        self.look_at_pos = (0, 0.3, 0)
        camera.look_at(self.look_at_pos)

    def define_rotate_angle(self, touch):
        theta_angle = (touch.dx / self.width) * -360
        phi_angle = -1 * (touch.dy / self.height) * 360
        return phi_angle, theta_angle

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if 'button' in touch.profile:
                if touch.button == 'scrollup':
                    if self.radius > 0:
                        self.radius *= 1.1
                    self.update_after_scroll()
                elif touch.button == 'scrolldown':
                    if self.radius > 0:
                        self.radius *= 0.9
                    self.update_after_scroll()
                else:
                    touch.grab(self)
                    self._touches.append(touch)

    def on_touch_up(self, touch):
        touch.ungrab(self)
        if touch in self._touches:
            self._touches.remove(touch)
        self.camera.update()

    def on_touch_move(self, touch):
        if touch in self._touches and touch.grab_current == self:
            if len(self._touches) == 1:
                if touch.button == 'right':
                    self.do_translate(touch)
                else:
                    self.do_rotate(touch)
            elif len(self._touches) == 2:
                pass

    def do_translate(self, touch):
        scale = 0.001
        x = self.look_at_pos[0] # + (touch.dx * scale)
        y = self.look_at_pos[1] - (touch.dy * scale)
        z = self.look_at_pos[2]
        self.look_at_pos = (x, y, z)
        self.camera.look_at(self.look_at_pos)

    def do_rotate(self, touch):
        d_phi, d_theta = self.define_rotate_angle(touch)
        self.phi += d_phi
        self.theta += d_theta

        _phi = math.radians(self.phi)
        _theta = math.radians(self.theta)
        z = self.radius * math.cos(_theta) * math.sin(_phi)
        z += self.look_at_pos[2]
        x = self.radius * math.sin(_theta) * math.sin(_phi)
        x += self.look_at_pos[0]
        y = self.radius * math.cos(_phi)
        y += self.look_at_pos[1]
        self.camera.pos = x, y, z
        self.camera.look_at(self.look_at_pos)

    def update_after_scroll(self):
        _phi = math.radians(self.phi)
        _theta = math.radians(self.theta)
        z = self.radius * math.cos(_theta) * math.sin(_phi)
        z += self.look_at_pos[2]
        x = self.radius * math.sin(_theta) * math.sin(_phi)
        x += self.look_at_pos[0]
        y = self.radius * math.cos(_phi)
        y += self.look_at_pos[1]
        self.camera.pos = x, y, z
        self.camera.look_at(self.look_at_pos)


class MainApp(App):

    def build(self):
        self.renderer = Renderer(shader_file=shader_file)
        self.renderer.set_clear_color((.6, .6, .6, 1.))
        scene = Scene()

        camera = PerspectiveCamera(90, 1, 0.1, 2500)
        self.camera = camera

        root = BaseBox()
        trackball = ObjectTrackball(camera, 1)

        # robot = URDF.from_xml_file('./RS2-1032-segmented-def.SLDASM/urdf/RS2-1032-segmented-def.SLDASM.urdf')
        # robot = URDF.from_xml_file('./RS2-1021-segmented-def-urdf/urdf/RS2-1021-segmented-def-urdf.urdf')
        robot = URDF.from_xml_file('./RS2-7FN-Def-URDF-Exp/urdf/RS2-7FN-Def-URDF-Exp.urdf')
        link_dict = {}

        for link in robot.links:

            # get geometry each link
            filename = link.visual.geometry.filename
            filename = filename.replace('package:/', '.')
            print(filename)
            stl = mesh.Mesh.from_file(filename)
            geo = STLGeometry(stl)

            # if len(geo.vertices) == 0:
            #     geo = BoxGeometry(0.1, 0.1, 0.1)

            material = Material(color=link.visual.material.color.rgba,
                                diffuse=link.visual.material.color.rgba,
                                specular=(.01, .01, .01),
                                shininess=4)

            try:
                obj = Mesh(geo, material, name=link.name)
            except Exception as e:
                print(e)
                geo = BoxGeometry(0.1, 0.1, 0.1)
                obj = Mesh(geo, material, name=link.name)

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
