#!/bin/bash

TARBALL=$(realpath $1)

# fail on error
set -e

# Check if the provided filename exist
if ! test -f "$TARBALL"; then
	echo "Usage:"
	echo "  $0 path/to/gurobi*linux64.tar.gz"
	exit 1
fi

# go to the directory where this script lies in
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd dependencies

# unpack the tarball
echo Unpacking $TARBALL
tar xf $TARBALL
GUROBI_ROOT=$(realpath "$(ls | grep "gurobi")/linux64")
echo Gurobi root is $GUROBI_ROOT

# Append the appropriate CMake options for the configure step of Storm
cd ..
echo 'STORM_CMAKE_OPTIONS_GUROBI="-DSTORM_USE_GUROBI=ON -DGUROBI_ROOT='$GUROBI_ROOT'"' >> storm/install_settings.sh

# Copy to Modest
cp $GUROBI_ROOT/lib/libgurobi* Modest/

echo "Gurobi installed. Now execute the following command to enter your gurobi license key:"
echo $GUROBI_ROOT/bin/grbgetkey
