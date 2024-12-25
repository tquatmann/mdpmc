# Benchmark Data for The Revised Practitioner's Guide to MDP Model Checking Algorithms

## Abstract
This artifact allows to review and reproduce the experiments from the paper *A Revised Practitioner's Guide to MDP Model Checking Algorithms*.
The package contains all original logfiles and derived data used to generate the plots as in the paper.
Furthermore, the artifact contains the model checking tools `Storm` and `mcsta` in the version exercised in the paper, the used Docker container, as well as benchmark instances and execution scripts to reproduce the experiments.

See also the artifact of the conference paper: https://zenodo.org/records/7509474

## Overview of Contents

The artifact repository contains
- A copy of this README as well as license information.
- An archive `original_results.tar.gz` which contains logfiles and derived data (including browsable html tables and .csv tables from which we derive our plots).
- An archive `reproduce.tar.gz` which contains
  - The benchmark instances in directory `qcomp`
  - The python scripts to run experiments and process the obtained logfiles in `scripts`
  - Facilities to quickly check if the tools work as expected in directory `quickcheck`
  - directories similar to the ones in `original_results.tar.gz` but with the logfiles removed
- An archive `tools.tar.gz` which contains the exercised tools `Storm` and `mcsta` (part of the Modest Toolset) as well as licensing information
- An archive `docker.tar.gz` containing our docker image (cf. Sec 6.4)

**Throughout the artifact, the *practitioners-set-2024* is called *community24***.

## Reviewing our Experiments

The archive `original_results.tar.gz` contains logfiles and derived data (including a browsable html table and the .csv tables from which we derive our plots).

The archive contains directories
- `claix23` (Sec 6.1),
- `claix23-all` (Sec 6.2),
- `claix23-permute` (Sec 6.3),
- `claix23-variance` (not in paper),
- `premise` (Sec 6.2),
- `hardware-experiments` (Sec 6.4),

These directories each contain
- subdirectories for the individual benchmark sets (the *practitioners-set-2024* is called *community24*) which then contain
  - tables in html format which allow to review the experiments in greater detail, inspect logfiiles, etc. Each cell shows the model checking time of a configuration (column) on a benchmark instance (row). Clicking on a cell opens a page showing the precise command and the corresponding logfile.
  - `.csv` files used for our quantile and scatter plots
  - `.json` files containing general statistics like number of incorrect results.
- the raw log files (directory names starting with `logs`)
- a file `inv.json` containing the command lines.
- a script `cpdata.sh` that copies over all data used for the plots in the paper to the `latex/` directory.

The archive further contains a `latex/` directory which contains the code used to generate the paper plots. The provided script `build_latex.sh` builds the document (assuming a working lualatex installation).
 
## Reproducing Our Experiments

`reproduce.tar.gz` contains model files and scripts to reproduce the experiments from the paper.
The archive contains

