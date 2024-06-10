from .utility import *

data = OrderedDict()
description = OrderedDict()

def load_benchmark_set(name : str, descr: str):
    data[name] = load_json(os.path.join(sys.path[0], "data/{}.json".format(name)))
    description[name] = [descr, "({} benchmarks)".format(len(data[name]))]

load_benchmark_set("quickcheck", "A single QVBS instance to quickly check if the installation was successful.")
load_benchmark_set("all-jani", "All benchmarks with Jani files")
load_benchmark_set("community-superset", "All benchmarks that are considered for the community set")
load_benchmark_set("qvbs-full", "All QVBS Benchmarks, including 'qvbs-hard' set")
load_benchmark_set("qvbs-hard", "Hard QVBS Benchmarks")
load_benchmark_set("gridworld", "gridworld benchmarks")
load_benchmark_set("mec-only", "benchmarks that contain mecs that are neither gridworld nor qvbs")
load_benchmark_set("mec-subset", "benchmarks that are known to contain mecs")
load_benchmark_set("premise", "Runtime Monitoring Benchmarks")
