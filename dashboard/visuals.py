import numpy as np
import plotly.graph_objects as go
import pyvista as pv
from trame.widgets import plotly as ply_widget
from trame.widgets import pyvista as pv_widget

class Battery:
	def __init__(self, state):
		self.input = state.input
		self.x = []
		self.results_figure = go.Figure()
		self.temp_gains : float = []
		

		self._build_x()
		self._build_temp_gains(state)
		self._build_scene()

	def _build_x(self):
		for i in range(8):
			self.x.append(f"Battery {i+1}")

	def _build_temp_gains(self, state):
		temps = state.results_temps
		for i in range(len(temps)):
			if i % 2 == 0:
				self.temp_gains.append(temps[i+1] - temps[i])
	
	def _build_scene(self):		
		self.results_figure.add_trace(
			go.Bar(
				x=self.x,
				y=self.temp_gains,
				name="Temperature Change in Batteries"
			)
		)
		self.results_figure.update_layout(
			title="Temeperate Gain in Batteries",
			xaxis_title="Battery",
			yaxis_title="Temperature Change (°C)",
			margin=dict(l=40, r=20, t=50, b=40)
		)

	def update_results(self, state):
		temps = state.results_temps
		self.temp_gains: float = []
		for i in range(len(temps)):
			if i % 2 == 0:
				self.temp_gains.append(temps[i+1] - temps[i])
		self.results_figure.data[0].y = self.temp_gains

	def reset_camera(self):
		self.results_figure.update_xaxes(autorange=True)
		self.results_figure.update_yaxes(autorange=False)
	
