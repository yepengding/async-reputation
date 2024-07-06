from __future__ import annotations

import threading
import time
from queue import Queue

from config import TRANSMISSION_DELAY
from core.constants import PeerScore
from logging.logger import Logger
from models.event import Event, NodeEvent


class Node(threading.Thread):
    """
    A class that represents a node in the network.
    :author: Yepeng Ding
    """

    def __init__(self, identifier: int):
        self.__id: int = identifier
        self.__connected_nodes: [Node] = []
        self.__node_channel: NodeChannel = NodeChannel()
        self.__event_channel: EventChannel = EventChannel()
        self.__peer_scores: dict[int, int] = {}

        self.__logger: Logger = Logger(f'Node {self.__id}')
        super(Node, self).__init__()

    def run(self) -> None:
        while True:
            if self.__event_channel.not_empty():
                event_received = self.__event_channel.get()
                # Broadcast
                self.__broadcast(event_received)

                # Reevaluate scores of other nodes
                for n in self.__connected_nodes:
                    self.__peer_scores[n.__id] = PeerScore.INITIAL.value
                # Get events from other nodes
                node_events = self.__node_channel.get_node_events_by_event_id(event_received.id)
                for e in node_events:
                    self.__peer_scores[e.node_id] = PeerScore.POSITIVE.value \
                        if e.message == event_received.message else PeerScore.NEGATIVE.value

                # Consume processed events
                self.__node_channel.remove_node_events_by_event_id(event_received.id)

    def connect(self, nodes: [Node]) -> None:
        """
        Connects to the connected nodes.
        :param nodes:
        :return:
        """
        self.__connected_nodes = nodes
        for n in self.__connected_nodes:
            self.__peer_scores[n.__id] = PeerScore.INITIAL.value

    def receive(self, event: Event) -> None:
        """
        Receive an event
        :param event:
        :return:
        """
        time.sleep(TRANSMISSION_DELAY)
        self.__event_channel.add(event)
        self.__logger.debug(f"Event ({event}) received")

    def receive_from(self, node_id: int, event: Event) -> None:
        """
        Receive an event from another node.
        :param node_id:
        :param event:
        :return:
        """
        time.sleep(TRANSMISSION_DELAY)
        self.__node_channel.add(node_id, event)
        self.__logger.debug(f"Event ({event}) received from node {node_id}")

    def __broadcast(self, event: Event) -> None:
        """
        Broadcast an event to all connected nodes.
        :param event:
        :return:
        """
        for n in self.__connected_nodes:
            n.receive_from(self.__id, event)
        self.__logger.debug(f"Broadcast ({event}) ")

    @property
    def peer_scores(self) -> dict[int, int]:
        return self.__peer_scores

    @property
    def id(self):
        return self.__id


class EventChannel:
    """
    A class that implements the channel for a node to receive events.
    """

    def __init__(self):
        self.__queue = Queue(0)

    def add(self, event: Event):
        self.__queue.put(event)

    def get(self) -> Event | None:
        if not self.__queue.empty():
            return self.__queue.get()
        else:
            return None

    def not_empty(self) -> bool:
        return not self.__queue.empty()


class NodeChannel:
    """
    A class that implements the channel for a node to receive messages from its connected nodes.
    """

    def __init__(self):
        self.__queue = Queue(0)
        self.__buffer: [NodeEvent] = []

    def add(self, node_id: int, event: Event):
        self.__queue.put(NodeEvent(event.id, event.message, node_id))

    def remove_node_events_by_event_id(self, event_id: int):
        self.__buffer = list(filter(lambda e: e.id != event_id, self.__buffer))

    def get_node_events_by_event_id(self, event_id: int) -> [NodeEvent]:
        self.__load_to_buffer()
        return list(filter(lambda e: e.id == event_id, self.__buffer))

    def __load_to_buffer(self):
        while not self.__queue.empty():
            self.__buffer.append(self.__queue.get())
