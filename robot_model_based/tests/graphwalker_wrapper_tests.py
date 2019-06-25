import unittest
import logging
import os
import mock

from robot_model_based.graphwalker_wrapper import GraphwalkerWrapper


class GraphwalkerWrapperTests(unittest.TestCase):
    """
    Unitary Tests for GraphwalkerWrapper class.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self._gw = GraphwalkerWrapper(r'/home/bob/graphwalker-cli-3.4.2.jar')

    def test_init(self):
        self.assertEqual('java -jar /home/bob/graphwalker-cli-3.4.2.jar "$@"',
                         self._gw._cmd)

    @mock.patch('subprocess.check_output')
    def test_check_model_format(self, subprocess_mock):
        correct_model = 'correct_model.graphml'
        incorrect_model = 'incorrect_model.graphml'
        subprocess_mock.side_effect = ['No issues found with the model(s).',
                                       'Error']
        response = self._gw.check_model_format(correct_model)
        self.assertEqual(True, response)
        response = self._gw.check_model_format(incorrect_model)
        self.assertEqual(False, response)
        subprocess_mock.assert_has_calls(
            [mock.call(r'{cmd} check -m {model_path} '
                       r'"random(edge_coverage(100))"'.format(
                           cmd=self._gw._cmd, model_path=correct_model),
                       shell=True),
             mock.call(
                    r'{cmd} check -m {model_path} "random(edge_coverage(100))"'
                    r''.format(cmd=self._gw._cmd, model_path=incorrect_model),
                    shell=True)
             ]
        )

    @mock.patch(('robot_model_based.graphwalker_wrapper.GraphwalkerWrapper.'
                 '_parse_sequence'))
    @mock.patch('subprocess.check_output')
    def test_generate_path(self, subprocess_mock, parse_seq_mock):
        model = 'MyModel.graphml'
        retrieved_paths = ''.join((r'{"modelName":"air_handler_system"}', os.linesep)) + ''.join((r'{"modelName":"air_handler_system","data":[],"currentElementID":"n1","currentElementName":"Idle","properties":[{"x":380},{"y":225}]}', os.linesep)) + ''.join((r'{"modelName":"air_handler_system","data":[],"currentElementID":"e2","currentElementName":"TurnAcOn","properties":[]}', os.linesep)) + ''.join((r'{"modelName":"air_handler_system","data":[],"currentElementID":"n3","currentElementName":"CoolingDown","properties":[{"x":240},{"y":321}]}', os.linesep)) + ''.join((r'{"modelName":"air_handler_system","data":[],"currentElementID":"e9","currentElementName":"ReachTemp","properties":[]}', os.linesep)) + ''.join((r'{"modelName":"air_handler_system","data":[],"currentElementID":"n1","currentElementName":"Idle","properties":[{"x":380},{"y":225}]}', os.linesep))
        expected_path = [{"modelName": "air_handler_system"},
                         {"modelName": "air_handler_system", "data": [],
                          "currentElementID":"n1",
                          "currentElementName":"Idle",
                          "properties":[{"x": 380}, {"y": 225}]},
                         {"modelName": "air_handler_system", "data": [],
                          "currentElementID":"e2",
                          "currentElementName":"TurnAcOn", "properties":[]},
                         {"modelName": "air_handler_system", "data": [],
                          "currentElementID":"n3",
                          "currentElementName":"CoolingDown",
                          "properties":[{"x": 240}, {"y": 321}]},
                         {"modelName": "air_handler_system", "data": [],
                          "currentElementID":"e9",
                          "currentElementName":"ReachTemp", "properties":[]},
                         {"modelName": "air_handler_system",
                          "data": [], "currentElementID":"n1",
                          "currentElementName":"Idle",
                          "properties":[{"x": 380}, {"y": 225}]}
                         ]
        parse_seq_mock.side_effect = [expected_path]
        subprocess_mock.side_effect = [retrieved_paths]
        self._gw.generate_path(model, 'random', 'edge_coverage', '100')
        subprocess_mock.assert_called_once_with(
            r'{cmd} offline -o -m {model} "random(edge_coverage(100))"'
            ''.format(cmd=self._gw._cmd, model=model), shell=True)
        self.assertEqual(expected_path, self._gw.sequence)
