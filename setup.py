from distutils.core import setup

from version import version

setup(
    name='robot-graphwalker',
    version=version,
    packages=['graph_robot_mbt'],
    license='GNU General Public License v3.0',
    long_description=open('README.md').read()
)