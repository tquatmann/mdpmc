# Benchmark Data for The Revised Practitioner's Guide to MDP Model Checking Algorithms

See also the artifact of the conference paper: https://zenodo.org/records/7509474

## Abstract
This artifact allows to review and replicate the experiments from the paper *A Revised Practitioner's Guide to MDP Model Checking Algorithms*.
The package contains all original logfiles and the scripts that extract the relevant data from those logs to generate the plots as in the paper.

TODO: the rest of the abstract is old text and should be replaced accordingly:
Furthermore, the artifact contains the model checking tools `Storm` and `mcsta` with their dependencies and convenient installation scripts as well as all benchmark instances.
We provide installation instructions for those LP solvers that, due to licensing reasons, could not be included in this artifact.
The user can thus replicate all experiments from the paper.
An appropriate subset of the experiments is given to allow a review in a timely manner. In addition, single experiments can be handpicked for replication.

## Overview of Contents
The directory `mdpmc` contains

- A copy of this README as well as license information.
- Directories `claix23` (Sec 6.1), `claix23-all` (Sec 6.2), `claix23-permute` (Sec 6.3), `claix23-variance` (not in paper), `premise` (Sec 6.2), `hardware-experiments` (Sec 6.4), which contain raw data and commands for reproducing the experiments from the indicated sections.
- Facilities to quickly check if the tools work as expected in directory `quickcheck`
- The benchmark instances in directory `qcomp`
- The python scripts to run multiple experiments and process the obtained logfiles in `scripts`
- Information for running the experiments in a `docker` container (cf. Sec 6.4)
- A directory `latex` used to reproduce the plots from the paper. TODO

## Benchmark sets

Section 5.3 of the paper lists several benchmark sets. These are stored in the subdirectory `scripts/data`. 
**In this artifact, the *practitioners-set-2024* is called *community24***.


## Running a subset of experiments using a Docker container

TODO: write a step-by-step guide how to run the experiments on the practitioners set (as in Sec 6.4) so that a beautiful plot is obtained in the end

## Running full experiments without Docker

See file `tools/README.md` for detailed instructions on how to install the tools.
TODO: write that readme file

### Quick Check

To quickly check if the installation of Storm, mcsta, and the LP solvers work as expected, open a terminal window, then

```
cd  quickcheck/
python3 ../scripts/run.py quick.json
```

This executes all 114 configurations on a small benchmark instance. This should take one or two minutes.
Afterwards, run 

```
python3 ../scripts/postprocess_quickcheck.py logs/
```

to check which configurations are working properly.
Configurations involving unavailabe LP solvers (see above) are expected to fail.

### Reviewing and reproducing the Experiments

The Directories
- `claix23` (Sec 6.1), 
- `claix23-all` (Sec 6.2), 
- `claix23-permute` (Sec 6.3),
- `claix23-variance` (not in paper), TODO
- `premise` (Sec 6.2), and
- `hardware-experiments` (Sec 6.4) TODO: no logfiles yet
 
each contain an archive `logs.tar.gz` containing the logfiles from our experiments, a file `inv.json` containing information for reproducing the experiments, and a script `cpdata.sh` that copies over all data used for the plots in the paper to the `latex/` directory.

To review our experimental results, unpack the logfiles, e.g., using `tar xf logs.tar.gz`.
Then, run `python3 ../scripts/postprocess.py logs/` to generate the derived data (i.e. `.csv` files for quantile and scatter plots and detailed result tables) from the logs.
The script creates a subdirectory for each benchmark set (cf. Sec 5.4). Note that only certain benchmark sets are relevant for a given set of experiments. Look at `cpdata.sh` to see which subdirectories are relevant.
Opening the file `$BENCHMARK_SET/table/table.html` in a web browser shows an interactive result table where each cell shows the model checking time of a configuration (column) on a benchmark instance (row). Clicking on a cell opens a page showing the precise command and the corresponding logfile.

To reproduce the experiments from the paper, remove the `logs/` directory (in case it exists) and run `python3 ../scripts/run.py inv.json` in the respective directory.
Depending on the experiment, this will take a lot of time (possibly multiple days).
Once this is complete, new logfiles should be available in the `logs/` directory.
Run `python3 ../scripts/postprocess.py logs/` to generate the derived data from the logs (see above).
Running `./cpdata.sh` copies the data used for the plots in the paper to the `mdpmc/latex/` directory located at the root of this artifact.
This step overwrites the data from our experiments with the data from the replicated experiments.
(Re-)building the latex document with `pdflatex main.tex` then shows the reproduced figures.

TODO: make the latex document

It is also possible to run a custom subset of experiments. Create a new directory, say, `mdpmc/replication/`. `cd` into that directory and run `python3 ../scripts/run.py`.
The command line interface will guide you through the process of selecting the benchmark set and the tool configurations.

## Other Experiments
TODO: The following is from the tacas submission. Might want to update.
To replicate the information presented in Table 1, run `./hmmdp.sh` in the `mdpmc` directory. It step-by-step executes the commands needed to obtain the outcomes presented in Table 1. 
When the corresponding LP solver is not installed, the corresponding commands will fail. See *Installation of LP Solvers*.
