"""
Python library for computing diefficiency metrics **dief@t** and **dief@k**.

The metrics **dief@t** and **dief@k** allow for measuring the diefficiency during
an elapsed time period *t* or while *k* answers are produced, respectively.
**dief@t** and **dief@k** rely on the computation of the area under the curve (AUC) of
answer traces, and thus capturing the answer rate concentration over a time interval.
"""
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.figure import Figure

from diefpy.radaraxes import radar_factory


DEFAULT_COLORS = ("#ECC30B", "#D56062", "#84BCDA")
"""Default colors for printing plots: yellow, red, blue"""


def dieft(inputtrace: np.ndarray, inputtest: str, t: float = -1.0, continue_to_end: bool = True) -> np.ndarray:
    """
    Computes the **dief@t** metric for a specific test at a given time point *t*.

    **dief@t** measures the diefficiency during an exlapsed time period *t* by computing
    the area under the curve of the answer traces.
    By default, the function computes the maximum of the execution time among the approaches
    in the answer trace, i.e., until the point in time when the slowest approach finishes.

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :param t: Point in time to compute dief@t for. By default, the function computes the maximum of the execution time
              among the approaches in the answer trace.
    :param continue_to_end: Indicates whether the AUC should be continued until the end of the time frame
    :return: Dataframe with the dief@t values for each approach. Attributes of the dataframe: test, approach, dieft.

    **Examples**

    >>> dieft(traces, "Q9.sparql")
    >>> dieft(traces, "Q9.sparql", 7.5)
    """
    # Initialize output structure.
    df = np.empty(shape=0, dtype=[('test', inputtrace['test'].dtype),
                                  ('approach', inputtrace['approach'].dtype),
                                  ('dieft', float)])

    # Obtain test and approaches to compare.
    results = inputtrace[inputtrace['test'] == inputtest]
    approaches = np.unique(results['approach'])

    # Obtain maximum t over all approaches if t is not set.
    if t == -1:
        t = np.max(results['time'])

    # Compute dieft per approach.
    for a in approaches:
        dief = 0
        subtrace = results[(results['approach'] == a) & (results['time'] <= t)]

        if continue_to_end:
            com = np.array([(inputtest, a, len(subtrace), t)],
                           dtype=[('test', subtrace['test'].dtype),
                                  ('approach', subtrace['approach'].dtype),
                                  ('answer', int),
                                  ('time', float)]
                           )

            if len(subtrace) == 1 and subtrace['answer'] == 0:
                pass
            else:
                subtrace = np.concatenate((subtrace, com), axis=0)

        if len(subtrace) > 1:
            dief = np.trapz(subtrace['answer'], subtrace['time'])

        res = np.array([(inputtest, a, dief)],
                       dtype=[('test', subtrace['test'].dtype),
                              ('approach', subtrace['approach'].dtype),
                              ('dieft', float)])
        df = np.append(df, res, axis=0)

    return df


def diefk(inputtrace: np.ndarray, inputtest: str, k: int = -1) -> np.ndarray:
    """
    Computes the **dief@k** metric for a specific test at a given number of answers *k*.

    **dief@k** measures the diefficiency while *k* answers are produced by computing
    the area under the curve of the answer traces.
    By default, the function computes the minimum of the total number of answer produces by the approaches.

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :param k: Number of answers to compute dief@k for. By default, the function computes the minimum of the total number
              of answers produced by the approaches.
    :return: Dataframe with the dief@k values for each approach. Attributes of the dataframe: test, approach, diefk.

    **Examples**

    >>> diefk(traces, "Q9.sparql")
    >>> diefk(traces, "Q9.sparql", 1000)
    """
    # Initialize output structure.
    df = np.empty(shape=0, dtype=[('test', inputtrace['test'].dtype),
                                  ('approach', inputtrace['approach'].dtype),
                                  ('diefk', float)])

    # Obtain test and approaches to compare.
    results = inputtrace[inputtrace['test'] == inputtest]
    approaches = np.unique(results['approach'])

    # Obtain k per approach.
    if k == -1:
        n = []
        for a in approaches:
            x = results[results['approach'] == a]
            n.append(len(x))
        k = min(n)

    # Compute diefk per approach.
    for a in approaches:
        dief = 0
        subtrace = results[(results['approach'] == a) & (results['answer'] <= k)]
        if len(subtrace) > 1:
            dief = np.trapz(subtrace['answer'], subtrace['time'])
        res = np.array([(inputtest, a, dief)],
                       dtype=[('test', inputtrace['test'].dtype),
                              ('approach', inputtrace['approach'].dtype),
                              ('diefk', float)])
        df = np.append(df, res, axis=0)

    return df


