from internal.export import *
from internal.processlogs import *
from internal.utility import *
import sys
import os

def exportData(settings, benchmark_set_id, exec_data, groups_tools_configs_sorted):
    
    benchmark_set = load_json(os.path.realpath(os.path.join(sys.path[0], "internal/{}.json").format(benchmark_set_id)))
    ensure_directory(benchmark_set_id)
    scatterfile = os.path.join(benchmark_set_id, settings.results_file_scatter())
    print("\tGenerating file {} for scatter plots".format(scatterfile))
    scatter_csv = generate_scatter_csv(settings, exec_data, benchmark_set, groups_tools_configs_sorted)
    save_csv(scatter_csv, scatterfile)
    quantilefile = os.path.join(benchmark_set_id, settings.results_file_quantile())
    print("\tGenerating file {} for quantile plots".format(quantilefile))
    quantile_csv = generate_quantile_csv(settings, exec_data, benchmark_set, groups_tools_configs_sorted)
    save_csv(quantile_csv, quantilefile)
    
    tabledir = os.path.join(benchmark_set_id, settings.results_dir_table())
    print("\tGenerating interactive html table in directory {}".format(tabledir))
    generate_table(settings, exec_data, benchmark_set, groups_tools_configs_sorted, tabledir)

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
    exportData(settings, "qvbs-full", exec_data, groups_tools_configs)
    exportData(settings, "qvbs-hard", exec_data, groups_tools_configs)
    exportData(settings, "premise", exec_data, groups_tools_configs)
