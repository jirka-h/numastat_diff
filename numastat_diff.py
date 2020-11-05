#!/usr/bin/env python3

# Compute numerical difference by subtracting values from two subsequent
# numastat (or similar) outputs.
# Example usage:
#   numastat > numastat.start ; COMMAND; numastat > numastat.end
#   numastat_diff.py--start numastat.start --end numastat.end
#

# Copyright (C) 2020  Jirka Hladky <hladky DOT jiri AT gmail DOT com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import pandas as pd
import argparse

epilog = """
Example usage:
numastat > numastat.start ; COMMAND; numastat > numastat.end
numastat_diff.py--start numastat.start --end numastat.end

Output shows how numastat statistics has changed while running COMMAND,
computing end-start for all numerical values.
"""
parser = argparse.ArgumentParser(
        description='Script to subtract numerical values from two '
        '(not only) numastat log files end.log minus start.log',
        epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--start", type=argparse.FileType('r'),
                    help="Path to start log file.", required=True)
parser.add_argument("--end", type=argparse.FileType('r'),
                    help="Path to end log file.", required=True)
parser.add_argument("--verbose", help="Verbose log", action="store_true")
args = parser.parse_args()

start = pd.read_table(args.start, sep=r'\s+', engine='python')
end = pd.read_table(args.end, sep=r'\s+', engine='python')

if not (start.columns == end.columns).all():
    print("ERROR: Files have different columns", file=sys.stderr)
    for i, val in enumerate(start.columns == end.columns):
        if not val:
            print("'{}' differs from '{}'"
                  .format(start.columns[i], end.columns[i]), file=sys.stderr)
    print("Exiting", file=sys.stderr)
    sys.exit(1)

if not (start.index == end.index).all():
    print("ERROR: Files have different rows", file=sys.stderr)
    for i, val in enumerate(start.index == end.index):
        if not val:
            print("'{}' differs from '{}'"
                  .format(start.index[i], end.index[i]), file=sys.stderr)
    print("Exiting", file=sys.stderr)
    sys.exit(1)

try:
    diff = end - start
    print(diff)
    sys.exit(0)
except TypeError:
    print("WARNING: Simple end-start failed, some values are not numeric?",
          file=sys.stderr)
    if args.verbose:
        print("Start dataframe", file=sys.stderr)
        print(start.applymap(type), file=sys.stderr)
        print("End dataframe", file=sys.stderr)
        print(end.applymap(type), file=sys.stderr)

print("INFO: Converting dataframes using "
      "pandas.to_numeric(x, errors='coerce')", file=sys.stderr)
start_nm = start.applymap(lambda x: pd.to_numeric(x, errors='coerce'))
end_nm = end.applymap(lambda x: pd.to_numeric(x, errors='coerce'))
try:
    diff = end_nm - start_nm
    pd.options.display.float_format = '{:,.0f}'.format
    print(diff)
    sys.exit(0)
except TypeError:
    print("Subtracting dataframes converted with pandas.to_numeric has also "
          "failed, giving up.", file=sys.stderr)
    sys.exit(1)