def diefk2(inputtrace: np.ndarray, inputtest: str, kp: float = -1.0) -> np.ndarray:
    """
    Computes the **dief@k** metric for a specific test at a given percentage of answers *kp*.

    **dief@k** measures the diefficiency while the first *kp* percent of answers are produced
    by computing the area under the curve of the answer traces.
    By default, this function behaves the same as ``diefk``. This also holds for kp = 1.0.
    The function computes the portion *kp* of the minimum number of answers produces by the approaches.

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :param kp: Ratio of answers to compute dief@k for (kp in [0.0;1.0]). By default and when kp=1.0, this function behaves
               the same as diefk. It computes the kp portion of the minimum number of answers produced by the approaches.
    :return: Dataframe with the dief@k values for each approach. Attributes of the dataframe: test, approach, diefk.

    **Examples**

    >>> diefk2(traces, "Q9.sparql")
    >>> diefk2(traces, "Q9.sparql", 0.25)
    """
    # Obtain test and approaches to compare.
    results = inputtrace[inputtrace['test'] == inputtest]
    approaches = np.unique(results['approach'])

    # Obtain k per approach.
    n = []
    for a in approaches:
        x = results[results['approach'] == a]
        n.append(len(x))
    k = min(n)
    if kp > -1:
        k = k * kp

    # Compute diefk.
    df = diefk(inputtrace, inputtest, k)

    return df


def plot_answer_trace(inputtrace: np.ndarray, inputtest: str, colors: list = DEFAULT_COLORS) -> Figure:
    """
    Plots the answer trace of a given test for all approaches.

    Answer traces record the points in time when an approach produces an answer.
    The plot generated by this function shows the answer traces of all approaches
    for the same test, e.g., execution of a specific query.

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :param colors: List of colors to use for the different approaches.
    :return: Plot of the answer traces of each approach when evaluating the input test.

    **Examples**

    >>> plot_answer_trace(traces, "Q9.sparql")
    >>> plot_answer_trace(traces, "Q9.sparql", ["#ECC30B","#D56062","#84BCDA"])
    """
    # Obtain test and approaches to compare.
    results = inputtrace[inputtrace['test'] == inputtest]
    approaches = np.unique(inputtrace['approach'])

    color_map = dict(zip(approaches, colors))

    # Generate plot.
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    for a in approaches:
        subtrace = results[results['approach'] == a]
        if subtrace.size == 0:
            continue
        plt.plot(subtrace['time'], subtrace['answer'], color=color_map[a], label=a, marker='o', markeredgewidth=0.0, linestyle='None')

    plt.xlabel('Time')
    plt.ylabel('# Answers Produced')
    plt.legend(loc='upper left')
    plt.title(inputtest, fontsize=16, loc="center", pad=20)
    plt.tight_layout()

    return fig


def plot_all_answer_traces(inputtrace: np.ndarray, colors: list = DEFAULT_COLORS) -> list:
    """
    Plots the answer traces of all tests; one plot per test.

    Answer traces record the points in time when an approach produces an answer.
    This function generates one plot per test showing the answer traces of all
    approaches for that specific test.

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param colors: List of colors to use for the different approaches.
    :return: Plot of the answer traces of each approach when evaluating the input test.

    **Examples**

    >>> plot_all_answer_traces(traces)
    >>> plot_all_answer_traces(traces, ["#ECC30B","#D56062","#84BCDA"])
    """
    # Obtain tests.
    tests = np.unique(inputtrace['test'])

    plots = []

    # Plot the answer traces for each test.
    for t in tests:
        plots.append(plot_answer_trace(inputtrace, t, colors))

    return plots


