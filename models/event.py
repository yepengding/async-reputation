class Event(object):
    """
    A class that represents an event.
    :author: Yepeng Ding
    """

    def __init__(self, identifier: int, message: str):
        self._identifier = identifier
        self._message = message

    def __str__(self):
        return f'{self._identifier} | {self._message}'

    @property
    def id(self):
        return self._identifier

    @property
    def message(self):
        return self._message


class NodeEvent(Event):
    """
    A class that represents an event emitted from a node in the network.
    :author: Yepeng Ding
    """

    def __init__(self, identifier: int, message: str, node_id: int):
        self._node_id = node_id
        super().__init__(identifier, message)

    @property
    def node_id(self):
        return self._node_id
