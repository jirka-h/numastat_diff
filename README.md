# numastat_diff
Script to subtract numerical values from two (not only) numastat log files end.log minus start.log

## Example usage:
```sh
numastat > numastat.start ; COMMAND; numastat > numastat.end
numastat_diff.py--start numastat.start --end numastat.end
```

Output shows how numastat statistics has changed while running COMMAND,
computing end-start for all numerical values.

```sh
$ cat numastat.start
                           node0           node1           node2           node3           node4           node5           node6           node7
numa_hit                 2965587         2016852         6769405         4850482        12265903         2819726         2426895         3347187
numa_miss                      0               0               0               0               0               0               0               0
numa_foreign                   0               0               0               0               0               0               0               0
interleave_hit             19833           19801           19837           19809           19825           19812           19835           19805
local_node               2956775         1986434         6744727         4823219        12227344         2792479         2399335         3279632
other_node                  8812           30418           24678           27263           38559           27247           27560           67555

$ cat numastat.end
                           node0           node1           node2           node3           node4           node5           node6           node7
numa_hit                 2965739         2016985         6777313         4852033        12266105         2819861         2426895         3350379
numa_miss                      0               0               0               0               0               0               0               0
numa_foreign                   0               0               0               0               0               0               0               0
interleave_hit             19833           19801           19837           19809           19825           19812           19835           19805
local_node               2956923         1986567         6752635         4824770        12227546         2792614         2399335         3279740
other_node                  8816           30418           24678           27263           38559           27247           27560           70639

$ numastat_diff.py --start numastat.start --end numastat.end
                node0  node1  node2  node3  node4  node5  node6  node7
numa_hit          152    133   7908   1551    202    135      0   3192
numa_miss           0      0      0      0      0      0      0      0
numa_foreign        0      0      0      0      0      0      0      0
interleave_hit      0      0      0      0      0      0      0      0
local_node        148    133   7908   1551    202    135      0    108
other_node          4      0      0      0      0      0      0   3084
```

Bernd Finger has suggested a awk script. It's in the `Awk` directory.
```sh
Awk/numastat_diff.awk Example/numastat.start Example/numastat.end
```
