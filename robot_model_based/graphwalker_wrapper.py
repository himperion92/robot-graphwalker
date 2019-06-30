import logging
import os
import json
import subprocess


class IncorrectModelError(Exception):
    "Exception raised when a graph model has an incorrect format."


class GraphwalkerWrapper(object):
    def __init__(self, graphwalker_location):
        """
        Initializes python graphwalker wrapper.

        Args:
            graphwalker_location (str): path to the location of graphwalker
            .jar file.

        Returns:
            None.
        """

        self._logger = logging.getLogger(__name__)
        self._cmd = r'java -jar {gw} "$@"'.format(gw=graphwalker_location)
        self.sequence = []

    def check_model_format(self, model):
        """
        Checks that graphml model has a correct format

        Args:
            model (str): path to the .graphml model file.

        Returns:
            None.

        Raises:
            IncorrectModelError: whenever the format of the graph model is
                incorrect.
        """

        self._logger.info(
            r'Checking "{model}" model format...'.format(model=model))
        check_cmd = (
            r'{cmd} check -m {model} "random(edge_coverage(100))"'
            ).format(cmd=self._cmd, model=model)
        response = subprocess.check_output(check_cmd, shell=True)

        if 'No issues found with the model' not in response:
            raise IncorrectModelError(r'Model format is incorrect!')

    def generate_path(self, model, generator, stop_condition, condition):
        """
        Generates a execution path sequence following the selected strategy for
        the given model.

        Args:
            model (str): path to the .graphml model file.
            generator (str): possible values: random, weighted random,
                quick_random, a_star.
            stop_condition (str): possible values: edge_coverage,
                vertex_coverage, requirement_coverage,
                dependency_edge_coverage, reached_vertex, reached_edge,
                time_duration, lenght, never.
            condition: (str): possible values depend on stop_condition.
                Normally, a number representing a given percentage or threshold
                is required.

        Returns:
            Generated sequence.
        """

        self._logger.info(
            (
                r'Generating execution path for "{model}" model...'
            ).format(model=model))
        offline_cmd = (
            r'{cmd} offline -o -m {model_path} "random(edge_coverage(100))"'
            ).format(cmd=self._cmd, model_path=model)
        response = subprocess.check_output(offline_cmd, shell=True)
        self.sequence = self._parse_sequence(response)
        self._logger.info('Execution path successfully generated!')
        return self.sequence

    def _parse_sequence(self, response):
        """
        Parses the output of graphwalker 'offline' command and translates it
        into a dictionary.

        Args:
            response (str): output of graphwalker offline command.

        Returns:
            (list): sequence with complete information about nodes and edges.
        """

        sequence = []
        self._logger.info('Parsing generated sequence...')
        response = response.split(os.linesep)

        if response[-1] == "":
            del response[-1]

        for step in response:
            self._logger.debug(r'Step: "{step}"'.format(step=step))
            print step
            sequence.append(json.loads(step))

        self._logger.info('Sequence successfully parsed!')
        return sequence
