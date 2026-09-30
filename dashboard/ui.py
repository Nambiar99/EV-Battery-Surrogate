import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pyvista as pv
import plotly as ply
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vuetify3 as v3
from trame.widgets import html, client
from trame.widgets import plotly as ply_widget
from trame.widgets import pyvista as pv_widget
from trame.widgets import vtk
from pyvista.trame.ui import plotter_ui

css_path = PROJECT_ROOT / "dashboard" / "style.css"
pv.set_jupyter_backend('trame')
pv.global_theme.trame.default_mode = 'client'

def build_main_ui(server, state, ctrl, config, battery):
	with VAppLayout(server) as layout:
		with layout.root:
			html.Script("document.title = 'Battery Surrogate';")
			client.Style(css_path.read_text())
			with v3.VApp() as app:
				with v3.VAppBar(color="#343333", elevation=2, density="default"):
					v3.VAppBarNavIcon(icon="mdi-battery-charging")
					v3.VToolbarTitle("Battery Surrogate Dashboard", classes="text-h6 font-weight-bold")
					v3.VSpacer()
					v3.VChip("Client-Side Rendering Active", color="white", variant="outlined", size="small", classes="mr-4")
				with v3.VMain():
					with html.Div(classes="dashboard"):
						with html.Div(classes="sidebar"):
							ui_build_sidebar(ctrl)
						with html.Div(classes="main"):
							ui_build_viewers(state, config, battery, ctrl)

def ui_build_viewers(state, config, battery, ctrl):
	with html.Div(classes="top-container"):
		with html.Div(classes="mesh-container"):
			ui_build_mesh(config)
		with html.Div(classes="temp-results-container"):
			ui_build_temp_results()
	with html.Div(classes="results-container"):
		ui_build_results(battery, ctrl)
		
def ui_build_geometry(config):
	plotter = pv.Plotter(off_screen=True)
	geo = pv.read_meshio(config["geo_file"])
	plotter.add_mesh(geo, show_edges=True)
	plotter_ui(plotter, mode="client")

def ui_build_mesh(config):
	plotter = pv.Plotter(off_screen=True)
	geo = pv.read_meshio(config["mesh_file"])
	plotter.add_mesh(geo, show_edges=True)
	plotter_ui(plotter, mode="client")
	
def ui_build_results(battery, ctrl):
	view = ply_widget.Figure(battery.results_figure,)
	ctrl.view_update = view.update
	# ctrl.reset_camera = battery.reset_camera
	
def ui_build_sidebar(ctrl):
	v3.VTextField(
		v_model=("input_velocity",),
		label="Input Velocity",
		hide_details=True,
		classes="param-box",
	)
	v3.VTextField(
		v_model=("inlet_temp",),
		label="Inlet Temperature",
		hide_details=True,
		classes="param-box",
	)
	v3.VTextField(
		v_model=("battery_temp",),
		label="Battery Temperature",
		hide_details=True,
		classes="param-box",
	)
	for i in range(7):
		v3.VTextField(
			v_model=(f"cooler_temp[{i}]",),
			label=f"Cooler {i+1} Temperature",
			hide_details=True,
			classes="param-box",
			change="flushState('cooler_temp')",
		)
	v3.VBtn(
		"Run",
		block=True,
		classes="button",
		click=ctrl.run_sim
	)

def ui_build_temp_results():
	with v3.VRow():
		for i in range(16):
			battery_num = (i // 2) + 1
			direction = "INLET" if i % 2 == 0 else "OUTLET"
			with v3.VCol(cols=6):
				v3.VTextField(
					model_value=(f"`${{results_temps[{i}]}} ± ${{results_temps_std[{i}]}} °C`",),
					label=f"Battery {battery_num} {direction} Temperature",
					hide_details=True,
					classes="param-box",
					readonly=True,
					change="flushState('cooler_temp')",
				)
