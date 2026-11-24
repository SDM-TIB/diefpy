import json
import pathlib
import warnings
from importlib.resources import files

import numpy as np
import pytest
from matplotlib.colors import to_hex

import diefpy.dief as diefpy


def _resource_path(package: str, resource: str) -> str:
    return str(files(package).joinpath(resource))


def _expected_key(value) -> str:
    """The expected values are stored by argument value; the default (None) is stored under -1."""
    return '-1' if value is None else str(value)


@pytest.fixture(scope="session")
def traces():
    input_file_traces = _resource_path('diefpy', 'data/traces.csv')
    return diefpy.load_trace(input_file_traces)


@pytest.fixture(scope="session")
def metrics():
    input_file_metrics = _resource_path('diefpy', 'data/metrics.csv')
    return diefpy.load_metrics(input_file_metrics)


@pytest.fixture(scope="session")
def data_performance_metrics():
    file_name = _resource_path('diefpy', 'tests/expected_values/performance_metrics.json')
    file = pathlib.Path(file_name)
    return json.loads(file.read_text())


@pytest.fixture
def expected_performance_metrics(request, data_performance_metrics):
    approach = request.node.funcargs['approach']
    test = request.node.funcargs['test']
    metric = request.node.funcargs['metric']
    return data_performance_metrics[approach][test][metric]


@pytest.fixture(scope="session")
def actual_performance_metrics(traces, metrics):
    return diefpy.performance_of_approaches_with_dieft(traces, metrics, continue_to_end=False)


@pytest.mark.parametrize('approach', ['Selective', 'Random', 'NotAdaptive'])
@pytest.mark.parametrize('test', ['Q9.rq', 'Q14.rq'])
@pytest.mark.parametrize('metric', ['tfft', 'totaltime', 'comp', 'throughput', 'invtfft', 'invtotaltime', 'dieft'])
def test_performance_metrics(approach, test, metric, expected_performance_metrics, actual_performance_metrics):
    actual = actual_performance_metrics
    actual = actual[(actual['approach'] == approach) & (actual['test'] == test)][metric][0]
    assert expected_performance_metrics == pytest.approx(actual, abs=1e-5)


@pytest.fixture(scope="session")
def data_continuous_efficiency():
    file_name = _resource_path('diefpy', 'tests/expected_values/continuous_efficiency.json')
    file = pathlib.Path(file_name)
    return json.loads(file.read_text())


@pytest.fixture
def expected_continuous_efficiency(request, data_continuous_efficiency):
    approach = request.node.funcargs['approach']
    test = request.node.funcargs['test']
    metric = request.node.funcargs['metric']
    return data_continuous_efficiency[approach][test][metric]


@pytest.fixture(scope="session")
def actual_continuous_efficiency(traces):
    return diefpy.continuous_efficiency_with_diefk(traces)


@pytest.mark.parametrize('approach', ['Selective', 'Random', 'NotAdaptive'])
@pytest.mark.parametrize('test', ['Q9.rq', 'Q14.rq'])
@pytest.mark.parametrize('metric', ['diefk25', 'diefk50', 'diefk75', 'diefk100'])
def test_continuous_efficiency(approach, test, metric, expected_continuous_efficiency, actual_continuous_efficiency):
    actual = actual_continuous_efficiency
    actual = actual[(actual['approach'] == approach) & (actual['test'] == test)][metric][0]
    assert expected_continuous_efficiency == pytest.approx(actual, abs=1e-3)


@pytest.fixture(scope="session")
def data_dieft():
    file_name = _resource_path('diefpy', 'tests/expected_values/dieft.json')
    file = pathlib.Path(file_name)
    return json.loads(file.read_text())


@pytest.fixture
def expected_dieft(request, data_dieft):
    approach = request.node.funcargs['approach']
    test = request.node.funcargs['test']
    time = request.node.funcargs['time']
    return data_dieft[approach][test][_expected_key(time)]


