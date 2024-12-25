This package includes Storm and mcsta in the versions as used in the paper.
We describe the installation here, assuming a Linux system with an x86-64 architecture.
Alternatively, we provide a Docker container that already contains the tools in the versions provided here.

## Usage with our scripts

Our scripts for reproducing the experiments expect the following binaries to exist in the root directory of the reproduce archive:

- `./tools/Modest/modest`
- `./tools/storm/build/bin/storm`

You can either install the tools directly in these directories or create symlinks like this (replace with your paths accordingly):

```
ln -s ./path/to/modest/ ./mdpmc/tools/Modest
ln -s ./path/to/storm/build/bin ./mdpmc/tools/storm/build/bin
```


## Installation of the Modest Toolset

The artifact includes a pre-build version of `mcsta` as part of the Modest toolset.
For installation, simply unpack the archive `Modest-Toolset-v3.1.259-g48dcb6391-linux-x64.zip`.
The LP solvers GLOP, HiGHS, and LP_SOLVE are included.
The LP solvers [COPT v7.1.3](https://www.shanshu.ai/copt), [CPLEX v22.1.1.0](https://www.ibm.com/analytics/cplex-optimizer), [Gurobi v11.0.0](https://www.gurobi.com/), and [Mosek v10.2](https://www.mosek.com/) are not included and need to be obtained (and licensed) separately.

mcsta tries to find the LP solver libraries automatically. If this fails, add the respective paths to the `Externals.defaults` file located in the `Modest` directory.
For example, the file may look like this:

```json
{
"dot-path": "",
"qcomp-source": "",
"qcomp-cache-path": "",
"copt-path": "/opt/copt71/lib",
"cplex-path": "/opt/cplex/cplex/bin/x86-64_linux",
"gurobi-path": "/opt/gurobi1100/linux64/lib/",
"mosek-path": "/opt/mosek/10.2/tools/platform/linux64x86/bin"
}
```

See [the website of the Modest Toolset](https://www.modestchecker.net/Docs/) for more information.


## Installation of Storm

The artifact contains the source code of Storm as used in the paper.
Alternatively, the official release of Storm 1.9.0 can be used which contains all features exercised in our experiments.
The [Storm website](https://www.stormchecker.org/documentation/obtain-storm/build.html) contains documentation on how to build Storm and its dependencies.

For quick reference, start by building the dependenciies, e.g., for Ubuntu and Debian systems:

```
sudo apt-get install build-essential git cmake libboost-all-dev libcln-dev libgmp-dev libginac-dev automake libglpk-dev libhwloc-dev libz3-dev libeigen3-dev
```

Next, install SoPlex and/or Gurobi (optional). Once completed, build Storm:

```
cd storm
mkdir build
cd build
cmake .. -DSTORM_USE_GUROBI=ON -DSTORM_USE_SOPLEX=ON # Change to OFF if you do not have Gurobi or SoPlex
# Check the output of the cmake command to see if Gurobi and Soplex are found.
# If not, try adding the cmake options -DGUROBI_ROOT=path/to/gurobi -DSOPLEX_ROOT=path/to/soplex
make storm-main -j4 # Replace 4 with the number of cores you want to use for compilation
```


