from .benchmark import *
from .utility import *
import internal.storm
import internal.mcsta
import sys
import os

def process_tool_result(result, notes, settings, benchmark, execution_json):
    if result is not None:
        execution_json["result"] = str(result)  # convert to str to not loose precision
        result = try_to_bool_or_number(result)
        if result is not None and "exact" in execution_json["configuration-id"]:
            benchmark.store_reference_result(str(result), "{}.{}".format(execution_json["tool"],execution_json["configuration-id"]))
        if benchmark.has_reference_result():
            execution_json["result-correct"] = is_result_correct(settings, benchmark.get_reference_result(), result)
            if is_number(result) and is_number_or_interval(benchmark.get_reference_result()):
                execution_json["absolute-error"] = try_to_float(get_absolute_error(benchmark.get_reference_result(), result))
                execution_json["relative-error"] = try_to_float(get_relative_error(benchmark.get_reference_result(), result))
                if not execution_json["result-correct"]:
                    # Prepare a message
                    if settings.is_relative_precision():
                        error_kind = "a relative"
                        error_value = execution_json["relative-error"]
                    else:
                        error_kind = "an absolute"
                        error_value = execution_json["absolute-error"]
                    if is_number(result) and not (isinstance(result,float) or isinstance(result,int)):
                        execution_result_str = "'{}' (approx. {})".format(result, try_to_float(result))
                    else:
                        execution_result_str = "'{}'".format(result)
                    if is_number(benchmark.get_reference_result()) and not (isinstance(benchmark.get_reference_result(), float) or isinstance(benchmark.get_reference_result(), int)):
                        ref_result_str = "'{}' (approx. {})".format(benchmark.get_reference_result(), try_to_float(benchmark.get_reference_result()))
                    elif (isinstance(benchmark.get_reference_result(), dict) or isinstance(benchmark.get_reference_result(), OrderedDict)) and "lower" in benchmark.get_reference_result() and "upper" in benchmark.get_reference_result():
                        ref_result_str = "[{},{}]".format(try_to_float(benchmark.get_reference_result()["lower"]), try_to_float(benchmark.get_reference_result()["upper"]))
                    else:
                        ref_result_str = "'{}'".format(benchmark.get_reference_result())
                    notes.append("The tool result {} is tagged as incorrect. The reference result is {} which means {} error of '{}' which is larger than the goal precision '{}'.".format(execution_result_str, ref_result_str, error_kind, error_value, try_to_float(settings.goal_precision())))
            elif not execution_json["result-correct"]:
                notes.append("Result '{}' is tagged as incorrect because it is different from the reference result '{}'.".format(result, benchmark.get_reference_result()))
        else:
            notes.append("Correctness of result is not checked because no reference result is available.")
    else:
        has_timeout = "timeout" in execution_json and execution_json["timeout"]
        has_error = "execution-error" in execution_json and execution_json["execution-error"]
        if not has_timeout and not has_error:
            notes.append("Unable to obtain tool result.")
            execution_json["execution-error"] = True

def parse_tool_output(settings, execution_json):
    with open(execution_json["log"], 'r') as logfile:
        log = logfile.read()

    benchmark = get_benchmark_from_id(settings, execution_json["benchmark-id"])
    
    notes = []
    if execution_json["tool"] == internal.storm.get_name():
        execution_json["supported"] = not internal.storm.is_not_supported(log)
        result = None
        mctime = internal.storm.get_MC_Time(log)
        if mctime is not None:
            if float(mctime) <= 1800:
                execution_json["model-checking-time"] = mctime
                result = internal.storm.get_result(log, benchmark)
            else:
                execution_json["timeout"] = True
            execution_json["memout"] = False
            execution_json["expected-error"] = False
        else:
            execution_json["memout"] = internal.storm.is_memout(log)
            execution_json["expected-error"] = internal.storm.is_expected_error(log)
    elif execution_json["tool"] == "mcsta":
        execution_json["supported"] = not internal.mcsta.is_not_supported(log)
        result = None
        mctime = internal.mcsta.get_MC_Time(log)
        if mctime is not None:
            if float(mctime) <= 1800:
                execution_json["model-checking-time"] = mctime
                result = internal.mcsta.get_result(log, benchmark)
            else:
                execution_json["timeout"] = True
            execution_json["memout"] = False
            execution_json["expected-error"] = False
        else:
            execution_json["memout"] = internal.mcsta.is_memout(log)
            execution_json["expected-error"] = internal.mcsta.is_expected_error(log)
    else:
        print("Error: Unknown tool '{}'".format(execution_jsion["tool"]))
    
    process_tool_result(result, notes, settings, benchmark, execution_json)
    execution_json["notes"] = notes    

def get_all_tools_configs():
    return [("Storm", c.identifier) for c in internal.storm.get_configurations()] + [("mcsta", c.identifier) for c in internal.mcsta.get_configurations()] 

def gather_execution_data(settings, logdirs, tools_configs):
    exec_data = OrderedDict() # Tool -> Config -> Benchmark -> Data
    for t,c in tools_configs:
        if t not in exec_data: exec_data[t] = OrderedDict()
        exec_data[t][c] = OrderedDict()
    for logdir_input in logdirs:
        logdir = os.path.expanduser(logdir_input)
        assert os.path.isdir(logdir), f"Error: directory '{logdir}' does not exist."
        print("\nGathering execution data for logfiles in {} ...".format(logdir))
        json_files = [ f for f in os.listdir(logdir) if f.endswith(".json") and os.path.isfile(os.path.join(logdir, f)) ]
        progress = Progressbar(len(json_files))   
        i = 0
        for execution_json in [ load_json(os.path.join(logdir, f)) for f in json_files ]:
            progress.print_progress(i)
            i += 1
            tool = execution_json["tool"]
            config = execution_json["configuration-id"]
            benchmark = execution_json["benchmark-id"]
            if benchmark in exec_data[tool][config]:
                print("Error: Multiple result files found for {}.{}.{}".format(tool,config,benchmark))
            else:
                execution_json["log"] = os.path.join(logdir, execution_json["log"])
                parse_tool_output(settings, execution_json)
                exec_data[tool][config][benchmark] = execution_json    
    print("\n")
    return exec_data
