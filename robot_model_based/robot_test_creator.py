import logging

from robot.running import TestSuite


class RobotTestCreator(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.test_suite = None

    def create_test_from_seq(self, graph_seq, libs, **kwargs):
        """
        Creates a single Robot Framework test suite containing a test case for
        a given graphwalker sequence.

        Args:
            graph_seq (list): generated graphwalker sequence.
            libs (list): list with the paths to the libraries to be imported.
            suite_name (str, optional): name of the Robot Framework test suite.
            test_name  (str, optional): name of the Robot Framework test case.
            tags (list, optional): list of tags to include in the test case.
            description (str, optional): description of the test case.

        Returns:
            (robot.running.model.TestSuite): created test suite object.
        """

        suite_name = kwargs.pop('suite_name', graph_seq[0]['modelName'])
        self._logger.info(
            'Creating test suite "{suite_name}"...'.format(
                suite_name=suite_name))
        self.test_suite = TestSuite(suite_name)
        self._import_test_libs(libs)
        self._create_test_case(graph_seq, **kwargs)
        self._logger.info('Test suite successfully created.')
        return self.test_suite

    def _import_test_libs(self, libs):

        """
        Imports the given test libraries to the target test suite.

        Args:
            libs (list): list with the paths to the libraries to be imported.

        Returns:
            None.
        """

        for lib in libs:
            self._logger.debug(
                'Importing test library "{lib}"...'.format(lib=lib))
            self.test_suite.resource.imports.library(lib)

    def _create_test_case(self, graph_seq, **kwargs):
        """
        Creates a test case within the given test suite for a target
        graphwalker sequence.

        Args:
            graph_seq (list): generated graphwalker sequence.
            test_name (str, optional): name of the test case to be created.
            tags (list, optional): list of tags to include in the test case.
            description (str, optional): description of the test case.

        Returns:
            None.
        """

        test_name = kwargs.get('test_name', graph_seq[0]['modelName'])
        tags = kwargs.get('tags', [])
        description = kwargs.get('description', None)
        self._logger.info(
            'Creating test case "{test_name}"...'.format(test_name=test_name))
        test_case = self.test_suite.tests.create(test_name)

        if description:
            self._logger.debug(
                'Adding the following description: "{description}"'.format(
                    description=description))
            test_case.doc.create(description)

        for tag in tags:
            self._logger.debug('Adding tag "{tag}"'.format(tag=tag))
            test_case.tags.create(tag)

        itersteps = iter(graph_seq)
        next(itersteps)
        for step in itersteps:
            keyword = step['currentElementName']
            self._logger.debug(
                'Adding the following keyword: "{keyword}"'.format(
                    keyword=keyword))
            test_case.keywords.create(keyword)
            # TODO handle actions and checks

        self._logger.info('Test case successfully created.')
