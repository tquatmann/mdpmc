from .benchmark import Benchmark
from .invocation import Invocation
from .execution import *
from .configuration import *

def get_name():
    """ should return the name of the tool """
    return "Storm"

# This token can be used in a configuration command and will be replaced by some (integer) seed value (allowing to determinize random executions)
RANDOM_SEED_TOKEN = "<%SEED%>"

def test_installation(settings, configuration = None):
    """
    Performs a quick check to test wether the installation works. 
    Returns an error message if something went wrong and 'None' otherwise.
    """
    storm_executable = set_mdpmc_dir(os.path.join(settings.storm_binary_dir(), "storm"))
    if not os.path.exists(storm_executable):
         return "Binary '{}' does not exist.".format(storm_executable)    
    command_line = storm_executable + " {}".format("" if configuration is None else configuration.command)
    command_line = command_line.replace(RANDOM_SEED_TOKEN, str(get_seed(0)))
    try:
        test_out, test_time, test_code = execute_command_line(command_line, 10)
        if test_code != 0:
            return "Error while executing:\n\t{}\nNon-zero return code: '{}'.".format(command_line, test_code)
    except KeyboardInterrupt:
        return "Error: Execution interrupted."
    except Exception:
        return "Error while executing\n\t{}\n".format(command_line)

    
def is_benchmark_supported(benchmark : Benchmark, configuration : Configuration):
    """ Auxiliary function that returns True if the provided benchmark is not supported by Storm and no known external conversion tool can help."""
    # Storm does not support CTMCs with infinite state-spaces
    if benchmark.is_prism_inf() and benchmark.is_ctmc():
        return False
    return True

