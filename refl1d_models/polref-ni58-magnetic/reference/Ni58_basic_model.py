from refl1d.names import *
from copy import copy
import numpy as np
import sys
import os
from types import MethodType
from numpy import inf
from refl1d.probe.probe import make_probe
from bumps.parameter import Parameter
from bumps.util import push_seed
from refl1d.probe.resolution import FWHM2sigma
from pathlib import Path

def logstep(start, stop, step, base=10.0):
    """
    Creates a log spaced 1d array by defining a step size and a base
    In the form of dQ/Q - i.e. dQ\\Q*Qpoint
    """
    logrange = [start]
    point = start
    while point < stop:
        point = point+base**(np.log10(step*point)/np.log10(base))
        logrange.append(point)
    return np.array(logrange)

def QT2L(Q, T):
    """
    Simple Q,T to L conversion

    Q = 4 pi sin(T) / L   ==>  L = 4 pi sin(T) / Q
    """
    return 4 * np.pi * np.sin(np.radians(T)) / Q

def TOF_loader(T=0.25, dQoQ=0.02,
               Q_sim_range=(0.005, 0.2),
               filename=None, skiprows=1, **kw):
    """
    Loads and creates NeutronProbe objects for TOF stitched datasets
    I.e. from multiple angles. In the case of ISIS NR instruments we
    typically have a constant dq/q resolution which the data is binned to at
    the end of the reduction.

    *T* incident theta for the lowest angle
    *dQoQ* dq/q resolution data has been binned to
    *filename* filename of the data set to be loaded
    *kw* keyword arguments (kwargs) to be passed to NeutronProbe()
    """

    # np.loadtext is currently set for simple 3 column POLREF data
    # if you aim to use this loader for other data, talk to your local contact
    # to understand the data format, and how best to load it.

    if filename is not None:
        data = np.loadtxt(filename, skiprows=skiprows).T
        if dQoQ is None:
            Q, R, dR, dQo = data
        else:
            Q, R, dR = data
            dQo = (Q*dQoQ)
        data_in = (R, dR)
    else:
        Q = logstep(Q_sim_range[0], Q_sim_range[1], dQoQ, base=dQoQ)
        data_in = None

    L = QT2L(Q, T)
    # Converting the dq/q resolution into a dq value for each Q point
    # dQ = FWHM2sigma(dQo)
    # Since we take dL/L = 0, dQ/Q = dT/T, so dT = T * dQoQ
    dT = T *dQoQ

    probe_out = NeutronProbe(
        T=T,
        dT=dT,
        L=L,
        dL=0,
        data=data_in,
        # For standard TOF measurements resolution is assumed to be normal (gaussian)
        #  For measurements with many wavelengths and many angles (say cw measurements)
        #  then a uniform resolution can be used instead.
        resolution='normal',
        **kw
    )

    return probe_out


