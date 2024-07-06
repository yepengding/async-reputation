import config
from core.constants import LogLevel


class Logger(object):
    """
    A class that implements logging.
    :author: Yepeng Ding
    """

    def __init__(self, name):
        self.__name = name
        self.__level = config.LOG_LEVEL

    def debug(self, message: str):
        if self.__level >= LogLevel.DEBUG:
            print(f'{ConsoleColor.OKCYAN}DEBUG - {self.__name}: {message}{ConsoleColor.ENDC}')

    def info(self, message: object):
        if self.__level >= LogLevel.INFO:
            print(f'{ConsoleColor.OKBLUE}INFO - {self.__name}: {str(message)}{ConsoleColor.ENDC}')


class ConsoleColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