def plot_execution_time(metrics: np.ndarray, colors: list = DEFAULT_COLORS, log_scale: bool = False) -> Figure:
    """
    Creates a bar chart with the overall *execution time* for all the tests and approaches in the metrics data.

    Bar chart presenting the conventional performance measure *execution time*.
    Each test is represented as a group of bars representing the approaches.

    :param metrics: Dataframe with the metrics. Attributes of the dataframe: test, approach, tfft, totaltime, comp.
    :param colors: List of colors to use for the different approaches.
    :param log_scale: (optional) If log_scale is set to True, logarithmic scale for the y-axis will be used.
    :return: Plot of the execution time for all tests and approaches in the metrics data provided.

    **Examples**

    >>> plot_execution_time(metrics)
    >>> plot_execution_time(metrics, ["#ECC30B","#D56062","#84BCDA"])
    >>> plot_execution_time(metrics, log_scale=True)
    >>> plot_execution_time(metrics, ["#ECC30B","#D56062","#84BCDA"], log_scale=True)
    """
    # Obtain test and approaches to compare.
    approaches = np.unique(metrics['approach'])
    tests = np.unique(metrics['test'])

    color_map = dict(zip(approaches, colors))

    fig, ax = plt.subplots(figsize=(0.95*len(tests), 5), dpi=100)
    fig.subplots_adjust(top=0.85, bottom=0.25, left=0.08)

    index = np.arange(len(tests))
    bar_width = 0.8 / len(approaches)

    # Compute x position of bar.
    def compute_x_pos(number_approaches: int, approach_pos: int) -> float:
        lower = -0.4 + bar_width / 2
        upper = 0.4 - bar_width / 2
        return lower + approach_pos*(upper - lower)/(number_approaches-1)

    # Generate plot.
    a_num = -1
    for a in approaches:
        a_num += 1
        submetrics = metrics[metrics['approach'] == a]
        tests_in_approach = np.unique(submetrics['test'])

        results = []
        for t in tests:
            if t not in tests_in_approach:
                results.append(0.0)
            else:
                results.append(submetrics[submetrics['test'] == t]['totaltime'][0])

        offset = compute_x_pos(len(approaches), a_num)
        ax.set_xlim(-0.4, len(tests)-0.6)
        plt.bar(index + offset, results, bar_width, color=color_map[a], label=a)

    plt.xticks(range(0, len(tests)), tests, rotation=90)
    ax.set_xlabel("Performed Test", fontsize='large', labelpad=10)
    ax.set_ylabel("Execution Time [s]", fontsize='large')
    ax.legend(approaches, bbox_to_anchor=(1, 1), loc="upper left", labelspacing=0.1, fontsize='medium', frameon=False)
    plt.title("Execution Time for Performed Tests", fontsize=16, loc="center", pad=10)
    if log_scale:
        ax.set_yscale('log')
    plt.tight_layout()

    return fig


def load_trace(filename: str) -> np.ndarray:
    """
    Reads answer traces from a CSV file.

    Answer traces record the points in time when an approach produces an answer.
    The attribues of the file specified in the header are expected to be:

    * *test*: the name of the executed test
    * *approach*: the name of the approach executed
    * *answer*: the number of the answer produced
    * *time*: time elapsed from the start of the execution until the generation of the answer

    :param filename: Path to the CSV file that contains the answer traces.
                     Attributes of the file specified in the header: test, approach, answer, time.
    :return: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.

    **Examples**

    >>> load_trace("data/traces.csv")
    """
    # Loading data.
    # names=True is not an error, it is valid for reading the column names from the data
    df = np.genfromtxt(filename, delimiter=',', names=True, dtype=None, encoding="utf8")

    # Return dataframe in order.
    return df[['test', 'approach', 'answer', 'time']]


