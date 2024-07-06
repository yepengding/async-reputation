
from core.constants import PerfScore


class Consumer(object):
    """
    A class that implements an event consumer.
    """

    def __init__(self, node_ids: [int]):
        self.__perf_scores = {}
        # Initialize performance scores
        for i in node_ids:
            self.__perf_scores[i] = PerfScore.DEFAULT.value


