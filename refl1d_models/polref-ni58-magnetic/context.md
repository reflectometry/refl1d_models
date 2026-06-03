
# PNR Fitting Context

## Dataset Overview

The data to be fitted are **polarised neutron reflectometry (PNR)** data from a:

- **1200 Å Ni[58] magnetic layer**
- Deposited on a **Si substrate**

## Data Format

The data files are in **3-column ASCII format** with **no header**.

The columns are:

1. `Q` — momentum transfer
2. `R` — reflectivity
3. `dR` — reflectivity uncertainty

## Data Files

There are two data files:

- Files with the suffix `_u.dat` contain **spin-up** data
- Files with the suffix `_d.dat` contain **spin-down** data

## Reflectometry Geometry

The reflectometry geometry is:

```text
air / solid
```

Where:

* **Superphase:** air
* **Subphase:** Si substrate

## Measurement Details

The data are stitched PNR reflectometry data using the lowest scattering angle:

```text
theta = 0.25 degrees
```

The data were reduced using a resolution of:

```text
dQ/Q = 0.01
```

## Modelling Hypotheses

The following structural and magnetic hypotheses should be considered during fitting.

### Surface Layer

There may be a **NiO surface layer**.

### Substrate Interface Layer

There may be a **SiO2 interface layer** between the Ni\[58] layer and the Si substrate.

### Magnetically Dead Layers

There may be **magnetically dead layers** at both interfaces of the Ni\[58] layer:

* Top interface of the Ni\[58] layer
* Bottom interface of the Ni\[58] layer

### Magnetic vs Nuclear Interfaces

The magnetic interfaces of the Ni\[58] layer may differ from the nuclear, or structural, interfaces.

In particular:

* The magnetic interface above the Ni\[58] layer may differ from the corresponding nuclear interface.
* The magnetic interface below the Ni\[58] layer may differ from the corresponding nuclear interface.
* The magnetic depth profile should therefore not necessarily be constrained to match the nuclear scattering length density profile exactly.
