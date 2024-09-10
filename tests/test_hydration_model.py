from refl1d_models.hydration_model import experiment


def test_hydration_model():
    """
    Example use and test of the hydration model
    """
    r, dr = experiment.reflectivity()
    assert len(r) == 150
