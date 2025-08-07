import rcdb
from rcdb import RCDBProvider
import sys

# open connection
db = RCDBProvider("mysql://rcdb@clasdb.jlab.org/rcdb")


RunNum_min = int(sys.argv[-2])
RunNum_max = int(sys.argv[-1])


# get runs 
runs = db.get_runs( RunNum_min, RunNum_max )

for r in runs:
  if r.get_condition_value( "evio_files_count" ) < 10 :
    continue;
  print  r.number, r.get_condition_value( "run_start_time" ) 
