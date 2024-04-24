from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "0.0.1"

ext_modules = [
    Pybind11Extension(
        "treebase",
        ["src/main.cpp"],
        define_macros=[("VERSION_INFO", __version__)],
    ),
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="treebase",
    version=__version__,
    author="Zebulun Arendsee",
    author_email="zbwrnz@gmail.com",
    url="https://github.com/morloc-project/examples",
    description="A python wrapper around the C++ rooted tree type",
    long_description_content_type="text/markdown",
    long_description="",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    entry_points={"console_scripts": ["rooted=rooted_tree.main:main"]},
    python_requires=">=3.7",
)
