from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tree",
    version="0.1.0",
    description="Tree functions for morloc case study",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zebulun Arendsee",
    author_email="zbwrnz@gmail.com",
    packages=["tree"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["tree=tree.main:main"]},
    py_modules=["tree"],
    zip_safe=False,
)