@pytest.mark.parametrize('approach', ['Selective', 'Random', 'NotAdaptive'])
@pytest.mark.parametrize('test', ['Q9.rq'])
@pytest.mark.parametrize('time', [None, 7.5])
def test_dieft(approach, test, time, traces, expected_dieft):
    res = diefpy.dieft(traces, test, time, continue_to_end=False)
    actual = res[res['approach'] == approach]['dieft'][0]
    assert expected_dieft == pytest.approx(actual, abs=1e-3)


@pytest.fixture(scope="session")
def data_diefk():
    file_name = _resource_path('diefpy', 'tests/expected_values/diefk.json')
    file = pathlib.Path(file_name)
    return json.loads(file.read_text())


@pytest.fixture
def expected_diefk(request, data_diefk):
    approach = request.node.funcargs['approach']
    test = request.node.funcargs['test']
    answers = request.node.funcargs['answers']
    return data_diefk[approach][test][_expected_key(answers)]


@pytest.mark.parametrize('approach', ['Selective', 'Random', 'NotAdaptive'])
@pytest.mark.parametrize('test', ['Q9.rq'])
@pytest.mark.parametrize('answers', [None, 1000])
def test_diefk(approach, test, answers, traces, expected_diefk):
    res = diefpy.diefk(traces, test, answers)
    actual = res[res['approach'] == approach]['diefk'][0]
    assert expected_diefk == pytest.approx(actual, abs=1e-3)


@pytest.fixture(scope="session")
def data_diefk2():
    file_name = _resource_path('diefpy', 'tests/expected_values/diefk2.json')
    file = pathlib.Path(file_name)
    return json.loads(file.read_text())


@pytest.fixture
def expected_diefk2(request, data_diefk2):
    approach = request.node.funcargs['approach']
    test = request.node.funcargs['test']
    percentage = request.node.funcargs['percentage']
    return data_diefk2[approach][test][str(percentage)]


@pytest.mark.parametrize('approach', ['Selective', 'Random', 'NotAdaptive'])
@pytest.mark.parametrize('test', ['Q9.rq'])
@pytest.mark.parametrize('percentage', [0.25, 1.0])
def test_diefk2(approach, test, percentage, traces, expected_diefk2):
    res = diefpy.diefk2(traces, test, percentage)
    actual = res[res['approach'] == approach]['diefk'][0]
    assert expected_diefk2 == pytest.approx(actual, abs=1e-3)


@pytest.mark.parametrize('loader,header,row,expected_fields', [
    (diefpy.load_trace, 'test,approach,answer,time', 'Q1.rq,A,1,0.5', ('test', 'approach', 'answer', 'time')),
    (diefpy.load_metrics, 'test,approach,tfft,totaltime,comp', 'Q1.rq,A,0.1,1.0,5',
     ('test', 'approach', 'tfft', 'totaltime', 'comp')),
])
def test_loaders_return_one_dimensional_array_for_single_row(tmp_path, loader, header, row, expected_fields):
    file = tmp_path / 'single_row.csv'
    file.write_text(header + '\n' + row + '\n')
    result = loader(str(file))
    assert result.ndim == 1
    assert len(result) == 1
    assert result.dtype.names == expected_fields


def _approaches(data, test):
    return np.unique(data['approach'][data['test'] == test]).tolist()


def _legend_labels(fig):
    return [text.get_text() for text in fig.axes[0].get_legend().get_texts()]


def _radar_values(fig):
    """Returns the values of all lines of the radar plot as 2D array (rows: approaches, columns: spokes)."""
    return np.array([line.get_ydata() for line in fig.axes[0].lines])


