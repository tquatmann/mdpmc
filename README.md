# Benchmark Data for a Practitioner's Guide to MDP Model Checking Algorithms

Taken from the original artifact: https://zenodo.org/records/7509474

## Abstract
This artefact allows to review and replicate the experiments from the paper *A Practitioner's Guide to MDP Model Checking Algorithms*.
The package contains all original logfiles and the scripts that extract the relevant data from those logs to generate the plots as in the paper.
Furthermore, the artefact contains the model checking tools `Storm` and `mcsta` with their dependencies and convenient installation scripts as well as all benchmark instances.
We provide installation instructions for those LP solvers that, due to licensing reasons, could not be included in this artefact.
The user can thus replicate all experiments from the paper.
An appropriate subset of the experiments is given to allow a review in a timely manner. In addition, single experiments can be handpicked for replication.


## VM Preparation

The base memory for the virtual machine should be set to at least 4 GB (preferably more). In VirtualBox, this can be done at `Settings > System > Motherboard`. We also recommend to enable at least 4 processor cores.

Copy the directory `mdpmc` into the home folder `/home/tacas23/` of the artifact VM. That is, you should be able to find this readme under`/home/tacas23/mdpmc/README.md`.

## Overview of Contents
The directory `mdpmc` contains

- A copy of this README as well as license information.
- Relevant tools and installation scripts in directory `tools`.
- Facilities to quickly check if the tools work as expected in directory `quickcheck`
- The benchmark instances in directory `qcomp`
- The original logfiles and derived data in directory `original`
- The python scripts to run multiple experiments and process the obtained logfiles in `scripts`
- A directory `replication` containing data used for replicating the experiments.
- A document `configurations.pdf` that lists all 57 considered combinations of tools, algorithms, algorithm configurations, and LP solvers. For each such combination, we give an identifier (as used in the scripts of this artefact) in bold letters, the occurrences in the paper, and the command line for either storm or mcsta.

## Installation of LP Solvers (optional)

Our experiments consider various LP solvers. For some solvers, the license prohibits their inclusion in this artifact. Those solvers can be installed assuming an appropriate license and an Internet connection (to activate/obtain the licenses). All solvers are free for academic users. Our instructions below assume an academic user.
It is also possible to evaluate the artifact without installing any commercial solver. Experiments involving those solvers then cannot be replicated.
We recommend to (at least) install Gurobi and SoPlex as they are used frequently.

Before installing any of the LP solvers, the Internet connection needs to be enabled. In VirtualBox this is done by enabling the checkbox at `Settings > Network > Adapter 1 > Enable Network Adapter`. The virtual machine has to be powered off for this.
Make sure that the directory `mdpmc` is copied into the home folder of the artifact VM

### Installing Gurobi (recommended)

1. Register as an academic user at https://pages.gurobi.com/registration.
2. Make sure that you are logged in and download the Gurobi Optimizer at https://www.gurobi.com/downloads/. We recommend downloading the file gurobi9.5.2_linux64.tar.gz as we used version 9.5.0 in the paper. The recently released version 10 should also work for Storm, but is not yet supported by mcsta.
3. Obtain an academic license key by visiting https://www.gurobi.com/downloads/end-user-license-agreement-academic/. Once you have the license, you will see a command line like `grbgetkey XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` at the bottom of the webpage. You will need this key in Step 6.
4. Open a terminal window, `cd` to the directory `mdpmc/tools/`, and execute `./install_gurobi.sh ~/Downloads/gurobi9.5.2_linux64.tar.gz` (you might need to change the version number and/or the file location). This script unpacks the downloaded file in appropriate directories and makes sure that the correct options will be set when building Storm later.
5. Execute `./dependencies/gurobi952/linux64/bin/grbgetkey XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`, where you insert the key from above. Store the license key file in `/home/tacas23`.

Gurobi wants to contact the licensing server with a certain regularly, even after the installation. In case of issues referring to the Gurobi license, it could help to repeat Step 5 (with an active Internet connection).

### Installing SoPlex (recommended)

Open a terminal window, then

```
cd /home/tacas/mdpmc/tools/
./install_soplex.sh
```

