#!/bin/bash

# Stop on error
set -e

# Get the number of available threads for multithreaded compiling
THREADS=$(nproc)

# cd to the directory where the script lies in
cd "$( dirname "${BASH_SOURCE[0]}" )"

echo "Installing dependencies. You might need to enter the root password"
cd dependencies/packages
sudo dpkg -i *.deb

cd ../carl

echo "Installing carl using $THREADS threads"
mkdir -p build
cd build
cmake .. -DUSE_CLN_NUMBERS=ON -DUSE_GINAC=ON
make lib_carl -j$THREADS

cd ../../../storm/

echo "Installing Storm using $THREADS threads"
source install_settings.sh
STORM_CMAKE_OPTIONS="$STORM_CMAKE_OPTIONS_GUROBI $STORM_CMAKE_OPTIONS_SOPLEX -DSTORM_USE_SPOT_SYSTEM=OFF"
echo "CMAKE Options: $STORM_CMAKE_OPTIONS"
mkdir -p build
cd build
cmake .. $STORM_CMAKE_OPTIONS
make storm-main -j$THREADS

cd ../../../
source setenv.sh
echo source $MDPMC_DIR/setenv.sh >> $HOME/.bashrc

echo "Installation successfull."
echo "Open a new terminal window to ensure that environment variables are properly set."
