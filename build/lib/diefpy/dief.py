#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt


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
    approaches = set(results['approach'])

    # Obtain maximum t over all approaches if t is not set.
    if t == -1:
        t = np.max(results['time'])

    # Compute dieft per approach.
    for a in approaches:
        dief = 0
        subtrace = results[(results['approach'] == a) & (results['time'] <= t)]
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


def diefk(inputtrace: np.ndarray, inputtest: np.ndarray, k: int = -1) -> np.ndarray:
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
    approaches = set(inputtrace['approach'])

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
    approaches = set(inputtrace['approach'])

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


def plot_answer_trace(inputtrace: np.ndarray, inputtest: str) -> plt:
    """
    This function plots the answer trace of a given test.

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :return: Plot of the answer traces of each approach when evaluating the input test.
    """
    # Obtain test and approaches to compare.
    results = inputtrace[inputtrace['test'] == inputtest]
    approaches = set(inputtrace['approach'])

    # Generate plot.
    for a in approaches:
        subtrace = results[results['approach'] == a]
        plt.plot(subtrace['time'], subtrace['answer'], label=a, marker='o', markeredgewidth=0.0, linestyle='None')

    plt.xlabel('Time')
    plt.ylabel('# Answers Produced')
    plt.legend(loc='upper left')
    plt.show()

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
    return df[['test', 'approach', 'tfft', 'totalttime', 'comp']]


def experiment1(traces: np.ndarray, metrics: np.ndarray) -> np.ndarray:
    """
    Compares dief@t with other benchmark metrics as in <doi:10.1007/978-3-319-68204-4_1>.
    This function repeats the results reported in "Experiment 1".
    "Experiment 1" compares the performance of querying approaches when using metrics defined in the
    literature (total execution time, time for the first tuple, throughput, and completeness) and the metric dieft@t.

    :param traces: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :param metrics: Metrics dataframe with the result of the other metrics.
                    The structure is as follows: test, approach, tfft, totaltime, comp.
    :return: Dataframe with all the metrics.
             The structure is: test, approach, tfft, totaltime, comp, throughput, invtfft invtotaltime, dieft
    """
    # TODO: actual implementation
    return np.empty([1, 9])


def plotExperiment1Test(allmetrics: np.ndarray, q: str, title: str = None) -> None:
    """
    Generate radar plots that compare dief@t with other benchmark metrics in a specific test
    as in <doi:10.1007/978-3-319-68204-4_1>.
    This function plots the results reported for a single given test in "Experiment 1".
    "Experiment 1" compares the performance of querying approaches when using metrics defined in the
    literature (total execution time, time for the first tuple, throughput, and completeness) and the metric dieft@t.

    :param allmetrics: Dataframe with all the metrics from "Experiment 1".
    :param q: ID of the selected test to plot.
    :param title: Title used in the plot; defaults to the selected test ID.
    """
    # TODO: actual implementation
    if not title:
        title = q
    pass


def plotExperiment1(allmetrics: np.ndarray) -> None:
    """
    Generate radar plots that compare dief@t with other benchmark metrics in all tests
    as in <doi:10.1007/978-3-319-68204-4_1>.
    This function plots the results reported in "Experiment 1".
    "Experiment 1" compares the performance of querying approaches when using metrics defined in the
    literature (total execution time, time for the first tuple, throughput, and completeness) and the metric dieft@t.

    :param allmetrics: Dataframe with all the metrics from "Experiment 1".
    """
    # Obtain queries.
    queries = np.unique(allmetrics['test'])

    # Plot the metrics for each test in "Experiment 1"
    for q in queries:
        plotExperiment1Test(allmetrics, q)


def experiment2(traces: np.ndarray) -> np.ndarray:
    """
    Compares dief@k at different answer portions as in <doi:10.1007/978-3-319-68204-4_1>.
    This function repeats the results reported in "Experiment 2".
    "Experiment 2" measures the continuous efficiency of approaches when producing
    the first 25%, 50%, 75%, and 100% of the answers.

    :param traces: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :return: Dataframe with all the metrics. The structure is: test, approach, diefk25, diefk50, diefk75, diefk100.
    """
    # TODO: actual implementation
    return np.empty([1, 6])


def plotExperiment2Test(diefkDF: np.ndarray, q: str) -> None:
    """
    Generate radar plots that compare dief@k at different answer completeness in a specific test
    as in  <doi:10.1007/978-3-319-68204-4_1>.
    This function plots the results reported for a single given test in "Experiment 2".
    "Experiment 2" measures the continuous efficiency of approaches when producing
    the first 25%, 50%, 75%, and 100% of the answers.

    :param diefkDF: Dataframe with the results from "Experiment 2".
    :param q: ID of the selected test to plot.
    """
    # TODO: actual implementation
    pass


def plotExperiment2(diefkDF: np.ndarray) -> None:
    """
    Generate radar plots that compare dief@k at different answer completeness in a specific test
    as in  <doi:10.1007/978-3-319-68204-4_1>.
    This function plots the results reported in "Experiment 2".
    "Experiment 2" measures the continuous efficiency of approaches when producing
    the first 25%, 50%, 75%, and 100% of the answers.

    :param diefkDF: Dataframe with the results from "Experiment 2".
    """
    # Obtain queries.
    queries = np.unique(diefkDF['test'])

    # Plot the metrics for each test in "Experiment 2"
    for q in queries:
        plotExperiment1Test(diefkDF, q)
