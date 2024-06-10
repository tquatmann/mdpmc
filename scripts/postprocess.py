from internal.export import *
from internal.processlogs import *
from internal.utility import *
from internal import benchmarksets
import sys
import os

def exportData(settings, benchmark_set_id, exec_data, groups_tools_configs_sorted):

    groups_tools_configs_filtered = [(g,t,c) for g,t,c in groups_tools_configs_sorted if g in exec_data and t in exec_data[g] and c in exec_data[g][t] and len(exec_data[g][t][c]) > 0]
    benchmark_set = load_json(os.path.realpath(os.path.join(sys.path[0], "data/{}.json").format(benchmark_set_id)))
    ensure_directory(benchmark_set_id)
    scatterfile = os.path.join(benchmark_set_id, settings.results_file_scatter())
    print("\tGenerating file {} for scatter plots".format(scatterfile))
    scatter_csv = generate_scatter_csv(settings, exec_data, benchmark_set, groups_tools_configs_filtered)
    save_csv(scatter_csv, scatterfile)
    quantilefile = os.path.join(benchmark_set_id, settings.results_file_quantile())
    print("\tGenerating file {} for quantile plots".format(quantilefile))
    quantile_csv = generate_quantile_csv(settings, exec_data, benchmark_set, groups_tools_configs_filtered)
    save_csv(quantile_csv, quantilefile)
    
    tabledir = os.path.join(benchmark_set_id, settings.results_dir_table())
    print("\tGenerating interactive html table in directory {}".format(tabledir))
    generate_table(settings, exec_data, benchmark_set, groups_tools_configs_filtered, tabledir)

    statsfile = os.path.join(benchmark_set_id, settings.results_file_stats())
    print("\tGenerating file {} for statistics".format(statsfile))
    stats_json = generate_stats_json(settings, exec_data, benchmark_set, groups_tools_configs_filtered)
    save_json(stats_json, statsfile)


if __name__ == "__main__":
    print("Benchmarking tool.")
    print("This script gathers data of executions and exports them in various ways.")
    print("Usages:")
    print("python3 {} reads the log file directory from the default settings file.".format(sys.argv[0]))
    print("python3 {} path/to/first/logfiles/ path/to/second/logfiles/ ...    reads from multiple log file directories '".format(sys.argv[0]))
    print("")
    if (len(sys.argv) == 2 and sys.argv[1] in ["-h", "-help", "--help"]):
        exit(1)

    settings = Settings()
    logdirs = sys.argv[1:]
    if len(logdirs) == 0:
        logdirs = [settings.logs_dir()]
    print("Selected log dir(s): {}".format(", ".join(logdirs)))
    print("")

    groups_tools_configs = get_all_groups_tools_configs(logdirs) # group names are derived from the directory names
    exec_data = gather_execution_data(settings, logdirs, groups_tools_configs)  # Group -> Tool -> Config -> Benchmark -> [Data array]

    for benchmarkset_id in benchmarksets.data.keys():
        exportData(settings, benchmarkset_id, exec_data, groups_tools_configs)

