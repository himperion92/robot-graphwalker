import unittest
import logging
import mock
from robot.running import TestSuite, TestCase

from graph_robot_mbt.robot_test_creator import RobotTestCreator


class RobotTestCreatorTests(unittest.TestCase):
    """
    Unitary tests for RobotTestCreator class.
    """

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self._tc_creator = RobotTestCreator()

    def test_import_test_libs(self):
        self._tc_creator.test_suite = mock.Mock()
        libs = ['Lib1', 'Lib2']
        self._tc_creator._import_test_libs(libs)
        self._tc_creator.test_suite.resource.imports.library.assert_has_calls(
            [mock.call(libs[0]), mock.call(libs[1])])

    def test_create_test_case(self):
        ts_mock = mock.Mock(spec_set=TestSuite())
        tc_mock = mock.Mock(spec_set=TestCase())
        ts_mock.tests.create.side_effect = [tc_mock]
        self._tc_creator.test_suite = ts_mock
        graph_seq = [{"modelName": "air_handler_system"},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID":"n1", "currentElementName":"Idle",
                      "properties":[{"x": 380}, {"y": 225}]},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID": "e3",
                      "currentElementName": "TurnOff", "properties":[]},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID": "n4", "currentElementName": "OFF",
                      "properties":[{"x": 608}, {"y": 116}]}]
        self._tc_creator._create_test_case(
            graph_seq, test_name='tc1', tags=['tag1', 'tag2'],
            description='Description')
        ts_mock.tests.create.assert_called_once_with('tc1')
        tc_mock.doc.create.assert_called_once_with('Description')
        tc_mock.tags.create.assert_has_calls([mock.call('tag1'),
                                              mock.call('tag2')])
        tc_mock.keywords.create.assert_has_calls(
            [mock.call(graph_seq[1]['currentElementName']),
             mock.call(graph_seq[2]['currentElementName']),
             mock.call(graph_seq[3]['currentElementName'])])

    def test_create_test_case_default(self):
        ts_mock = mock.Mock(spec_set=TestSuite())
        tc_mock = mock.Mock(spec_set=TestCase())
        ts_mock.tests.create.side_effect = [tc_mock]
        self._tc_creator.test_suite = ts_mock
        graph_seq = [{"modelName": "air_handler_system"},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID":"n1", "currentElementName":"Idle",
                      "properties":[{"x": 380}, {"y": 225}]},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID": "e3",
                      "currentElementName": "TurnOff", "properties":[]},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID": "n4", "currentElementName": "OFF",
                      "properties":[{"x": 608}, {"y": 116}]}]
        self._tc_creator._create_test_case(graph_seq)
        ts_mock.tests.create.assert_called_once_with(graph_seq[0]['modelName'])
        tc_mock.doc.create.assert_not_called()
        tc_mock.tags.create.assert_not_called()
        tc_mock.keywords.create.assert_has_calls(
            [mock.call(graph_seq[1]['currentElementName']),
             mock.call(graph_seq[2]['currentElementName']),
             mock.call(graph_seq[3]['currentElementName'])])

    @mock.patch('graph_robot_mbt.robot_test_creator.RobotTestCreator'
                '._create_test_case')
    @mock.patch('graph_robot_mbt.robot_test_creator.RobotTestCreator'
                '._import_test_libs')
    def test_create_test_from_seq(self, import_libs_mock, create_tc_mock):
        graph_seq = [{"modelName": "air_handler_system"},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID":"n1", "currentElementName":"Idle",
                      "properties":[{"x": 380}, {"y": 225}]},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID": "e3",
                      "currentElementName": "TurnOff", "properties":[]},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID": "n4", "currentElementName": "OFF",
                      "properties":[{"x": 608}, {"y": 116}]}]
        libs = ['Lib1', 'Lib2']
        self._tc_creator.create_test_from_seq(graph_seq, libs,
                                              suite_name='ts1',
                                              test_name='tc1',
                                              tags=['tag1', 'tag2'],
                                              description='TC Description')
        self.assertEqual('ts1', self._tc_creator.test_suite.name)
        import_libs_mock.assert_called_once_with(libs)
        create_tc_mock.assert_called_once_with(graph_seq,
                                               test_name='tc1',
                                               tags=['tag1', 'tag2'],
                                               description='TC Description')

    @mock.patch('graph_robot_mbt.robot_test_creator.RobotTestCreator'
                '._create_test_case')
    @mock.patch('graph_robot_mbt.robot_test_creator.RobotTestCreator'
                '._import_test_libs')
    def test_create_test_from_seq_default(self, import_libs_mock,
                                          create_tc_mock):
        graph_seq = [{"modelName": "air_handler_system"},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID":"n1", "currentElementName":"Idle",
                      "properties":[{"x": 380}, {"y": 225}]},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID": "e3",
                      "currentElementName": "TurnOff", "properties":[]},
                     {"modelName": "air_handler_system", "data": [],
                      "currentElementID": "n4", "currentElementName": "OFF",
                      "properties":[{"x": 608}, {"y": 116}]}]
        libs = ['Lib1', 'Lib2']
        self._tc_creator.create_test_from_seq(graph_seq, libs)
        self.assertEqual(graph_seq[0]['modelName'],
                         self._tc_creator.test_suite.name)
        import_libs_mock.assert_called_once_with(libs)
        create_tc_mock.assert_called_once_with(graph_seq)
