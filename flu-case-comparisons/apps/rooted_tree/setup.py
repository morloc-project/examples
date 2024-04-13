from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "0.0.1"

ext_modules = [
    Pybind11Extension(
        "rooted_tree",
        ["src/main.cpp"],
        define_macros=[("VERSION_INFO", __version__)],
    ),
]

setup(
    name="rooted_tree",
    version=__version__,
    author="Zebulun Arendsee",
    author_email="zbwrnz@gmail.com",
    url="https://github.com/morloc-project/examples",
    description="A python wrapper around the C++ rooted tree type",
    long_description="",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
)
