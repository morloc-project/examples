FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt-get update && \
    apt-get install -y \
    make \
    python3-pip \
    libeigen3-dev \
    git \
    vim \
    && apt-get clean

# apt-get installes the eigen libraries into a `eigen3` subfolder, but
# pybind11 expects the main `Eigen` folder to be in PATH
RUN ln -s /usr/include/eigen3/Eigen /usr/include/Eigen

RUN pip3 install pybind11 numpy

# CMD ["bash"]
CMD pip install apps/rooted_tree/
