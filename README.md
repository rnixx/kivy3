# Kivy3 - 3D graphics framework for Kivy

Kivy3 is the framework which helps people work with 3D elements and rendering
within Kivy application. Basically with Kivy and Kivy3 you may create a 3D
application for any platform Kivy supports, such as: iOS, Android, Windows,
OSX, Linux (including Raspberry Pi).

Kivy3 provides a toolset and abstraction levels to work with 3D objects like
Camera, Scene, Renderers, loaders you may use to load 3D objects.

# Installation

First create a virtual environment.

    $ python3 -m venv .

Install all needed dependencies.

    $ ./bin/pip install Cython==0.29.9
    $ ./bin/pip install kivy==1.11.1
    $ ./bin/pip install numpy
    $ ./bin/pip install scipy
    $ ./bin/pip install numpy-stl
    $ ./bin/pip install https://github.com/ros-infrastructure/catkin_pkg/archive/0.4.17.tar.gz
    $ ./bin/pip install https://github.com/ros/urdf_parser_py/archive/0.4.3.tar.gz

For further info about kivy visit
[Kivy documentation](https://kivy.org/docs/installation/installation.html).

After successful Kivy installation install Kivy3 with this:

    $ ./bin/pip install https://github.com/JohnSumskas/kivy3/zipball/sbarlowbpl/john_merger

# Packaging kivy3

Kivy3 is a pure python package, currently available only at GitHub, which
means that for packaging it e.g. for Android you need to clone the folder
to your application folder (the one with `main.py`). If you can run the app
on a desktop machine, it should work even on other platforms.

Don't forget to add an include exception for additional files, such as shader
(`*.glsl`) and other files you may find in the `kivy3` folder.
