from __future__ import annotations

import threading
import time

from config import TRANSMISSION_DELAY
from core.constants import PerfScore
from logging.logger import Logger
from models.channel import EventChannel
from models.event import NodeEvent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.node import Node


class Consumer(threading.Thread):
    """
    A class that implements an event consumer.
    :author: Yepeng Ding
    """

    def __init__(self, identifier: int):
        self._id: int = identifier
        self._connected_nodes: [Node] = []
        self._event_channel: EventChannel = EventChannel[NodeEvent]()
        self._perf_scores = {}
        self._terminate: bool = False
        self._logger = Logger('Consumer')
        super(Consumer, self).__init__()

    def connect(self, nodes: [Node]) -> None:
        """
        Connects to nodes.
        :param nodes:
        :return:
        """
        self._connected_nodes = nodes
        # Initialize performance scores
        for n in self._connected_nodes:
            n.connect_consumer(self)
            self._perf_scores[n.id] = PerfScore.DEFAULT.value

    def run(self) -> None:
        while not self._terminate:
            pass

    def receive(self, event: NodeEvent) -> None:
        """
        Receive an event
        :param event: node event
        :return:
        """
        time.sleep(TRANSMISSION_DELAY)
        self._event_channel.add(event)
        self._logger.info(f"Event ({event}) received")

    def terminate(self) -> None:
        self._terminate = True
        self._logger.debug(f"{self._id} is terminating")