def load_metrics(filename: str) -> np.ndarray:
    """
    Reads the other metrics from a CSV file.

    Conventional query performance measurements.
    The attribues of the file specified in the header are expected to be:

    * *test*: the name of the executed test
    * *approach*: the name of the approach executed
    * *tfft*: time elapsed until the first answer was generated
    * *totaltime*: time elapsed until the last answer was generated
    * *comp*: number of answers produced

    :param filename: Path to the CSV file that contains the other metrics.
                     Attributes of the file specified in the header: test, approach, tfft, totaltime, comp.
    :return: Dataframe with the other metrics. Attributes of the dataframe: test, approach, tfft, totaltime, comp.

    **Examples**

    >>> load_trace("data/metrics.csv")
    """
    # Loading data.
    # names=True is not an error, it is valid for reading the column names from the data
    df = np.genfromtxt(filename, delimiter=',', names=True, dtype=None, encoding="utf8")

    # Return dataframe in order.
    return df[['test', 'approach', 'tfft', 'totaltime', 'comp']]


def performance_of_approaches_with_dieft(traces: np.ndarray, metrics: np.ndarray, continue_to_end: bool = True) -> np.ndarray:
    """
    Compares **dief@t** with other conventional metrics used in query performance analysis.

    This function repeats the results reported in "Experiment 1" of :cite:p:`dief`.
    "Experiment 1" compares the performance of testing approaches when using metrics defined in the
    literature (*total execution time*, *time for the first tuple*, *throughput*, and *completeness*) and the metric **dieft@t**.

    :param traces: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param metrics: Metrics dataframe with the result of the other metrics.
                    The structure is as follows: test, approach, tfft, totaltime, comp.
    :param continue_to_end: Indicates whether the AUC should be continued until the end of the time frame
    :return: Dataframe with all the metrics.
             The structure is: test, approach, tfft, totaltime, comp, throughput, invtfft, invtotaltime, dieft

    **Examples**

    >>> performance_of_approaches_with_dieft(traces, metrics)
    """
    # Initialize output structure.
    df = np.empty(shape=0, dtype=[('test', traces['test'].dtype),
                                  ('approach', traces['approach'].dtype),
                                  ('tfft', metrics['tfft'].dtype),
                                  ('totaltime', metrics['totaltime'].dtype),
                                  ('comp', metrics['comp'].dtype),
                                  ('throughput', float),
                                  ('invtfft', float),
                                  ('invtotaltime', float),
                                  ('dieft', float)])

    # Obtain tests and approaches.
    tests = np.unique(metrics['test'])
    approaches = np.unique(metrics['approach'])

    # Compute metrics: dieft, throughput, inverse of execution time, inverse of time for the first tuple.
    for t in tests:
        subtrace = traces[traces['test'] == t]
        dieft_res = dieft(subtrace, t, continue_to_end=continue_to_end)

        for a in approaches:
            if a not in np.unique(dieft_res['approach']):
                continue

            dieft_ = dieft_res[(dieft_res['approach'] == a) & (dieft_res['test'] == t)]['dieft'][0]
            submetric = metrics[(metrics['approach'] == a) & (metrics['test'] == t)]

            throughput = submetric['comp'][0] / submetric['totaltime'][0]
            invtfft = 1 / submetric['tfft'][0]
            invtotaltime = 1 / submetric['totaltime'][0]

            res = np.array([(t, a, submetric['tfft'][0], submetric['totaltime'][0], submetric['comp'][0],
                             throughput, invtfft, invtotaltime, dieft_)],
                           dtype=[('test', submetric['test'].dtype),
                                  ('approach', submetric['approach'].dtype),
                                  ('tfft', submetric['tfft'].dtype),
                                  ('totaltime', submetric['totaltime'].dtype),
                                  ('comp', submetric['comp'].dtype),
                                  ('throughput', float),
                                  ('invtfft', float),
                                  ('invtotaltime', float),
                                  ('dieft', float)])
            df = np.append(df, res, axis=0)

    return df


