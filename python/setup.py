import sys
import os
import platform
import subprocess
import re

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion


CMAKE_OPTIONS = {'BUILD_PYTHON_MODULE': 'ON'}


def check_cmake_version():
    try:
        out = subprocess.check_output(['cmake', '--version'])
    except OSError:
        raise RuntimeError(
            "CMake must be installed to build this project")

    if platform.system() == "Windows":
        cmake_version = LooseVersion(
            re.search(r'version\s*([\d.]+)', out.decode()).group(1))
        if cmake_version < '3.1.0':
            raise RuntimeError("CMake >= 3.1.0 is required on Windows")


def get_version():
    """Get version string using git, source (root) directory, or conda
    build environment variable, formatted according to pep440.
    This functions calls a cmake script.
    """
    check_cmake_version()

    cmake_script = os.path.join('cmake', 'PrintVersion.cmake')
    cmake_args = ['-DINCLUDEDIR=include', '-P', cmake_script]

    out = subprocess.check_output(['cmake'] + cmake_args,
                                  cwd=os.pardir,
                                  stderr=subprocess.STDOUT)
    version_str = out.decode().strip()
    return version_str


class CMakeExtension(Extension):
    def __init__(self, name, source_dir='', cmake_options=None):
        Extension.__init__(self, name, sources=[])

        self.source_dir = os.path.abspath(source_dir)
        self.cmake_options = cmake_options or {}


class CMakeBuild(build_ext):
    def run(self):
        check_cmake_version()

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]
        cmake_args += ['-D{}={}'.format(k, v)
                       for k, v in ext.cmake_options.items()]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'
                           .format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']

        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = (
            '{} -DVERSION_INFO=\\"{}\\"'
            .format(env.get('CXXFLAGS', ''), self.distribution.get_version())
        )

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # note: need to run "pip install . -v" to see cmake output
        subprocess.check_call(['cmake', ext.source_dir] + cmake_args,
                              cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                              cwd=self.build_temp)


ext_modules = [
    CMakeExtension('_emodlib_py',
                   source_dir='..',
                   cmake_options=CMAKE_OPTIONS)
]


def readme():
    with open('README.rst') as f:
        return f.read()
        
        
setup(
    name='emodlib',
    version=get_version(),
    maintainer='Edward Wenger',
    maintainer_email='wenger.edward@gmail.com',
    url='https://github.com/edwenger/emodlib',
    description=('A library of demographic, within-host, and contact-network'
                 ' algorithms for disease modeling.'),
    long_description=readme(),
    packages=find_packages(),
    ext_modules=ext_modules,
    install_requires=['pyyaml'],
    cmdclass={'build_ext': CMakeBuild},
    zip_safe=False,
)
