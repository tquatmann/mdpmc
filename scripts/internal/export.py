from .benchmark import *
from .utility import *
from . import storm
from . import mcsta
from collections import Counter
import os

def get_runtime(result_json):
    if "model-checking-time" in result_json:
        return result_json["model-checking-time"]
    else:
        raise AssertionError("no model checking time in {}".format(result_json))

class CombinedResult(object):
    def __init__(self, result_json_array):
        if (len(result_json_array) == 0):
            raise AssertionError("Empty array of results.")

        self.num_not_supported = 0
        self.num_ignored = 0
        self.num_expected_error = 0
        self.num_unexpected_error = 0
        self.num_memout = 0
        self.num_timeout = 0
        self.num_incorrect = 0
        self.runtimes = []
        self.walltimes = []
        self.return_codes = []

        for res_json in result_json_array:
            if not res_json["supported"]: self.num_not_supported += 1
            elif False: self.num_ignored += 1 # Nothing ignored right now
            elif "expected-error" in res_json and res_json["expected-error"]:
                self.num_expected_error += 1
            elif "execution-error" in res_json and res_json["execution-error"]:
                self.num_unexpected_error += 1
            elif "timeout" in res_json and res_json["timeout"]: self.num_timeout += 1
            elif "memout" in res_json and res_json["memout"]: self.num_memout += 1
            elif "result-correct" in res_json and not res_json["result-correct"]:
                self.num_incorrect += 1
            else:
                self.runtimes.append(get_runtime(res_json))
            self.walltimes.append(res_json["wallclock-time"])
            if "return-codes" in res_json:
                self.return_codes += res_json["return-codes"]

        # assert consistency
        for n in [self.num_not_supported, self.num_ignored]:
            if n != 0 and n != len(result_json_array):
                raise AssertionError("Inconsistent results: {} not supported, {} ignored, {} total".format(self.num_not_supported, self.num_ignored, len(result_json_array)))
    def average_runtime(self):
        if len(self.runtimes) == 0:
            return None
        return sum(self.runtimes) / len(self.runtimes)




# Generates a csv containing runtimes. A row corresponds to a benchmark, a column corresponds to a tool/config combination.
# The first three columns contain the benchmark id, the model type, and the original format
# The last column contains the lowest runtime of the corresponding rows.
def generate_scatter_csv(settings, exec_data, benchmark_ids, groups_tools_configs, property_filter=None):
    MIN_VALUE = 1 # runtimes will be set to max(MIN_VALUE, actual runtime)
    MAX_VALUE = 512 # runtimes will be set to min(MAX_VALUE, actual runtime)
    TO_VALUE = 724 # timeout
    MO_VALUE = 724 # Out of memory
    NA_VALUE = 724 # not available
    NS_VALUE = 724 # not supported
    INC_VALUE = 724 # Incorrect result
    ERR_VALUE = 724 # error
    ND_VALUE = 724 # not displayed
    
    result = [ ["benchmark", "Type", "Orig", "Prop"] + ["{}.{}.{}".format(g,t,c) for (g,t,c) in groups_tools_configs] + ["best"] ]
    for benchmark_id in benchmark_ids:
        benchmark = get_benchmark_from_id(settings, benchmark_id)
        if property_filter is not None and benchmark.get_short_property_type() not in property_filter: 
            continue
        row = [benchmark_id, benchmark.get_model_type().lower(), benchmark.get_original_format().lower(), benchmark.get_short_property_type()]
        best_value = NA_VALUE
        for (group, tool, config) in groups_tools_configs:
            value = NA_VALUE
            if benchmark_id in exec_data[group][tool][config]:
                combined_res = CombinedResult(exec_data[group][tool][config][benchmark_id])
                if combined_res.num_unexpected_error > 0:
                    print("Unexpected execution result for '{}.{}.{}.{}'".format(group, tool, config, benchmark_id))
                if combined_res.num_ignored > 0:
                    value = ND_VALUE
                elif combined_res.num_not_supported > 0:
                    value = NS_VALUE
                elif combined_res.num_incorrect > 0: # count as incorrect if at least one result is inc.
                    value = INC_VALUE
                elif len(combined_res.runtimes) > 0:
                    value = min(MAX_VALUE, max(MIN_VALUE, combined_res.average_runtime()))
                    best_value = min(best_value, value)
                elif combined_res.num_timeout > 0: # do not consider TO / MO in average
                    value = TO_VALUE
                elif combined_res.num_memout > 0:
                    value = MO_VALUE
                elif combined_res.num_unexpected_error + combined_res.num_expected_error > 0:
                    value = ERR_VALUE
                else:
                    print("Unexpected execution result for '{}.{}.{}.{}'".format(group, tool, config, benchmark_id))
            row.append(str(value))
        row.append(str(best_value))
        result.append(row)
    return result


