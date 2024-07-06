import random
import time

from config import EVENT_INTERVAL
from logging.logger import Logger
from models.consumer import Consumer
from models.event import Event
from models.node import Node


class Simulator(object):
    """
    A class that creates a simulation environment.
    :author: Yepeng Ding
    """

    def __init__(self, node_number: int, event_number: int):
        self._node_number = node_number
        self._event_number = event_number

        # Instantiate nodes
        self._nodes = [Node(i) for i in range(self._node_number)]
        # Connect each node to the other nodes
        for n in self._nodes:
            n.connect(list(filter(lambda _n: _n.id != n.id, self._nodes)))

        # Instantiate an event consumer
        self._consumer = Consumer(list(map(lambda _n: _n.id, self._nodes)))

        # Connect the consumer to all nodes
        for n in self._nodes:
            n.connect_consumer(self._consumer)

        self._logger = Logger('Simulator')

    def run(self):
        """
        Start the simulation by starting all nodes.
        :return:
        """
        for n in self._nodes:
            n.start()

        self._generate_events()

    def _generate_events(self):
        """
        Generate events and randomly send to nodes.
        :return:
        """
        for i in range(self._event_number):
            random.shuffle(self._nodes)
            for n in self._nodes:
                n.receive(Event(i, f'event_{i}'))
            time.sleep(EVENT_INTERVAL)

            self._logger.info([n.id for n in self._nodes])
            for n in self._nodes:
                self._logger.info(n.peer_scores)

    def stop(self):
        """
        Stop the simulation by terminating all nodes.
        :return:
        """
        for n in self._nodes:
            n.terminate()
            n.join()
