#!/bin/bash

# Stop on error
set -e

# cd to the directory where the script lies in
cd "$( dirname "${BASH_SOURCE[0]}" )"


# Run the HMMDP model with different settings
cd tools/Modest
echo "Running the haddad-monmege-mdp model with different solvers and settings."
echo "Some of them will produce wrong results. The correct results are:"
echo "* 1/3 (0.333...) for PMinGoal"
echo "* 2/3 (0.666...) for PMaxGoal"

# mcsta

echo 
read -rsp $'Press enter to run mcsta with VI for N=19 (very rough underapproximation, for comparison)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=19" --alg ValueIteration

echo 
read -rsp $'Press enter to run mcsta with II for N=19 (for comparison)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=19" --alg IntervalIteration

echo 
read -rsp $'Press enter to run mcsta with LP using COPT for N=18 (correct results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=18" --alg LinearProgramming --lp-solver Copt
echo 
read -rsp $'Press enter to run mcsta with LP using COPT for N=19 (wrong results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=19" --alg LinearProgramming --lp-solver Copt

echo 
read -rsp $'Press enter to run mcsta with LP using CPLEX for N=18 (correct results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=18" --alg LinearProgramming --lp-solver CPLEX
echo 
read -rsp $'Press enter to run mcsta with LP using CPLEX for N=19 (wrong results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=19" --alg LinearProgramming --lp-solver CPLEX

echo 
read -rsp $'Press enter to run mcsta with LP using Glop for N=25 (correct results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=25" --alg LinearProgramming --lp-solver Glop
echo 
read -rsp $'Press enter to run mcsta with LP using Glop for N=26 (wrong result for PMaxGoal)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=26" --alg LinearProgramming --lp-solver Glop
echo 
read -rsp $'Press enter to run mcsta with LP using Glop for N=29 (wrong result for PMaxGoal)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=29" --alg LinearProgramming --lp-solver Glop
echo 
read -rsp $'Press enter to run mcsta with LP using Glop for N=30 (failure for PMinGoal, wrong result for PMaxGoal)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=30" --alg LinearProgramming --lp-solver Glop

echo 
read -rsp $'Press enter to run mcsta with LP using Gurobi for N=18 (correct results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=18" --alg LinearProgramming --lp-solver Gurobi
echo 
read -rsp $'Press enter to run mcsta with LP using Gurobi for N=19 (wrong results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=19" --alg LinearProgramming --lp-solver Gurobi

echo 
read -rsp $'Press enter to run mcsta with LP using HiGHS for N=22 (correct results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=22" --alg LinearProgramming --lp-solver HiGHS
echo 
read -rsp $'Press enter to run mcsta with LP using HiGHS for N=23 (wrong results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=23" --alg LinearProgramming --lp-solver HiGHS

echo 
read -rsp $'Press enter to run mcsta with LP using lp_solve for N=28 (correct results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=28" --alg LinearProgramming --lp-solver LPSolve
echo 
read -rsp $'Press enter to run mcsta with LP using lp_solve for N=29 (wrong results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=29" --alg LinearProgramming --lp-solver LPSolve

echo 
read -rsp $'Press enter to run mcsta with LP using Mosek for N=22 (correct results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=22" --alg LinearProgramming --lp-solver Mosek
echo 
read -rsp $'Press enter to run mcsta with LP using Mosek for N=23 (wrong results)...\n'
./modest mcsta hmmdp.modest -S Memory --unsafe -D -E "N=23" --alg LinearProgramming --lp-solver Mosek

# Storm

echo 
read -rsp $'Press enter to run Storm with LP using GLPK for N=24 (correct results)...\n'
../storm/build/bin/storm --jani hmmdp.jani --janiproperty -const N=24 --minmax:method lp --lpsolver glpk
echo 
read -rsp $'Press enter to run Storm with LP using GLPK for N=25 (wrong result for PMaxGoal)...\n'
../storm/build/bin/storm --jani hmmdp.jani --janiproperty -const N=25 --minmax:method lp --lpsolver glpk
echo 
read -rsp $'Press enter to run Storm with LP using GLPK for N=51 (wrong result for PMaxGoal)...\n'
../storm/build/bin/storm --jani hmmdp.jani --janiproperty -const N=51 --minmax:method lp --lpsolver glpk
echo 
read -rsp $'Press enter to run Storm with LP using GLPK for N=52 (failure for PMinGoal, wrong result for PMaxGoal)...\n'
../storm/build/bin/storm --jani hmmdp.jani --janiproperty -const N=52 --minmax:method lp --lpsolver glpk

echo 
read -rsp $'Press enter to run Storm with LP using SoPlex for N=34 (correct results)...\n'
../storm/build/bin/storm --jani hmmdp.jani --janiproperty -const N=34 --minmax:method lp --lpsolver soplex
echo 
read -rsp $'Press enter to run Storm with LP using SoPlex for N=35 (wrong results)...\n'
../storm/build/bin/storm --jani hmmdp.jani --janiproperty -const N=35 --minmax:method lp --lpsolver soplex

echo 
read -rsp $'Press enter to run Storm with PI for N=20 (correct results)...\n'
../storm/build/bin/storm --jani hmmdp.jani --janiproperty -const N=20 --minmax:method pi
echo 
read -rsp $'Press enter to run Storm with PI for N=21 (wrong results)...\n'
../storm/build/bin/storm --jani hmmdp.jani --janiproperty -const N=21 --minmax:method pi

echo
echo Done!
