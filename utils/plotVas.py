import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Read the Excel file (requires openpyxl: pip install openpyxl)
file_path = "../data/data.xlsx"
df = pd.read_excel(file_path)

# Clean column names just in case there are extra spaces
df.columns = df.columns.str.strip()


# 2. Function to plot and fit a 2nd-order regression for target subject(s)
def plot_subject_regression(data: pd.DataFrame, subjects: list[int]):
    sub_df = data[data["Subject"].isin(subjects)].copy()

    if sub_df.empty:
        print(f"No data found for Subject(s): {subjects}")
        return

    plt.figure(figsize=(8, 5))

    for subj, group in sub_df.groupby("Subject"):
        x = group["Speed"].to_numpy(dtype=float)
        y = group["Rate"].to_numpy(dtype=float)

        # Scatter plot of raw observations
        scatter = plt.scatter(x, y, label=f"Subject {subj} (data)", s=80, color="#c4a008")
        # color = scatter.get_facecolor()[0]

        # Fit 2nd-order polynomial: y = a*x^2 + b*x + c (requires at least 3 points)
        if len(np.unique(x)) >= 3:
            coeffs = np.polyfit(x, y, deg=2)
            poly = np.poly1d(coeffs)
            a, b, c = coeffs

            # Smooth curve across the Speed range
            x_smooth = np.linspace(x.min(), x.max(), 200)
            y_smooth = poly(x_smooth)

            y_pred = poly(x)
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else np.nan

            eq_str = f"y = {a:.3f}x² + {b:.3f}x + {c:.3f}"
            plt.plot(
                x_smooth,
                y_smooth,
                color='#c1819e',
                linestyle="--",
                linewidth=3,
                #label=f"Subject {subj} fit: {eq_str} (R²={r2:.2f})",
            )
            print(f"Subject {subj}: {eq_str} | R² = {r2:.4f}")
        else:
            print(f"Subject {subj}: Not enough unique Speed values for 2nd-order fit.")

    plt.title(f"Pleassantness")
    plt.xlabel("Speed (cm/s)")
    plt.ylabel("Rate")
    # plt.xlim([1,22])
    plt.grid(True, linestyle=":", alpha=0.6)
    # plt.xticks([3,10,20])
    # plt.legend()
    plt.tight_layout()
    plt.show()


# --- Examples ---
target_subject = 13
plot_subject_regression(df, [target_subject])

# Multiple subjects together (e.g., 1 and 2):
# plot_subject_regression(df, [7, 8])

## Do results impact on the next one??
