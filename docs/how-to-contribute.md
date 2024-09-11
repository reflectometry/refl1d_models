
How to submit a model example
=============================

Submitting your model examples will help the community understand how
to use refl1d!

Models are useful when they are annotated, and if they are accompanied by example data. You can submit data in any format that you can read in your model script.

The following is an example of how one might structure a submitted model:

```python
"""
Model description

Describe your model and what it unique about it.
"""

import numpy as np
from refl1d.names import SLD, Experiment, FitProblem, Parameter, QProbe

#####################################################################
# Probe: this is where you also load your data and define your probe.
q = np.logspace(np.log10(0.009), np.log10(0.18), num=150)
dq = 0.025 * q / 2.35

probe = QProbe(q, dq)

#####################################################################
# Materials: this is where you define your materials
silicon = SLD(name="Si", rho=2.07, irho=0.0)
d2o = SLD(name="D2O", rho=6.13, irho=0.0)

#####################################################################
# Sample: This is where you define your film structure
sample = ( d2o(0, 5) | silicon )

#####################################################################
# This is where you define your fit parameters and constraints
probe.intensity = Parameter(value=1.0, name="normalization")
probe.background.range(0.0, 1e-05)
sample["D2O"].interface.range(25.0, 150.0)

# Create the experiment and the problem objects
experiment = Experiment(probe=probe, sample=sample)
problem = FitProblem(experiment)
```

You can either send your model and data to us be email, or create
a pull request. Creating a pull requests is preferred and will ensure
a speedier response.