# Generates a csv containing runtimes. The first column denotes the row indices. Each of the remaining column corresponds to a tool/config combination. The last column corresponds to the fastest tool/config
# An entry in the ith row corresponds to the runtime of the ith fastest benchmark
def generate_quantile_csv(settings, exec_data, benchmark_ids, groups_tools_configs):
    MIN_VALUE = 0.1 # runtimes will be set to max(MIN_VALUE, actual runtime)
    runtimes_best_dict = OrderedDict()
    groups_tools = []
    for (g,t,c) in groups_tools_configs:
        if g not in runtimes_best_dict: runtimes_best_dict[g] = OrderedDict()
        if t not in runtimes_best_dict[g]:
            runtimes_best_dict[g][t] = OrderedDict()
            groups_tools.append((g,t))

    result = [ ["n"] + ["{}.{}.{}shifted".format(g,t,c) for (g,t,c) in groups_tools_configs]  + ["{}.{}.bestshifted".format(g,t) for g,t in groups_tools]] # append 'shifted' for compatibility with qcomp latex
    result.append([1] + [MIN_VALUE] * (len(groups_tools_configs) + len(groups_tools))) # prevents Latex error when there are no runtimes for a tool,config
    runtimes = OrderedDict()
    for (group, tool, config) in groups_tools_configs:
        runtimes_gtc = []
        for benchmark_id in benchmark_ids:
            if benchmark_id in exec_data[group][tool][config]:
                combined_res = CombinedResult(exec_data[group][tool][config][benchmark_id])
                if combined_res.num_ignored + combined_res.num_not_supported + combined_res.num_incorrect == 0 and len(combined_res.runtimes) > 0:
                    value = max(MIN_VALUE, combined_res.average_runtime())
                    runtimes_gtc.append(value)
                    if benchmark_id not in runtimes_best_dict[group][tool]:
                        runtimes_best_dict[group][tool][benchmark_id] = value
                    else:
                        runtimes_best_dict[group][tool][benchmark_id] = min(runtimes_best_dict[group][tool][benchmark_id], value)
        runtimes_gtc.sort()
        runtimes["{}.{}.{}".format(group, tool,config)] = runtimes_gtc
    for (group,tool) in groups_tools:
        runtimes_best = [ runtimes_best_dict[group][tool][b] for b in runtimes_best_dict[group][tool] ]
        runtimes_best.sort()
        runtimes["{}.{}.best".format(group,tool)] = runtimes_best
    for i in range(len(benchmark_ids)):
        row = [str(i+1)]
        for gtc in runtimes:
            if i < len(runtimes[gtc]):
                row.append(str(runtimes[gtc][i]))
            else:
                row.append("")
        result.append(row)
    return result

# Aux function for writing in files with proper indention
def write_line(file, indention, content):
    file.write("\t"*indention + content + "\n")

# Generates an html log page for the given result within output_dir/logs/
def create_log_page(settings, result_json_array, group, output_dir):
    combined_res = CombinedResult(result_json_array)
    b = get_benchmark_from_id(settings, result_json_array[0]["benchmark-id"])
    logs = []
    for result_json in result_json_array:
        if not "log" in result_json:
            raise AssertionError("Expected a log file.")
        with open(result_json["log"], 'r') as logfile:
            logs += logfile.read().split("#" * 40)
    htmlfilename = os.path.basename(result_json_array[0]["log"])
    htmlfilename = htmlfilename[:htmlfilename.rfind(".run")] + ".html"
    f_path = os.path.join(group, htmlfilename)
    with open(os.path.join(output_dir, f_path), 'w') as f:
        indention = 0
        write_line(f, indention, "<!DOCTYPE html>")
        write_line(f, indention, "<html>")
        write_line(f, indention, "<head>")
        indention += 1
        write_line(f, indention, '<meta charset="UTF-8">')
        write_line(f, indention, "<title>{}.{}.{} - {} {} {}</title>".format(group,result_json_array[0]["tool"], result_json_array[0]["configuration-id"], b.get_model_short_name(), b.get_property_name(), b.get_parameter_values_string()))
