# Docker-based benchmarking

## Prerequisites
- A host machine with docker installed. If this machine has an ARM64 processor, some things may not work.
- ~12 hours time
- A Gurobi WLS license https://www.gurobi.com/features/web-license-service/

## Steps

1. Load the docker image:
```
docker load -i docker_mdpmc.tar
```
The container is based on an container for the probabilistic model checker as provided by the Storm developers, for details, 
see [this documentation](https://www.stormchecker.org/documentation/obtain-storm/docker.html).

2. Start the docker container in detached mode, while pointing to the Gurobi license:
```
docker run -it -d  --volume=$HOME/gurobi.lic:/opt/gurobi/gurobi.lic  --platform linux/amd64 --workdir /opt/practitioners/hardware-experiment --name benchmarkrunner sjunges/mdpmc /bin/bash
```
3. Test whether the Gurobi license was passed correctly by executing a storm invocation:
```
docker exec -it benchmarkrunner /opt/storm/build/bin/storm --prism /opt/practitioners/qcomp/benchmarks/mdp/random-grid/random-grid.prism --prop "Tmin=? [F x=N&y=N&z=N]"  -const "N=4,pstay=0.1,pover=0.1" --minmax:method lp --lpsolver gurobi
```
The output should contain something along the lines `Set parameter WLSAccessID` and print a result of `9.3` at the end. 

4. Run the benchmarks (in the background). This will take ~12 hours.
```
docker exec -it -d benchmarkrunner python3 ../scripts/run.py inv.json 
```
You may now step away from the machine.
5. Check progress. If you want to see how far the machine is, run:
```
docker exec -it benchmarkrunner ls logs -rt1 |  grep ".log" | wc -l    
```
This counts the number of produced log-files. 
Once the number reaches 480, you can proceed to the next step.
6. Copy the log files to your host
```
docker cp benchmarkrunner:/opt/practitioners/hardware-experiment/logs .
```
7. Manually inspect the log files or follow the instructions from the reproduce archive to generate insightful plots.


