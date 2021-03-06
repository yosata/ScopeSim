# ScopeSim 
## A telescope observation simulator for Python

[![Build Status](https://travis-ci.org/astronomyk/ScopeSim.svg?branch=master)](https://travis-ci.org/astronomyk/ScopeSim)
[![Documentation Status](https://readthedocs.org/projects/scopesim/badge/?version=latest)](https://scopesim.readthedocs.io/en/latest/?badge=latest)

#### Supported python versions
[![Python 2.7](https://img.shields.io/badge/Python-2.7-red.svg)]()
[![Python 3.5](https://img.shields.io/badge/Python-3.5-brightgreen.svg)]()
[![Python 3.6](https://img.shields.io/badge/Python-3.6-brightgreen.svg)]()
[![Python 3.7](https://img.shields.io/badge/Python-3.7-brightgreen.svg)]()
[![Python 3.8](https://img.shields.io/badge/Python-3.8-red.svg)]()

#### Dependencies

[![Numpy](https://img.shields.io/badge/Numpy->=1.13-brightgreen.svg)]()
[![Scipy](https://img.shields.io/badge/Scipy-1.2.0-orange.svg)]()
[![Matplotlib](https://img.shields.io/badge/Matplotlib->=3.0-brightgreen.svg)]()

[![Astropy](https://img.shields.io/badge/Astropy-<=3.9-yellow.svg)]()
[![Synphot](https://img.shields.io/badge/Synphot-0.1.3-orange.svg)]()

[![requests](https://img.shields.io/badge/requests->=2.21-brightgreen.svg)]()
[![beautifulsoup4](https://img.shields.io/badge/beautifulsoup4->=4.7-brightgreen.svg)]()
[![pyyaml](https://img.shields.io/badge/pyyaml->=3.13-brightgreen.svg)]()

#### Optional dependencies
[![skycalc_ipy](https://img.shields.io/badge/skycalc_ipy->=0.1-brightgreen.svg)]()
[![anisocado](https://img.shields.io/badge/anisocado->=0.1-brightgreen.svg)]()


## Summary

Telescopy aims to simulate images of astronomical objects observed with visual 
and infrared instruments. It does this by creating models of the optical train 
and astronomical objects and then pushing the object through the optical train. 
The resulting 2D image is then broadcast to a detector chip and read out into a 
FITS file. 

This code was originally based on the [SimCADO](www.univie.ac.at/simcado) package

## Dependencies

```
numpy >= 1.13
scipy == 1.2.0
astropy < 4.0
synphot < 0.2
pyyaml
requests
beautifulsoup
```

## Documentation
The main set of documentation can be found here: 
https://scopesim.readthedocs.io/en/latest/

A basic Jupyter Notebook can be found here: 
[scopesim_basic_intro.ipynb](docs/source/_static/scopesim_basic_intro.ipynb)
