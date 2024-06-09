from internal.benchmark import *
from internal.utility import *
import os




settings = Settings()

def is_considered(benchmark):
    if not any([benchmark.is_mdp(), benchmark.is_ma(), benchmark.is_pta()]): return False
    if not any([benchmark.is_unbounded_probabilistic_reachability(), benchmark.is_unbounded_expected_time(), benchmark.is_unbounded_expected_reward(), benchmark.is_unbounded_expected_steps()]): return False
    if benchmark.is_unbounded_probabilistic_reachability() and benchmark.has_reference_result() and benchmark.get_reference_result() == 1.0: return False
    if benchmark.get_model_short_name() in ["repudiation_malicious", "repudiation_honest"]: return False # not supported by storm
    if benchmark.get_identifier() in [        "dpm.8-6-5.PminQueuesFull",
                                              "dpm.8-8-5.PminQueuesFull",
                                              "dpm.8-6-5.PmaxQueuesFull",
                                              "dpm.8-8-5.PmaxQueuesFull",
                                              "dpm.8-6-5.PminQueue1Full",
                                              "dpm.8-8-5.PminQueue1Full",
                                              "dpm.8-6-5.PmaxQueue1Full",
                                              "dpm.8-8-5.PmaxQueue1Full",
                                              "dpm.8-6-5.TminQueuesFull",
                                              "dpm.8-8-5.TminQueuesFull",
                                              "flexible-manufacturing.21-1.M2Fail_E",
                                              "vgs.4-10000.MaxPrReachFailed",
                                              "vgs.5-10000.MaxPrReachFailed",
                                              "vgs.4-10000.MinExpTimeFailed",
                                              "vgs.5-10000.MinExpTimeFailed",
                                              "beb.5-16-15.LineSeized",
                                              "beb.6-16-15.LineSeized",
                                              "beb.5-16-15.GaveUp",
                                              "beb.6-16-15.GaveUp",
                                              "blocksworld.10.goal",
                                              "blocksworld.14.goal",
                                              "blocksworld.18.goal",
                                              "boxworld.10-5.goal",
                                              "boxworld.10-10.goal",
                                              "boxworld.15-10.goal",
                                              "boxworld.15-15.goal",
                                              "boxworld.20-20.goal",
                                              "consensus.10-2.c1",
                                              "consensus.8-2.c2",
                                              "consensus.10-2.c2",
                                              "consensus.8-2.disagree",
                                              "consensus.10-2.disagree",
                                              "consensus.8-2.steps_max",
                                              "consensus.10-2.steps_max",
                                              "consensus.8-2.steps_min",
                                              "consensus.10-2.steps_min",
                                              "csma.4-4.all_before_max",
                                              "csma.4-6.all_before_max",
                                              "csma.4-4.all_before_min",
                                              "csma.4-6.all_before_min",
                                              "csma.4-4.some_before",
                                              "csma.4-6.some_before",
                                              "csma.4-4.time_max",
                                              "csma.4-6.time_max",
                                              "csma.4-4.time_min",
                                              "csma.4-6.time_min",
                                              "exploding-blocksworld.10.goal",
                                              "exploding-blocksworld.15.goal",
                                              "exploding-blocksworld.17.goal",
                                              "firewire.true-36-800.elected",
                                              "firewire.true-36-600.time_max",
                                              "firewire.true-36-800.time_max",
                                              "firewire.true-36-600.time_min",
                                              "firewire.true-36-800.time_min",
                                              "firewire.true-36-600.time_sending",
                                              "firewire.true-36-800.time_sending",
                                              "firewire_dl.36-200.deadline",
                                              "ij.30.stable",
                                              "ij.40.stable",
                                              "ij.50.stable",
                                              "philosophers-mdp.10.eat",
                                              "philosophers-mdp.20.eat",
                                              "philosophers-mdp.30.eat",
                                              "random-predicates.a.goal",
                                              "random-predicates.b.goal",
                                              "random-predicates.c.goal",
                                              "random-predicates.d.goal",
                                              "rectangle-tireworld.30.goal",
                                              "resource-gathering.1000000-0-0.expsteps",
                                              "triangle-tireworld.441.goal",
                                              "triangle-tireworld.1681.goal",
                                              "triangle-tireworld.3721.goal",
                                              "triangle-tireworld.6561.goal",
                                              "zenotravel.6-5-3.goal",
                                              "zenotravel.10-5-3.goal",
                                              "zenotravel.20-10-6.goal",
                                              "csma-pta.2-4.collisions",
                                              "csma-pta.2-8.collisions",
                                              "csma-pta.4-4.collisions",
                                              "csma-pta.4-8.collisions",
                                              "csma_abst-pta.1-1000.eventually",
                                              "csma_abst-pta.1-1750.eventually",
                                              "csma_abst-pta.1-1800.eventually",
                                              "csma_abst-pta.1-2000.eventually",
                                              "csma_abst-pta.1-3000.eventually",
                                              "firewire-pta.360-2500.eventually",
                                              "firewire-pta.360-5000.eventually",
                                              "firewire-pta.360-7500.eventually"
                                              ]: return False # state space does not build in time or qualitative property (same selection as in TACAS)
    return True

def is_premise(benchmark):
    return benchmark.is_drn()
def is_gridworld(benchmark):
    return benchmark.get_model_short_name() in ["refuel-mdp", "obstacle-mdp", "avoid-mdp", "evade-mdp", "intercept-mdp", "airport-mdp", "random-grid"]

def is_mec_only(benchmark): # Benchmarks that are *only* in the MEC set
    return benchmark.get_model_short_name() in ["bigmec", "manymecs", "mer", "sensor", "consensus-mec", "wlan-mec"]

def is_qvbs(benchmark):
    return not any([is_premise(benchmark), is_gridworld(benchmark), is_mec_only(benchmark)])

def save_set(benchmarks, setname):
    print("Saving set '{}' with {} benchmarks".format(setname, len(benchmarks)))
    save_json([ benchmark.get_identifier() for benchmark in benchmarks], os.path.join(sys.path[0], "data", setname + ".json"))



all = [ b for b in get_all_benchmarks(settings, set_mdpmc_dir(os.path.join(settings.benchmark_dir(), "index.json"))) if is_considered(b)]
all_jani = [ b for b in all if b.has_janifile()]

premise = [ b for b in all if is_premise(b)]
gridworld = [ b for b in all if is_gridworld(b)]
qvbs_full = [ b for b in all if is_qvbs(b)]
mec_only = [ b for b in all if is_mec_only(b)]

quickcheck = [ get_benchmark_from_id(settings, "firewire.false-3-800.time_sending")]

# assert that we indeed have all benchmarks
all_classified_ids = [b.get_identifier() for b in premise + gridworld + qvbs_full + mec_only]
unused_ids = [b.get_identifier() for b in all if b.get_identifier() not in all_classified_ids]
if len(all) != len(all_classified_ids):
    print("Not all benchmarks classified. Unused IDs:\n\t\"{}\"".format("\",\n\t\"".join(unused_ids)))
    print("{} benchmarks found, {} benchmarks classified, {} missing".format(len(all), len(all_classified_ids), len(all) - len(all_classified_ids)))

save_set(premise, "premise")
save_set(gridworld, "gridworld")
save_set(qvbs_full, "qvbs-full")
save_set(all_jani, "all-jani")
save_set(quickcheck, "quickcheck")
