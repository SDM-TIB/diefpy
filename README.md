[![Build Status](https://github.com/SDM-TIB/diefpy/actions/workflows/testroutine.yml/badge.svg?branch=master)](https://github.com/SDM-TIB/diefpy/actions/workflows/testroutine.yml)
[![Latest Release](http://img.shields.io/github/release/SDM-TIB/diefpy.svg?logo=github)](https://github.com/SDM-TIB/diefpy/releases)
[![DOI](https://zenodo.org/badge/351839805.svg)](https://zenodo.org/badge/latestdoi/351839805)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[![Python Versions](https://img.shields.io/pypi/pyversions/diefpy)](https://pypi.org/project/diefpy)
[![Package Format](https://img.shields.io/pypi/format/diefpy)](https://pypi.org/project/diefpy)
[![Package Status](https://img.shields.io/pypi/status/diefpy)](https://pypi.org/project/diefpy)
[![Package Version](https://img.shields.io/pypi/v/diefpy)](https://pypi.org/project/diefpy)

&nbsp;

Philipp D. Rohde, Nikoleta Themeliotou
# diefpy

Python package for computing diefficiency metrics **_dief@t_** and **_dief@k_**.

The metrics **_dief@t_** and **_dief@k_** allow for measuring the diefficiency during 
an elapsed time period _t_ or while _k_ answers are produced, respectively. 
**_dief@t_** and **_dief@k_** rely on the computation of the area under the curve (AUC) of 
answer traces, and thus capturing the answer rate concentration over a time interval.

This fork of the [original diefpy repo](https://github.com/maribelacosta/diefpy) by Maribel Acosta provides a complete Python3 version.

## Description

![Overview of Result Plots](https://raw.githubusercontent.com/SDM-TIB/diefpy/master/docs/_images/diefpy-overview.png "Overview of Result Plots")
Figure 1: Overview of Result Plots.

Fig. 1 gives an overview of the result plots that can be produced using the package.
Firstly, the overall _Execution Time_ for all the tests and approaches (NotAdaptive, Random and Selective) in the metrics
data can be created as a bar plot. 
For evaluating the input tests an answer trace of each approach (NotAdaptive, Random and Selective) can be created which shows how many answers were produced. 
Finally, two Radar Plots can be created. The Radar Plot on the left compares **_dief@t_** with other benchmark metrics in a specific test. The other benchmark metrics being conventional metrics like _total execution time_, _time for the first tuple_, _throughput_, and _number of answers produced_. 
The Radar Plot on the right compares **_dief@k_** at different answer completeness percentages in a specific test by measuring the continuous efficiency of approaches when producing
the first 25%, 50%, 75%, and 100% of the answers.

## Installation

You can build and install diefpy from source
```bash
git clone git@github.com:SDM-TIB/diefpy.git
cd diefpy
python -m pip install -e .
```

or downloading it from PyPI:
```bash
python -m pip install diefpy
```

**Notice:** Most likely you want to install diefpy into a virtual environment for the experiments you were running.

## Usage 
We refer the user to the [documentation](https://sdm-tib.github.io/diefpy/) of the library for a detailed explanation of the implemented functionality.
The page also includes some [examples](https://sdm-tib.github.io/diefpy/examples/).
Additionally, there is an iPython notebook in the `example` folder that demonstrates the use of the diefpy library.

## Publications
[1] Maribel Acosta, Maria-Esther Vidal, York Sure-Vetter. Diefficiency Metrics: Measuring the Continuous Efficiency of Query Processing Approaches. In Proceedings of the International Semantic Web Conference, 2017. Nominated to Best Paper Award at the Resource Track. [https://doi.org/10.1007/978-3-319-68204-4_1](https://doi.org/10.1007/978-3-319-68204-4_1)

[2] Maribel Acosta, Maria-Esther Vidal. Measuring the Performance of Continuous Query Processing Approaches with dief@t and dief@k. In  the International Semantic Web Conference, Posters and Demos, 2017. [online](https://iswc2017.ai.wu.ac.at/wp-content/uploads/papers/PostersDemos/paper602.pdf)
