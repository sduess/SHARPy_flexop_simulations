# SHARPy Simulations of the SuperFlexop

This repository contains scripts to simulate the nonlinear aeroelastic gust response of the (Super)Flexop with SHARPy, and to generate a linearized version (plus optional reduced-order model) of this aircraft model. 

Both, the nonlinear aeroelastic simulation environment [SHARPy](http://github.com/imperialcollegelondon/sharpy) and the SHARPy version of the [(Super)Flexop model](http://github.com/sduess/flexop_model) are included in this repository as submodules.


## Installation

Clone the repository to your local computer. Navigate into the sharpy folder 
```bash
cd <path-to-repository>/lib/sharpy
```
and install SHARPy as described in the [documentation](https://ic-sharpy.readthedocs.io/en/latest/content/installation.html). 

## Running Simulations
First, activate SHARPy's conda environment and append the location of the `flexop-model` folder to the system's path with
```bash
source <path-to-flexop-model>/bin/FLEXOP_vars.sh
```

Now, the user should be all set to either run a nonlinear aeroelastic gust response study of the (Super)Flexop with 
```bash
python <path-to-repository>/run_nonlinear_simulation.py
```
or generate a linear full-order order reduced-order model of this model with 
```bash
python <path-to-repository>/generate_linear_system.py
```
Note that both scripts contain several parameters to be specified by the user.

## Postprocessors

An example postprocessor script is added to the repo. This script exports displacement and rotation of the tip node as well as the wing root bending and torsional moments computed for each timestep of a gust response simulation saved under a given case name.

## Copyleft

We are happy to share our effort with the community and we welcome contributions to the code base. If you found this dataset useful we would ask you to cite the references below in any publications or reports based on it.

## References

[1] Duessler, S., & Palacios, R.. LQG-based Gust Load Alleviation Systems for Very Flexible Aircraft. AIAA SciTech, 2023.

[2] Duessler, S., & Palacios, R.. Enhanced Unsteady Vortex Lattice Aerodynamics for Nonlinear Flexible Aircraft Dynamic Simulation. AIAA Journal, 2023. *to appear*

## Contact

If you have any questions and want to get in touch, 
[contact us](https://www.imperial.ac.uk/aeroelastics/people/duessler/).

If you have any questions on how to use the model or find any bugs please file an issue. 
