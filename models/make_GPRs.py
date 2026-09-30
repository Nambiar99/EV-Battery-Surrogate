import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from models.utils import train_model

from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.gaussian_process.kernels import (ConstantKernel, Matern, WhiteKernel)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = PROJECT_ROOT / "data" / "thermal_data.csv"
PLOT_PATH = PROJECT_ROOT / "plots"

INPUT_COLUMNS = [
	"inlet_velocity",
	"inlet_temp",
	"battery_temp",
	"cooler_1_temp",
	"cooler_2_temp",
	"cooler_3_temp",
	"cooler_4_temp",
	"cooler_5_temp",
	"cooler_6_temp",
	"cooler_7_temp",
]

TARGET = [
	"b1_out",
	"b2_in",
	"b2_out",
	"b3_in",
	"b3_out",
	"b4_in",
	"b4_out",
	"b5_in",
	"b5_out",
	"b6_in",
	"b6_out",
	"b7_in",
	"b7_out",
	"b8_in",
	"b8_out"
	]

df = pd.read_csv(DATA_PATH)

k = 0
metrics = []

fig, axs = plt.subplots(4,4, figsize=(20,10))
axs_flat = axs.ravel()


for i in range(15):
	if i > 0 and i % 2 != 0:
		k += 1
	INPUT = INPUT_COLUMNS[:3 + k]
	X = df[INPUT].values
	y = df[TARGET[i]].values - 273.15
	model_name = "GPR_" + str(TARGET[i]) + ".joblib"
	file_name = PROJECT_ROOT / "gpr_models" / str(model_name)
	mae, rmse, r2, y_test, y_pred, y_std = train_model(X, y, len(INPUT), file_name)
	metrics.append({
		"model_name": model_name,
		"MAE": mae,
		"RMSE": rmse,
		"R2": r2
	})
	axs_flat[i].errorbar(y_test, y_pred, yerr=2*y_std, fmt="o", alpha=0.8, capsize=3)
	minimum = min(y_test.min(), y_pred.min())
	maximum = max(y_test.max(), y_pred.max())

	axs_flat[i].plot([minimum, maximum], [minimum, maximum], "--")
	axs_flat[i].set_xlabel(f"Actual {TARGET[i]} (°C)")
	axs_flat[i].set_ylabel(f"Predicted {TARGET[i]} (°C)")
	axs_flat[i].set_title(f"GPR PRediction: {TARGET[i]}")

fig.suptitle("GPR Error Plots")
plt.tight_layout()
plot_file = PLOT_PATH / "gpr_error_plot.png"
plt.savefig(plot_file, dpi=300)
plt.show()
df_metrics = pd.DataFrame(metrics)
df_metrics.to_csv(PLOT_PATH / "gpr_models.csv")
print(df_metrics)


