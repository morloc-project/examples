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
    r-base \
    && apt-get clean \
    && python3 -m pip install --upgrade pip setuptools wheel

# apt-get installes the eigen libraries into a `eigen3` subfolder, but
# pybind11 expects the main `Eigen` folder to be in PATH
RUN ln -s /usr/include/eigen3/Eigen /usr/include/Eigen

RUN pip3 install pybind11 numpy biopython requests rpy2 click

COPY modules /cases-lib
WORKDIR /cases-lib

RUN pip3 install treebase/
RUN pip3 install tree/
RUN pip3 install retrieveFlu/

ENV R_HOME="/usr/lib/R"
ENV R_LIBS="/usr/lib/R/library"
ENV R_LIBS_SITE="/usr/lib/R/library"

RUN Rscript -e 'install.packages("ape", repos  = "https://cloud.r-project.org")' && \
    R CMD build flutree && \
    R CMD INSTALL flutree_*.tar.gz
