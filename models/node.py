from __future__ import annotations

import threading
import time

from config import TRANSMISSION_DELAY
from core.constants import PeerScore
from logging.logger import Logger
from models.channel import NodeChannel, EventChannel
from models.consumer import Consumer
from models.event import Event, NodeEvent


class Node(threading.Thread):
    """
    A class that represents a node in the network.
    :author: Yepeng Ding
    """

    def __init__(self, identifier: int):
        self._id: int = identifier
        self._connected_nodes: [Node] = []
        self._connected_consumers: [Consumer] = []
        self._node_channel: NodeChannel = NodeChannel()
        self._event_channel: EventChannel = EventChannel[Event]()
        self._peer_scores: dict[int, int] = {}
        self._terminate: bool = False
        self._logger: Logger = Logger(f'Node {self._id}')
        super(Node, self).__init__()

    def run(self) -> None:
        while not self._terminate:
            if self._event_channel.not_empty():
                event_received = self._event_channel.get()
                # Notify consumers
                self._notify(event_received)

                # Broadcast
                self._broadcast(event_received)

                # Reevaluate scores of other nodes
                for n in self._connected_nodes:
                    self._peer_scores[n.id] = PeerScore.DEFAULT.value
                # Get events from other nodes
                node_events = self._node_channel.get_node_events_by_event_id(event_received.id)
                for e in node_events:
                    self._peer_scores[e.node_id] = PeerScore.POSITIVE.value \
                        if e.message == event_received.message else PeerScore.NEGATIVE.value

                # Consume processed events
                self._node_channel.remove_node_events_by_event_id(event_received.id)

    def connect(self, nodes: [Node]) -> None:
        """
        Connects to the other nodes.
        :param nodes:
        :return:
        """
        self._connected_nodes = nodes
        for n in self._connected_nodes:
            self._peer_scores[n.id] = PeerScore.DEFAULT.value

    def connect_consumer(self, consumer: Consumer) -> None:
        """
        Connects to the given consumer.
        :param consumer:
        :return:
        """
        self._connected_consumers.append(consumer)

    def receive(self, event: Event) -> None:
        """
        Receive an event
        :param event:
        :return:
        """
        time.sleep(TRANSMISSION_DELAY)
        self._event_channel.add(event)
        self._logger.debug(f"Event ({event}) received")

    def receive_from(self, node_id: int, event: Event) -> None:
        """
        Receive an event from another node.
        :param node_id:
        :param event:
        :return:
        """
        time.sleep(TRANSMISSION_DELAY)
        self._node_channel.add(node_id, event)
        self._logger.debug(f"Event ({event}) received from node {node_id}")

    def terminate(self) -> None:
        self._terminate = True
        self._logger.debug(f"{self._id} is terminating")

    def __push(self, event: Event) -> None:
        """
        Push an event to all connected consumers.
        :param event:
        :return:
        """

    def _notify(self, event: Event) -> None:
        for c in self._connected_consumers:
            c.receive(NodeEvent(event.id, event.message, self._id))

    def _broadcast(self, event: Event) -> None:
        """
        Broadcast an event to all connected nodes.
        :param event:
        :return:
        """
        for n in self._connected_nodes:
            n.receive_from(self._id, event)
        self._logger.debug(f"Broadcast ({event})")

    @property
    def peer_scores(self) -> dict[int, int]:
        return self._peer_scores

    @property
    def id(self):
        return self._id
