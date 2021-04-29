import unittest
import diefpy.dief as diefpy
from pkg_resources import resource_filename


class DiefTestCase(unittest.TestCase):

    def test_dieft0(self):
        input_file = resource_filename(__name__, 'traces.csv')
        traces = diefpy.load_trace(input_file)
        test = "Q9.rq"
        res = diefpy.dieft(traces, test)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['dieft'][0], 14588.18, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['dieft'][0], 27963.93, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['dieft'][0], 28563.16, 2)

    def test_dieft1(self):
        input_file = resource_filename(__name__, 'traces.csv')
        traces = diefpy.load_trace(input_file)
        test = "Q9.rq"
        t = 7.5
        res = diefpy.dieft(traces, test, t)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['dieft'][0], 1203.705, 3)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['dieft'][0], 5192.282, 3)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['dieft'][0], 7485.623, 3)

    def test_diefk0(self):
        input_file = resource_filename(__name__, 'traces.csv')
        traces = diefpy.load_trace(input_file)
        test = "Q9.rq"
        res = diefpy.diefk(traces, test)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk'][0], 14588.18, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk'][0], 12992.97, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk'][0], 20232.39, 2)

    def test_diefk1(self):
        input_file = resource_filename(__name__, 'traces.csv')
        traces = diefpy.load_trace(input_file)
        test = "Q9.rq"
        k = 1000
        res = diefpy.diefk(traces, test, k)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk'][0], 1106.507, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk'][0], 1524.351, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk'][0], 1197.350, 2)

    def test_diefk2(self):
        input_file = resource_filename(__name__, 'traces.csv')
        traces = diefpy.load_trace(input_file)
        test = "Q9.rq"
        kp = 0.25
        res = diefpy.diefk2(traces, test, kp)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk'][0], 1430.417, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk'][0], 1692.541, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk'][0], 1764.715, 2)

    def test_experiment1(self):
        input_file_taces = resource_filename(__name__, 'traces.csv')
        input_file_metrics = resource_filename(__name__, 'metrics.csv')
        traces = diefpy.load_trace(input_file_taces)
        metrics = diefpy.load_metrics(input_file_metrics)
        res = diefpy.experiment1(traces, metrics)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['tfft'][0], 0.2416301, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Selective']['totaltime'][0], 12.209977, 2)
        self.assertEqual(res[res['approach'] == 'Selective']['comp'][0], 5151)
        self.assertAlmostEqual(res[res['approach'] == 'Selective']['throughput'][0], 421.8681, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Selective']['invtfft'][0], 4.138558, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Selective']['invtotaltime'][0], 0.08190024, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Selective']['dieft'][0], 14588.18, 2)

        self.assertAlmostEqual(res[res['approach'] == 'Random']['tfft'][0], 0.3326499, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['totaltime'][0], 9.303557, 2)
        self.assertEqual(res[res['approach'] == 'Random']['comp'][0], 5151)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['throughput'][0], 553.6592, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['invtfft'][0], 3.006163, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['invtotaltime'][0], 0.10748577, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['dieft'][0], 27963.93, 2)

        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['tfft'][0], 0.3710840, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['totaltime'][0], 10.592792, 2)
        self.assertEqual(res[res['approach'] == 'NotAdaptive']['comp'][0], 5151)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['throughput'][0], 486.2741, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['invtfft'][0], 2.694808, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['invtotaltime'][0], 0.09440382, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['dieft'][0], 28563.16, 2)

    def test_experiment2(self):
        input_file = resource_filename(__name__, 'traces.csv')
        traces = diefpy.load_trace(input_file)
        res = diefpy.experiment2(traces)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk25'][0], 1430.417, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk50'][0], 5537.021, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk75'][0], 9389.35, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk100'][0], 14588.18, 2)

        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk25'][0], 1692.541, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk50'][0], 4636.632, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk75'][0], 7105.38, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk100'][0], 12992.97, 2)

        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk25'][0], 1764.715, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk50'][0], 6162.528, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk75'][0], 11684.55, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk100'][0], 20232.39, 2)


if __name__ == '__main__':
    unittest.main()
