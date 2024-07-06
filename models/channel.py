from queue import Queue
from typing import Generic, TypeVar

from models.event import NodeEvent, Event

T = TypeVar("T", Event, NodeEvent)


class EventChannel(Generic[T]):
    """
    A class that implements the channel for a node to receive events.
    """

    def __init__(self):
        self.__queue = Queue(0)

    def add(self, event: T):
        self.__queue.put(event)

    def get(self) -> T:
        if not self.__queue.empty():
            return self.__queue.get()

    def not_empty(self) -> bool:
        return not self.__queue.empty()


class NodeChannel(object):
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