- directory `qcomp` which is an extended copy of the [QComp](https://qcomp.org/) repository that also includes our additional benchmarks
- directory `scripts` which contains the python scripts to run experiments and process the obtained logfiles
- directory `quickcheck` which contains an invocation of a simple benchmark to check the tool installation
- directories similar to the ones in `original_results.tar.gz` but with the logfiles removed


### Benchmark Sets

Section 5.3 of the paper lists several benchmark sets. The model and property files can be found in `qcomp/benchmarks`. The exact instances considered in each set are in `scripts/data`. The *practitioners-set-2024* is called *community24*.

### Using Docker

The artifact repository contains a docker image (cf. Sec. 6.4 of the paper) which can be used to perform a subset of the experiments in reasonable time (i.e. a few hours).
Download the archive `docker.tar.gz` and follow the provided readme to obtain a directory containing log files. 
Then, copy the obtained logfiles to the `hardware-experiments` directory. Rename the directory to `logs-own` and run `./postprocess.sh`.
After the postprocessing step, detailed results can be shown by opening `community24/table/table.html` in a web browser.
Furthermore, the document `latex/0_main.pdf` contains the plots similar to those from Section 6.4 of the paper (restricted to just two plattforms).

### Preparations for Running Experiments without Docker

To run the experiments without Docker, the tools *Storm* and *mcsta* as well as their dependencies (including the respective LP solvers) need to be installed. We expect a UNIX (Linux or macOS) system.
The `tools.tar.gz` archive from the artifact repository contains the precise versions of the tools used in the paper as well as installation instructions.
Alternatively, existing installations of [the Modest Toolset](https://www.modestchecker.net/) version 3.1.260 (containing mcsta)  and [Storm](https://stormchecker.org) version 1.9.0 can be used.
Newer versions likely work as well, but might yield different results due to changes in the tools.

The scripts expect that executables `tools/Modest/modest` and `tools/storm/build/bin/storm` exist in the artifact directory (i.e. directory `tools` is located at the same level as `scripts` and `qcomp`).
If the tools are installed in a different location, the executables can be symlinked to the expected location, e.g., by running
`ln -s path/to/modest/ path/to/tools/Modest` and `ln -s path/to/storm/build/bin path/to/tools/storm/build/bin`

To test the installation and the scripts, you may `cd` into the `quickcheck` directory and run `python3 ../scripts/run.py quick.json`.
This will execute all 114 configurations on a small benchmark instance, which should take one or two minutes.
Then, run `python3 ../scripts/postprocess_quickcheck.py logs/` to check which configurations are working properly.
Configurations involving unavailabe LP solvers are expected to fail. Moreover, The configuration `logs.Storm.pi-mono-gmres-bicgstab` is expected to fail since the bicgstab method fails to converge for the given instance. 

### Reproducing Individual Runs

One way to assert reproducability of our results is to "challenge" individual runs.
When reviewing our results in an html table (see above), the logpages show the exact tool invocation.
Executing this command allows to compare our obtained log with the one obtained on the local machine.
For this, it might be convenient to set the `$MDPMC_DIR` environment variable via `export MDMPC_DIR=/path/to/mdpmc`.

### Running All Experiments from Section 6.1 to 6.3

To reproduce the experiments from Section 6.1 to 6.3 of the paper, change into one of the result directories `claix23*`, `premise`.
Run `python3 ../scripts/run.py inv.json` in the respective directory. This runs all associated experiments and will likely take multiple days.
Once the experiments are finished, run `python3 ../scripts/postprocess.py logs/` to generate the derived data from the logs (i.e. `.csv` files for quantile and scatter plots and detailed result tables in html).
Note that this command will create multiple directories referring to the different benchmark sets, even though the corresponding set of experiments only considers one or two of these benchmark sets.
The contents of the `cpdata.sh` script indicate what subdirectories are relevant.

You may use the script `build_latex.sh` to generate the latex document that contains the plots from the paper (see the section on reviewing our experiments above).
However, it might be necessary to edit the file `latex/0_main.tex` to remove those figures that refer to experiments that did not run.

### Reproducing Experiments from Section 6.4

Section 6.4 studies the influence of different benchmarking hardware. Reproducing this set of experiments would require access to those plattforms (or at least a similar range of plattforms).
As this is potentially difficult, this artifact allows to run the experiments on a single machine and compare that to our results on our main benchmarking plattform `claix23`.

To run the experiments, change into the `hardware-experiments` directory and run `python3 ../scripts/run.py inv.json`.
This command will take approximately 12 hours and creates a set of logfiles in the directory `logs-own/`. 
Alternatively, the logfiles can be obtained from our Docker container (see above).
Once the logfiles are in place, run `./postprocess.sh` to process the log files.

Detailed results can be shown by opening `community24/table/table.html` in a web browser.
Furthermore, the document `latex/0_main.pdf` contains the plots similar to those from Section 6.4 of the paper (restricted to just two plattforms).


