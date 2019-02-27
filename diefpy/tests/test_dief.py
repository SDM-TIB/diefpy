import unittest
import diefpy.dief as diefpy
from pkg_resources import resource_filename


class DiefTestCase(unittest.TestCase):

    def test_dieft0(self):
        input_file = resource_filename(__name__, 'traces.csv')
        traces = diefpy.load_answer_trace(input_file)
        test = "Q9.sparql"
        res = diefpy.dieft(traces, test)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['dieft'][0], 14588.18, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['dieft'][0], 27963.93, 2)
        self.assertAlmostEqual (res[res['approach'] == 'NotAdaptive']['dieft'][0], 28563.16, 2)

    def test_dieft1(self):
        input_file = resource_filename (__name__, 'traces.csv')
        traces = diefpy.load_answer_trace (input_file)
        test = "Q9.sparql"
        t = 7.5
        res = diefpy.dieft(traces, test, t)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['dieft'][0], 1203.705, 3)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['dieft'][0], 5192.282, 3)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['dieft'][0], 7485.623, 3)

    def test_diefk0(self):
        input_file = resource_filename(__name__, 'traces.csv')
        traces = diefpy.load_answer_trace(input_file)
        test = "Q9.sparql"
        res = diefpy.diefk(traces, test)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk'][0], 14588.18, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk'][0], 12992.97, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk'][0], 20232.39, 2)

    def test_diefk1(self):
        input_file = resource_filename(__name__, 'traces.csv')
        traces = diefpy.load_answer_trace(input_file)
        test = "Q9.sparql"
        k = 1000
        res = diefpy.diefk(traces, test, k)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk'][0], 1106.507, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk'][0], 1524.351, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk'][0], 1197.350, 2)

    def test_diefk2(self):
        input_file = resource_filename(__name__, 'traces.csv')
        traces = diefpy.load_answer_trace(input_file)
        test = "Q9.sparql"
        kp = 0.25
        res = diefpy.diefk2(traces, test, kp)

        self.assertAlmostEqual(res[res['approach'] == 'Selective']['diefk'][0], 1430.417, 2)
        self.assertAlmostEqual(res[res['approach'] == 'Random']['diefk'][0], 1692.541, 2)
        self.assertAlmostEqual(res[res['approach'] == 'NotAdaptive']['diefk'][0], 1764.715, 2)


if __name__ == '__main__':
    unittest.main()
