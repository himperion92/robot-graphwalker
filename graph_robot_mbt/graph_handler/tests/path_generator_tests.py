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

    @mock.patch('subprocess.call')
    def test_check_model_format(self, call_mock):
        correct_model = 'correct_model.graphml'
        call_mock.(
            r'gw check -m {model_path} "random(edge_coverage(100))"'.format(
                model_path=correct_model))
        response = self._path_gen.check_model_format('dummy_model.graphml')
        self.assertEqual(True, response)
        call_mock.assert_called_once_with(
            r'gw check -m {model_path} "random(edge_coverage(100))"'.format(
                model_path=correct_model))

        
