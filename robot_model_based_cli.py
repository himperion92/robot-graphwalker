import logging
import argparse

from robot_model_based.graphwalker_wrapper import GraphwalkerWrapper
from robot_model_based.robot_test_creator import RobotTestCreator
from robot_test_executor import RobotTestExecutor


def main():
    parser = argparse.ArgumentParser(
        description='Graphwalker - Robot Framework model based test generator')
    parser.add_argument('--graphwalker', '-w', help='Path to the graphwalker'
                        '.jar file', required=True)
    parser.add_argument('--graph', '-g', help='Path to the graph file',
                        required=True)
    parser.add_argument('--generator', '-e',
                        help='Assign a path generator strategy (https://graphw'
                        'alker.github.io/generators_and_stop_conditions). '
                        'Possible values: random, weighted random, '
                        'quick_random, a_star.', required=True)
    parser.add_argument('--stopcondition', '-s',
                        help='Assign a path generator strategy (https://graphw'
                        'alker.github.io/generators_and_stop_conditions). '
                        'Possible values: edge_coverage, vertex_coverage, '
                        'requirement_coverage, dependency_edge_coverage, '
                        'reached_vertex, reached_edge, time_duration, lenght, '
                        'never.', required=True)
    parser.add_argument('--condition', '-c',
                        help='Assign a path generator strategy (https://graphw'
                        'alker.github.io/generators_and_stop_conditions). '
                        'Possible values depend on stop_condition. Normally, a'
                        ' number representing a given percentage or threshold '
                        'is required.', required=True)
    parser.add_argument('--testsuite', '-t', help='Test Suite name',
                        required=True)
    parser.add_argument('--testcase', '-n', help='Test Case name',
                        required=True)
    parser.add_argument('--libraries', '-l', nargs='+',
                        help='libraries to be imported', required=True)
    parser.add_argument('--report', '-r', help='Path where the report files'
                        'will be stored', required=True)

    args = parser.parse_args()
    graphwalker_wrapper = GraphwalkerWrapper(args.graphwalker)
    robot_tc_creator = RobotTestCreator()
    robot_tc_executor = RobotTestExecutor()
    print -1
    graphwalker_wrapper.check_model_format(args.graph)
    print 0
    graph_sequence = graphwalker_wrapper.generate_path(args.graph,
                                                       args.generator,
                                                       args.stopcondition,
                                                       args.condition)
    print 1
    test_suite = robot_tc_creator.create_test_from_seq(
        graph_sequence, args.libraries, suite_name=args.testsuite,
        test_name=args.testcase)
    print 2
    robot_tc_executor.execute_test_suite(test_suite, args.report)
    print 3

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()