#        write_line(f, indention, '<link rel="stylesheet" type="text/css" href="{}">'.format("http://qcomp.org/style.css")) # TODO: Might want to add another style
        write_line(f, indention, '<link rel="stylesheet" type="text/css" href=../style.css>') # TODO: Might want to add another style
        indention -= 1
        write_line(f, indention, '</head>')
        write_line(f, indention, '<body>')
        write_line(f, indention, '<h1>{}.{}.{}</h1>'.format(group,result_json_array[0]["tool"],result_json_array[0]["configuration-id"]))

        write_line(f, indention, '<div class="box">')
        indention += 1
        write_line(f, indention, '<div class="boxlabelo"><div class="boxlabelc">Benchmark</div></div>')
        write_line(f, indention, '<table style="margin-bottom: 0.75ex;">')
        indention += 1
        write_line(f, indention, '<tr><td>Model:</td><td><a href="{}">{}</a> <span class="tt">v.{}</span> ({})</td></tr>'.format("http://qcomp.org/benchmarks/index.html#{}".format(b.get_model_short_name()), b.get_model_short_name(), b.index_json["version"], b.get_model_type().upper()))
        write_line(f, indention, '<tr><td>Parameter(s)</td><td>{}</td></tr>'.format(", ".join(['<span class="tt">{}</span> = {}'.format(p["name"], p["value"]) for p in b.get_parameters()])))
        write_line(f, indention, '<tr><td>Property:</td><td><span class="tt">{}</span> ({})</td></tr>'.format(b.get_property_name(), b.get_property_type()))
        indention -= 1
        write_line(f, indention, "</table>")
        indention -= 1
        write_line(f, indention, "</div>")

        write_line(f, indention, '<div class="box">')
        indention += 1
        write_line(f, indention, '<div class="boxlabelo"><div class="boxlabelc">Invocation ({})</div></div>'.format(result_json_array[0]["configuration-id"]))
        f.write('\t' * indention + '<pre style="overflow: auto; padding-bottom: 1.5ex; padding-top: 1ex; font-size: 15px; margin-bottom: 0ex;  margin-top: 0ex;">')
        commands_str = "\n".join(result_json_array[0]["commands"])
        for filtered_path in settings.filtered_paths():
            commands_str = commands_str.replace(filtered_path, "")
        f.write(commands_str)
        f.write('</pre>\n')
        write_line(f, indention, result_json_array[0]["invocation-note"])
        indention -= 1
        write_line(f, indention, "</div>")

        write_line(f, indention, '<div class="box">')
        indention += 1
        write_line(f, indention, '<div class="boxlabelo"><div class="boxlabelc">Execution</div></div>')
        write_line(f, indention, '<table style="margin-bottom: 0.75ex;">')
        indention += 1
        walltime_str = ""
        for result_json in result_json_array:
            if result_json["timeout"]:
                walltime_str += "&gt {}s (Timeout), ".format(result_json["time-limit"])
            else:
                walltime_str += "{:.3f}s, ".format(result_json["wallclock-time"])
        write_line(f, indention, '<tr><td>Walltime:</td><td style="{}">{}</td></tr>'.format("color: red;" if combined_res.num_timeout > 0 else "tt", walltime_str[:-2]))
        if len(combined_res.runtimes) == 0:
            write_line(f, indention, '<tr><td>Considered runtime:</td><td style="color: red">None</td></tr>')
        elif len(combined_res.runtimes) == 1:
            write_line(f, indention, '<tr><td>Considered runtime:</td><td style="tt">{:.3f}s</td></tr>'.format(combined_res.runtimes[0]))
        else:
            write_line(f, indention, '<tr><td>Considered runtimes:</td><td style="tt">[{}], average={:.3f}s</td></tr>'.format(", ".join(["{:.3f}s".format(r) for r in combined_res.runtimes]), combined_res.average_runtime()))
        return_codes = combined_res.return_codes
        if combined_res.num_expected_error + combined_res.num_unexpected_error > 0:
            write_line(f, indention, '<tr><td>Return code(s):</td><td style="tt; color: red;">{}</td></tr>'.format(", ".join([str(rc) for rc in return_codes])))
        else:
            write_line(f, indention, '<tr><td>Return code(s):</td><td style="tt">{}</td></tr>'.format(", ".join([str(rc) for rc in return_codes])))
        for result_json in result_json_array:
            first = True
            for note in result_json["notes"]:
                write_line(f, indention, '<tr><td>{}</td><td>{}</td></tr>'.format("Note(s):" if first else "", note))
                first = False
            if "relative-error" in result_json:
                write_line(f, indention, '<tr><td>Relative Error:</td><td style="tt{}">{}</td></tr>'.format("" if result_json["result-correct"] else "; color: red", result_json["relative-error"]))
        indention -= 1
        write_line(f, indention, "</table>")
        indention -= 1
        write_line(f, indention, "</div>")

        for log in logs:
            for filtered_path in settings.filtered_paths():
                log = log.replace(filtered_path, "")
            pos = log.find("\n", log.find("Output:\n")) + 1
            pos_end = log.find("#############################", pos)
            if pos_end < 0:
                pos_end = len(log)
            log_str = log[pos:pos_end].strip()
            if len(log_str) != 0:
                write_line(f, indention, '<div class="box">')
                indention += 1
                write_line(f, indention, '<div class="boxlabelo"><div class="boxlabelc">Log</div></div>')
                f.write("\t" * indention + '<pre style="overflow:auto; padding-bottom: 1.5ex">')
                f.write(log_str)
                write_line(f, indention, '</pre>')
                indention -= 1
                write_line(f, indention, "</div>")

            pos = log.find("##############################Output to stderr##############################\n")
            if pos >= 0:
                pos = log.find("\n", pos) + 1
                write_line(f, indention, '<div class="box">')
                indention += 1
                write_line(f, indention, '<div class="boxlabelo"><div class="boxlabelc">STDERR</div></div>')
                f.write("\t" * indention + '<pre style="overflow:auto; padding-bottom: 1.5ex">')
                pos_end = log.find("#############################", pos)
                if pos_end < 0:
                    pos_end = len(log)
                f.write(log[pos:pos_end].strip())
                write_line(f, indention, '</pre>')
                indention -= 1
                write_line(f, indention, "</div>")
        write_line(f, indention, "</body>")
        write_line(f, indention, "</html>")
    return f_path

