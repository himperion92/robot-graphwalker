import logging
import subprocess


class PathGenerator(object):
    def __init__(self):
        self._logging = logging.getLogger(__name__)

    def check_model_format(self, model):
        """
        Checks that graphml model has a correct format
        
        Args:
            model(str): path to the .graphml model file 

        Returns:
            True if format is correct, False otherwise
        """

        check_cmd = r'gw check -m {model_path} "random(edge_coverage(100))"'.format(model_path=correct_model))
        response=subprocess.call(check_cmd)

    