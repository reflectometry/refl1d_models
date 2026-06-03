"""Auto-generated analyzer model (Ni58_basic_model) — created by create-model (POLREF)."""

import os
import numpy as np
from pathlib import Path
from refl1d.names import *


# ── Data location (edit to point at your local data copy) ───
DATA_DIR = os.path.join(os.path.expanduser('~'), 'git/refl1d_models/refl1d_models/polref-ni58-magnetic')


def logstep(start, stop, step, base=10.0):
    """Log-spaced 1d array defined by a dQ/Q step and a base."""
    logrange = [start]
    point = start
    while point < stop:
        point = point + base ** (np.log10(step * point) / np.log10(base))
        logrange.append(point)
    return np.array(logrange)


def QT2L(Q, T):
    """Q, theta -> wavelength:  L = 4 pi sin(T) / Q."""
    return 4 * np.pi * np.sin(np.radians(T)) / Q


def TOF_loader(T=0.25, dQoQ=0.02, Q_sim_range=(0.005, 0.2),
               filename=None, skiprows=0, **kw):
    """Build a NeutronProbe for a TOF stitched dataset (constant dQ/Q)."""
    if filename is not None:
        data = np.loadtxt(filename, skiprows=skiprows).T
        if dQoQ is None:
            Q, R, dR, dQo = data
        else:
            Q, R, dR = data
            dQo = Q * dQoQ
        data_in = (R, dR)
    else:
        Q = logstep(Q_sim_range[0], Q_sim_range[1], dQoQ, base=dQoQ)
        data_in = None

    L = QT2L(Q, T)
    # dL/L = 0, so dQ/Q = dT/T -> dT = T * dQ/Q
    dT = T * dQoQ

    return NeutronProbe(
        T=T, dT=dT, L=L, dL=0, data=data_in,
        resolution="normal", **kw,
    )


def load_probe_polref(filename, angle, dQoQ, name=None, path=None,
                      pol_mode=None, field=None, **kw):
    """Build one probe (unpolarized, PNR, or PA) from a stitched dataset.

    For polarized data the per-cross-section instrument parameters are linked
    to the ``pp`` cross-section so they refine as one.
    """
    if name is None:
        name = filename
    if path is None:
        path = os.getcwd()
    filepath = Path(path) / filename

    if pol_mode not in ("pnr", "pa"):
        probe = TOF_loader(T=angle, dQoQ=dQoQ, filename=f"{filepath}.dat",
                           name=name, **kw)
        probe.intensity.name = f"intensity {name}"
        probe.background.name = f"background {name}"
        probe.sample_broadening.name = f"sample_broadening {name}"
        probe.theta_offset.name = f"theta_offset {name}"
        for par in (probe.intensity, probe.background,
                    probe.sample_broadening, probe.theta_offset):
            par.tags = ["inst", "nuisance"]
        return probe

    if pol_mode == "pa":
        files = dict(data_mm=f"{filepath}_dd.dat", data_mp=f"{filepath}_du.dat",
                     data_pm=f"{filepath}_ud.dat", data_pp=f"{filepath}_uu.dat")
    else:
        files = dict(data_mm=f"{filepath}_d.dat", data_mp=None,
                     data_pm=None, data_pp=f"{filepath}_u.dat")

    cross_sections = [
        None if data is None
        else TOF_loader(T=angle, dQoQ=dQoQ, filename=data, name=name, **kw)
        for data in files.values()
    ]
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
    for par in (probe.pp.intensity, probe.pp.background,
                probe.pp.sample_broadening, probe.pp.theta_offset):
        par.tags = ["inst", "nuisance"]
    return probe


# Materials
Si = Material(formula='Si')
NiO_surface = Material(formula='NiO')
Ni58 = Material(formula='Ni[58]')
SiO2_interface = Material(formula='SiO2')

# Slabs
Si_sub = Slab(material=Si, thickness=0, interface=5.0)
NiO_surface_layer = Slab(material=NiO_surface, thickness=20.0, interface=5.0)
Ni58_layer = Slab(material=Ni58, thickness=1200.0, interface=5.0)
SiO2_interface_layer = Slab(material=SiO2_interface, thickness=15.0, interface=5.0)

# Sample
sample = (Si_sub | SiO2_interface_layer | Ni58_layer(magnetism=Magnetism(rhoM=2.0, interface_above=5.0, interface_below=5.0, name='Ni58 magnetism')) | NiO_surface_layer | air)

# Fit parameters
Ni58.density.pmp(-50.0, 0.0)
NiO_surface_layer.thickness.range(0.0, 100.0)
NiO_surface_layer.thickness.tags = ['structure', 'sample']
NiO_surface_layer.interface.range(0.0, 50.0)
NiO_surface_layer.interface.tags = ['structure', 'sample']
sample[Ni58].magnetism.rhoM.range(0.0, 5.0)
sample[Ni58].magnetism.rhoM.tags = ['magnetism', 'sample']
sample[Ni58].magnetism.dead_above.range(0.0, 100.0)
sample[Ni58].magnetism.dead_above.tags = ['magnetism', 'sample']
sample[Ni58].magnetism.dead_below.range(0.0, 100.0)
sample[Ni58].magnetism.dead_below.tags = ['magnetism', 'sample']
sample[Ni58].magnetism.interface_above.range(0.0, 50.0)
sample[Ni58].magnetism.interface_above.tags = ['magnetism', 'sample']
sample[Ni58].magnetism.interface_below.range(0.0, 50.0)
sample[Ni58].magnetism.interface_below.tags = ['magnetism', 'sample']
Ni58_layer.thickness.range(0.0, 1500.0)
Ni58_layer.thickness.tags = ['structure', 'sample']
Ni58_layer.interface.range(0.0, 50.0)
Ni58_layer.interface.tags = ['structure', 'sample']
SiO2_interface_layer.thickness.range(0.0, 100.0)
SiO2_interface_layer.thickness.tags = ['structure', 'sample']
SiO2_interface_layer.interface.range(0.0, 50.0)
SiO2_interface_layer.interface.tags = ['structure', 'sample']
Si_sub.interface.range(0.0, 50.0)
Si_sub.interface.tags = ['structure', 'sample']

# ── State: Ni58_stitched (PNR) ──
probe = load_probe_polref(
    filename='Ni58_stitched',
    path=DATA_DIR,
    angle=0.25,
    dQoQ=0.01,
    name='Ni58_stitched',
    pol_mode='pnr',
    field=0.0,
    skiprows=0,
    intensity=1.0,
    background=1e-07,
    back_reflectivity=False,
)
probe.pp.intensity.range(0.1, 10.0)
probe.pp.background.range(1e-09, 0.001)
probe.pp.sample_broadening.range(-(0.01 * 0.25), 0.03)
experiment = Experiment(probe=probe, sample=sample, dz=2, step_interfaces=False, auto_tag=True)

problem = FitProblem(experiment)
