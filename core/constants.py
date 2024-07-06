from enum import IntEnum, Enum


class PerfScore(Enum):
    DEFAULT: float = 0.5


class PeerScore(Enum):
    DEFAULT: float = 0.5,
    POSITIVE: float = 1.0,
    NEGATIVE: float = 0.0,


class LogLevel(IntEnum):
    INFO = 1
    DEBUG = 2
