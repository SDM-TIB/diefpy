import numpy as np
import matplotlib.pyplot as plt
from diefpy.radaraxes import radar_factory


def dieft(inputtrace: np.ndarray, inputtest: str, t: float = -1.0) -> np.ndarray:
    """
    This function computes the dief@t metric.

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :param t: Point in time to compute dieft. By default, the function computes the minimum of the execution time
              among the approaches in the answer trace.
    :return: Dataframe with the dief@t values for each approach. Attributes of the dataframe: test, approach, dieft.
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
    This function computes the dief@k metric at a given k (number of answers).

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :param k: Number of answers to compute diefk. By default, the function computes the minimum of the total number
              of answers produced by the approaches.
    :return: Dataframe with the dief@k values for each approach. Attributes of the dataframe: test, approach, diefk.
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
    This function computes the dief@k metric at a given kp (percentage of answers).

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :param kp: Ratio of answers to compute diefk (kp in [0.0;1.0]). By default and when kp=1.0, this function behaves
               the same as diefk. It computes the kp portion of the minimum number of answers produced by the approaches.
    :return: Dataframe with the dief@k values for each approach. Attributes of the dataframe: test, approach, diefk.
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


def plot_answer_trace(inputtrace: np.ndarray, inputtest: str, colors: list) -> plt:
    """
    This function plots the answer trace of a given test.

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :param colors: List of colors to use for the different approaches.
    :return: Plot of the answer traces of each approach when evaluating the input test.
    """
    # Obtain test and approaches to compare.
    results = inputtrace[inputtrace['test'] == inputtest]
    approaches = np.unique(inputtrace['approach'])

    color_map = dict(zip(approaches, colors))

    # Generate plot.
    plt.subplots(figsize=(10, 6), dpi=100)
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

    return plt


def plot_all_answer_traces(inputtrace: np.ndarray, colors: list) -> list:
    """
    This function plots the answer traces of all tests; one plot per test.

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param colors: List of colors to use for the different approaches.
    :return: Plot of the answer traces of each approach when evaluating the input test.
    """
    # Obtain tests.
    tests = np.unique(inputtrace['test'])

    plots = []

    # Plot the answer traces for each test.
    for t in tests:
        plots.append(plot_answer_trace(inputtrace, t, colors))

    return plots


def plot_execution_time(metrics: np.ndarray, colors: list, log_scale: bool = False) -> plt:
    """
    This function creates a bar plot with the overall execution time for all
    the tests and approaches in the metrics data.

    :param metrics: Dataframe with the metrics. Attributes of the dataframe: test, approach, tfft, totaltime, comp.
    :param colors: List of colors to use for the different approaches.
    :param log_scale: (optional) If log_scale is set to True, logarithmic scale for the y-axis will be used.
    :return: Plot of the execution time for all tests and approaches in the metrics data provided.
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

    return plt


def load_trace(filename: str) -> np.ndarray:
    """
    This function reads answer traces from a CSV file.

    :param filename: Path to the CSV file that contains the answer traces.
                     Attributes of the file specified in the header: test, approach, answer, time.
    :return: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    """
    # Loading data.
    # names=True is not an error, it is valid for reading the column names from the data
    df = np.genfromtxt(filename, delimiter=',', names=True, dtype=None, encoding="utf8")

    # Return dataframe in order.
    return df[['test', 'approach', 'answer', 'time']]


def load_metrics(filename: str) -> np.ndarray:
    """
    This function reads the other metrics from a CSV file.

    :param filename: Path to the CSV file that contains the other metrics.
                     Attributes of the file specified in the header: test, approach, tfft, totaltime, comp.
    :return: Dataframe with the other metrics. Attributes of the dataframe: test, approach, tfft, totaltime, comp.
    """
    # Loading data.
    # names=True is not an error, it is valid for reading the column names from the data
    df = np.genfromtxt(filename, delimiter=',', names=True, dtype=None, encoding="utf8")

    # Return dataframe in order.
    return df[['test', 'approach', 'tfft', 'totaltime', 'comp']]


