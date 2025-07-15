import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

# Base file paths
base_eff_path = "/w/hallb-scshelf2102/clas12/suman/SW_25/efficiency/efficiency_s{}_l{}.txt"
base_voltage_path = "/w/hallb-scshelf2102/clas12/suman/SW_25/stripVoltages/B_DET_BMT_HV_SEC{}_L{}_STRIP.txt"
output_tex = "/w/hallb-scshelf2102/clas12/suman/SW_25/test/efficiency_voltage_report.tex"

# Process all 18 tiles (S1 L1 to S3 L6)
with open(output_tex, "w") as f_tex:
    f_tex.write("\\documentclass[a4paper,12pt]{article}\n")
    f_tex.write("\\usepackage{tikz}\n")
    f_tex.write("\\usepackage{pgfplots}\n")
    f_tex.write("\\usepackage[utf8]{inputenc}\n")
    f_tex.write("\\usepackage[a4paper,margin=1in]{geometry}\n")
    f_tex.write("\\pgfplotsset{compat=1.18}\n")
    f_tex.write("\\usepackage{amsmath}\n")
    f_tex.write("\\usepackage{amssymb}\n")
    f_tex.write("\\usepackage{booktabs}\n")
    f_tex.write("\\usepackage{graphicx}\n")
    f_tex.write("\\usepackage{DejaVuSans}\n")  # Font for compatibility
    f_tex.write("\\begin{document}\n")

    for sector in range(1, 4):
        for layer in range(1, 7):
            eff_file = base_eff_path.format(sector, layer)
            voltage_file = base_voltage_path.format(sector, layer)
            output_file = f"/w/hallb-scshelf2102/clas12/suman/SW_25/test/comparison_s{sector}_l{layer}.txt"

            # Read data
            eff_data = pd.read_csv(eff_file, sep='\s+')
            eff_data["RunNumber"] = eff_data["RunNumber"].astype(int)
            voltage_data = pd.read_csv(voltage_file, sep='\s+', names=["RunNumber", "Voltage"])
            voltage_data = voltage_data[~voltage_data["RunNumber"].isin([20005, 20011])]

            # Merge data
            merged = eff_data.merge(voltage_data, on="RunNumber", how="left")

            # Filter efficiencies < 0.9
            low_eff = merged[merged["Efficiency"] < 0.9].copy()

            # Identify zero-voltage runs
            zero_voltage = low_eff[low_eff["Voltage"] == 0] if "Voltage" in low_eff.columns and not low_eff["Voltage"].isna().all() else pd.DataFrame()

            # Save comparison
            with open(output_file, "w") as f_out:
                f_out.write(f"Tile S{sector} L{layer} (Efficiency < 0.9):\n")
                f_out.write("Note: Voltage data may be missing or zero for some runs.\n")
                if not zero_voltage.empty:
                    f_out.write("Zero Voltage Runs:\n")
                    for _, row in zero_voltage.iterrows():
                        run = row["RunNumber"]
                        eff = row["Efficiency"]
                        f_out.write(f"Run {run}, Efficiency {eff:.3f}, Voltage 0.000 V\n")
                f_out.write("Other Runs (Efficiency < 0.9):\n")
                for _, row in low_eff.iterrows():
                    run = row["RunNumber"]
                    eff = row["Efficiency"]
                    voltage = row["Voltage"]
                    if pd.isna(voltage):
                        f_out.write(f"Run {run}, Efficiency {eff:.3f}, Voltage: Missing\n")
                    elif voltage != 0:
                        f_out.write(f"Run {run}, Efficiency {eff:.3f}, Voltage {voltage:.3f} V\n")

            # Create plot
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
            ax2.plot(low_eff["RunNumber"].to_numpy(), low_eff["Voltage"].to_numpy(), marker="o", markersize=3, alpha=0.6, color="red", label="Voltage")
            if not zero_voltage.empty:
                ax2.plot(zero_voltage["RunNumber"].to_numpy(), np.zeros(len(zero_voltage)), marker="s", markersize=8, color="purple", linestyle="", label="Zero Voltage")
            ax2.tick_params(axis="y", labelcolor="red")
            ax2.set_ylim(0, max(low_eff["Voltage"].max() if not pd.isna(low_eff["Voltage"].max()) else 600, 600) + 100)
            ax2.grid(True, linestyle="--", alpha=0.7)

            plt.title(f"Efficiency and Voltage vs Run Number for S{sector} L{layer} (Efficiency < 0.9)", pad=15)
            fig.tight_layout()

            # Save TikZ code to a temporary string and write to LaTeX file
            tikz_code = tikzplotlib.get_tikz_code(figure=fig)
            f_tex.write(f"\\clearpage\n")
            f_tex.write(f"\\section{{Tile S{sector} L{layer}}}\n")
            f_tex.write(f"\\begin{{figure}}[h]\n")
            f_tex.write(f"\\centering\n")
            f_tex.write(tikz_code)
            f_tex.write(f"\\caption{{Efficiency and Voltage vs Run Number for S{sector} L{layer} (Efficiency < 0.9)}}\n")
            f_tex.write(f"\\end{{figure}}\n")
            plt.close()

    f_tex.write("\\end{document}\n")

# Compile LaTeX to PDF
import os
os.system("latexmk -pdf /w/hallb-scshelf2102/clas12/suman/SW_25/test/efficiency_voltage_report.tex")