# Generates an interactive html table from the results
def generate_table(settings, exec_data, benchmark_ids, groups_tools_configs, output_dir):
    SHOW_UNSUPPORTED = True # Also add entries for benchmarks that are known to be unsupported
    
    ensure_directory(output_dir)
    for g in set([g for (g,t,c) in groups_tools_configs]):
        ensure_directory(os.path.join(output_dir, g))

    first_tool_col = 6
    num_cols = first_tool_col + len(groups_tools_configs)

    with open (os.path.join(output_dir, "table.html"), 'w') as tablefile:
        tablefile.write(r"""<!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Benchmark results</title>
      <link rel="stylesheet" type="text/css" href="style.css">
      <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.13/css/jquery.dataTables.min.css">
      <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/1.2.4/css/buttons.dataTables.min.css">
      <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/fixedheader/3.1.2/css/fixedHeader.dataTables.min.css">

      <script type="text/javascript" language="javascript" charset="utf8" src="https://code.jquery.com/jquery-1.12.4.js"></script>
      <script type="text/javascript" language="javascript" charset="utf8" src="https://cdn.datatables.net/1.10.13/js/jquery.dataTables.min.js"></script>
      <script type="text/javascript" language="javascript" charset="utf8" src="https://cdn.datatables.net/fixedheader/3.1.2/js/dataTables.fixedHeader.min.js"></script>
      <script type="text/javascript" language="javascript" charset="utf8" src="https://cdn.datatables.net/buttons/1.2.4/js/dataTables.buttons.min.js"></script>
      <script type="text/javascript" language="javascript" charset="utf8" src="https://cdn.datatables.net/buttons/1.2.4/js/buttons.colVis.min.js"></script>

      <script>
        $(document).ready(function() {
          // Set correct file
          $("#content").load("data.html");
        } );

        function updateBest(table) {
          // Remove old best ones
          table.cells().every( function() {
            $(this.node()).removeClass("best");
          });
          table.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
              var bestValue = -1
              var bestIndex = -1
              $.each( this.data(), function( index, value ){
                if (index > 5 && table.column(index).visible()) {
    			    var text = $(value).text()
    	            if (["TO", "ERR", "INC", "MO", "NS", ""].indexOf(text) < 0) {
    				    var number = parseFloat(text);
    	                if (bestValue == -1 || bestValue > number) {
    	                  // New best value
    	                  bestValue = number;
    	                  bestIndex = index;
    	                }
    				  }
    			  }
              });
              // Set new best
              if (bestIndex >= 0) {
                $(table.cell(rowIdx, bestIndex).node()).addClass("best");
              }
          } );
      }
      </script>
    </head>
    """)
        indention = 0
        write_line(tablefile, indention, "<body>")
        write_line(tablefile, indention, "<div>")
        indention +=1
        write_line(tablefile, indention, '<table id="table" class="display">')
        indention += 1
        write_line(tablefile, indention, '<thead>')
        indention += 1
        write_line(tablefile, indention, '<tr>')
        indention += 1
        for head in ["Model", "Type", "Original", "Parameters", "Property", "Type"] + ["{}.{}.{}".format(g,t,c) for (g,t,c) in groups_tools_configs]:
            write_line(tablefile, indention, '<th>{}</th>'.format(head))
        indention -= 1
        write_line(tablefile, indention, '</tr>')
        indention -= 1
        write_line(tablefile, indention, '</thead>')
        write_line(tablefile, indention, '<tbody>')
        indention += 1

        for benchmark_id in benchmark_ids:
            b = get_benchmark_from_id(settings, benchmark_id)
            write_line(tablefile, indention, '<tr>')
            indention += 1
            write_line(tablefile, indention, '<td><a href="{}">{}</a></td>'.format("http://qcomp.org/benchmarks/index.html#{}".format(b.get_model_short_name()), b.get_model_short_name()))
            write_line(tablefile, indention, '<td>{}</td>'.format(b.get_model_type().upper()))
            write_line(tablefile, indention, '<td>{}</td>'.format(b.get_original_format()))
            write_line(tablefile, indention, '<td>{}</td>'.format(b.get_parameter_values_string()))
            write_line(tablefile, indention, '<td>{}</td>'.format(b.get_property_name()))
            write_line(tablefile, indention, '<td>{}</td>'.format(b.get_short_property_type()))
            for (g,t,c) in groups_tools_configs:
                cell_content = ""
                if benchmark_id in exec_data[g][t][c]:
                    combined_res = CombinedResult(exec_data[g][t][c][benchmark_id])
                    link_attributes = ""
                    if combined_res.num_unexpected_error > 0:
                        print("Unexpected execution result for '{}.{}.{}' (found while creating table)".format(t, c, benchmark_id))
                    if combined_res.num_ignored > 0:
                        res_str = "-"
                        link_attributes = " class='ignore'"
                    elif combined_res.num_not_supported > 0:
                        res_str = "NS" if SHOW_UNSUPPORTED else None
                        link_attributes = " class='unsupported'"
                    elif combined_res.num_incorrect > 0: # count as incorrect if at least one result is inc.
                        res_str = "INC"
                        link_attributes = " class='incorrect'"
                    elif len(combined_res.runtimes) > 0:
                        res_str = "%.1f" % combined_res.average_runtime()
                    elif combined_res.num_timeout > 0:
                        res_str = "TO"
                        link_attributes = " class='timeout'"
                    elif combined_res.num_memout > 0:
                        res_str = "MO"
                        link_attributes = " class='memout'"
                    elif combined_res.num_unexpected_error + combined_res.num_expected_error > 0:
                        res_str = "ERR"
                        link_attributes = " class='error'"
                    else:
                        print("Unexpected execution result for '{}.{}.{}'".format(t, c, benchmark_id))
                    if res_str is not None:
                        logpage = create_log_page(settings, exec_data[g][t][c][benchmark_id], g, output_dir)
                        cell_content = "<a href='{}' {}>{}</a>".format(logpage, link_attributes, res_str)                
                write_line(tablefile, indention, '<td>{}</td>'.format(cell_content))
            indention -= 1
            write_line(tablefile, indention, '</tr>')
        indention -= 1
        write_line(tablefile, indention, '</tbody>')
        indention -= 1
        indention -= 1
        write_line(tablefile, indention, '</table>')
        write_line(tablefile, indention, "<script>")
        indention +=1
        write_line(tablefile, indention, 'var table = $("#table").DataTable( {')
        indention += 1
        write_line(tablefile, indention, '"paging": false,')
        write_line(tablefile, indention, '"autoWidth": false,')
        write_line(tablefile, indention, '"info": false,')
        write_line(tablefile, indention, 'fixedHeader: {')
        indention += 1
        write_line(tablefile, indention, '"header": true,')
        indention -= 1
        write_line(tablefile, indention, '},')
        write_line(tablefile, indention, '"dom": "Bfrtip",')
        write_line(tablefile, indention, 'buttons: [')
        indention += 1
        for columnIndex in range(first_tool_col, num_cols):
            write_line(tablefile, indention, '{')
            indention += 1
            write_line(tablefile, indention, 'extend: "columnsToggle",')
            write_line(tablefile, indention, 'columns: [{}],'.format(columnIndex))
            indention -= 1
            write_line(tablefile, indention, "},")
        tool_columns = [i for i in range(first_tool_col, num_cols)]
        for text, show, hide in zip(["Show all", "Hide all"], [tool_columns, []], [[], tool_columns]):
            write_line(tablefile, indention, '{')
            indention += 1
            write_line(tablefile, indention, 'extend: "colvisGroup",')
            write_line(tablefile, indention, 'text: "{}",'.format(text))
            write_line(tablefile, indention, 'show: {},'.format(show))
            write_line(tablefile, indention, 'hide: {}'.format(hide))
            indention -= 1
            write_line(tablefile, indention, "},")
        indention -= 1
        write_line(tablefile, indention, "],")
        indention -= 1
        write_line(tablefile, indention, "});")
        indention -= 1
        write_line(tablefile, indention, "")
        indention += 1
        write_line(tablefile, indention, 'table.on("column-sizing.dt", function (e, settings) {')
        indention += 1
        write_line(tablefile, indention, "updateBest(table);")
        indention -= 1
        write_line(tablefile, indention, "} );")
        indention -= 1
        write_line(tablefile, indention, "")
        indention += 1
        write_line(tablefile, indention, "updateBest(table);")
        indention -= 1
        write_line(tablefile, indention, "</script>")
        indention -= 1
        write_line(tablefile, indention, "</div>")
        write_line(tablefile, indention, "</body>")
        write_line(tablefile, indention, "</html>")

    with open (os.path.join(output_dir, "style.css"), 'w') as stylefile:
