import os
import aircraft
import numpy as np
import sharpy.utils.algebra as algebra
from helper_functions.get_settings import get_settings


cases_route = '../01_case_files/01_case_files/'
output_route = './output/'

case_name = 'flexop_sigma_03_free_flight_linear'


# Trim values for SuperFLEXOP
trim_values = {'alpha':6.796482976011756182e-03, 
                'delta':-1.784287512500099069e-03,
                'thrust': 2.290077074834680371e+00
                }

lifting_only = True # ignore nonlifting bodies
wing_only = False # Wing only or full configuration (wing+tail)
dynamic = True 
use_rom = False

flow = [
        'BeamLoader', 
        'Modal',
        'AerogridLoader',
        'StaticCoupled',
        # 'StaticTrim',     
        'DynamicCoupled',
        'Modal',
        'LinearAssembler',
        # 'AsymptoticStability',
        'SaveData',
]

# Set cruise parameter
alpha = trim_values['alpha'] # rad
u_inf = 45 
rho = 1.1336 # corresponds to an altitude of 800  m
gravity =  True
horseshoe =  False 
wake_length = 10
cfl1 = True 
free_flight = True
cs_deflection = trim_values['delta'] # rad
cs_deflection_initial = cs_deflection 
thrust = trim_values['thrust'] 
num_modes = 21
num_chord_panels = 8
n_elem_multiplier = 2

# Init FLEXOP Model
flexop_model = aircraft.FLEXOP(case_name, cases_route, output_route)
flexop_model.clean()
flexop_model.init_structure(sigma=0.3, # SuperFLEXOP 0.3, ModifiedFLEXOP 1.
                            n_elem_multiplier=n_elem_multiplier, # Discretisation of wing and tail
                            n_elem_multiplier_fuselage = 1, # Discretisation of fuselage beam
                            lifting_only=lifting_only, 
                            wing_only = wing_only) 

flexop_model.init_aero(m=num_chord_panels, cs_deflection = cs_deflection) 
flexop_model.structure.set_thrust(thrust)
#  Simulation settings
CFL = 1
dt = CFL * flexop_model.aero.chord_main_root / flexop_model.aero.m / u_inf
# numerics
n_step = 5
structural_relaxation_factor = 0.6
relaxation_factor = 0.2
tolerance = 1e-6
fsi_tolerance = 1e-4
num_cores = 4
newmark_damp = 0.5e-4
n_tstep = 1 

# ROM settings
rom_settings = {
    'use': use_rom,
    'rom_method': ['Krylov'],
    'rom_method_settings': {'Krylov': {
                                        'algorithm': 'mimo_rational_arnoldi',
                                        'r': 4, 
                                        'frequency': np.array([0]),
                                        'single_side': 'observability',
                                        },
                           }
                }
# Get settings dict
settings = get_settings(flexop_model,
                        flow,
                        dt,
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
                        n_tsteps = n_tstep,
                        num_modes = num_modes,
                        rom_settings = rom_settings)

# Generate finale FLEXOP model
flexop_model.generate()
flexop_model.create_settings(settings)
flexop_model.run()