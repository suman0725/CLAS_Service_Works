import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# File paths
eff_file = "/w/hallb-scshelf2102/clas12/suman/SW_25/efficiency/efficiency_s1_l1.txt"
voltage_file = "/w/hallb-scshelf2102/clas12/suman/SW_25/stripVoltages/B_DET_BMT_HV_SEC1_L1_STRIP.txt"
output_file = "/w/hallb-scshelf2102/clas12/suman/SW_25/test/comparison_s1_l1.txt"

# Read data
eff_data = pd.read_csv(eff_file, sep='\s+')
eff_data["RunNumber"] = eff_data["RunNumber"].astype(int)
voltage_data = pd.read_csv(voltage_file, sep='\s+', names=["RunNumber", "Voltage"])
voltage_data = voltage_data[~voltage_data["RunNumber"].isin([20005, 20011])]

# Merge data, keeping all runs even if voltage is missing
merged = eff_data.merge(voltage_data, on="RunNumber", how="left")

# Filter efficiencies < 0.9
low_eff = merged[merged["Efficiency"] < 0.9].copy()

# Identify zero-voltage runs
zero_voltage = low_eff[low_eff["Voltage"] == 0] if "Voltage" in low_eff.columns and not low_eff["Voltage"].isna().all() else pd.DataFrame()

# Save comparison, noting zero-voltage and missing data
with open(output_file, "w") as f:
    f.write("Tile S1 L1 (Efficiency < 0.9):\n")
    f.write("Note: Voltage data may be missing or zero for some runs.\n")
    if not zero_voltage.empty:
        f.write("Zero Voltage Runs:\n")
        for _, row in zero_voltage.iterrows():
            run = row["RunNumber"]
            eff = row["Efficiency"]
            f.write(f"Run {run}, Efficiency {eff:.3f}, Voltage 0.000 V\n")
    f.write("Other Runs (Efficiency < 0.9):\n")
    for _, row in low_eff.iterrows():
        run = row["RunNumber"]
        eff = row["Efficiency"]
        voltage = row["Voltage"]
        if pd.isna(voltage):
            f.write(f"Run {run}, Efficiency {eff:.3f}, Voltage: Missing\n")
        elif voltage != 0:
            f.write(f"Run {run}, Efficiency {eff:.3f}, Voltage {voltage:.3f} V\n")

# Plot with focus on efficiency < 0.9 and zero voltage
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.set_xlabel("Run Number")
ax1.set_ylabel("Efficiency", color="blue")
ax1.plot(low_eff["RunNumber"].to_numpy(), low_eff["Efficiency"].to_numpy(), marker="o", markersize=6, alpha=0.6, color="blue", label="Efficiency < 0.9")
if not zero_voltage.empty:
    ax1.plot(zero_voltage["RunNumber"].to_numpy(), zero_voltage["Efficiency"].to_numpy(), marker="s", markersize=8, color="purple", linestyle="", label="Zero Voltage")
ax1.tick_params(axis="y", labelcolor="blue")
ax1.set_ylim(0, 1.1)
ax1.grid(True, linestyle="--", alpha=0.7)

ax2 = ax1.twinx()
ax2.set_ylabel("Voltage (V)", color="red")
# Plot voltage with smaller circles, highlight zero
ax2.plot(low_eff["RunNumber"].to_numpy(), low_eff["Voltage"].to_numpy(), marker="o", markersize=3, alpha=0.6, color="red", label="Voltage")
if not zero_voltage.empty:
    ax2.plot(zero_voltage["RunNumber"].to_numpy(), np.zeros(len(zero_voltage)), marker="s", markersize=8, color="purple", linestyle="", label="Zero Voltage")
ax2.tick_params(axis="y", labelcolor="red")
ax2.set_ylim(0, max(low_eff["Voltage"].max() if not pd.isna(low_eff["Voltage"].max()) else 600, 600) + 100)
ax2.grid(True, linestyle="--", alpha=0.7)

plt.title("Efficiency and Voltage vs Run Number for S1 L1 (Efficiency < 0.9)", pad=15)
fig.tight_layout()
fig.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=10)
plt.savefig("/w/hallb-scshelf2102/clas12/suman/SW_25/test/s1_l1_plot.png", dpi=300)
plt.close()