This will automatically download the appropriate version of SoPlex from GitHub and install SoPlex and its dependencies. The script also ensures that the correct options will be set when building Storm later.

### Installing Copt

1. Obtain a trial license for Linux via the form at https://www.shanshu.ai/copt.
   After some time (usually within 2 working days), you will receive an email with a license key.
   Note this key and insert it in place of KEY in step 3.
2. Download and unpack COPT:
   ```
   cd /home/tacas/mdpmc/tools/Modest
   wget https://pub.shanshu.ai/download/copt/5.0.5/linux64/CardinalOptimizer-5.0.5-lnx64.tar.gz
   tar -xzf CardinalOptimizer-5.0.5-lnx64.tar.gz
	 ln -s copt50/lib/libcopt.so libcopt.so
   ```
3. Obtain a license file (using your license key in place of KEY):
   ```
   copt50/bin/copt_licgen -key KEY
   ```
4. Test the installation:
   ```
   ./modest mcsta qcomp://brp -E "N=16,MAX=2" --props p1 --alg LinearProgramming --lp-solver COPT
   ```
   If successful, the output should report probability 0.0004233334437734178 for property p1.
   The output must not contain a "Could not find COPT license: COPT is running in size-limited mode" warning or a "COPT licensing error" message.


### Installing Cplex

1. Register at https://www.ibm.com/academic/topic/data-science, then download the "ILOG CPLEX Optimization Studio" (from the "Software" category, may need to allow pop-ups):
   1. Select the "HTTP" method for download.
   2. Check the checkbox for package "IBM ILOG CPLEX Optimization Studio V22.1.0 for Linux x86-64".
   3. Agree to the license agreement below the list of items.
   4. Use the download button that just appeared to download file `cplex_studio2210.linux_x86_64.bin`.
2. Transfer the downloaded file into the VM; if needed, make it executable, and run it:
   ```
   chmod +x cplex_studio2210.linux_x86_64.bin
   sudo ./cplex_studio2210.linux_x86_64.bin
   ```
   Proceed through the installation, using the default install folder (`/opt/ibm/ILOG/CPLEX_Studio221`).
3. Create a symbolic link to the CPLEX library so that mcsta finds it:
   ```
   cd /home/tacas/mdpmc/tools/Modest
   ln -s /opt/ibm/ILOG/CPLEX_Studio221/cplex/bin/x86-64_linux/libcplex2210.so libcplex2210.so
   ```
4. Test the installation:
   ```
   ./modest mcsta qcomp://brp -E "N=16,MAX=2" --props p1 --alg LinearProgramming --lp-solver CPLEX
   ```
   If successful, the output should report probability 0.0004233334437734178 for property p1.

### Installing HiGHS

HiGHS is currently not distributed with the Modest Toolset due to its large size.
To use HiGHS with mcsta in this artifact, compile the exact version we used for the experiments from source:
1. Run the following commands:
   ```
   cd /home/tacas/mdpmc/tools/Modest
   git clone https://github.com/ERGO-Code/HiGHS.git
   cd HiGHS
   git checkout 2466dbf7213359461a501647b2b40c8569c71756
   mkdir build
   cd build
   cmake ..
   make
   cd ../..
   ln -s HiGHS/build/lib/libhighs.so.1.2.2 libhighs.so
   ```
2. To test the installation, run the following command and verify that the output reports probability 0.0004233334437734178 for property p1:
   ```
   ./modest mcsta qcomp://brp -E "N=16,MAX=2" --props p1 --alg LinearProgramming --lp-solver HiGHS
   ```

### Installing Mosek

1. Request an academic license at https://www.mosek.com/products/academic-licenses/.
   You will receive an email with a license file called mosek.lic.
   Save this file inside folder mdpmc/tools/Modest of the artefact in the VM.
2. Download and unpack Mosek:
   ```
   cd /home/tacas/mdpmc/tools/Modest
   wget https://download.mosek.com/stable/10.0.34/mosektoolslinux64x86.tar.bz2
   tar -xf mosektoolslinux64x86.tar.bz2
	 ln -s mosek/10.0/tools/platform/linux64x86/bin/libmosekxx10_0.so libmosekxx10_0.so
   ```
