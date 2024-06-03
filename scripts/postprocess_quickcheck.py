from internal.export import *
from internal.processlogs import *
from internal.utility import *
import sys
import os
  

if __name__ == "__main__":
    print("Benchmarking tool.")
    print("This script gathers data of the executions from the quickcheck and reports (un)successful runs.")
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

    groups_tools_configs = get_all_groups_tools_configs(logdirs)
    exec_data = gather_execution_data(settings, logdirs, groups_tools_configs)  # Tool -> Config -> Benchmark -> [Data array]
    unsuccessful = OrderedDict()
    for g,t,c in groups_tools_configs:
        gtc_data = exec_data[g][t][c]
        fail_reason = None
        if len(gtc_data) > 1:
            fail_reason = "Multiple benchmark files"
        elif len(gtc_data) == 0:
            fail_reason = "Not tested"
        elif "firewire.false-3-800.time_sending" not in gtc_data:
            fail_reason = "Wrong benchmark"
        elif len(gtc_data["firewire.false-3-800.time_sending"]) != 1:
            fail_reason = "not a unique run"
        else:
            exec_json = gtc_data["firewire.false-3-800.time_sending"][0]
            if exec_json["timeout"]:
                fail_reason = "Timeout"
            elif "result" not in exec_json:
                fail_reason = "No result"
                for lpsolver in ["gurobi", "soplex", "Copt", "Cplex", "Gurobi", "HiGHS", "Mosek"]:
                    if lpsolver in "".join(exec_json["commands"]):
                        fail_reason += f"; LP solver '{lpsolver}' might not be installed correctly."
                        break
            elif not exec_json["result-correct"]:
                fail_reason = f"Incorrect result: {exec_json['result']}"
        if fail_reason is not None:
            unsuccessful[f"{g}.{t}.{c}"] = fail_reason
    
    print("{}/{} configurations were tested successfully.".format(len(groups_tools_configs) - len(unsuccessful), len(groups_tools_configs)))
    if len(unsuccessful) > 0:
        print("{}/{} configurations do not work:".format(len(unsuccessful), len(groups_tools_configs)))
        print("\t" + "\n\t".join([f"{c}: {reason}" for c,reason in unsuccessful.items()]))
        print("Note: failed tests for configurations that use an uninstalled LP solver are expected.")
    
            
    