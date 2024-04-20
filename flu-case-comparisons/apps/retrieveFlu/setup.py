from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="retrieveFlu",
    version="0.1.0",
    description="Data retrieval function and executable for flu case study",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zebulun Arendsee",
    author_email="zbwrnz@gmail.com",
    packages=["retrieveFlu"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["retrieve=retrieveFlu:main"]},
    py_modules=["retrieveFlu"],
    zip_safe=False,
)
