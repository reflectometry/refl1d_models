import os
from pathlib import Path

from bumps.fitters import fit

from refl1d_models.mixed_model import create_mixed_model


def test_mixed_model():
    """
    Example use and test of the mixed model
    """
    data_dir = str(Path(__file__).parent / "data")
    data_file = os.path.join(data_dir, "REFL_211832_combined_data_auto.txt")

    problem, experiment = create_mixed_model(data_file)
    results = fit(problem, method="amoeba", samples=2000, burn=2000, pop=20, verbose=1)

    assert results.success
    assert results.fun / len(experiment.probe.Q) < 5
