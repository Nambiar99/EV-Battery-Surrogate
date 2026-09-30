import numpy as np
import joblib
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.gaussian_process.kernels import (ConstantKernel, Matern, WhiteKernel)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_model(X, y, len_x, file_name):
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

	x_scaler = StandardScaler()
	X_train_scaled = x_scaler.fit_transform(X_train)
	X_test_scaled = x_scaler.transform(X_test)
	print(x_scaler.mean_)

	kernel = (ConstantKernel(1.0, (1e-3,1e3)) * 
			Matern(length_scale=np.ones(len_x),length_scale_bounds=(1e-2,1e4)) + 
			WhiteKernel(noise_level=1e-3, noise_level_bounds=(1e-10,1e1)))

	model = GPR(kernel=kernel, 
				normalize_y=True, 
				n_restarts_optimizer=5, 
				random_state=42)
	model.fit(X_train_scaled, y_train)

	joblib.dump(model, file_name)
	scaler_file_name = file_name.with_name(file_name.stem + "_scaler.joblib")
	joblib.dump(x_scaler, scaler_file_name)
	print(f"{file_name} model and scaler saved.")

	y_pred, y_std = model.predict(X_test_scaled, return_std=True)
	mae = mean_absolute_error(y_test, y_pred)
	rmse = np.sqrt(mean_squared_error(y_test, y_pred))
	r2 = r2_score(y_test, y_pred)

	return mae, rmse, r2, y_test, y_pred, y_std