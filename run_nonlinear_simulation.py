import flexop as aircraft
import os
from helper_functions.get_settings import get_settings

"""
    TThis script includes all the necessary steps to start a dynamic simulation of the Flexop or Superflexop, 
    namely:
    1) Specifying several main parameters, such as case name, aircraft model options, etc. 
    2) Defining the gust velocity field, e.g. 1-cosine gust or continuous turbulence. 
    3) Define pre-defined control surface deflection if needed.
    4) Set flight conditions.
    5) Specify parameters to control the lattice grid discretisation. The values used here lead to sufficient 
       convergence for dynamic gust response simulations of the FLEXOP.
    6) The aircraft model is initialized and saved as an object. 
    7) Other parameters dependent on the model geometry and discretisation are defined.
    8) Some numerical parameters for the structural solver are specified. 
    9) The solvers used and their order within a simulation is set, known as SHARPy's 'flow'.
    10) SHARPy's final simulation settings are defined using the parameters specified in the 
       previous steps. For more information about each solver, please check our documentation
       (https://ic-sharpy.readthedocs.io/en/latest/content/solvers.html).
    11) All required SHARPY input files are written, i.e. structural and aerodynamic models as well as simulation settings.
    12) Finally, the simulation starts.

    Important to note is that 1) to 3) include the parameters the user likes to specify for its individual gust simulation. 
    Most other parameters are very general or successfully tested/verified.

"""

# 1) Specify main parameters
case_name = 'superflexop_free'
lifting_only = True # ignore nonlifting bodies
wing_only = False # Wing only or full configuration (wing+tail)
wake_discretisation = False # Wake discretisation (reduces the simulation time by about 20 %)
use_trim = False # If trim values are known, they can be insert in the dictionary below. Please double check values!

factor_material_stiffness = 0.3 # Modified Flexop: 1.0, SuperFlexop: 0.3
num_cores = 4
simulation_time = 2*60 # 2 min

free_flight = True # True: Free-flight; False: clamped
gravity = True

# 2) Specify Gust velocity field
use_gust = True
gust_settings  = {
    'gust_shape': '1-cos',
    'gust_length': 10.,
    'gust_intensity': 0.1,
    }
"""
    Example for continuous gust input:
    gust_settings  = {
        'gust_shape': 'time varying',
        'file': <insert_path_to_velocity_field_input>, # File includes time series of gust velocities, i.e. 4 columns: time[s]  U_x U_y U_z
        'gust_component': [2], # list of velocity components considered (0: U_x, 1: U_y, 2: U_z)
        }    

"""

# 3) Define dynamic control surface input
dynamic_cs_input = False # True if pre-defined control surface deflection used
if dynamic_cs_input:
    route_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

    dict_predefined_cs_input_files = {
        '0' : None, # aileron 1 (inboard right)
        '1' : None, # aileron 2
        '2' : None, # aileron 3
        '3' : route_dir + '/deflection_input_files/deflection_input_outboard_aileron.csv', # aileron 4 (outboard right)
        '4' : None, # elevator 1 (inboard right)
        '5' : None, # elevator 2 (outboard right)
        '6' : None, # aileron 5 (inboard left)
        '7' : None, # aileron 6
        '8' : None, # aileron 7
        '9' :  route_dir + '/deflection_input_files/deflection_input_outboard_aileron.csv', # aileron 8 (outboard left)
        '10' : None, # elevator 3 (inboard left)
        '11' : None, # elevator 4 (outboard left))
    }
    ailerons_type = [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
else:
    ailerons_type = 0


# 4) Set cruise parameter SuperFlexop
trim_values = {'alpha':6.796482976011756182e-03, 
                'delta':-1.784287512500099069e-03,
                'thrust': 2.290077074834680371e+00
                }

alpha =  trim_values['alpha'] 
u_inf = 45 
rho = 1.1336 # corresponds to an altitude of 800  m
cs_deflection = trim_values['delta']
thrust = trim_values['thrust'] 

# 5) Discretisation parameters (sufficient convergence for dynamic simulations)
num_chord_panels = 8
n_elem_multiplier = 2 
horseshoe =  False 
wake_length = 10
cfl1 = not wake_discretisation

# 6) Init aircraft model
cases_route = './cases/'
output_route = './output/'
flexop_model = aircraft.FLEXOP(case_name, cases_route, output_route)
flexop_model.clean()
flexop_model.init_structure(sigma=factor_material_stiffness, 
                            n_elem_multiplier=n_elem_multiplier, 
                            n_elem_multiplier_fuselage = 1, 
                            lifting_only=lifting_only, 
                            wing_only = wing_only) 
flexop_model.init_aero(m=num_chord_panels,
                       cs_deflection = cs_deflection,
                       ailerons_type = ailerons_type) 
flexop_model.structure.set_thrust(thrust)

# 7) Other parameters
CFL = 1
dt = CFL * flexop_model.aero.chord_main_root / flexop_model.aero.m / u_inf
gust_settings['gust_offset'] = 10 * dt *u_inf # Gust encounters starts 10 ts after simulation start
number_timesteps = int(simulation_time / dt)

# 8) Structural parameters
structural_relaxation_factor = 0.6
relaxation_factor = 0.2
tolerance = 1e-6 
fsi_tolerance = 1e-4 
newmark_damp = 0.5e-4

# 9) Define SHARPy flow
flow = ['BeamLoader', 
        'AerogridLoader',
        'StaticCoupled',
        'StaticTrim',
        'BeamLoads',
        'BeamPlot',
        'AerogridPlot',
        'AeroForcesCalculator',
        'DynamicCoupled',
]
postprocessor_each_timestep = ['BeamLoads', 'SaveData'] #, 'AerogridPlot',  'BeamPlot']
if use_trim:    
    flow.remove('StaticCoupled')
else:
    flow.remove('StaticTrim')

                
# 10) Get settings dict
settings = get_settings(flexop_model,
                        flow,
                        dt,
                        gust = use_gust,
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
                        n_tstep = number_timesteps,
                        postprocessor_each_timestep=postprocessor_each_timestep,
                        dynamic_cs_input = dynamic_cs_input,
                        dict_predefined_cs_input_files = dict_predefined_cs_input_files                                
                        )

# 11) Generate all required input files for a SHARPy simulation
flexop_model.generate()
flexop_model.structure.calculate_aircraft_mass()
flexop_model.create_settings(settings)

# 12) Run simulation
flexop_model.run()