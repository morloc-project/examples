FROM ubuntu:22.04 as morloc-debug

RUN apt-get update && apt-get install -y git curl pkg-config libglib2.0-dev

# Build morloc
RUN curl -SL https://get.haskellstack.org/ | sh

# Get the latest morloc release
RUN git clone https://github.com/morloc-project/morloc

# Update nameservers for DNS resolution, I needed to do this `morloc test` for
# some reason, it wasn't necessary for `morloc install`. Go figure.
RUN    echo "nameserver 8.8.8.8" >> /etc/resolv.conf \
    && echo "nameserver 8.8.4.4" >> /etc/resolv.conf

# Build morloc
RUN cd morloc && stack install && morloc test --fast

# Set the timezone, this avoids hanging later on
RUN DEBIAN_FRONTEND=noninteractive TZ=Antarctica/Troll apt-get -y install tzdata

RUN apt-get install -y r-base python3.10 libgsl-dev git pip libeigen3-dev hyperfine
RUN python3 -m pip install --upgrade pip setuptools
RUN pip3 install pybind11 numpy biopython requests rpy2 click

# apt-get installs the eigen libraries into a `eigen3` subfolder, but
# pybind11 expects the main `Eigen` folder to be in PATH
RUN ln -s /usr/include/eigen3/Eigen /usr/include/Eigen

ENV R_HOME="/usr/lib/R"
ENV R_LIBS="/usr/lib/R/library"
ENV R_LIBS_SITE="/usr/lib/R/library"

# Set up R environment
RUN Rscript -e 'install.packages(c("rlang", "future"), repos  = "https://cloud.r-project.org")'

ENV PATH="/root/.local/bin:$PATH"

# Setup the morloc home
RUN morloc init
RUN echo "lang_python3 : python3" >> $HOME/.morloc/config

# Install the morloc modules that are required for the morloc tests to pass
RUN morloc install prelude
RUN morloc install types
RUN morloc install conventions
RUN morloc install base
RUN morloc install rbase
RUN morloc install pybase
RUN morloc install cppbase
RUN morloc install math

RUN apt-get install -y vim

# Copy over custom vimrc
COPY assets/vimrc /root/.vimrc
COPY assets/README /root/README

# Set up vim highlighting for morloc
RUN git clone https://github.com/morloc-project/vimmorloc \
  && mkdir -p ~/.vim/syntax/ \
  && mkdir -p ~/.vim/ftdetect/ \
  && cp vimmorloc/loc.vim ~/.vim/syntax/ \
  && echo 'au BufRead,BufNewFile *.loc set filetype=loc' > ~/.vim/ftdetect/loc.vim \
  && rm -rf vimmorloc

#### Setup workflow managers

# Install snakemake and dependencies
# The pulp downgrade is required to avoid breaking change in new versions
RUN pip3 install snakemake pulp==2.7.0

# Install nextflow and dependencies
RUN  pip3 install nextflow \
  && apt-get install -y default-jre wget \
  && nextflow info

# Install JSON library needed for json module
RUN apt-get install nlohmann-json3-dev
RUN apt-get install time

#### Setup morloc modules for case study
RUN  morloc install json   --commit a593104c \
  && morloc install bio    --commit ef3554c6 \
  && morloc install matrix --commit 12b2ad34

# Cleanup to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