#        write_line(stylefile, 0, '@import url("{}");'.format(os.path.join(qcomp_root, "fonts/Tajawal/Tajawal.css"))) #TODO
        stylefile.write(r"""

    .best {
        background-color: lightgreen;
    }
    .error {
    	font-weight: bold;
    	background-color: lightcoral;
    }
    .incorrect {
        background-color: orange;
    	font-weight: bold;
    }
    .timeout {
        background-color: lightgray;
    }
    .memout {
        background-color: lightgray;
    }
    .unsupported {
        background-color: yellow;
    }
    .ignored {
        background-color: blue;
    }

    h1 {
    	font-size: 28px; font-weight: bold;
    	color: #000000;
    	padding: 1px; margin-top: 20px; margin-bottom: 1ex;
    }

    tt, .tt {
    	font-family: 'Courier New', monospace; line-height: 1.3;
    }

    .box {
    	margin: 2.5ex 0ex 1ex 0ex; border: 1px solid #D0D0D0; padding: 1.6ex 1.5ex 1ex 1.5ex; position: relative;
    }

    .boxlabelo {
    	position: absolute; pointer-events: none; margin-bottom: 0.5ex;
    }

    .boxlabel {
    	position: relative; top: -3.35ex; left: -0.5ex; padding: 0px 0.5ex; background-color: #FFFFFF; display: inline-block;
    }
    .boxlabelc {
    	position: relative; top: -3.17ex; left: -0.5ex; padding: 0px 0.5ex; background-color: #FFFFFF; display: inline-block;
    }
    """)
