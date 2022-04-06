"""
Visualizing Execution Time of SPARQL Query Engines
==================================================

In a classical analysis of the performance of query engines, plots to compare the overall execution time of the different query engines per query are presented.
With the ``diefpy`` package, it is possible to generate these plots from the metrics file using the ``diefpy.plot_execution_time`` method.
"""

import diefpy

COLORS = ["#ECC30B", "#D56062", "#84BCDA"]

# Load the result of the other metrics (execution time, etc.) from FigShare.
metrics = diefpy.load_metrics("https://ndownloader.figshare.com/files/9660316")

# Plot the execution times of all queries and query engines as a bar chart from the metrics file.
diefpy.plot_execution_time(metrics, COLORS, log_scale=True).show()

#%%
# **Conclusion:** For most of the queries, the performance of the different approaches is comparable in terms of
# execution time. nLDE ``Not Adaptive`` is not able to produce results for the queries ``Q4.sparql`` and ``Q5.sparql.``
# Additionally, the nLDE ``Selective`` outperforms the other approaches for query ``Q2.sparql`` while exhibiting the
# worst performance for query ``Q17.sparql``.
