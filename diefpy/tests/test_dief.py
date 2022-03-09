import json
import pathlib

import pytest
from pkg_resources import resource_filename

import diefpy.dief as diefpy


@pytest.fixture(scope="session")
def traces():
    input_file_traces = resource_filename('diefpy', 'data/traces.csv')
    return diefpy.load_trace(input_file_traces)


@pytest.fixture(scope="session")
def metrics():
    input_file_metrics = resource_filename('diefpy', 'data/metrics.csv')
    return diefpy.load_metrics(input_file_metrics)


@pytest.fixture(scope="session")
def data_performance_metrics():
    file_name = resource_filename('diefpy', 'tests/expected_values/performance_metrics.json')
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
    file_name = resource_filename('diefpy', 'tests/expected_values/continuous_efficiency.json')
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
    file_name = resource_filename('diefpy', 'tests/expected_values/dieft.json')
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
    file_name = resource_filename('diefpy', 'tests/expected_values/diefk.json')
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
    file_name = resource_filename('diefpy', 'tests/expected_values/diefk2.json')
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