def plot_performance_of_approaches_with_dieft(allmetrics: np.ndarray, q: str, colors: list = DEFAULT_COLORS) -> Figure:
    """
    Generates a radar plot that compares **dief@t** with conventional metrics for a specific test.

    This function plots the results reported for a single given test in "Experiment 1" (see :cite:p:`dief`).
    "Experiment 1" compares the performance of testing approaches when using metrics defined in the literature
    (*total execution time*, *time for the first tuple*, *throughput*, and *completeness*) and the metric **dieft@t**.

    :param allmetrics: Dataframe with all the metrics from "Experiment 1".
    :param q: ID of the selected test to plot.
    :param colors: List of colors to use for the different approaches.
    :return: Matplotlib radar plot for the specified test over the provided metrics.

    **Examples**

    >>> plot_performance_of_approaches_with_dieft(extended_metrics, "Q9.sparql")
    >>> plot_performance_of_approaches_with_dieft(extended_metrics, "Q9.sparql", ["#ECC30B","#D56062","#84BCDA"])
    """
    # Initialize output structure.
    df = np.empty(shape=0, dtype=[('invtfft', allmetrics['invtfft'].dtype),
                                  ('invtotaltime', allmetrics['invtotaltime'].dtype),
                                  ('comp', float),
                                  ('throughput', allmetrics['throughput'].dtype),
                                  ('dieft', allmetrics['dieft'].dtype)])

    # Obtain approaches.
    approaches = np.unique(allmetrics['approach'])
    color_map = dict(zip(approaches, colors))
    labels = []
    for a in approaches:
        submetric_approaches = allmetrics[(allmetrics['approach'] == a) & (allmetrics['test'] == q)]

        if submetric_approaches.size == 0:
            continue
        else:
            labels.append(a)

        res = np.array([((submetric_approaches['invtfft']), (submetric_approaches['invtotaltime']), (submetric_approaches['comp']),
                        (submetric_approaches['throughput']), (submetric_approaches['dieft']))],
                       dtype=[('invtfft', submetric_approaches['invtfft'].dtype),
                              ('invtotaltime', submetric_approaches['invtotaltime'].dtype),
                              ('comp', float),
                              ('throughput', submetric_approaches['throughput'].dtype),
                              ('dieft', submetric_approaches['dieft'].dtype)])
        df = np.append(df, res, axis=0)

    # Get maximum values
    maxs = [df['invtfft'].max(), df['invtotaltime'].max(), df['comp'].max(), df['throughput'].max(), df['dieft'].max()]

    # Normalize the data
    for row in df:
        row['invtfft'] = row['invtfft'] / maxs[0]
        row['invtotaltime'] = row['invtotaltime'] / maxs[1]
        row['comp'] = row['comp'] / maxs[2]
        row['throughput'] = row['throughput'] / maxs[3]
        row['dieft'] = row['dieft'] / maxs[4]

    # Plot metrics using spider plot.
    df = df.tolist()
    N = len(df[0])
    theta = radar_factory(N, frame='polygon')
    spoke_labels = ['(TFFT)^-1', '(ET)^-1       ', 'Comp', 'T', '     dief@t']
    case_data = df
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)
    ax.set_ylim(0, 1)
    ticks_loc = ax.get_yticks()
    ax.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    ax.set_yticklabels("" for _ in ticks_loc)
    legend_handles = []
    for d, label in zip(case_data, labels):
        legend_handles.append(mlines.Line2D([], [], color=color_map[label], ls='-', label=label))
        ax.plot(theta, d, label=label, color=color_map[label], zorder=10, clip_on=False)
        ax.fill(theta, d, label=label, facecolor=color_map[label], alpha=0.15)

    ax.set_varlabels(spoke_labels)
    ax.tick_params(labelsize=14)
    ax.legend(handles=legend_handles, loc=(0.80, 0.90), labelspacing=0.1, fontsize='medium', frameon=False)

    plt.setp(ax.spines.values(), color="grey")
    plt.title(q, fontsize=16, loc="center", pad=30)
    plt.tight_layout()

    return fig