def performance_of_approaches_with_dieft(traces: np.ndarray, metrics: np.ndarray) -> np.ndarray:
    """
    Compares dief@t with other benchmark metrics as in <doi:10.1007/978-3-319-68204-4_1>.
    This function repeats the results reported in "Experiment 1".
    "Experiment 1" compares the performance of testing approaches when using metrics defined in the
    literature (total execution time, time for the first tuple, throughput, and completeness) and the metric dieft@t.

    :param traces: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param metrics: Metrics dataframe with the result of the other metrics.
                    The structure is as follows: test, approach, tfft, totaltime, comp.
    :return: Dataframe with all the metrics.
             The structure is: test, approach, tfft, totaltime, comp, throughput, invtfft, invtotaltime, dieft
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
        dieft_res = dieft(subtrace, t)

        for a in approaches:
            if a not in np.unique(dieft_res['approach']):
                continue

            dieft_ = dieft_res[dieft_res['approach'] == a]['dieft'][0]
            submetric = metrics[metrics['approach'] == a]

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


def plot_performance_of_approaches_with_dieft(allmetrics: np.ndarray, q: str, colors: list) -> plt:
    """
    Generate radar plots that compare dief@t with other benchmark metrics in a specific test
    as in <doi:10.1007/978-3-319-68204-4_1>.
    This function plots the results reported for a single given test in "Experiment 1".
    "Experiment 1" compares the performance of testing approaches when using metrics defined in the
    literature (total execution time, time for the first tuple, throughput, and completeness) and the metric dieft@t.

    :param allmetrics: Dataframe with all the metrics from "Experiment 1".
    :param q: ID of the selected test to plot.
    :param colors: List of colors to use for the different approaches.
    """
    # Initialize output structure.
    df = np.empty(shape=0, dtype=[('invtfft', allmetrics['invtfft'].dtype),
                                  ('invtotaltime', allmetrics['invtotaltime'].dtype),
                                  ('comp', allmetrics['comp'].dtype),
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
                              ('comp', submetric_approaches['comp'].dtype),
                              ('throughput', submetric_approaches['throughput'].dtype),
                              ('dieft', submetric_approaches['dieft'].dtype)])
        df = np.append(df, res, axis=0)

    # Get maximum values
    maxs = [df['invtfft'].max(), df['invtotaltime'].max(), df['comp'].max(), df['throughput'].max(), df['dieft'].max()]
    max_ = max(maxs)

    # Normalize the data
    for row in df:
        row['invtfft'] = row['invtfft'] / maxs[0] * max_
        row['invtotaltime'] = row['invtotaltime'] / maxs[1] * max_
        row['comp'] = row['comp'] / maxs[2] * max_
        row['throughput'] = row['throughput'] / maxs[3] * max_
        row['dieft'] = row['dieft'] / maxs[4] * max_

    # Plot metrics using spider plot.
    df = df.tolist()
    N = len(df[0])
    theta = radar_factory(N, frame='polygon')
    spoke_labels = ['(TFFT)^-1', '(ET)^-1       ', 'Comp', 'T', '     dief@t']
    case_data = df
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)
    ax.set_ylim(0, max_)
    ax.set_yticklabels(["", "", "", "", ""])
    for d, label in zip(case_data, labels):
        ax.plot(theta, d, color=color_map[label], zorder=10, clip_on=False)
        ax.fill(theta, d, facecolor=color_map[label], alpha=0.15)

    ax.set_varlabels(spoke_labels)
    ax.tick_params(labelsize=14)
    ax.legend(labels, loc=(0.80, 0.90), labelspacing=0.1, fontsize='medium', frameon=False)

    plt.setp(ax.spines.values(), color="grey")
    plt.title(q, fontsize=16, loc="center", pad=30)
    plt.tight_layout()

    return plt


def plot_all_performance_of_approaches_with_dieft(allmetrics: np.ndarray, colors: list) -> list:
    """
    Generate radar plots that compare dief@t with other benchmark metrics in all tests
    as in <doi:10.1007/978-3-319-68204-4_1>.
    This function plots the results reported in "Experiment 1".
    "Experiment 1" compares the performance of testing approaches when using metrics defined in the
    literature (total execution time, time for the first tuple, throughput, and completeness) and the metric dieft@t.

    :param allmetrics: Dataframe with all the metrics from "Experiment 1".
    :param colors: List of colors to use for the different approaches.
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
    Compares dief@k at different answer portions as in <doi:10.1007/978-3-319-68204-4_1>.
    This function repeats the results reported in "Experiment 2".
    "Experiment 2" measures the continuous efficiency of approaches when producing
    the first 25%, 50%, 75%, and 100% of the answers.

    :param traces: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :return: Dataframe with all the metrics. The structure is: test, approach, diefk25, diefk50, diefk75, diefk100.
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


