#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt


def dieft(inputtrace, inputtest, t=-1.0):
    """
    This function computes the dief@t metric.

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :type inputtrace: numpy.ndarray
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :type inputtest: str
    :param t: Point in time to compute dieft. By default, the function computes the minimum of the execution time among the approaches in the answer trace.
    :type t: float
    :return: Dataframe with the dief@t values for each approach. Attributes of the dataframe: test, approach, dieft.
    :rtype: numpy.ndarray
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


def diefk(inputtrace, inputtest, k=-1):
    """
    This function computes the dief@k metric at a given k (number of answers).

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :type inputtrace: numpy.ndarray
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :type inputtest: str
    :param k: Number of answers to compute diefk. By default, the function computes the minimum of the total number of answers produced by the approaches.
    :type k: int
    :return: Dataframe with the dief@k values for each approach. Attributes of the dataframe: test, approach, diefk.
    :rtype: numpy.ndarray
    """
    # Initialize output structure.
    df = np.empty(shape=0, dtype=[('test', inputtrace['test'].dtype),
                                  ('approach', inputtrace['approach'].dtype),
                                  ('diefk', float)])

    # Obtain test and approaches to compare.
    results = inputtrace[inputtrace['test'] == inputtest]
    approaches = set(inputtrace['approach'])
    print("approaches:", approaches)

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


def diefk2(inputtrace, inputtest, kp=-1.0):
    """
    This function computes the dief@k metric at a given kp (percentage of answers).

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :type inputtrace: numpy.ndarray
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :type inputtest: str
    :param kp: Ratio of answers to compute diefk (kp in [0.0;1.0]). By default and when kp=1.0, this function behaves the same as diefk. It computes the kp portion of of minimum of of number of answers  produced by the approaches.
    :type kp: float
    :return: Dataframe with the dief@k values for each approach. Attributes of the dataframe: test, approach, diefk.
    :rtype: numpy.ndarray
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


def plot_answer_trace(inputtrace, inputtest):
    """
    This function plots the answer trace of a given test.

    :param inputtrace: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :type inputtrace: numpy.ndarray
    :param inputtest: Specifies the specific test to analyze from the answer trace.
    :type inputtest: str
    :return: Plot of the answer traces of each approach when evaluating the input test.
    :rtype: matplotlib.pyplot.plot
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


def load_trace(filename):
    """
    This function reads answer traces from a CSV file.

    :param filename: Path to the CSV file that contains the answer traces. Attributes of the file specified in the header: test, approach, answer, time.
    :type filename: str
    :return: Dataframe with the answer trace. Attributes of the dataframe: test, approach, answer, time.
    :rtype: numpy.ndarray
    """
    # Loading data.
    # names=True is not an error, it is valid for reading the column names from the data
    df = np.genfromtxt(filename, delimiter=',', names=True, dtype=None, encoding="utf8")

    # Return dataframe in order.
    return df[['test', 'approach', 'answer', 'time']]
