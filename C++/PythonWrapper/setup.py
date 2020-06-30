from setuptools import Extension, setup
from Cython.Build import cythonize
import setuptools
import os
import numpy
import platform

################################################################################
# prepare and find paths
################################################################################
# Current working directory
dirCurrent = os.path.abspath(os.getcwd())
# Build directory
dirBuild = os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..'))
# directory of cython definition files:
definition_files_dir = [os.path.join(dirBuild, 'PythonWrapper')]

################################################################################
# define cython package
################################################################################
source_files = [os.path.join(dirBuild, 'PythonWrapper', 'MPCCWrapper.pyx'),
                os.path.join(dirBuild, 'PythonWrapper', 'MPCCWrapperClass.cpp')]

include_dirs = [numpy.get_include(),
                os.path.join(dirBuild, 'External', 'blasfeo', 'lib', 'include'),
                os.path.join(dirBuild, 'External', 'hpipm', 'lib', 'include'),
                os.path.join(dirBuild, 'External', 'Eigen'),
                os.path.join(dirBuild, 'External', 'Json', 'include'),
                os.path.join(dirBuild)]

# Source files and include directories from code
source_files.append(os.path.join(dirBuild, 'types.cpp'))
source_files.append(os.path.join(dirBuild, 'Params', 'params.cpp'))
source_files.append(os.path.join(dirBuild, 'Spline', 'cubic_spline.cpp'))
source_files.append(os.path.join(dirBuild, 'Spline', 'arc_length_spline.cpp'))
source_files.append(os.path.join(dirBuild, 'Interfaces', 'hpipm_interface.cpp'))
source_files.append(os.path.join(dirBuild, 'Interfaces', 'solver_interface.cpp'))
source_files.append(os.path.join(dirBuild, 'Constraints', 'constraints.cpp'))
source_files.append(os.path.join(dirBuild, 'Constraints', 'bounds.cpp'))
source_files.append(os.path.join(dirBuild, 'Cost', 'cost.cpp'))
source_files.append(os.path.join(dirBuild, 'MPC', 'mpc.cpp'))
source_files.append(os.path.join(dirBuild, 'Params', 'track.cpp'))
source_files.append(os.path.join(dirBuild, 'Model', 'model.cpp'))
source_files.append(os.path.join(dirBuild, 'Model', 'integrator.cpp'))

# add libraries
libs = ['hpipm', 'blasfeo']

# library directories
library_dirs = [os.path.join(dirBuild, 'External/hpipm/lib/lib'),
                os.path.join(dirBuild, 'External/blasfeo/lib/lib')]

# prepare everything as python extension module
mpcc_extension = Extension(name="MPCC",
                            sources=source_files,
                            include_dirs=include_dirs,
                            language="c++",
                            library_dirs=library_dirs,
                            libraries=libs,
                            extra_compile_args=['-std=c++14'])

################################################################################
# build cython package
################################################################################
setup(
    name="mpcc",
    version="0.0.1",
    install_requires=['numpy'],
    ext_modules=cythonize(mpcc_extension,
    include_path=definition_files_dir,
    compiler_directives={'language_level': "3"}))