3. Copy the license file to a location where Mosek can find it:
   ```
   mkdir /home/tacas/mosek
	 cp mosek.lic /home/tacas/mosek/
   ```
4. Test the installation:
   ```
   ./modest mcsta qcomp://brp -E "N=16,MAX=2" --props p1 --alg LinearProgramming --lp-solver Mosek
   ```
   If successful, the output should report probability 0.0004233334437735165 for property p1.

## Installation of Storm

Open a terminal window, then

```
cd /home/tacas/mdpmc/tools/
./install.sh.
```

 This automatically installs Storm and its dependencies. Compilation can take some time (up to one hour).

Open a new terminal window once the installation is finished. This is to ensure that the environment variable `$MDPMC_DIR` is set to the location of the `mdpmc` directory.

The artifact includes a pre-build version of `mcsta`, so no additional steps are necessary.

Remark: For technical reasons, we did not include pre-build binaries for `storm` as those would depend on the availability of Gurobi and/or SoPlex.

## Quick Check

To quickly check if the installation of Storm, mcsta, and the LP solvers work as expected, open a terminal window, then

```
cd  /home/tacas/mdpmc/quickcheck/
python3 ../scripts/run.py quick.json
```

This executes all 57 exercised configurations on a small benchmark instance. This should take one or two minutes.
Afterwards, run 

```
python3 ../scripts/postprocess_quickcheck.py logs/
```

to check which configurations are working properly.
Configurations involving unavailbe LP solvers (see above) are expected to fail.
The file `mdpmc/configurations.pdf` lists all available configurations and the directory `mdpmc/quickcheck/logs` contains detailed logs.

## Reviewing our Experiments

The directory `mdpmc/original/` contains logfiles and derived data (i.e. `.csv` files for quantile and scatter plots and detailed result tables) of our experiments from the paper.
The derived data has already been generated from the logs via `python3 ../scripts/postprocess.py logs/`.
The subdirectory `plots` contains a latex file `plots.tex` and the compiled document `plots.pdf` which contains all the plots from the paper.
Opening the file `mdpmc/original/qvbs-full/table/table.html` in a web browser shows an interactive result table where each cell shows the model checking time of a configuration (column) on a benchmark instance (row). Clicking on a cell opens a page showing the precise command and the corresponding logfile.
The shown command can be copied into the terminal to run the corresponding experiment in the artefact VM.
The result tables for the other benchmark sets (`qvbs-hard` and `premise`) are similar.

## Replicating the Experiments

Besides the above-mentioned replication of individual experiments, we also provide means to automatically run *all* experiments (which roughly takes 120 days) or an appropriate subset of the experiments (which finishes in 3-4 hours).
To this end, open a terminal window, `cd` into `mdpmc/replication/`, and execute either

- `python3 ../scripts/run.py all.json` or
- `python3 ../scripts/run.py subset.json`.

After execution is finished, run `python3 ../scripts.postprocess.py logs/` to process the log files and generate the derived data, similar to the data in the directory `mdpmc/original/`.
Assuming that `pdflatex` is available, `cd plots/; pdflatex plots.tex` generates the document `plots.pdf` which can be compared with the paper.
For space reasons, we did not include a LaTeX distribution in the artefact. One can copy the `replication` directory back to the host system for this step.
Alternatively, one can install `pdflatex` inside the VM by enabling the Internet connection and running `sudo apt-get install texlive-latex-extra`

The subset considers exactly the invocations relevant for Figure 6 (b) and (c) as well as Figure 7 from the paper. However, the time limit was set to 60 seconds to ensure that running the subset finishes in reasonable time. The file /mdpmc/replication/plots/plots-subset-expected.pdf shows what we obtained when running the subset in a VM (with 6 enabled cores and 24 GB RAM available). Keep in mind that we measure the model *checking* time (excluding time for model construction) while the time limit applies to the entire tool invocation.

It is also possible to run a custom subset by running `python3 ../scripts/run.py` when in the `mdpmc/replication/` directory.

To replicate the information presented in Table 1, run `./hmmdp.sh` in the `mdpmc` directory. It step-by-step executes the commands needed to obtain the outcomes presented in Table 1. 
When the corresponding LP solver is not installed, the corresponding commands will fail. See *Installation of LP Solvers*.
