#!/usr/bin/awk -f
# Based on suggestion by Bernd Finger

BEGIN {
  if (ARGC!=3) {
    printf("Script requires two input arguments, got %d.\n", ARGC-1)
    for (i = 1; i < ARGC; i++) {
      printf "\tARGV[%d] = '%s'\n", i, ARGV[i]
    }
    printf("Usage: numastat_diff.awk numastat.start numastat.end\n")
    }
}

#First file
FNR==NR{
  n++
  if (NR==0) {print}
  if (NR>0){
    for (i=1; i<=NF; i++) {
      a[(FNR)][i]=$(i+1);
    }
    next
   }
 }

#Second file
NR>(n+1){
   printf ("%-15s ", $1);
   for (i=1; i<=NF-1; i++) {
      printf ("%10d ", $(i+1)-a[(FNR)][i]);
   }
   printf ("\n");
 }
