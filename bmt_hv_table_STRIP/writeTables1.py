
import numpy as np
import sys
print("Script started")
# Check if enough arguments are provided
if len(sys.argv) < 3:
    print("Too few arguments. Specify initial and final range")
    exit(1)

          # Parse command line arguments for initial and final run numbers
runI = int(sys.argv[1])
runF = int(sys.argv[2])
print("RunI:", runI)
print("RunF:", runF)
          # Default to "DRIFT", but allow for an override from the command line
Ch = "DRIFT"
if len(sys.argv) > 3:
  Ch = sys.argv[3]
print("Ch:", Ch)
                # Format string for the filename
fn = "B_DET_BMT_HV_SEC{}_L{}_{}.txt"

                # Load the data
data = {}
for i in range(1, 4):  # Layers
    for j in range(1, 7):  # Sectors
        f = fn.format(i, j, Ch)
        print("Loading data from:", f)
        d = np.loadtxt(f)
        if d.size == 0: 
            print("No data for sector{0}, layer{1}".format(j,i))
            continue
        data[i * 100 + j] = d[(d[:, 0] >= runI) & (d[:, 0] <= runF)]

                                                # Write the output in the new format
fout = open("bmt_hv_table_{}_{}_{}.txt".format(Ch, runI, runF), 'w')
component = 0  # Assuming component is a fixed value

for i in range(1, 4):  # For each sector
    for j in range(1, 7):  # For each layer
        print("Processing sector:",j,"layer:",i)
        d = data[i * 100 + j]

        # Check if there's a significant change in HV values
        if abs(d[0, 1] - d[-1, 1]) > 10:
            print("ERROR: L{} S{}, initial and final values are different".format(i, j))

        # Write the data in the new format: sector, layer, component, hv
        fout.write("{} {} {} {:.1f}\n".format(i, j, component, d[0, 1]))

fout.close()
print("Script finished")

