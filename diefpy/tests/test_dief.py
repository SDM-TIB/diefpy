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
    return data_dieft[approach][test][str(time)]


@pytest.mark.parametrize('approach', ['Selective', 'Random', 'NotAdaptive'])
@pytest.mark.parametrize('test', ['Q9.rq'])
@pytest.mark.parametrize('time', [-1, 7.5])
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
    return data_diefk[approach][test][str(answers)]


@pytest.mark.parametrize('approach', ['Selective', 'Random', 'NotAdaptive'])
@pytest.mark.parametrize('test', ['Q9.rq'])
@pytest.mark.parametrize('answers', [-1, 1000])
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
