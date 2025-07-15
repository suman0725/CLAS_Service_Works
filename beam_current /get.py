import rcdb
from rcdb import RCDBProvider
import sys

# Open RCDB connection
db = RCDBProvider("mysql://rcdb@clasdb.jlab.org/rcdb")

# Get run number range from command line arguments
RunNum_min = int(sys.argv[-2])
RunNum_max = int(sys.argv[-1])

# Output file name
output_filename = f"run_conditions_{RunNum_min}_{RunNum_max}.txt"

# Get the runs
runs = db.get_runs(RunNum_min, RunNum_max)

# Open the output file
with open(output_filename, "w") as outfile:
    # Write header
    outfile.write("RunNumber\tBeamCurrent(nA)\tTarget\n")

    for r in runs:
        # Safely check evio_files_count
        evio_files_count = r.get_condition_value("evio_files_count")
        if evio_files_count is None or evio_files_count < 10:
            continue

        # Get beam current
        beam_current = r.get_condition_value("beam_current")
        if beam_current is None:
            beam_current = "N/A"

        # Try different keys for target
        target_type = r.get_condition_value("target_type")
        if target_type is None:
            target_type = r.get_condition_value("target")
        if target_type is None:
            target_type = r.get_condition_value("comment")  # fallback
        if target_type is None:
            target_type = "N/A"

        # Write the line
        outfile.write(f"{r.number}\t{beam_current}\t{target_type}\n")

print(f"\n Output written to: {output_filename}")
