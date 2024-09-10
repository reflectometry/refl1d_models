"""
This module contains example definitions of probes used in refl1d models.
"""

import numpy as np
from refl1d.probe import QProbe


def create_qprobe(data_file_path: str, fwhm: bool = True) -> QProbe:
    """
    Create a QProbe object from a data file.

    :param data_file_path: path to the data file.
    :type data_file_path: str
    :return: QProbe object.
    :rtype: QProbe
    """
    if data_file_path is None:
        q = np.logspace(np.log10(0.005), np.log10(0.2), num=250)
        dq = 0.025 * q
        data = errors = None
    else:
        q, data, errors, dq = np.loadtxt(data_file_path, unpack=True)

    # If the Q resolution is given as FWHM, convert it to sigma
    if fwhm:
        dq /= 2.355

    probe = QProbe(q, dq, data=(data, errors))

    return probe
