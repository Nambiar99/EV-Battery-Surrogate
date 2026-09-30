import numpy as np

def initialize(state):
	state.results_figure = None
	state.input_velocity = 1
	state.inlet_temp = 15
	state.battery_temp = 30
	state.cooler_temp = [5, 5, 5, 5, 5, 5, 5]
	state.results_temps = [0.0] * 16
	state.results_temps_std = [0.0] * 16
	