def get_configurations():
    cfgs = []

    # VI-based
    cfgs.append(Configuration(id="vi-mono", note="Classical VI", command="--minmax:method vi "))
    cfgs.append(Configuration(id="vi-mono-mecq", note="Classical VI, always collapses mecs", command="--minmax:method vi --force-require-unique"))
    cfgs.append(Configuration(id="vi-topo", note="Classical VI, topological solving", command="--minmax:method topological --topological:minmax vi "))
    cfgs.append(Configuration(id="vi-topo-mecq", note="Classical VI, topological solving, always collapse mecs", command="--minmax:method topological --topological:minmax vi --force-require-unique"))
    cfgs.append(Configuration(id="ovi-mono", note="Optimistic VI, always collapses mecs", command="--minmax:method ovi  --sound"))
    cfgs.append(Configuration(id="ovi-topo", note="Optimistic VI, topological solving, always collapses mecs", command="--minmax:method topological --topological:minmax ovi  --sound"))
    cfgs.append(Configuration(id="svi-mono", note="Sound VI, always collapses mecs", command="--minmax:method svi  --sound"))
    cfgs.append(Configuration(id="svi-topo", note="Sound VI, topological solving, always collapses mecs", command="--minmax:method topological --topological:minmax svi  --sound"))
    cfgs.append(Configuration(id="ii-mono", note="II, always collapses mecs", command="--minmax:method ii  --sound"))
    cfgs.append(Configuration(id="ii-topo", note="II, topological solving, always collapses mecs", command="--minmax:method topological --topological:minmax ii  --sound"))
    cfgs.append(Configuration(id="rs-topo-mecq-exact", note="RationalSearch (exact), topological solving, mec quotient", command="--minmax:method topological --topological:minmax rs --force-require-unique  --exact"))
    cfgs.append(Configuration(id="rs-mono-mecq-exact", note="RationalSearch (exact), mec quotient", command="--minmax:method rs --force-require-unique  --exact"))

    # PI-based
    cfgs.append(Configuration(id="pi-mono-gmres", note="PI with gmres as LinEqSolver,", command="--minmax:method pi --eqsolver gmm++"))
    cfgs.append(Configuration(id="pi-mono-gmres-diagprecond", note="PI with gmres as LinEqSolver, diagonal preconditioner,", command="--minmax:method pi --eqsolver gmm++ --gmm++:precond diagonal"))
    cfgs.append(Configuration(id="pi-mono-gmres-noprecond", note="PI with gmres as LinEqSolver, no preconditioner,", command="--minmax:method pi --eqsolver gmm++ --gmm++:precond none"))
    cfgs.append(Configuration(id="pi-mono-gmres-bicgstab", note="PI with bicgstab as LinEqSolver,", command="--minmax:method pi --eqsolver gmm++ --gmm++:method bicgstab"))
    cfgs.append(Configuration(id="pi-mono-gmres-qmr", note="PI with qmr as LinEqSolver,", command="--minmax:method pi --eqsolver gmm++ --gmm++:method qmr"))
    cfgs.append(Configuration(id="pi-mono-gmres-topo", note="PI with gmres (topological) as LinEqSolver,", command="--minmax:method pi --eqsolver topological --topological:eqsolver gmm++"))
    # cfgs.append(Configuration(id="pi-mono-mecq-gmres", note="PI with gmres as LinEqSolver, always collapses mecs", command="--minmax:method pi --force-require-unique"))
    cfgs.append(Configuration(id="pi-topo-gmres", note="PI with gmres as LinEqSolver, topological solving", command="--minmax:method topological --topological:minmax pi"))
    cfgs.append(Configuration(id="pi-topo-gmres-mono", note="PI (topological) with gmres as LinEqSolver (non-topo)", command="--minmax:method topological --topological:minmax pi --eqsolver gmm++"))
    # cfgs.append(Configuration(id="pi-topo-mecq-gmres", note="PI with gmres as LinEqSolver, topological solving, always collapses mecs", command="--minmax:method topological --topological:minmax pi --force-require-unique"))
    cfgs.append(Configuration(id="pi-mono-exactlu", note="PI with LU as LinEqSolver (exact)", command="--minmax:method pi --eqsolver eigen --exact"))
    cfgs.append(Configuration(id="pi-mono-exactlu-topo", note="PI (non-topo) with LU as LinEqSolver (exact) (topo)", command="--minmax:method pi --eqsolver topological --topological:eqsolver eigen --exact"))
    cfgs.append(Configuration(id="pi-topo-exactlu", note="PI with LU as LinEqSolver (exact), topological solving", command="--minmax:method topological --topological:minmax pi --exact"))
    cfgs.append(Configuration(id="pi-topo-exactlu-mono", note="PI (topological) with LU as LinEqSolver (exact, non-topo)", command="--minmax:method topological --topological:minmax pi --eqsolver eigen --exact"))
    cfgs.append(Configuration(id="pi-mono-lu", note="PI with LU as LinEqSolver,", command="--minmax:method pi --eqsolver eigen --eigen:method sparselu"))
    cfgs.append(Configuration(id="pi-topo-lu", note="PI with LU as LinEqSolver, topological solving", command="--minmax:method topological --topological:minmax pi --topological:eqsolver eigen --eigen:method sparselu"))
    cfgs.append(Configuration(id="pi-mono-ovi", note="PI with OVI as LinEqSolver,", command="--minmax:method pi  --eqsolver native --native:method ovi --sound"))
    cfgs.append(Configuration(id="pi-topo-ovi", note="PI with OVI as LinEqSolver, topological solving", command="--minmax:method topological --topological:minmax pi  --topological:eqsolver native --native:method ovi --sound"))
    cfgs.append(Configuration(id="pi-mono-vi", note="PI with VI as LinEqSolver,", command="--minmax:method pi  --eqsolver native --native:method power"))
    cfgs.append(Configuration(id="pi-topo-vi", note="PI with VI as LinEqSolver, topological solving", command="--minmax:method topological --topological:minmax pi  --topological:eqsolver native --native:method power"))
    cfgs.append(Configuration(id="vi2pi-mono-gmres", note="PI with gmres as LinEqSolver using VI warm-start", command="--minmax:method vi-to-pi --eqsolver gmm++"))
    cfgs.append(Configuration(id="vi2pi-mono-exactlu", note="PI with LU as LinEqSolver (exact) using VI warm-start", command="--minmax:method vi-to-pi --eqsolver eigen --exact"))
    cfgs.append(Configuration(id="vi2pi-topo-gmres", note="PI with gmres as LinEqSolver using VI warm-start, topological solving", command="--minmax:method topological --topological:minmax vi-to-pi"))
    cfgs.append(Configuration(id="vi2pi-topo-exactlu", note="PI with LU as LinEqSolver (exact) using VI warm-start, topological solving", command="--minmax:method topological --topological:minmax vi-to-pi --exact"))
    cfgs.append(Configuration(id="vi2pi-topo-gmres-mono", note="PI (topological) with gmres as LinEqSolver (non-topo) using VI warm-start", command="--minmax:method topological --topological:minmax vi-to-pi --eqsolver gmm++"))
    cfgs.append(Configuration(id="vi2pi-topo-exactlu-mono", note="PI (topological) with LU as LinEqSolver (exact, non-topo) using VI warm-start", command="--minmax:method topological --topological:minmax vi-to-pi --eqsolver eigen --exact"))
    cfgs.append(Configuration(id="vi2pi-mono-exactlu-topo", note="PI (non-topo) with LU as LinEqSolver (exact) (topo) using VI warm-start", command="--minmax:method vi-to-pi --eqsolver topological --topological:eqsolver eigen --exact"))

    # LP-based (gurobi)
    cfgs.append(Configuration(id="lp-mono-gurobi", note="LP using Gurobi (1 thread), non-topological solving", command="--minmax:method lp --lpsolver gurobi"))

    cfgs.append(Configuration(id="lp-mono-gurobi-4auto", note="LP with non-triv bounds using gurobi (4 threads)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --gurobi:method auto"))
    cfgs.append(Configuration(id="lp-mono-gurobi-4barrier", note="LP using gurobi (4 threads, barrier)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --gurobi:method barrier "))
    cfgs.append(Configuration(id="lp-mono-gurobi-4dualsimpl", note="LP using gurobi (4 threads, dualsimpl)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --gurobi:method dual-simplex "))
    cfgs.append(Configuration(id="lp-mono-gurobi-4primalsimpl", note="LP using gurobi (4 threads, primalsimpl)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --gurobi:method primal-simplex "))
    cfgs.append(Configuration(id="lp-gurobi-8auto", note="LP using gurobi (8 threads)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 8 --gurobi:method auto"))
    cfgs.append(Configuration(id="lp-gurobi-16auto", note="LP using gurobi (16 threads)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 16 --gurobi:method auto"))

    cfgs.append(Configuration(id="lp-gurobi95-1auto", note="LP using gurobi 9.5 (1 thread)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 1 --gurobi:method auto"))
    cfgs.append(Configuration(id="lp-gurobi95-4auto", note="LP using gurobi 9.5 (4 threads)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --gurobi:method auto"))
    cfgs.append(Configuration(id="lp-gurobi95-8auto", note="LP using gurobi 9.5 (8 threads)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 8 --gurobi:method auto"))
    cfgs.append(Configuration(id="lp-gurobi95-16auto", note="LP using gurobi 9.5 (16 threads)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 16 --gurobi:method auto"))

    cfgs.append(Configuration(id="lp-mono-gurobi-4autoeq", note="LP using gurobi (4 threads), eq. constr", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4  --minmax:lp-eq-unique-actions"))
    cfgs.append(Configuration(id="lp-mono-gurobi-4autoinit", note="LP using gurobi (4 threads), init opt. ", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4  --minmax:lp-objective-type onlyinitial"))
    cfgs.append(Configuration(id="lp-mono-gurobi-4autobnds", note="LP using gurobi (4 threads), nontriv bnds", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --minmax:lp-use-nontrivial-bounds"))
    cfgs.append(Configuration(id="lp-mono-gurobi-4autoinitbnds", note="LP using gurobi (4 threads), init opt., nontriv bnds", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --minmax:lp-objective-type onlyinitial --minmax:lp-use-nontrivial-bounds"))
    cfgs.append(Configuration(id="lp-topo-gurobi-4auto", note="LP using gurobi (4 threads), topol, eq. constr", command="--minmax:method topological --topological:minmax lp  --lpsolver gurobi --gurobi:threads 4"))
    cfgs.append(Configuration(id="lp-topo-gurobi-4autoeq", note="LP using gurobi (4 threads), topol, eq. constr", command="--minmax:method topological --topological:minmax lp  --lpsolver gurobi --gurobi:threads 4 --minmax:lp-eq-unique-actions"))
    cfgs.append(Configuration(id="lp-topo-gurobi-4autoinit", note="LP using gurobi (4 threads), topol, init opt. ", command="--minmax:method topological --topological:minmax lp  --lpsolver gurobi --gurobi:threads 4 --minmax:lp-objective-type onlyinitial --topological:relevant-values"))
    cfgs.append(Configuration(id="lp-topo-gurobi-4autobnds", note="LP using gurobi (4 threads), topol, nontriv bnds", command="--minmax:method topological --topological:minmax lp  --lpsolver gurobi --gurobi:threads 4 --minmax:lp-use-nontrivial-bounds"))
    cfgs.append(Configuration(id="lp-topo-gurobi-4autoinitbnds", note="LP using gurobi (4 threads), topol, init opt., nontriv bnds", command="--minmax:method topological --topological:minmax lp  --lpsolver gurobi --gurobi:threads 4 --minmax:lp-objective-type onlyinitial --topological:relevant-values --minmax:lp-use-nontrivial-bounds"))

    cfgs.append(Configuration(id="lp-topo-gurobi", note="LP using Gurobi (1 thread), topological solving", command="--minmax:method topological --topological:minmax lp --lpsolver gurobi"))
    cfgs.append(Configuration(id="lp-topo-mecq-gurobi", note="LP using Gurobi (1 thread), topological solving, always eliminate end components", command="--minmax:method topological --topological:minmax lp --lpsolver gurobi --force-require-unique"))
    cfgs.append(Configuration(id="lp-topo-mecq-gurobi-4auto", note="LP using Gurobi (4 threads), topological solving, always eliminate end components", command="--minmax:method topological --topological:minmax lp --lpsolver gurobi --gurobi:threads 4 --force-require-unique"))
    cfgs.append(Configuration(id="lp-mono-mecq-gurobi-4auto", note="LP using Gurobi (4 threads), non-topol., always eliminate end components", command="--minmax:method lp --lpsolver gurobi --gurobi:threads 4 --force-require-unique"))

    cfgs.append(Configuration(id="vi2lp-topo-gurobi", note="LP with VI warm-start using Gurobi (1 thread), topological solving", command="--minmax:method topological --topological:minmax vi-to-lp --lpsolver gurobi"))
    cfgs.append(Configuration(id="vi2lp-mono-gurobi", note="LP with VI warm-start using Gurobi (1 thread)", command="--minmax:method vi-to-lp --lpsolver gurobi"))

    cfgs.append(Configuration(id="vi2lp-topo-gurobi-4auto", note="LP with VI warm-start using Gurobi (4 threads), topological solving", command="--minmax:method topological --topological:minmax vi-to-lp --lpsolver gurobi --gurobi:threads 4"))
    cfgs.append(Configuration(id="vi2lp-topo-mecq-gurobi-4auto", note="LP with VI warm-start using Gurobi (4 threads), topological solving, mecq", command="--minmax:method topological --topological:minmax vi-to-lp --lpsolver gurobi --gurobi:threads 4 --force-require-unique"))
    cfgs.append(Configuration(id="vi2lp-mono-gurobi-4auto", note="LP with VI warm-start using Gurobi (4 threads)", command="--minmax:method vi-to-lp --lpsolver gurobi --gurobi:threads 4"))
    cfgs.append(Configuration(id="vi2lp-mono-mecq-gurobi-4auto", note="LP with VI warm-start using Gurobi (4 threads), mecq", command="--minmax:method vi-to-lp --lpsolver gurobi --gurobi:threads 4 --force-require-unique"))


    # LP-based (other)
    cfgs.append(Configuration(id="lp-mono-soplex-exact", note="LP using soplex (exact)", command="--minmax:method lp --lpsolver soplex --exact "))
    cfgs.append(Configuration(id="lp-mono-soplex", note="LP using soplex", command="--minmax:method lp --lpsolver soplex"))
    cfgs.append(Configuration(id="lp-mono-glpk", note="LP using glpk", command="--minmax:method lp --lpsolver glpk"))
    cfgs.append(Configuration(id="lp-mono-z3-exact", note="LP using z3 (exact)", command="--minmax:method lp --lpsolver z3 --exact"))
    cfgs.append(Configuration(id="vi2lp-mono-soplex-exact", note="LP with VI warm-start using soplex (exact)", command="--minmax:method vi-to-lp --lpsolver soplex --exact "))
    cfgs.append(Configuration(id="lp-topo-soplex-exact", note="LP using soplex (exact), topological solving", command="--minmax:method  topological --topological:minmax lp --lpsolver soplex --exact "))
    cfgs.append(Configuration(id="lp-topo-soplex", note="LP using soplex, topological solving", command="--minmax:method  topological --topological:minmax lp --lpsolver soplex"))
    cfgs.append(Configuration(id="lp-topo-glpk", note="LP using glpk, topological solving", command="--minmax:method  topological --topological:minmax lp --lpsolver glpk"))
    cfgs.append(Configuration(id="lp-topo-z3-exact", note="LP using z3 (exact), topological solving", command="--minmax:method  topological --topological:minmax lp --lpsolver z3 --exact"))
    cfgs.append(Configuration(id="vi2lp-topo-soplex-exact", note="LP with VI warm-start using soplex (exact), topological solving", command="--minmax:method  topological --topological:minmax vi-to-lp --lpsolver soplex --exact "))
    cfgs.append(Configuration(id="vi2lp-topo-mecq-soplex-exact", note="LP with VI warm-start using soplex (exact), topological solving, mecq", command="--minmax:method  topological --topological:minmax vi-to-lp --lpsolver soplex --exact --force-require-unique"))

    # bisimulation
    # cfgs.append(Configuration(id="vi-mono-bisim-expl", note="Classical VI, expl bisim", command="--minmax:method vi --bisimulation"))
    # cfgs.append(Configuration(id="vi-mono-bisim-cudd", note="Classical VI, symb bisim with cudd", command="--minmax:method vi --engine dd-to-sparse --bisimulation --ddlib cudd --cudd:maxmem 8192"))
    cfgs.append(Configuration(id="vi-mono-bisim-sylvan1", note="Classical VI, symb bisim with sylvan (1 thread)", command="--minmax:method vi --engine dd-to-sparse --bisimulation --ddlib sylvan --sylvan:threads 1 --sylvan:maxmem 8192"))
    # cfgs.append(Configuration(id="vi-mono-bisim-sylvan4", note="Classical VI, symb bisim with sylvan (4 threads)", command="--minmax:method vi --engine dd-to-sparse --bisimulation --ddlib sylvan --sylvan:threads 4 --sylvan:maxmem 8192"))
    # cfgs.append(Configuration(id="vi2pi-topo-exactlu-bisim-expl", note="PI (topol) with LU as LinEqSolver (exact) using VI warm, expl bisim", command="--minmax:method topological --topological:minmax vi-to-pi --exact --bisimulation"))
    cfgs.append(Configuration(id="vi2pi-topo-exactlu-bisim-sylvan1", note="PI (topol) with LU as LinEqSolver (exact) using VI warm, symb bisim 1th", command="--minmax:method topological --topological:minmax vi-to-pi --exact --engine dd-to-sparse --bisimulation --sylvan:threads 1 --sylvan:maxmem 8192"))
    # cfgs.append(Configuration(id="vi2pi-topo-exactlu-bisim-sylvan4", note="PI (topol) with LU as LinEqSolver (exact) using VI warm, symb bisim 4th", command="--minmax:method topological --topological:minmax vi-to-pi --exact --engine dd-to-sparse --bisimulation --sylvan:threads 4 --sylvan:maxmem 8192"))

    # state permutation
    cfgs.append(Configuration(id="vi-mono-bfs", note="Classical VI, bfs state order", command="--minmax:method vi --permute bfs"))
    cfgs.append(Configuration(id="vi-mono-reversebfs", note="Classical VI, reverse bfs state order", command="--minmax:method vi --permute reverse-bfs"))
    cfgs.append(Configuration(id="vi-mono-rnd", note="Classical VI, random state order", command="--minmax:method vi --permute random {}".format(RANDOM_SEED_TOKEN)))
    cfgs.append(Configuration(id="pi-mono-bfs", note="PI gmres, bfs state order", command="--minmax:method pi --permute bfs"))
    cfgs.append(Configuration(id="pi-mono-reversebfs", note="PI gmres, reverse bfs state order", command="--minmax:method pi --permute reverse-bfs"))
    cfgs.append(Configuration(id="pi-mono-rnd", note="PI gmres, random state order", command="--minmax:method pi --permute random {}".format(RANDOM_SEED_TOKEN)))
    cfgs.append(Configuration(id="lp-mono-bfs", note="PI gmres, bfs state order", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --permute bfs"))
    cfgs.append(Configuration(id="lp-mono-reversebfs", note="PI gmres, reverse bfs state order", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --permute reverse-bfs"))
    cfgs.append(Configuration(id="lp-mono-rnd", note="PI gmres, random state order", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --permute random {}".format(RANDOM_SEED_TOKEN)))


# cfgs.append(Configuration(id="lp", note="LP with non-triv bounds using gurobi (1 thread)", command="--minmax:method lp  --lpsolver gurobi --minmax:lp-use-nontrivial-bounds"))
    # cfgs.append(Configuration(id="lp-glpk-nobnds", note="LP using glpk", command="--minmax:method lp  --lpsolver glpk"))
    # cfgs.append(Configuration(id="lp-gurobi-16autonobnds", note="LP using gurobi (16 threads)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 16 "))
    # cfgs.append(Configuration(id="lp-gurobi-4auto", note="LP with non-triv bounds using gurobi (4 threads)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4  --minmax:lp-use-nontrivial-bounds "))
    # cfgs.append(Configuration(id="lp-gurobi-4autoeq", note="LP with non-triv bounds using gurobi (4 threads), eq. constr", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4  --minmax:lp-eq-unique-actions --minmax:lp-use-nontrivial-bounds "))
    # cfgs.append(Configuration(id="lp-gurobi-4autoinit", note="LP with non-triv bounds using gurobi (4 threads), init opt. ", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4  --minmax:lp-objective-type onlyinitial --topological:relevant-values --minmax:lp-use-nontrivial-bounds "))
    # cfgs.append(Configuration(id="lp-gurobi-4autoiniteq", note="LP with non-triv bounds using gurobi (4 threads), init opt., eq. constr", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4  --minmax:lp-objective-type onlyinitial --topological:relevant-values --minmax:lp-eq-unique-actions --minmax:lp-use-nontrivial-bounds "))
    # cfgs.append(Configuration(id="lp-gurobi-4autonobnds", note="LP using gurobi (4 threads)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 "))
    # cfgs.append(Configuration(id="lp-gurobi-4barriernobnds", note="LP using gurobi (4 threads, barrier)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --gurobi:method barrier "))
    # cfgs.append(Configuration(id="lp-gurobi-4dualsimplnobnds", note="LP using gurobi (4 threads, dualsimpl)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --gurobi:method dual-simplex "))
    # cfgs.append(Configuration(id="lp-gurobi-4primalsimplnobnds", note="LP using gurobi (4 threads, primalsimpl)", command="--minmax:method lp  --lpsolver gurobi --gurobi:threads 4 --gurobi:method primal-simplex "))
    # cfgs.append(Configuration(id="lp-mecq", note="LP with non-triv bounds using Gurobi, MEC Quotient", command="--minmax:method lp --force-require-unique  --lpsolver gurobi --minmax:lp-use-nontrivial-bounds"))
    # cfgs.append(Configuration(id="lp-mecq-topo", note="LP with non-triv bounds using Gurobi, topological solving, MEC Quotient", command="--minmax:method topological --topological:minmax lp --force-require-unique  --lpsolver gurobi --minmax:lp-use-nontrivial-bounds"))
    # cfgs.append(Configuration(id="lp-mecq-topo-glpk", note="LP with non-triv bounds using glpk, topological solving, MEC Quotient", command="--minmax:method topological --topological:minmax lp --force-require-unique  --lpsolver glpk --minmax:lp-use-nontrivial-bounds "))
    # cfgs.append(Configuration(id="lp-mecq-topo-gurobi-4auto", note="LP with non-triv bounds using gurobi (4 threads), topological solving, MEC Quotient", command="--minmax:method topological --topological:minmax lp --force-require-unique  --lpsolver gurobi --gurobi:threads 4  --minmax:lp-use-nontrivial-bounds "))
    # cfgs.append(Configuration(id="lp-mecq-topo-soplex", note="LP with non-triv bounds using soplex (inexact), topological solving, MEC Quotient", command="--minmax:method topological --topological:minmax lp --force-require-unique  --lpsolver soplex --minmax:lp-use-nontrivial-bounds "))
    # cfgs.append(Configuration(id="lp-mecq-topo-soplex-exact", note="LP with non-triv bounds using soplex (exact), topological solving, MEC Quotient", command="--minmax:method topological --topological:minmax lp --force-require-unique  --lpsolver soplex --exact  --minmax:lp-use-nontrivial-bounds "))
    # cfgs.append(Configuration(id="lp-mecq-topo-z3-exact", note="LP with non-triv bounds using z3 (exact), topological solving, MEC Quotient", command="--minmax:method topological --topological:minmax lp --force-require-unique  --lpsolver z3 --exact  --minmax:lp-use-nontrivial-bounds "))
    # cfgs.append(Configuration(id="lp-nobnds", note="LP using Gurobi (1 thread)", command="--minmax:method lp  --lpsolver gurobi"))
    # cfgs.append(Configuration(id="lp-soplex-exactnobnds", note="LP using soplex (exact)", command="--minmax:method lp  --lpsolver soplex --exact "))
    # cfgs.append(Configuration(id="lp-soplex-nobnds", note="LP using soplex (inexact)", command="--minmax:method lp  --lpsolver soplex"))
    # cfgs.append(Configuration(id="lp-topo", note="LP with non-triv bounds using gurobi (1 thread), topological solving", command="--minmax:method topological --topological:minmax lp  --lpsolver gurobi --minmax:lp-use-nontrivial-bounds"))
    # cfgs.append(Configuration(id="lp-z3-exactnobnds", note="LP using z3 (exact)", command="--minmax:method lp  --lpsolver z3 --exact "))
    # cfgs.append(Configuration(id="ovi-topo", note="Optimistic VI, topological solving", command="--minmax:method topological --topological:minmax ovi  --sound"))
    # cfgs.append(Configuration(id="rs-mecq-topo-exact", note="RationalSearch (exact), topological solving, MEC Quotient", command="--minmax:method topological --topological:minmax rs --force-require-unique  --exact"))
    # cfgs.append(Configuration(id="vi", note="Classical VI", command="--minmax:method vi "))
    # cfgs.append(Configuration(id="vi-mecq", note="Classical VI, MEC Quotient", command="--minmax:method vi --force-require-unique "))
    # cfgs.append(Configuration(id="vi-mecq-topo", note="Classical VI, topological solving, MEC Quotient", command="--minmax:method topological --topological:minmax vi --force-require-unique "))
    # cfgs.append(Configuration(id="vi-topo", note="Classical VI, topological solving", command="--minmax:method topological --topological:minmax vi "))
    # cfgs.append(Configuration(id="vi2lp-mecq-topo-gurobi", note="LP with non-triv bounds and VI warm-start using Gurobi (1 thread), topological solving, MEC Quotient", command="--minmax:method topological --topological:minmax vi-to-lp --lpsolver gurobi --minmax:lp-use-nontrivial-bounds --force-require-unique"))
    # cfgs.append(Configuration(id="vi2lp-mecq-topo-soplex-exact", note="LP with non-triv bounds and VI warm-start using soplex (exact), topological solving, MEC Quotient", command="--minmax:method topological --topological:minmax vi-to-lp --lpsolver soplex --exact --minmax:lp-use-nontrivial-bounds --force-require-unique"))


    return cfgs


def get_invocation(settings, benchmark : Benchmark, configuration : Configuration, run_id : int):
    """
    Returns an invocation that invokes the tool for the given benchmark and the given storm configuration.
    It can be assumed that the current directory is the directory from which execute_invocations.py is executed.
    """
    general_arguments = "--timemem" # Prints some timing and memory information
    
    invocation = Invocation()
    invocation.tool = get_name()
    invocation.configuration_id = configuration.identifier
    invocation.note = configuration.note
    invocation.benchmark_id = benchmark.get_identifier()
    invocation.run_id = run_id
    
    if is_benchmark_supported(benchmark, configuration):
        bdir = benchmark.get_portable_directory()
        storm_executable = os.path.join(settings.storm_binary_dir(), "storm")

        if (benchmark.is_prism() or benchmark.is_prism_ma()) and not benchmark.is_pta():
            benchmark_arguments = "--prism {} --prop {} {}".format(os.path.join(bdir, benchmark.get_prism_program_filename()), os.path.join(bdir, benchmark.get_prism_property_filename()), benchmark.get_property_name())
            if benchmark.get_open_parameter_def_string() != "":
                benchmark_arguments += " --constants {}".format(benchmark.get_open_parameter_def_string())
            if benchmark.is_ctmc():
                benchmark_arguments += " --prismcompat"
                invocation.note += " Use `--prismcompat` to ensure compatibility with prism benchmark."
        elif benchmark.is_drn():
            benchmark_arguments = "--explicit-drn {} --prop {} {}".format(os.path.join(bdir, benchmark.get_drn_filename()), os.path.join(bdir, benchmark.get_drn_property_filename()), benchmark.get_property_name())
            assert(benchmark.get_open_parameter_def_string() == "")
        else:
            # For jani input, it might be the case that preprocessing is necessary using moconv
            janifile = benchmark.get_janifilename()
            par_defs = benchmark.get_open_parameter_def_string()
            moconv_options = []
            if "nondet-selection" in benchmark.get_jani_features():
                moconv_options.append("--remove-disc-nondet")
                invocation.note += " Use moconv to handle currently unsupported jani feature 'nondet-selection'."
            if benchmark.is_pta():
                if benchmark.get_model_short_name() in ["repudiation_honest", "repudiation_malicious", "csma-pta", "csma_abst-pta"]:
                    invocation.note += " Unsupported PTA Benchmark."
                else:
                    moconv_options.append("--digital-clocks")
                    if benchmark.load_jani_file()["type"] == "sta":
                        moconv_options.append(" --unroll-distrs")
                    invocation.note += " Use moconv to convert the PTA to an MDP using digital-clocks semantics."
            if len(moconv_options) != 0:
                janifile_split = os.path.splitext(janifile)
                moconvoutfilename = "converted_{}.{}{}".format(janifile_split[0], par_defs, janifile_split[1])
                moconvoutfile = os.path.join(bdir, moconvoutfilename)
                if par_defs != "":
                    moconv_options.append(" --experiment " + par_defs)
                    par_defs = ""
                if not os.path.isfile(set_mdpmc_dir(moconvoutfile)):
                    moconv_command = "moconv {} {} --output {} --overwrite\n".format(os.path.join(bdir, janifile), " ".join(moconv_options), moconvoutfile)
                    with open("moconv.sh", 'a') as moconvscript :
                        moconvscript.write(moconv_command)
                    print("Required moconv call appended to file 'moconv.sh'")
                janifile = moconvoutfilename
            benchmark_arguments = "--jani {} --janiproperty {}".format(os.path.join(bdir, janifile), benchmark.get_property_name())
            if par_defs != "":
                benchmark_arguments += " --constants " + par_defs
        cfg_cmd = configuration.command.replace(RANDOM_SEED_TOKEN, str(get_seed(run_id)))
        invocation.add_command(storm_executable + " " + benchmark_arguments + " " + cfg_cmd + " " + general_arguments)
    else:
        invocation.note += " Benchmark not supported by Storm."    
    return invocation



def get_result(log, benchmark : Benchmark):
    """
    Parses the tool result
    The returned value should be either 'true', 'false', a decimal number, or a fraction.
    """

    pos = log.find("Model checking property \"{}\":".format(benchmark.get_property_name()))
    if pos < 0:
        return None
    pos = log.find("Result (for initial states): ", pos)
    if pos < 0:
        return None
    pos = pos + len("Result (for initial states): ")
    eol_pos = log.find("\n", pos)
    result = log[pos:eol_pos]
    pos_appr = result.find("(approx. ")
    if pos_appr >= 0:
        result = result[:pos_appr]
    return result
    
def get_MC_Time(logfile):
    """
    Tries to parse the model checking time
    """
    pos = logfile.find("Time for model checking: ")
    if pos >= 0:
        pos += len("Time for model checking: ")
        pos2 = logfile.find("s.", pos)
        num = logfile[pos:pos2]
        return float(num)
    return None

def get_Solve_Time(logfile):
  """
  Tries to parse the solving time of the underlying solution method (model checking time without prob0/1, ... preprocessing)
  """
  pos = logfile.find("Time for model solving: ")
  if pos >= 0:
      pos += len("Time for model solving: ")
      pos2 = logfile.find("s.", pos)
      num = logfile[pos:pos2]
      return float(num)
  return None
    
def get_Build_Time(logfile):
    """
    Tries to parse the model building time
    """
    pos = logfile.find("Time for model construction: ")
    if pos >= 0:
        pos += len("Time for model construction: ")
        pos2 = logfile.find("s.", pos)
        num = logfile[pos:pos2]
        return float(num)
    return None

def get_nontriv_mec_percentage(logfile):
    """
    Tries to parse the percentage of MEC states
    """
    pos1 = logfile.find("are trivial, i.e., consist of a single state. ")
    if pos1 >= 0:
        pos2 = logfile.find("%) are on a non-trivial mec.", pos1)
        pos1 = logfile.rfind("(", pos1, pos2) + 1
        num = logfile[pos1:pos2]
        return float(num)
    return None


def get_Acyclic(logfile):
    """
    Tries to find information whether or not the model is acyclic. Returns None if the information was not found
    """
    if "##Acyclic" in logfile:
        return True
    elif "##Cyclic" in logfile:
        return False
    else:
        return None
    
      
def get_NonTriv_Scc_States(logfile):
    """
    Tries to parse the number of non-trivial scc states from the logfile
    """
    pos = logfile.find("Number of states in non-trivial SCC: ")
    if pos >= 0:
        pos += len("Number of states in non-trivial SCC: ")
        pos2 = logfile.find(".", pos)
        num = logfile[pos:pos2]
        return int(num)
    return None

def is_not_supported(logfile):
    """
    Returns true if the logfile contains error messages that mean that the input is not supported.
    """
    # if one of the following error messages occurs, we are sure that the model is not supported.
    known_messages = []
    known_messages.append("The model type Markov Automaton is not supported by the dd engine.")
    known_messages.append("The model type CTMC is not supported by the dd engine.")
    known_messages.append("Cannot build symbolic model from JANI model whose system composition that refers to the automaton ")
    known_messages.append("Cannot build symbolic model from JANI model whose system composition refers to the automaton ")
    known_messages.append("The symbolic JANI model builder currently does not support assignment levels.")
    known_messages.append("repudiation") # Unsupported PTA benchmark
    known_messages.append("csma_abst") # Unsupported PTA benchmark
    known_messages.append("csma-pta") # Unsupported PTA benchmark
    known_messages.append("rectangle-tireworld.30.jani.gz") # too large jani benchmark
    for m in known_messages:
        if m in logfile:
            return True
            
    return False


def is_expected_error(logfile):
    """
    Returns true if the logfile contains a known error message that is to be expected.
    """
    known_messages = []
    known_messages.append("This version of storm was compiled without support for")
    known_messages.append("Unable to optimize glpk model (5)")
    known_messages.append("Soplex gives up on this problem")
    known_messages.append("Soplex failed")
    known_messages.append("Unable to find optimal solution for MinMax equation system")
    known_messages.append("The MinMax equation system is infeasible")
    for m in known_messages:
        if m in logfile:
            return True
    return False

def is_memout(logfile):
    """
    Returns true if the logfile indicates an out of memory situation.
    Assumes that a result could not be parsed successfully.
    """
    known_messages = []
    known_messages.append("Maximum memory exceeded.")
    known_messages.append("BDD Unique table full")
    known_messages.append("ERROR: The program received signal 11")
    known_messages.append("Unable to optimize Gurobi model (Out of memory, error code 10001).")
    for m in known_messages:
        if m in logfile:
            return True
    # if there is no error message and no result is produced, we assume out of memory.
    return "ERROR" not in logfile
