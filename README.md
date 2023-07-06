# flexop_rom_student_project

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
source <path-to-flexop-model>/bin/flexop_vars.sh
```

Now, the user should be all set to either run a nonlinear aeroelastic gust response study of the (Super)Flexop with 'run_nonlinear_simulation.py' or generate linear full-order order reduced-order model of this model with 'generate_linear_system.py'.

## Postprocessors



## References

[1] Duessler, S., & Palacios. A Control Design Framework for Gust Load Alleviation in more Flexible Aircraft. IFASD, 2022.

## Contact

If you have any questions and want to get in touch, 
[contact us](https://www.imperial.ac.uk/aeroelastics/people/duessler/).

If you have any questions on how to use the model or find any bugs please file an issue. 