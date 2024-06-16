# Set base image
ARG BASE_IMG=movesrwth/storm:ci
ARG BASE_PLATFORM=linux/amd64
FROM --platform=$BASE_PLATFORM  $BASE_IMG

# Specify configurations
# These configurations can be set from the commandline with:
# --build-arg <config_name>=<value>
# Specify number of threads to use for parallel compilation
ARG no_threads=1
ARG modest_version=v3.1.254
ARG modest_hash=gd8d4ba055
ARG mosek_version=10.2.0

RUN apt-get install unzip nano

## Download mosek
WORKDIR /opt/

# Set up environment variables
ENV MOSEKHOME=/opt/mosek/latest \
    MOSEKBIN=/opt/mosek/latest/tools/platform/linux64x86/bin

# Download and unpack latest MOSEK
RUN wget https://download.mosek.com/stable/$mosek_version/mosektoolslinux64x86.tar.bz2;  \
    tar -xf mosektoolslinux64x86.tar.bz2

# Download modest and update the Externals.defaults
RUN mkdir /opt/modest-tmp
WORKDIR /opt/modest-tmp
RUN wget https://www.modestchecker.net/Downloads/Modest-Toolset-$modest_version-$modest_hash-linux-x64.zip && \
    unzip Modest-Toolset-$modest_version-$modest_hash-linux-x64.zip && \
    mv Modest/ /opt/modest/ && rm -rf /opt/modest-tmp && \
    sed -i 's/\"gurobi-path\": \"\".*/\"gurobi-path\": \"\/opt\/gurobi\/linux64\/lib\/\"/' /opt/modest/Externals.defaults ; sed -i 's/\"mosek-path\": \"\".*/\"mosek-path\": \"\/opt\/mosek\/\"/' /opt/modest/Externals.defaults
COPY docker/modest_adapted_license.txt /opt/modest/license.txt
WORKDIR /opt/modest

#############
RUN mkdir /opt/practitioners
WORKDIR /opt/practitioners

# Copy the content of the current local repository into the Docker image
COPY . .

# The practitioners model checking assumes that tools are installed on hard-coded locations, which we fix using symlinks.
RUN ln -s /opt/modest/ /opt/practitioners/tools/Modest; ln -s /opt/storm /opt/practitioners/tools/storm