def plot_continuous_efficiency_with_diefk(diefkDF: np.ndarray, q: str, colors: list) -> plt:
    """
    Generate radar plots that compare dief@k at different answer completeness in a specific test
    as in  <doi:10.1007/978-3-319-68204-4_1>.
    This function plots the results reported for a single given test in "Experiment 2".
    "Experiment 2" measures the continuous efficiency of approaches when producing
    the first 25%, 50%, 75%, and 100% of the answers.

    :param diefkDF: Dataframe with the results from "Experiment 2".
    :param q: ID of the selected test to plot.
    :param colors: List of colors to use for the different approaches.
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
    max_ = max(maxs)

    # Normalize the data
    for row in df:
        row['diefk25'] = row['diefk25'] / maxs[0] * max_
        row['diefk50'] = row['diefk50'] / maxs[1] * max_
        row['diefk75'] = row['diefk75'] / maxs[2] * max_
        row['diefk100'] = row['diefk100'] / maxs[3] * max_

    # Plot metrics using spider plot.
    df = df.tolist()
    N = len(df[0])
    theta = radar_factory(N, frame='polygon')
    spoke_labels = ['k=25%', 'k=50%      ', 'k=75%', '        k=100%']
    case_data = df
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)
    ax.set_ylim(0, max_)
    ax.set_yticklabels(["", "", "", "", ""])
    for d, label in zip(case_data, labels):
        ax.plot(theta, d, color=color_map[label], zorder=10, clip_on=False)
        ax.fill(theta, d, facecolor=color_map[label], alpha=0.15)
    ax.set_varlabels(spoke_labels)
    ax.tick_params(labelsize=14, zorder=0)

    ax.legend(labels, loc=(0.80, 0.90), labelspacing=0.1, fontsize='medium', frameon=False)

    plt.setp(ax.spines.values(), color="grey")
    plt.title(q, fontsize=16, loc="center", pad=30)
    plt.tight_layout()

    return plt


def plot_all_continuous_efficiency_with_diefk(diefkDF: np.ndarray, colors: list) -> list:
    """
    Generate radar plots that compare dief@k at different answer completeness in a specific test
    as in  <doi:10.1007/978-3-319-68204-4_1>.
    This function plots the results reported in "Experiment 2".
    "Experiment 2" measures the continuous efficiency of approaches when producing
    the first 25%, 50%, 75%, and 100% of the answers.

    :param diefkDF: Dataframe with the results from "Experiment 2".
    :param colors: List of colors to use for the different approaches.
    """
    # Obtain tests.
    tests = np.unique(diefkDF['test'])

    plots = []
    # Plot the metrics for each test in "Experiment 2"
    for t in tests:
        plots.append(plot_continuous_efficiency_with_diefk(diefkDF, t, colors))

    return plots
