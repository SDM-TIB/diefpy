"""
Measuring Performance with dief@t
=================================

The metric **dief@t** measures the diefficiency of an engine in the first t time units of query execution.
Intuitively, approaches that produce answers at a higher rate in a certain period of time are more efficient.
**dief@t interpretation: Higher is better**.


The ``diefpy.dieft`` method computes the **dief@t** metric as follows.
"""
# sphinx_gallery_thumbnail_path = '_images/thumb_example_dieft.png'

import diefpy
import pandas as pd  # for displaying the data in a nice way

# Load the answer trace file with the query traces from FigShare.
traces = diefpy.load_trace("https://ndownloader.figshare.com/files/9625852")

#%%
# Compute **dief@t** of the approaches recorded in ``traces`` when executing ``Q9.sparql``
# until the time unit 10 (here: in seconds).
dt = diefpy.dieft(traces, "Q9.sparql", 10)
pd.DataFrame(dt).head()

#%%
# Compute **dief@t** of the approaches recorded in ``traces`` when executing ``Q9.sparql``
# until the time unit when the slowest approach finalizes its execution.
dt = diefpy.dieft(traces, "Q9.sparql")
pd.DataFrame(dt).head()

#%%
