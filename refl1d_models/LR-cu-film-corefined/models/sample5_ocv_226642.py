"""Auto-generated analyzer model (sample5_ocv_226642) — created by create-model."""

import os
import numpy as np
from bumps.fitters import fit
from refl1d.names import *

from refl1d.probe import make_probe

# ── Data location (edit to point at your local data copy) ───
DATA_DIR = os.path.join(os.path.expanduser('~'), 'git/refl1d_models/refl1d_models/LR-cu-film-corefined')


def create_sample(back_reflection=False):
    """Build a fresh sample stack for one state.

    Every probe in a given state is constructed with this stack,
    so all structural parameters (thickness / SLD / interface) are
    automatically tied across that state's segments via Python
    object identity. Each state gets its OWN call, so structural
    parameters are independent across states unless explicitly
    tied below with ``sample_B['X'].attr = sample_A['X'].attr``.

    ``back_reflection`` selects stack orientation so the default
    ``probe.back_reflectivity=False`` gives correct physics in both
    buried-interface and standard front-reflection geometries.
    """
    D2O = SLD(name='D2O', rho=6.19)
    Cu_oxide = SLD(name='Cu_oxide', rho=5.5)
    Cu = SLD(name='Cu', rho=6.55)
    Ti = SLD(name='Ti', rho=-1.95)
    Si = SLD(name='Si', rho=2.07)

    if back_reflection:
        sample = D2O(0, 5.0) | Cu_oxide(20.0, 8.0) | Cu(150.0, 10.0) | Ti(30.0, 8.0) | Si
        sample['D2O'].interface.range(5.0, 20.0)
    else:
        sample = Si | Ti(30.0, 8.0) | Cu(150.0, 10.0) | Cu_oxide(20.0, 8.0) | D2O(0, 5.0)
        sample['Si'].interface.range(5.0, 20.0)

    # Parameter ranges
    sample['D2O'].material.rho.range(4.19, 8.19)
    sample['Cu_oxide'].thickness.range(5.0, 60.0)
    sample['Cu_oxide'].material.rho.range(3.5, 7.5)
    sample['Cu_oxide'].interface.range(5.0, 15.0)
    sample['Cu'].thickness.range(50.0, 400.0)
    sample['Cu'].material.rho.range(4.55, 8.55)
    sample['Cu'].interface.range(5.0, 25.0)
    sample['Ti'].thickness.range(5.0, 80.0)
    sample['Ti'].material.rho.range(-5.5, 1.5)
    sample['Ti'].interface.range(5.0, 14.0)

    return sample


def create_q_probe(data_file):
    """Angle-independent probe for a combined REF_L file."""
    q, data, errors, dq = np.loadtxt(data_file).T
    dq = dq / 2.355  # FWHM → 1-sigma
    probe = QProbe(q, dq, data=(data, errors))
    probe.intensity = Parameter(value=1.0, name="intensity")
    probe.intensity.range(0.5, 1.5)
    return probe

def create_angle_probe(data_file, theta):
    """Angle-based probe from one REF_L partial file."""
    q, data, errors, dq = np.loadtxt(data_file).T
    wl = 4 * np.pi * np.sin(np.pi / 180 * theta) / q
    dT = dq / q * np.tan(np.pi / 180 * theta) * 180 / np.pi
    dL = 0 * q  # wavelength resolution placeholder
    probe = make_probe(
        T=theta, dT=dT, L=wl, dL=dL,
        data=(data, errors),
        radiation="neutron",
        resolution="uniform",
    )
    probe.intensity = Parameter(value=1.0, name="intensity")
    probe.intensity.range(0.5, 1.5)
    return probe


# ── State: run_226642_ocv (partials) ─────────────────────────
# All probes in this state share sample_run_226642_ocv, so every structural
# parameter (thickness, SLD, roughness) is tied across this state's
# segments by Python object identity — no explicit ties needed.
sample_run_226642_ocv = create_sample(back_reflection=True)
theta_offset_run_226642_ocv = Parameter(value=0.0, name="theta_offset_run_226642_ocv")
theta_offset_run_226642_ocv.range(-0.02, 0.02)
sample_broadening_run_226642_ocv = Parameter(value=0.0, name="sample_broadening_run_226642_ocv")
sample_broadening_run_226642_ocv.range(0.0, 0.01)
probe_run_226642_ocv_1 = create_angle_probe(os.path.join(DATA_DIR, 'REFL_226642_1_226642_partial.txt'), theta=0.370048)
probe_run_226642_ocv_1.theta_offset = theta_offset_run_226642_ocv
probe_run_226642_ocv_1.sample_broadening = sample_broadening_run_226642_ocv
experiment_run_226642_ocv_1 = Experiment(probe=probe_run_226642_ocv_1, sample=sample_run_226642_ocv)
probe_run_226642_ocv_2 = create_angle_probe(os.path.join(DATA_DIR, 'REFL_226642_2_226643_partial.txt'), theta=1.200155)
probe_run_226642_ocv_2.theta_offset = theta_offset_run_226642_ocv
probe_run_226642_ocv_2.sample_broadening = sample_broadening_run_226642_ocv
experiment_run_226642_ocv_2 = Experiment(probe=probe_run_226642_ocv_2, sample=sample_run_226642_ocv)
probe_run_226642_ocv_3 = create_angle_probe(os.path.join(DATA_DIR, 'REFL_226642_3_226644_partial.txt'), theta=3.50013)
probe_run_226642_ocv_3.theta_offset = theta_offset_run_226642_ocv
probe_run_226642_ocv_3.sample_broadening = sample_broadening_run_226642_ocv
experiment_run_226642_ocv_3 = Experiment(probe=probe_run_226642_ocv_3, sample=sample_run_226642_ocv)

problem = FitProblem([experiment_run_226642_ocv_1, experiment_run_226642_ocv_2, experiment_run_226642_ocv_3])
