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

    tools_configs = get_all_tools_configs() 
    exec_data = gather_execution_data(settings, logdirs, tools_configs)  # Tool -> Config -> Benchmark -> Data
    unsuccessful = OrderedDict()
    for t,c in tools_configs:
        tc_data = exec_data[t][c]
        fail_reason = None
        if len(tc_data) > 1:
            fail_reason = "Multiple benchmark files"
        elif len(tc_data) == 0:
            fail_reason = "Not tested"
        elif "firewire.false-3-800.time_sending" not in tc_data:
            fail_reason = "Wrong benchmark"
        else:
            exec_json = tc_data["firewire.false-3-800.time_sending"]
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
            unsuccessful[f"{t}.{c}"] = fail_reason
    
    print("{}/{} configurations were tested successfully.".format(len(tools_configs) - len(unsuccessful), len(tools_configs)))
    if len(unsuccessful) > 0:
        print("{}/{} configurations do not work:".format(len(unsuccessful), len(tools_configs)))
        print("\t" + "\n\t".join([f"{c}: {reason}" for c,reason in unsuccessful.items()]))
        print("Note: failed tests for configurations that use an uninstalled LP solver are expected.")
    
            
    