Our scripts expect the following binaries to exist in this directory:

- `./Modest/modest`
- `./storm/build/bin/storm`

These can also be symlinked here like this (replace with your paths accordingly):

```
ln -s /opt/modest/ /opt/mdpmc/tools/Modest
ln -s /opt/storm /opt/mdpmc/tools/storm
```



### OLD


## Installation of LP Solvers (optional)

Our experiments consider various LP solvers. For some solvers, the license prohibits their inclusion in this artifact. Those solvers can be installed assuming an appropriate license and an Internet connection (to activate/obtain the licenses). All solvers are free for academic users. Our instructions below assume an academic user.
It is also possible to evaluate the artifact without installing any commercial solver. Experiments involving those solvers then cannot be replicated.
We recommend to (at least) install Gurobi and SoPlex as they are used frequently.

Before installing any of the LP solvers, the internet connection needs to be enabled. In VirtualBox this is done by enabling the checkbox at `Settings > Network > Adapter 1 > Enable Network Adapter`. The virtual machine has to be powered off for this.
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
   Save this file inside folder mdpmc/tools/Modest of the artifact in the VM.
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
