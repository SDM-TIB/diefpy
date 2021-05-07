[![Build Status](https://travis-ci.org/maribelacosta/dief.svg?branch=master)](https://travis-ci.org/maribelacosta/diefpy)
[![DOI](https://zenodo.org/badge/109045351.svg)](https://zenodo.org/badge/latestdoi/109045351)


# diefpy
Python package for computing diefficiency metrics dief@t and dief@k.

The metrics dief@t and dief@k allow for measuring the diefficiency during an elapsed time period t or while k answers are produced, respectively. dief@t and dief@k rely on the computation of the area under the curve of answer traces, and thus capturing the answer rate concentration over a time interval.

## Examples
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

# Load the metrics
metrics = diefpy.load_metrics(resource_filename('diefpy', 'data/metrics.csv'))

# Reproduce the metrics from Experiment 1
exp1 = diefpy.experiment1(traces, metrics)

# Plot the metrics from Experiment 1
diefpy.plotExperiment1Test(exp1, 'Q9.rq', ["#ECC30B","#D56062","#84BCDA"]).show()

# Reproduce the metrics from Experiment 2
exp2 = diefpy.experiment2(traces)

# Plot the metrics from Experiment 2
diefpy.plotExperiment2Test(exp2, 'Q9.rq', ["#ECC30B","#D56062","#84BCDA"]).show()
```

It is also possible to generate the plots for all the tests and receive a list of plots instead of a single plot by using the following functions:
```python
diefpy.plot_all_answer_traces(traces, ["#ECC30B","#D56062","#84BCDA"])
diefpy.plotExperiment1(exp1, ["#ECC30B","#D56062","#84BCDA"])
diefpy.plotExperiment2(exp2, ["#ECC30B","#D56062","#84BCDA"])
```

## License 
This package is licensed under the MIT License.

## Publications
[1] Maribel Acosta, Maria-Esther Vidal, York Sure-Vetter. Diefficiency Metrics: Measuring the Continuous Efficiency of Query Processing Approaches. In Proceedings of the International Semantic Web Conference, 2017. Nominated to Best Paper Award at the Resource Track. 

[2] Maribel Acosta, Maria-Esther Vidal. Measuring the Performance of Continuous Query Processing Approaches with dief@t and dief@k. In  the International Semantic Web Conference, Posters and Demos, 2017.
