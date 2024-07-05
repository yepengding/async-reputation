import random
import time

from config import NODE_NUMBER, EVENT_NUMBER, EVENT_INTERVAL
from logging.logger import Logger
from models.event import Event
from models.node import Node

if __name__ == '__main__':
    logger = Logger("main")

    # Instantiate nodes
    nodes = [Node(i) for i in range(NODE_NUMBER)]
    # Connect each node to the other nodes
    for n in nodes:
        n.connect(list(filter(lambda _n: _n.id != n.id, nodes)))
    # Start all nodes
    for n in nodes:
        n.start()

    # Randomly send events
    for i in range(EVENT_NUMBER):
        random.shuffle(nodes)
        for n in nodes:
            n.receive(Event(i, f'event_{i}'))
        time.sleep(EVENT_INTERVAL)

        logger.info([n.id for n in nodes])
        for n in nodes:
            logger.info(n.get_score_metrics)

    for n in nodes:
        n.join()