@pytest.mark.parametrize('test', ['Q9.rq', 'Q14.rq'])
def test_plot_performance_of_approaches_with_dieft(test, actual_performance_metrics):
    fig = diefpy.plot_performance_of_approaches_with_dieft(actual_performance_metrics, test)
    lines = fig.axes[0].lines
    values = _radar_values(fig)

    assert _legend_labels(fig) == _approaches(actual_performance_metrics, test)
    assert [to_hex(line.get_color()) for line in lines] == [to_hex(c) for c in diefpy.DEFAULT_COLORS]
    # Five metrics; the radar plot repeats the first value to close the polygon.
    assert values.shape == (len(lines), 6)
    assert values[:, 0] == pytest.approx(values[:, -1])
    # Each metric is normalized by its maximum over all approaches.
    assert values[:, :-1].max(axis=0) == pytest.approx(1.0)
    assert values.min() >= 0.0


@pytest.mark.parametrize('test', ['Q9.rq', 'Q14.rq'])
def test_plot_continuous_efficiency_with_diefk(test, actual_continuous_efficiency):
    fig = diefpy.plot_continuous_efficiency_with_diefk(actual_continuous_efficiency, test)
    lines = fig.axes[0].lines
    values = _radar_values(fig)

    assert _legend_labels(fig) == _approaches(actual_continuous_efficiency, test)
    assert [to_hex(line.get_color()) for line in lines] == [to_hex(c) for c in diefpy.DEFAULT_COLORS]
    # Four metrics (25%, 50%, 75%, 100%); the radar plot repeats the first value to close the polygon.
    assert values.shape == (len(lines), 5)
    assert values[:, 0] == pytest.approx(values[:, -1], nan_ok=True)
    # Each metric is normalized by its maximum over all approaches. If dief@k is zero for all approaches
    # (too few answers for the given percentage), there is nothing to normalize and the values are 0.
    assert not np.isnan(values).any()
    maxima = values[:, :-1].max(axis=0)
    assert (np.isclose(maxima, 1.0) | np.isclose(maxima, 0.0)).all()
    assert values.min() >= 0.0


def test_plot_all_radar_plots(actual_performance_metrics, actual_continuous_efficiency):
    tests = np.unique(actual_performance_metrics['test'])
    assert len(diefpy.plot_all_performance_of_approaches_with_dieft(actual_performance_metrics)) == len(tests)
    assert len(diefpy.plot_all_continuous_efficiency_with_diefk(actual_continuous_efficiency)) == len(tests)


@pytest.mark.parametrize('test', ['Q9.rq', 'Q14.rq'])
def test_plot_answer_trace(test, traces):
    fig = diefpy.plot_answer_trace(traces, test)
    assert [line.get_label() for line in fig.axes[0].lines] == _approaches(traces, test)


def test_plot_all_answer_traces(traces):
    assert len(diefpy.plot_all_answer_traces(traces)) == len(np.unique(traces['test']))


@pytest.mark.parametrize('log_scale', [False, True])
def test_plot_execution_time(log_scale, metrics):
    fig = diefpy.plot_execution_time(metrics, log_scale=log_scale)
    assert fig.axes[0].get_yscale() == ('log' if log_scale else 'linear')
    assert len(fig.axes[0].patches) == len(metrics)


def test_plot_continuous_efficiency_with_diefk_zero_for_all_approaches(actual_continuous_efficiency):
    # In the test data, dief@k for 25% and 50% of the answers is zero for all approaches of Q14.
    q14 = actual_continuous_efficiency[actual_continuous_efficiency['test'] == 'Q14.rq']
    assert (q14['diefk25'] == 0).all() and (q14['diefk50'] == 0).all()

    with warnings.catch_warnings():
        warnings.simplefilter('error', RuntimeWarning)  # no "invalid value encountered in divide"
        fig = diefpy.plot_continuous_efficiency_with_diefk(actual_continuous_efficiency, 'Q14.rq')

    values = _radar_values(fig)
    assert (values[:, :2] == 0).all()  # spokes of 25% and 50%
    assert values[:, 2:4].max(axis=0) == pytest.approx(1.0)  # spokes of 75% and 100%


