import unittest
import diefpy.dief as diefpy
from pkg_resources import resource_filename


class DiefTestCase(unittest.TestCase):

    def test_dieft0(self):
        input_file = resource_filename('diefpy', 'data/traces.csv')
        traces = diefpy.load_trace(input_file)
        test = "Q9.rq"
        res = diefpy.dieft(traces, test)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['dieft'][0], 14588.18, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['dieft'][0], 12992.97, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['dieft'][0], 20232.39, 2)

    def test_dieft1(self):
        input_file = resource_filename('diefpy', 'data/traces.csv')
        traces = diefpy.load_trace(input_file)
        test = "Q9.rq"
        t = 7.5
        res = diefpy.dieft(traces, test, t)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['dieft'][0], 1196.724, 3)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['dieft'][0], 5179.909, 3)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['dieft'][0], 7431.953, 3)

    def test_diefk0(self):
        input_file = resource_filename('diefpy', 'data/traces.csv')
        traces = diefpy.load_trace(input_file)
        test = "Q9.rq"
        res = diefpy.diefk(traces, test)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk'][0], 14588.18, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk'][0], 12992.97, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk'][0], 20232.39, 2)

    def test_diefk1(self):
        input_file = resource_filename('diefpy', 'data/traces.csv')
        traces = diefpy.load_trace(input_file)
        test = "Q9.rq"
        k = 1000
        res = diefpy.diefk(traces, test, k)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk'][0], 1106.507, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk'][0], 1524.351, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk'][0], 1197.350, 2)

    def test_diefk2(self):
        input_file = resource_filename('diefpy', 'data/traces.csv')
        traces = diefpy.load_trace(input_file)
        test = "Q9.rq"
        kp = 0.25
        res = diefpy.diefk2(traces, test, kp)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk'][0], 1430.417, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk'][0], 1692.541, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk'][0], 1764.715, 2)

    def test_experiment1(self):
        input_file_taces = resource_filename('diefpy', 'data/traces.csv')
        input_file_metrics = resource_filename('diefpy', 'data/metrics.csv')
        traces = diefpy.load_trace(input_file_taces)
        metrics = diefpy.load_metrics(input_file_metrics)
        res = diefpy.performance_of_approaches_with_dieft(traces, metrics)

        # Check the values for Q9
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q9.rq')]['tfft'][0], 0.2416301, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q9.rq')]['totaltime'][0], 12.209977, 2)
        self.assertEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q9.rq')]['comp'][0], 5151)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q9.rq')]['throughput'][0], 421.8681, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q9.rq')]['invtfft'][0], 4.138558, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q9.rq')]['invtotaltime'][0], 0.08190024, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q9.rq')]['dieft'][0], 14588.18, 2)

        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q9.rq')]['tfft'][0], 0.3326499, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q9.rq')]['totaltime'][0], 9.303557, 2)
        self.assertEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q9.rq')]['comp'][0], 5151)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q9.rq')]['throughput'][0], 553.6592, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q9.rq')]['invtfft'][0], 3.006163, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q9.rq')]['invtotaltime'][0], 0.10748577, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q9.rq')]['dieft'][0], 12992.97, 2)

        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q9.rq')]['tfft'][0], 0.3710840, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q9.rq')]['totaltime'][0], 10.592792, 2)
        self.assertEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q9.rq')]['comp'][0], 5151)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q9.rq')]['throughput'][0], 486.2741, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q9.rq')]['invtfft'][0], 2.694808, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q9.rq')]['invtotaltime'][0], 0.09440382, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q9.rq')]['dieft'][0], 20232.39, 2)

        # Check the values for Q14
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q14.rq')]['tfft'][0], 51.13820291, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q14.rq')]['totaltime'][0], 198.65310788, 2)
        self.assertEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q14.rq')]['comp'][0], 5)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q14.rq')]['throughput'][0], 0.0251695, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q14.rq')]['invtfft'][0], 0.01955485, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q14.rq')]['invtotaltime'][0], 0.0050339, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q14.rq')]['dieft'][0], 233.78489006, 2)

        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q14.rq')]['tfft'][0], 44.490062, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q14.rq')]['totaltime'][0], 184.76617718, 2)
        self.assertEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q14.rq')]['comp'][0], 6)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q14.rq')]['throughput'][0], 0.03247348, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q14.rq')]['invtfft'][0], 0.02247693, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q14.rq')]['invtotaltime'][0], 0.00541225, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q14.rq')]['dieft'][0], 593.09502959, 2)

        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q14.rq')]['tfft'][0], 162.54994512, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q14.rq')]['totaltime'][0], 300.01341915, 2)
        self.assertEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q14.rq')]['comp'][0], 3)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q14.rq')]['throughput'][0], 0.00999955, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q14.rq')]['invtfft'][0], 0.00615196, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q14.rq')]['invtotaltime'][0], 0.00333318, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q14.rq')]['dieft'][0], 205.66096568, 2)

    def test_experiment2(self):
        input_file = resource_filename('diefpy', 'data/traces.csv')
        traces = diefpy.load_trace(input_file)
        res = diefpy.continuous_efficiency_with_diefk(traces)

        # Check the values for Q9
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q9.rq')]['diefk25'][0], 1430.417, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q9.rq')]['diefk50'][0], 5537.021, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q9.rq')]['diefk75'][0], 9389.35, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q9.rq')]['diefk100'][0], 14588.18, 2)

        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q9.rq')]['diefk25'][0], 1692.541, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q9.rq')]['diefk50'][0], 4636.632, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q9.rq')]['diefk75'][0], 7105.38, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q9.rq')]['diefk100'][0], 12992.97, 2)

        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q9.rq')]['diefk25'][0], 1764.715, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q9.rq')]['diefk50'][0], 6162.528, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q9.rq')]['diefk75'][0], 11684.55, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q9.rq')]['diefk100'][0], 20232.39, 2)

        # Check the values for Q14
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q14.rq')]['diefk25'][0], 0.0, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q14.rq')]['diefk50'][0], 0.0, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q14.rq')]['diefk75'][0], 18.15, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Selective') & (res['test'] == 'Q14.rq')]['diefk100'][0], 50.37, 2)

        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q14.rq')]['diefk25'][0], 0.0, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q14.rq')]['diefk50'][0], 0.0, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q14.rq')]['diefk75'][0], 7.936, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'Random') & (res['test'] == 'Q14.rq')]['diefk100'][0], 22.89, 2)

        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q14.rq')]['diefk25'][0], 0.0, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q14.rq')]['diefk50'][0], 0.0, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q14.rq')]['diefk75'][0], 152.30, 2)
        self.assertAlmostEqual(res[(res['approach'] == 'NotAdaptive') & (res['test'] == 'Q14.rq')]['diefk100'][0], 205.66, 2)


if __name__ == '__main__':
    unittest.main()
