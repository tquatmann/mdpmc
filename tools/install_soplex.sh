#!/bin/bash

# fail on error
set -e

# Get the number of available threads for multithreaded compiling
THREADS=$(nproc)

# go to the directory where this script lies in
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd dependencies

echo "Installing dependencies. You might need to enter the root password"
cd packages
sudo dpkg -i *.deb
cd ..

echo "Downloading Soplex"
TARBALL=Soplex-601-src.tar.gz
wget -O $TARBALL https://github.com/scipopt/soplex/archive/refs/tags/release-601.tar.gz
tar xf $TARBALL

echo "Installing Soplex"
SOPLEX_ROOT=$(realpath "$(ls | grep soplex)/")
echo Soplex root is $SOPLEX_ROOT
cd $SOPLEX_ROOT
mkdir build
cd build
cmake ..
make -j$THREADS
echo "Performing Soplex installation step which likely requires you to enter the root password"
sudo make install

# Append the appropriate CMake options for the configure step of Storm
cd ../../../
echo 'STORM_CMAKE_OPTIONS_SOPLEX="-DSTORM_USE_SOPLEX=ON"' >> storm/install_settings.sh

echo "Soplex installed."