def test_normalize_by_max():
    data = np.array([[0.0, 2.0, 1.0],
                     [0.0, 4.0, 3.0]])
    with warnings.catch_warnings():
        warnings.simplefilter('error', RuntimeWarning)
        normalized = diefpy._normalize_by_max(data)
    assert normalized == pytest.approx(np.array([[0.0, 0.5, 1 / 3],
                                                 [0.0, 1.0, 1.0]]))
    assert data[1, 1] == 4.0  # input is not modified


@pytest.mark.parametrize('call', [
    lambda data, test: diefpy.dieft(data['traces'], test),
    lambda data, test: diefpy.diefk(data['traces'], test),
    lambda data, test: diefpy.diefk2(data['traces'], test, 0.5),
    lambda data, test: diefpy.plot_answer_trace(data['traces'], test),
    lambda data, test: diefpy.plot_performance_of_approaches_with_dieft(data['performance'], test),
    lambda data, test: diefpy.plot_continuous_efficiency_with_diefk(data['efficiency'], test),
], ids=['dieft', 'diefk', 'diefk2', 'plot_answer_trace', 'plot_performance', 'plot_continuous_efficiency'])
def test_unknown_test_raises_helpful_error(call, traces, actual_performance_metrics, actual_continuous_efficiency):
    data = {'traces': traces, 'performance': actual_performance_metrics, 'efficiency': actual_continuous_efficiency}
    with pytest.raises(ValueError, match=r"Test 'Q99.rq' not found\. Available tests: Q9\.rq, Q14\.rq"):
        call(data, 'Q99.rq')


def test_unknown_test_does_not_leave_figure_open(traces):
    import matplotlib.pyplot as plt
    figures_before = plt.get_fignums()
    with pytest.raises(ValueError):
        diefpy.plot_answer_trace(traces, 'Q99.rq')
    assert plt.get_fignums() == figures_before


def test_performance_of_approaches_with_dieft_test_missing_in_traces(traces, metrics):
    traces_without_q14 = traces[traces['test'] != 'Q14.rq']
    with pytest.raises(ValueError, match=r"Test 'Q14\.rq' not found\. Available tests: Q9\.rq"):
        diefpy.performance_of_approaches_with_dieft(traces_without_q14, metrics)


def test_unknown_test_message_lists_at_most_ten_tests(traces):
    tests = [f'Q{i}' for i in range(1, 26)]
    data = np.array([(t, 'A', 1, 0.1) for t in tests], dtype=traces.dtype)
    with pytest.raises(ValueError) as excinfo:
        diefpy.dieft(data, 'unknown')
    message = str(excinfo.value)
    assert 'Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, ... (25 tests in total)' in message
    assert 'Q11' not in message


def _same(a, b):
    return a.dtype == b.dtype and bool((a == b).all())


def test_default_arguments_can_be_passed_as_none(traces):
    assert _same(diefpy.dieft(traces, 'Q9.rq'), diefpy.dieft(traces, 'Q9.rq', None))
    assert _same(diefpy.diefk(traces, 'Q9.rq'), diefpy.diefk(traces, 'Q9.rq', None))
    assert _same(diefpy.diefk2(traces, 'Q9.rq'), diefpy.diefk2(traces, 'Q9.rq', None))
    # By default and for kp=1.0, diefk2 behaves the same as diefk.
    assert _same(diefpy.diefk2(traces, 'Q9.rq'), diefpy.diefk(traces, 'Q9.rq'))
    assert _same(diefpy.diefk2(traces, 'Q9.rq', 1.0), diefpy.diefk(traces, 'Q9.rq'))


@pytest.mark.parametrize('function,name,minus_one', [
    (diefpy.dieft, 't', -1), (diefpy.dieft, 't', -1.0),
    (diefpy.diefk, 'k', -1), (diefpy.diefk, 'k', -1.0),
    (diefpy.diefk2, 'kp', -1), (diefpy.diefk2, 'kp', -1.0),
])
def test_minus_one_is_deprecated_but_still_selects_the_default(function, name, minus_one, traces):
    expected = function(traces, 'Q9.rq')
    with pytest.warns(DeprecationWarning, match=rf'Passing {name}=-1 .* {name}=None') as record:
        actual = function(traces, 'Q9.rq', minus_one)
    assert _same(actual, expected)
    assert len(record) == 1
    assert pathlib.Path(record[0].filename).samefile(__file__)  # the warning points to the caller


