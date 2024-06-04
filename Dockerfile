# Set base image
ARG BASE_IMG=movesrwth/storm:ci
ARG BASE_PLATFORM=linux/amd64
FROM --platform=$BASE_PLATFORM  $BASE_IMG

# Specify configurations
# These configurations can be set from the commandline with:
# --build-arg <config_name>=<value>
# Specify number of threads to use for parallel compilation
ARG no_threads=1

RUN apt-get install unzip

## install highs
# We currently use a fixed version based on modest requirements.
WORKDIR /opt/
RUN git clone https://github.com/ERGO-Code/HiGHS.git &&  \
    cd HiGHS &&  \
    git checkout 2466dbf7213359461a501647b2b40c8569c71756  
WORKDIR /opt/HiGHS/
RUN mkdir build && cd build &&  \
    cmake .. && \
    make -j$no_threads

## Download mosek
WORKDIR /opt/

# Set up environment variables
ENV MOSEKHOME=/opt/mosek/latest \
    MOSEKBIN=/opt/mosek/latest/tools/platform/linux64x86/bin

# Download and unpack latest MOSEK
RUN wget https://download.mosek.com/stable/10.0.34/mosektoolslinux64x86.tar.bz2;  \
    tar -xf mosektoolslinux64x86.tar.bz2

# Download modest
RUN mkdir /opt/modest-tmp
WORKDIR /opt/modest-tmp
RUN wget https://www.modestchecker.net/Downloads/Modest-Toolset-v3.1.246-ga72d2b6fd-linux-x64.zip && \
    unzip Modest-Toolset-v3.1.246-ga72d2b6fd-linux-x64.zip && \
    mv Modest/ /opt/modest/
WORKDIR /opt/modest
RUN rm -rf /opt/modest-tmp
RUN ln -s /opt/HiGHS/build/lib/libhighs.so.1.2.2 libhighs.so; ln -s /opt/mosek/10.0/tools/platform/linux64x86/bin/libmosekxx10_0.so libmosekxx10_0.so


#############
RUN mkdir /opt/practitioners
WORKDIR /opt/practitioners

# Copy the content of the current local repository into the Docker image
COPY . .

