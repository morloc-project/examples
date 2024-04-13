# I spent the whole damn morning trying to fix my latex environment on manjaro,
# all to no avail. So fuck that shit. I'll install it all on an ubuntu
# container.

FROM ubuntu:latest

# Set environment variables to avoid interactive prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt-get update && \
    apt-get install -y \
    make \
    python3-pip \
    libeigen3-dev \
    && apt-get clean

# apt-get installes the eigen libraries into a `eigen3` subfolder, but
# pybind11 expects the main `Eigen` folder to be in PATH
RUN ln -s /usr/include/eigen3/Eigen /usr/include/Eigen

RUN pip3 install pybind11 numpy

WORKDIR /case-comparison
COPY apps /case-comparison

CMD ["bash"]
# CMD pip install rooted_tree/
