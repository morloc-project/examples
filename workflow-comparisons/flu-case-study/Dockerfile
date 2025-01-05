# The Dockerfile for this build is available in the morloc
# GitHub repo v0.51.0.
FROM ghcr.io/morloc-project/morloc/morloc-full:0.51.1

# # Set environment variables to avoid interactive prompts during package installations
# ENV DEBIAN_FRONTEND=noninteractive
# ENV TZ=UTC

# The following are imported from the base:
#  * make
#  * python3-pip
#  * git
#  * vim
#  * r-base
#
# libeigen3-dev - eigen library for matrix operations in C++
RUN    apt-get update \
    && apt-get install -y libeigen3-dev pip hyperfine \
    && apt-get clean \
    && python3 -m pip install --upgrade pip setuptools wheel

# apt-get installs the eigen libraries into a `eigen3` subfolder, but
# pybind11 expects the main `Eigen` folder to be in PATH
RUN ln -s /usr/include/eigen3/Eigen /usr/include/Eigen

RUN pip3 install pybind11 numpy biopython requests rpy2 click


#### Setup the case study code and build apps
COPY modules /cases-lib
WORKDIR /cases-lib

RUN pip3 install treebase/ tree/ retrieveFlu/

ENV R_HOME="/usr/lib/R"
ENV R_LIBS="/usr/lib/R/library"
ENV R_LIBS_SITE="/usr/lib/R/library"

RUN    Rscript -e 'install.packages(c("ape", "optparse", "rlang", "future"), repos = "https://cloud.r-project.org")' \
    && R CMD build flutree \
    && R CMD INSTALL flutree_*.tar.gz

#### Setup workflow managers

# Install snakemake and dependencies
# The pulp downgrade is required to avoid breaking change in new versions
RUN pip3 install snakemake pulp==2.7.0

# Install nextflow and dependencies
RUN    pip3 install nextflow \
    && apt-get install -y default-jre wget \
    && nextflow info

# Install JSON library needed for json module
RUN apt-get install nlohmann-json3-dev
RUN apt-get install time

#### Setup morloc modules for case study
RUN    morloc install json   --commit a593104c \
    && morloc install bio    --commit ef3554c6 \
    && morloc install matrix --commit 12b2ad34

# Cleanup to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Remove module sources
RUN rm -rf /cases-lib
