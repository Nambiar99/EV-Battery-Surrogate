import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler



def load_models():
	PROJECT_ROOT = Path(__file__).resolve().parents[1]
	gpr_model_folder = PROJECT_ROOT / "gpr_models" 
	gpr_models = [joblib.load(file) 
	              for file in sorted(gpr_model_folder.glob("*.joblib"))
				  if "_scaler" not in file.name]
	x_scalers = [joblib.load(file) for file in sorted(gpr_model_folder.glob("*_scaler.joblib"))]
	return gpr_models, x_scalers


def return_temps(inputs, gpr_models, x_scalers):
	print(len(x_scalers))
	k = 0
	results_temps = []
	results_temps_std = []
	for i in range(15):
		model = gpr_models[i]
		scaler = x_scalers[i]
		if i > 0 and i % 2 != 0:
			k += 1
		X = inputs[:,:3 + k]
		X_scaled = scaler.transform(X)
		y_pred , y_std = model.predict(X_scaled, return_std=True)
		results_temps.append(round(float(y_pred[0]), 2))
		results_temps_std.append(round(float(y_std[0]), 2))

	return results_temps, results_temps_std