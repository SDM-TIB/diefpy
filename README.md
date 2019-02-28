# diefpy
Python package for computing diefficiency metrics dief@t and dief@k.

The metrics dief@t and dief@k allow for measuring the diefficiency during an elapsed time period t or while k answers are produced, respectively. dief@t and dief@k rely on the computation of the area under the curve of answer traces, and thus capturing the answer rate concentration over a time interval.

## Examples
Compute dief@t for the test `Q9.rq` based on the traces `traces.csv` provided as example in the package. 
```python
from diefpy import dief
from pkg_resources import resource_filename

# Use answer traces provided in the package: Compare three approaches "Selective", "Not Adaptive", "Random" when executing the test "Q9.rq".
traces = diefpy.load_trace(resource_filename('diefpy.tests', 'traces.csv')) 

# Plot answer traces for test "Q9.rq".
diefpy.plot_answer_trace(traces, "Q9.rq")

# Compute dief@t when t is the time where the slowest approach produced the last answer.
diefpy.dieft(traces, 'Q9.rq')

# Compute dief@t after 7.5 time units (seconds) of execution. 
diefpy.dieft(traces, 'Q9.rq', 7.5)
```

## License 
This package is licensed under the MIT License.

## Publications
[1] Maribel Acosta, Maria-Esther Vidal, York Sure-Vetter. Diefficiency Metrics: Measuring the Continuous Efficiency of Query Processing Approaches. In Proceedings of the International Semantic Web Conference, 2017. Nominated to Best Paper Award at the Resource Track. 

[2] Maribel Acosta, Maria-Esther Vidal. Measuring the Performance of Continuous Query Processing Approaches with dief@t and dief@k. In  the International Semantic Web Conference, Posters and Demos, 2017.
