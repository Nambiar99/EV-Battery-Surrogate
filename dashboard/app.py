import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from trame.app import get_server
from dashboard.visuals import Battery
from dashboard.ui import build_main_ui
from dashboard.utils import initialize
from models.call_GPR import return_temps, load_models

server = get_server()
server.title = "Battery Surrogate"
state, ctrl = server.state, server.controller
gpr_models, x_scalers = load_models()
initialize(state)
battery = Battery(state)


config = {
	"mesh_file": PROJECT_ROOT / "assets" / "battery.msh"
}

def run_sim():
	global inputs, results_temps, results_temps_std
	validate_inputs(state)
	inputs = np.array([[
		state.input_velocity, state.inlet_temp, state.battery_temp,
		*state.cooler_temp
	]])
	results_temps, results_temps_std = return_temps(inputs, gpr_models, x_scalers)
	stacked_temps = np.hstack((state.inlet_temp, results_temps))
	state.results_temps = stacked_temps.tolist()
	stacked_temps_std = np.hstack(([0.0], results_temps_std))
	state.results_temps_std = stacked_temps_std.tolist()
	battery.update_results(state)
	ctrl.view_update()
	
def validate_inputs(state):
	inputs = np.array([
			state.input_velocity, state.inlet_temp, state.battery_temp,
			*state.cooler_temp
		])
	inputs = inputs.astype(float)
	cooler_valid = all(5 <= num <= 15 for num in inputs[3:])
	conditions = [
		1 < inputs[0] < 3,
		15 < inputs[1] < 20,
		30 < inputs[2] < 35,
		cooler_valid
	]
	if not any(conditions):
		initialize(state)




ctrl.run_sim = run_sim



if __name__ == "__main__":
	
	build_main_ui(server, state, ctrl, config, battery)
	server.start(port=1234)