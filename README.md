[![Build Status](https://github.com/SDM-TIB/diefpy/actions/workflows/testroutine.yml/badge.svg?branch=master)](https://github.com/SDM-TIB/diefpy/actions/workflows/testroutine.yml)
[![Latest Release](http://img.shields.io/github/release/SDM-TIB/diefpy.svg?logo=github)](https://github.com/SDM-TIB/diefpy/releases)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4973516.svg)](https://doi.org/10.5281/zenodo.4973516)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[![Python Versions](https://img.shields.io/pypi/pyversions/diefpy)](https://pypi.org/project/diefpy)
[![Package Format](https://img.shields.io/pypi/format/diefpy)](https://pypi.org/project/diefpy)
[![Package Status](https://img.shields.io/pypi/status/diefpy)](https://pypi.org/project/diefpy)
[![Package Version](https://img.shields.io/pypi/v/diefpy)](https://pypi.org/project/diefpy)

&nbsp;

Philipp D. Rohde, Nikoleta Themeliotou
# diefpy

Python package for computing diefficiency metrics dief@t and dief@k.

The metrics dief@t and dief@k allow for measuring the diefficiency during 
an elapsed time period t or while k answers are produced, respectively. 
dief@t and dief@k rely on the computation of the area under the curve of 
answer traces, and thus capturing the answer rate concentration over a time 
interval.

This fork of the [original diefpy repo](https://github.com/maribelacosta/diefpy) by Maribel Acosta provides a complete Python3 version.

### Description

![Overview of Result Plots](https://raw.githubusercontent.com/SDM-TIB/diefpy/master/docs/diefpy-overview.png "Overview of Result Plots")
Figure 1: Overview of Result Plots.

Fig. 1 gives an overview of the result plots that can be produced using the package.
Firstly the overall Execution Time for all the tests and approaches (NotAdaptive, Random and Selective) in the metrics
data can be created as a bar plot. 
For evaluating the input tests an answer trace of each approach (NotAdaptive, Random and Selective) can be created which shows how many answers were produced. 
Finally two Radar Plots can be created. The Radar Plot on the left compares dief@t with other benchmark metrics in a specific test. The other benchmark metrics being total execution time, time for the first tuple, throughput, and completeness. 
The Radar Plot on the right compares dief@k at different answer completeness in a specific test by measuring the continuous efficiency of approaches when producing
the first 25%, 50%, 75%, and 100% of the answers.

### Usage 
Compute dief@t and dief@k for the test `Q9.rq` based on the traces `traces.csv` and metrics `metrics.csv` provided as example in the package. 
```python
import diefpy
from pkg_resources import resource_filename

# Use answer traces provided in the package: Compare three approaches "Selective", "Not Adaptive", "Random" when executing the test "Q9.rq".
traces = diefpy.load_trace(resource_filename('diefpy', 'data/traces.csv')) 

# Plot answer traces for test "Q9.rq".
diefpy.plot_answer_trace(traces, "Q9.rq", ["#ECC30B","#D56062","#84BCDA"]).show()

# Compute dief@t when t is the time where the slowest approach produced the last answer.
diefpy.dieft(traces, 'Q9.rq')

# Compute dief@t after 7.5 time units (seconds) of execution. 
diefpy.dieft(traces, 'Q9.rq', 7.5)

# Compute dief@k when k is the minimum of retrieved answers across the approaches.
diefpy.diefk(traces, 'Q9.rq')

# Compute dief@k after 10 results.
diefpy.diefk(traces, 'Q9.rq', 10)

# Compute dief@k when k is 50% of the answers retrieved.
diefpy.diefk2(traces, 'Q9.rq', 0.5)

# Load the metrics.
metrics = diefpy.load_metrics(resource_filename('diefpy', 'data/metrics.csv'))

# Compute the metrics for performance analysis with dief@t.
exp1 = diefpy.performance_of_approaches_with_dieft(traces, metrics)

# Plot the metrics for performance analysis with dief@t.
diefpy.plot_performance_of_approaches_with_dieft(exp1, 'Q9.rq', ["#ECC30B","#D56062","#84BCDA"]).show()

# Compute the metrics for continuous efficiency with dief@k.
exp2 = diefpy.continuous_efficiency_with_diefk(traces)

# Plot the metrics for continuous efficiency with dief@k.
diefpy.plot_continuous_efficiency_with_diefk(exp2, 'Q9.rq', ["#ECC30B","#D56062","#84BCDA"]).show()
```

It is also possible to generate the plots for all the tests and receive a list of plots instead of a single plot by using the following functions:
```python
diefpy.plot_all_answer_traces(traces, ["#ECC30B","#D56062","#84BCDA"])
diefpy.plot_all_performance_of_approaches_with_dieft(exp1, ["#ECC30B","#D56062","#84BCDA"])
diefpy.plot_all_continuous_efficiency_with_diefk(exp2, ["#ECC30B","#D56062","#84BCDA"])
```

### Publications
[1] Maribel Acosta, Maria-Esther Vidal, York Sure-Vetter. Diefficiency Metrics: Measuring the Continuous Efficiency of Query Processing Approaches. In Proceedings of the International Semantic Web Conference, 2017. Nominated to Best Paper Award at the Resource Track. [https://doi.org/10.1007/978-3-319-68204-4_1](https://doi.org/10.1007/978-3-319-68204-4_1)

[2] Maribel Acosta, Maria-Esther Vidal. Measuring the Performance of Continuous Query Processing Approaches with dief@t and dief@k. In  the International Semantic Web Conference, Posters and Demos, 2017. [online](https://iswc2017.ai.wu.ac.at/wp-content/uploads/papers/PostersDemos/paper602.pdf)
