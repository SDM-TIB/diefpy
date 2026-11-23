"""
Measuring Performance with dief@k
=================================

The metric **dief@k** measures the diefficiency of a query engine while producing the first k answers when
executing a query. Intuitively, approaches that require a shorter period of time to produce a certain number of
answers are more efficient. **dief@k interpretation: Lower is better**.

The ``diefpy.diefk`` and ``diefpy.diefk2`` methods compute the **dief@k** metric as follows.
"""
# sphinx_gallery_thumbnail_path = '_images/thumb_example_diefk.png'

import diefpy
import pandas as pd  # for displaying the data in a nice way

# Load the answer trace file with the query traces from FigShare.
traces = diefpy.load_trace("https://ndownloader.figshare.com/files/9625852")

#%%
# Compute **dief@k** of the approaches recorded in ``traces`` when executing ``Q9.sparql``
# and producing the first 2,000 answers.
dk = diefpy.diefk(traces, "Q9.sparql", 2000)
pd.DataFrame(dk).head()

#%%
# Compute **dief@k** of the approaches recorded in ``traces`` when executing ``Q9.sparql``
# and producing the first *k* answers, where *k* is the minimum of the total answers
# produced among all the approaches.
dk = diefpy.diefk(traces, "Q9.sparql")
pd.DataFrame(dk).head()

#%%
# Compute **dief@k** of the approaches recorded in ``traces`` when executing ``Q9.sparql``
# and producing 50% of the answers.
dk = diefpy.diefk2(traces, "Q9.sparql", 0.50)
pd.DataFrame(dk).head()

#%%
