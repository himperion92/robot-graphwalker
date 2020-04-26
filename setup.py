from distutils.core import setup

from version import version

setup(
    name='robot-graphwalker',
    version=version,
    packages=['robot_model_based', 'robot_graphic_seq'],
    license='GNU General Public License v3.0',
    long_description=open('README.md').read()
)