def plot_all_performance_of_approaches_with_dieft(allmetrics: np.ndarray, colors: list = DEFAULT_COLORS) -> list:
    """
    Generates radar plots that compare dief@t with conventional metrics; one plot per test.

    This function plots the results reported in "Experiment 1" (see :cite:p:`dief`).
    "Experiment 1" compares the performance of testing approaches when using metrics defined in the literature
    (*total execution time*, *time for the first tuple*, *throughput*, and *completeness*) and the metric **dieft@t**.

    :param allmetrics: Dataframe with all the metrics from "Experiment 1".
    :param colors: List of colors to use for the different approaches.
    :return: List of matplotlib radar plots (one per test) over the provided metrics.

    **Examples**

    >>> plot_all_performance_of_approaches_with_dieft(extended_metrics)
    >>> plot_all_performance_of_approaches_with_dieft(extended_metrics, ["#ECC30B","#D56062","#84BCDA"])
    """
    # Obtain tests.
    tests = np.unique(allmetrics['test'])

    plots = []

    # Plot the metrics for each test in "Experiment 1"
    for t in tests:
        plots.append(plot_performance_of_approaches_with_dieft(allmetrics, t, colors))

    return plots


def continuous_efficiency_with_diefk(traces: np.ndarray) -> np.ndarray:
    """
    Compares **dief@k** at different answer completeness percentages.

    This function repeats the results reported in "Experiment 2"
    (see :cite:p:`dief`).
    "Experiment 2" measures the continuous efficiency of approaches when producing
    the first 25%, 50%, 75%, and 100% of the answers.

    :param traces: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :return: Dataframe with all the metrics. The structure is: test, approach, diefk25, diefk50, diefk75, diefk100.

    **Examples**

    >>> continuous_efficiency_with_diefk(traces)
    """
    # Initialize output structure.
    df = np.empty(shape=0, dtype=[('test', traces['test'].dtype),
                                  ('approach', traces['approach'].dtype),
                                  ('diefk25', float),
                                  ('diefk50', float),
                                  ('diefk75', float),
                                  ('diefk100', float)])

    # Obtain tests and approaches.
    tests = np.unique(traces['test'])
    approaches = np.unique(traces['approach'])

    # Compute diefk for different k%: 25, 50, 75, 100.
    for t in tests:
        subtrace = traces[traces['test'] == t]
        k25DF = diefk2(subtrace, t, 0.25)
        k50DF = diefk2(subtrace, t, 0.50)
        k75DF = diefk2(subtrace, t, 0.75)
        k100DF = diefk2(subtrace, t, 1.00)

        for a in approaches:
            if a not in np.unique(k25DF['approach']) \
                    or a not in np.unique(k50DF['approach']) \
                    or a not in np.unique(k75DF['approach']) \
                    or a not in np.unique(k100DF['approach']):
                continue

            diefk25 = k25DF[k25DF['approach'] == a]['diefk'][0]
            diefk50 = k50DF[k50DF['approach'] == a]['diefk'][0]
            diefk75 = k75DF[k75DF['approach'] == a]['diefk'][0]
            diefk100 = k100DF[k100DF['approach'] == a]['diefk'][0]

            res = np.array([(t, a, diefk25, diefk50, diefk75, diefk100)],
                           dtype=[('test', traces['test'].dtype),
                                  ('approach', traces['approach'].dtype),
                                  ('diefk25', float),
                                  ('diefk50', float),
                                  ('diefk75', float),
                                  ('diefk100', float)])
            df = np.append(df, res, axis=0)

    return df


