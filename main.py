from config import NODE_NUMBER, EVENT_NUMBER
from logging.logger import Logger
from simulator.simulator import Simulator

if __name__ == '__main__':
    logger = Logger("main")

    simulator = Simulator(NODE_NUMBER, EVENT_NUMBER)

    simulator.run()

    simulator.stop()
