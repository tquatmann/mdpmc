Original Results
================

This archive contains logfiles and derived data (including a browsable html table and the .csv tables from which we derive our plots).

The archive contains directories
- `claix23` (Sec 6.1),
- `claix23-all` (Sec 6.2),
- `claix23-permute` (Sec 6.3),
- `claix23-variance` (not in paper),
- `premise` (Sec 6.2),
- `hardware-experiments` (Sec 6.4),

These directories each contain
- subdirectories for the individual benchmark sets (the *practitioners-set-2024* is called *community24*) which then contain
  - tables in html format which allow to review the experiments in greater detail, inspect logfiiles, etc. Each cell shows the model checking time of a configuration (column) on a benchmark instance (row). Clicking on a cell opens a page showing the precise command and the corresponding logfile.
  - `.csv` files used for our quantile and scatter plots
  - `.json` files containing general statistics like number of incorrect results.
- the raw log files (directory names starting with `logs`)
- a file `inv.json` containing the command lines.
- a script `cpdata.sh` that copies over all data used for the plots in the paper to the `latex/` directory.

The archive further contains a `latex/` directory which contains the code used to generate the paper plots. The provided script `build_latex.sh` builds the document (assuming a working lualatex installation).