def plot_continuous_efficiency_with_diefk(diefkDF: np.ndarray, q: str, colors: list = DEFAULT_COLORS) -> Figure:
    """
    Generates a radar plot that compares **dief@k** at different answer completeness percentages for a specific test.

    This function plots the results reported for a single given test in "Experiment 2"
    (see :cite:p:`dief`).
    "Experiment 2" measures the continuous efficiency of approaches when producing
    the first 25%, 50%, 75%, and 100% of the answers.

    :param diefkDF: Dataframe with the results from "Experiment 2".
    :param q: ID of the selected test to plot.
    :param colors: List of colors to use for the different approaches.
    :return: Matplotlib plot for the specified test over the provided metrics.

    **Examples**

    >>> plot_continuous_efficiency_with_diefk(diefkDF, "Q9.sparql")
    >>> plot_continuous_efficiency_with_diefk(diefkDF, "Q9.sparql", ["#ECC30B","#D56062","#84BCDA"])
    """
    # Initialize output structure.
    df = np.empty(shape=0, dtype=[('diefk25', float),
                                  ('diefk50', float),
                                  ('diefk75', float),
                                  ('diefk100', float)])

    # Obtain approaches.
    approaches = np.unique(diefkDF['approach'])
    labels = []
    color_map = dict(zip(approaches, colors))

    for a in approaches:
        submetric_approaches = diefkDF[(diefkDF['approach'] == a) & (diefkDF['test'] == q)]

        if submetric_approaches.size == 0:
            continue
        else:
            labels.append(a)

        res = np.array([((submetric_approaches['diefk25']), (submetric_approaches['diefk50']), (submetric_approaches['diefk75']),
                        (submetric_approaches['diefk100']))],
                       dtype=[('diefk25', submetric_approaches['diefk25'].dtype),
                              ('diefk50', submetric_approaches['diefk50'].dtype),
                              ('diefk75', submetric_approaches['diefk75'].dtype),
                              ('diefk100', submetric_approaches['diefk100'].dtype)])

        df = np.append(df, res, axis=0)

    # Get maximum values
    maxs = [df['diefk25'].max(), df['diefk50'].max(), df['diefk75'].max(), df['diefk100'].max()]

    # Normalize the data
    for row in df:
        row['diefk25'] = row['diefk25'] / maxs[0]
        row['diefk50'] = row['diefk50'] / maxs[1]
        row['diefk75'] = row['diefk75'] / maxs[2]
        row['diefk100'] = row['diefk100'] / maxs[3]

    # Plot metrics using spider plot.
    df = df.tolist()
    N = len(df[0])
    theta = radar_factory(N, frame='polygon')
    spoke_labels = ['k=25%', 'k=50%      ', 'k=75%', '        k=100%']
    case_data = df
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)
    ax.set_ylim(0, 1)
    ticks_loc = ax.get_yticks()
    ax.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    ax.set_yticklabels("" for _ in ticks_loc)
    legend_handles = []
    for d, label in zip(case_data, labels):
        legend_handles.append(mlines.Line2D([], [], color=color_map[label], ls='-', label=label))
        ax.plot(theta, d, color=color_map[label], zorder=10, clip_on=False)
        ax.fill(theta, d, facecolor=color_map[label], alpha=0.15)
    ax.set_varlabels(spoke_labels)
    ax.tick_params(labelsize=14, zorder=0)

    ax.legend(handles=legend_handles, loc=(0.80, 0.90), labelspacing=0.1, fontsize='medium', frameon=False)

    plt.setp(ax.spines.values(), color="grey")
    plt.title(q, fontsize=16, loc="center", pad=30)
    plt.tight_layout()

    return fig


def plot_all_continuous_efficiency_with_diefk(diefkDF: np.ndarray, colors: list = DEFAULT_COLORS) -> list:
    """
    Generates radar plots that compare **dief@k** at different answer completeness percentages; one per test.

    This function plots the results reported in "Experiment 2"
    (see :cite:p:`dief`).
    "Experiment 2" measures the continuous efficiency of approaches when producing
    the first 25%, 50%, 75%, and 100% of the answers.

    :param diefkDF: Dataframe with the results from "Experiment 2".
    :param colors: List of colors to use for the different approaches.
    :return: List of matplotlib plots (one per test) over the provided metrics.


    **Examples**

    >>> plot_all_continuous_efficiency_with_diefk(diefkDF)
    >>> plot_all_continuous_efficiency_with_diefk(diefkDF, ["#ECC30B","#D56062","#84BCDA"])
    """
    # Obtain tests.
    tests = np.unique(diefkDF['test'])

    plots = []
    # Plot the metrics for each test in "Experiment 2"
    for t in tests:
        plots.append(plot_continuous_efficiency_with_diefk(diefkDF, t, colors))

    return plots
