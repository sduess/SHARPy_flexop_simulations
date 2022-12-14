import os
import aircraft
import numpy as np
import sharpy.utils.algebra as algebra
from helper_functions.get_settings import get_settings

cases_route = '../../01_case_files/'
output_route = './output/'

case_name = 'flexop_clamped_L_10_I_10_test'


lifting_only = True # ignore nonlifting bodies
wing_only = False # Wing only or full configuration (wing+tail)
dynamic = True 
controllable = False # needed when nonlinear in closed-loop
wake_discretisation = False 
symmetry_condition =  False 

flow = ['BeamLoader', 
        'AerogridLoader',
        'AerogridPlot',
        'BeamPlot',
        'StaticCoupled',
        # 'StaticTrim',
        'BeamPlot',
        'AerogridPlot',
        'AeroForcesCalculator',
        'DynamicCoupled',
]

# Set cruise parameter
trim_values = {'alpha':6.796482976011756182e-03, 
                'delta':-1.784287512500099069e-03,
                'thrust': 2.290077074834680371e+00
                }

alpha =  trim_values['alpha'] 
u_inf =45 
rho = 1.1336 # corresponds to an altitude of 800  m
gravity = True
horseshoe =  False 
wake_length = 10 #5
cfl1 = not wake_discretisation
free_flight = False # False: clamped
cs_deflection = trim_values['delta']
thrust = trim_values['thrust'] 

num_chord_panels = 8
n_elem_multiplier = 2 

flexop_model = aircraft.FLEXOP(case_name, cases_route, output_route)
flexop_model.clean()
flexop_model.init_structure(sigma=0.3, 
                            n_elem_multiplier=n_elem_multiplier, 
                            n_elem_multiplier_fuselage = 1, 
                            lifting_only=lifting_only, wing_only = wing_only, 
                            symmetry_condition = symmetry_condition) 
flexop_model.init_aero(m=num_chord_panels, cs_deflection = cs_deflection, controllable = controllable) 
flexop_model.structure.set_thrust(thrust)

# Other parameters
CFL = 1
dt = CFL * flexop_model.aero.chord_main_root / flexop_model.aero.m / u_inf
# numerics
n_step = 5
structural_relaxation_factor = 0.6
relaxation_factor = 0.2
tolerance = 1e-6 
fsi_tolerance = 1e-4 
num_cores = 8
newmark_damp = 0.5e-4
n_tstep = 250


# Gust velocity field
gust_settings  ={'gust_shape': '1-cos',
                'gust_length': 10.,
                'gust_intensity': 0.1,
                'gust_offset': 10 * dt *u_inf}
                
# Get settings dict
settings = get_settings(flexop_model,
                        flow,
                        dt,
                        gust = True,
                        gust_settings = gust_settings,
                        alpha = alpha,
                        cs_deflection = cs_deflection,
                        u_inf = u_inf,
                        rho = rho,
                        thrust = thrust,
                        wake_length = wake_length,
                        free_flight = free_flight,
                        num_cores = num_cores,
                        tolerance = tolerance,
                        fsi_tolerance = fsi_tolerance,
                        structural_relaxation_factor = structural_relaxation_factor,
                        newmark_damp = newmark_damp,
                        n_tstep = n_tstep                                
                        )

flexop_model.generate()
flexop_model.structure.calculate_aircraft_mass()
flexop_model.create_settings(settings)
flexop_model.run()