def load_probe_polref(filename, angle, dQoQ, name=None, path=None, pol_mode=None, field=None, **kw):
    """
    creates one probe (Neutron, Polarized - PA or PNR) from one measurement - could be one angle or stitched dataset.
    If polarized, sets some default values and links instrumental parameters for each cross-section together
    """

    if name is None:
        name = filename
    if path is None:
        path = os.getcwd()

    filepath = Path(path)/filename

    if (pol_mode != "pnr") and (pol_mode != "pa"):
        probe = TOF_loader(T=angle, dQoQ=dQoQ, filename=f"{filepath}.dat", name=name, **kw)

        probe.intensity.name = f"intensity {name}"
        probe.background.name = f"background {name}"
        probe.sample_broadening.name = f"sample_broadening {name}"
        probe.theta_offset.name = f"theta_offset {name}"

        probe.intensity.tags = ["inst", "nuisance"]
        probe.background.tags = ["inst", "nuisance"]
        probe.sample_broadening.tags = ["inst", "nuisance"]
        probe.theta_offset.tags = ["inst", "nuisance"]

    else:
        if pol_mode == "pa":
            files = dict(data_mm=f"{filepath}_dd.dat",
                         data_mp=f"{filepath}_du.dat",
                         data_pm=f"{filepath}_ud.dat",
                         data_pp=f"{filepath}_uu.dat")
        else:
            files = dict(data_mm=f"{filepath}_d.dat",
                         data_mp=None,
                         data_pm=None,
                         data_pp=f"{filepath}_u.dat")

        cross_sections = []
        for data in files.values():
            if data is None:
                cross_sections.append(None)
            else:
                cross_sections.append(TOF_loader(T=angle, dQoQ=dQoQ, filename=data, name=name, **kw))
        if field is None:
            field = 0.0

        probe = PolarizedNeutronProbe(cross_sections, Aguide=270, H=field, name=name)

        for xs in (probe.mm, probe.mp, probe.pm, probe.pp):
            if xs is not None:
                xs.name = name
                xs.intensity = probe.pp.intensity
                xs.sample_broadening = probe.pp.sample_broadening
                xs.theta_offset = probe.pp.theta_offset
                xs.background = probe.pp.background

        probe.pp.intensity.name = f"intensity {name}"
        probe.pp.background.name = f"background {name}"
        probe.pp.sample_broadening.name = f"sample_broadening {name}"
        probe.pp.theta_offset.name = f"theta_offset {name}"

        probe.pp.intensity.tags = ["inst", "nuisance"]
        probe.pp.background.tags = ["inst", "nuisance"]
        probe.pp.sample_broadening.tags = ["inst", "nuisance"]
        probe.pp.theta_offset.tags = ["inst", "nuisance"]

    return probe

dQoQ = 0.01
theta = 0.25
probe = load_probe_polref(filename="Ni58_stitched",
                          angle=0.25, dQoQ=0.01, name="Ni58",
                          pol_mode="pnr",
                          intensity=1.0, background=1e-7, back_reflectivity=False)

probe.pp.intensity.range(1e-1, 10)
probe.pp.background.range(1e-9, 1e-3)
probe.pp.sample_broadening.range(-(dQoQ*theta), 0.03)

# Set materials/SLDs
Si = Material(formula="Si")
Ni = Material(formula="Ni[58]")


Si_sub = Slab(material=Si, thickness=0, interface=5)
Ni_layer = Slab(material=Ni, thickness=1200, interface=5)

# Sample construction/Stack

sample = (Si_sub
          | Ni_layer(magnetism=Magnetism(rhoM=2.0, interface_above=5, interface_below=5, name="Ni Layer Sample 1"))
          | air
          )


# Fit params

Ni.density.pmp(-50, 0)

sample[Ni].magnetism.rhoM.range(0, 5)
sample[Ni].magnetism.dead_above.range(0, 100)
sample[Ni].magnetism.dead_below.range(0, 100)
sample[Ni].magnetism.interface_above.range(0, 50)
sample[Ni].magnetism.interface_below.range(0, 50)

sample[Ni].magnetism.rhoM.tags = ["magnetism", "sample"]
sample[Ni].magnetism.dead_above.tags = ["magnetism", "sample"]
sample[Ni].magnetism.dead_below.tags = ["magnetism", "sample"]
sample[Ni].magnetism.interface_above.tags = ["magnetism", "sample"]
sample[Ni].magnetism.interface_below.tags = ["magnetism", "sample"]


Ni_layer.thickness.range(0, 1500)
Ni_layer.thickness.tags = ["structure", "sample"]

Ni_layer.interface.range(0, 50)
Ni_layer.interface.tags = ["structure", "sample"]

Si_sub.interface.range(0, 50)
Si_sub.interface.tags = ["structure", "sample"]

zed = 2
step = False

experiment = Experiment(probe=probe, sample=sample, dz=zed, step_interfaces=step, auto_tag=True)

problem = FitProblem(experiment)
