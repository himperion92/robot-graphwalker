import unittest
import logging
import mock

from graph_robot_mbt.graph_handler.path_generator import PathGenerator


class PathGeneratorTests(unittest.TestCase):
    """
    Unit Tests for PathGenerator class.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self._path_gen = PathGenerator()

    @mock.patch('subprocess.check_output')
    def test_check_model_format(self, check_out_mock):
        correct_model = 'correct_model.graphml'
        incorrect_model = 'incorrect_model.graphml'
        check_out_mock.side_effect = ['No issues found with the model(s).',
                                      'Error']
        response = self._path_gen.check_model_format(correct_model)
        self.assertEqual(True, response)
        response = self._path_gen.check_model_format(incorrect_model)
        self.assertEqual(False, response)
        check_out_mock.assert_has_calls(
            [mock.call(
                (
                    r'gw check -m {model_path} "random(edge_coverage(100))"'
                ).format(model_path=correct_model)),
             mock.call(
                (
                    r'gw check -m {model_path} "random(edge_coverage(100))"'
                ).format(model_path=incorrect_model))]
        )
