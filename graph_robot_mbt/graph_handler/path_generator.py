import logging
import subprocess


class PathGenerator(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def check_model_format(self, model):
        """
        Checks that graphml model has a correct format

        Args:
            model(str): path to the .graphml model file

        Returns:
            True if format is correct, False otherwise
        """

        check_cmd = (
            r'gw check -m {model_path} "random(edge_coverage(100))"'
            ).format(model_path=model)
        response = subprocess.check_output(check_cmd)

        return True if 'No issues found with the model' in response else False
