"""
This module provides an example of a mixed model.
In this example, we incoherently add two cross-sections
from a non-polarized neutron reflectometry experiment on
a nickel film.
"""

from refl1d.names import SLD, FitProblem, MixedExperiment

from .probes import create_qprobe


def create_mixed_model(datafile: str = None):
    """
    Create a mixed model for the given datafile
    :param datafile: The datafile to use for the model
    """

    # Define a probe
    probe = create_qprobe(datafile)

    # Define the materials for the structure
    # The SLD class defines the material properties.
    # The rho parameter is the scattering length density of the material.
    thf = SLD("THF", rho=6.2)
    silicon = SLD("Si", rho=2.07)
    titanium = SLD("Ti", rho=-2.0)

    # In this exammple, we are using the same material for the up and down spins
    # In this case, nickel has a nominal SLD of 9.4 +- 1.46 for the two spin states
    nickel_up = SLD("Ni_up", rho=8.3)
    nickel_down = SLD("Ni_down", rho=10.4)

    # Here we will add an oxide layer on top of the nickel
    material = SLD(name="material", rho=5.6)

    # Create the sample structure
    # In this case the incoming beam is coming through the Si substrate
    sample_up = thf(0, 5) | material(34, 20) | nickel_up(555, 10) | titanium(50, 3) | silicon
    sample_down = thf(0, 5) | material(34, 20) | nickel_down(555, 10) | titanium(50, 3) | silicon

    # Create a MixedExperiment. We provide the two samples, the probe, the ratio of the contribution
    # of the two samples, and whether the two samples are coherently added or not.
    experiment = MixedExperiment(samples=[sample_up, sample_down], probe=probe, ratio=[1, 0.75], coherent=False)

    # Define the range of the parameters
    sample_down["THF"].material.rho.range(5.5, 7)
    sample_down["THF"].interface.range(1, 25)

    sample_up["Ni_up"].material.rho.range(5, 12)
    sample_down["Ni_down"].material.rho.range(5, 12)
    sample_down["Ni_down"].interface.range(1, 25)
    sample_down["Ni_down"].thickness.range(400, 600)

    sample_down["Ti"].thickness.range(10.0, 80.0)
    sample_down["Ti"].material.rho.range(-3.0, 0)
    sample_down["Ti"].interface.range(1.0, 23.0)

    sample_up["Ti"].thickness = sample_down["Ti"].thickness
    sample_up["Ti"].interface = sample_down["Ti"].interface
    sample_up["Ti"].material.rho = sample_down["Ti"].material.rho

    sample_down["material"].thickness.range(10.0, 50.0)
    sample_down["material"].material.rho.range(1.0, 6)
    sample_down["material"].interface.range(1.0, 33.0)

    sample_up["material"].thickness = sample_down["material"].thickness
    sample_up["material"].interface = sample_down["material"].interface
    sample_up["material"].material.rho = sample_down["material"].material.rho

    probe.intensity.range(0.8, 1.5)

    sample_up["Ni_up"].thickness = sample_down["Ni_down"].thickness
    sample_up["Ni_up"].interface = sample_down["Ni_down"].interface

    # Choose a range on the ratio of the two samples
    experiment.ratio[1].range(0, 5)

    # Create a FitProblem
    problem = FitProblem(experiment)

    return problem, experiment


# The following is only necessary so this python file can be
# used as a model with the refl1d cli.
problem, _ = create_mixed_model()
