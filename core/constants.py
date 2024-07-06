from enum import IntEnum


class PeerScore(IntEnum):
    INITIAL = 0,
    POSITIVE = 1,
    NEGATIVE = -1,


class LogLevel(IntEnum):
    INFO = 1
    DEBUG = 2