def test_valid_arguments_do_not_warn(traces):
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        diefpy.dieft(traces, 'Q9.rq')
        diefpy.dieft(traces, 'Q9.rq', None)
        diefpy.dieft(traces, 'Q9.rq', 7.5)
        diefpy.diefk(traces, 'Q9.rq')
        diefpy.diefk(traces, 'Q9.rq', 1000)
        diefpy.diefk2(traces, 'Q9.rq')
        diefpy.diefk2(traces, 'Q9.rq', 0.25)
        diefpy.continuous_efficiency_with_diefk(traces)


@pytest.mark.parametrize('function,kwargs,message', [
    (diefpy.dieft, {'t': -2}, r'^t must not be negative, but is -2\.$'),
    (diefpy.dieft, {'t': -0.5}, r'^t must not be negative'),
    (diefpy.dieft, {'t': float('nan')}, r'^t must not be negative'),
    (diefpy.diefk, {'k': 0}, r'^k must be at least 1, but is 0\.$'),
    (diefpy.diefk, {'k': -5}, r'^k must be at least 1'),
    (diefpy.diefk, {'k': 0.5}, r'^k must be at least 1'),
    (diefpy.diefk, {'k': float('nan')}, r'^k must be at least 1'),
    (diefpy.diefk2, {'kp': 0}, r'^kp must be greater than 0 and at most 1, but is 0\.$'),
    (diefpy.diefk2, {'kp': -0.5}, r'^kp must be greater than 0 and at most 1'),
    (diefpy.diefk2, {'kp': -5}, r'^kp must be greater than 0 and at most 1'),  # was the default before
    (diefpy.diefk2, {'kp': 1.5}, r'^kp must be greater than 0 and at most 1, but is 1\.5\.$'),
    (diefpy.diefk2, {'kp': 1.0000001}, r'^kp must be greater than 0 and at most 1'),
    (diefpy.diefk2, {'kp': float('nan')}, r'^kp must be greater than 0 and at most 1'),
])
def test_invalid_arguments_raise_value_error(function, kwargs, message, traces):
    with warnings.catch_warnings():
        warnings.simplefilter('error')  # not a deprecation case
        with pytest.raises(ValueError, match=message):
            function(traces, 'Q9.rq', **kwargs)


def test_boundary_values_are_valid(traces):
    # No time has elapsed or only one answer is considered: there is no area under the curve.
    assert (diefpy.dieft(traces, 'Q9.rq', 0)['dieft'] == 0).all()
    assert (diefpy.diefk(traces, 'Q9.rq', 1)['diefk'] == 0).all()
    assert _same(diefpy.diefk2(traces, 'Q9.rq', 1.0), diefpy.diefk(traces, 'Q9.rq'))
    # A few answers and a small kp yield fewer than two answers and, hence, zero without an error.
    assert (diefpy.diefk2(traces, 'Q14.rq', 0.25)['diefk'] == 0).all()


def test_diefk_rounds_the_number_of_answers_down(traces):
    n = min(np.count_nonzero((traces['test'] == 'Q9.rq') & (traces['approach'] == a)) for a in np.unique(traces['approach']))
    assert n % 2 == 1  # kp * n = 0.5 * n is not an integer
    k = int(n * 0.5)
    expected = diefpy.diefk(traces, 'Q9.rq', k)
    assert _same(diefpy.diefk2(traces, 'Q9.rq', 0.5), expected)
    assert _same(diefpy.diefk(traces, 'Q9.rq', k + 0.5), expected)
    assert not _same(diefpy.diefk(traces, 'Q9.rq', k + 1), expected)
