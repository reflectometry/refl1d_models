"""
Hydration model example. This model shows an example of a film with a solvent
penetrating into the surface layer. The SLD of the surface layer is a linear
combination of the SLD of the base material and the solvent, according to a
hydration parameter.

$$ \rho_{top} = (1 - f) \rho_{base} + f \rho_{solvent} $$

where $f$ is the hydration parameter.
"""

import numpy as np
from refl1d.names import SLD, Experiment, FitProblem, Parameter, QProbe

# Probe ########################################################################
# This is where you also load your data
q = np.logspace(np.log10(0.009), np.log10(0.18), num=150)
dq = 0.025 * q / 2.35

probe = QProbe(q, dq)

# Materials ####################################################################
silicon = SLD(name="Si", rho=2.07, irho=0.0)
d2o = SLD(name="D2O", rho=6.13, irho=0.0)
titanium = SLD(name="Ti", rho=-1.238, irho=0.0)
copper = SLD(name="Cu", rho=6.446, irho=0.0)
material = SLD(name="material", rho=-1.648, irho=0.1)
sei = SLD(name="SEI", rho=4.581, irho=0.1)

# Film definition ##############################################################
sample = (
    d2o(0, 43.77) | sei(177.7, 23.04) | material(21.73, 18.22) | copper(566.1, 9.736) | titanium(52.91, 12.7) | silicon
)

# Parameter ranges #############################################################
sample["Ti"].thickness.range(20.0, 60.0)
sample["Ti"].material.rho.range(-2.0, 0.0)
sample["Ti"].interface.range(1.0, 20.0)
sample["Cu"].thickness.range(10.0, 800.0)
sample["Cu"].interface.range(8.0, 15.0)
sample["material"].thickness.range(15.0, 100.0)
sample["material"].material.rho.range(-3.0, 8.0)
sample["material"].interface.range(1.0, 35.0)
sample["SEI"].thickness.range(100.0, 300.0)
sample["SEI"].interface.range(5.0, 25.0)

# Define a base SLD value for the SEI layer
base_sld = Parameter(value=3, name="base_sld").range(-3.0, 8.0)

# Define a solvent penetration parameter for the SEI layer
solvent_penetration = Parameter(value=0.0, name="penetration").range(0, 1)

# The SLD of the SEI layer is a linear combination of the base SLD and the solvent SLD,
# according to the solvent penetration parameter
sample["SEI"].material.rho = base_sld * (1 - solvent_penetration) + sample["D2O"].material.rho * solvent_penetration

# The probe has a normalization parameter and a background parameter
probe.intensity = Parameter(value=1.0, name="normalization")
probe.background.range(0.0, 1e-05)
sample["D2O"].interface.range(25.0, 150.0)

# Create the experiment and the problem objects
experiment = Experiment(probe=probe, sample=sample)
problem = FitProblem(experiment)
