from enum import Enum, auto
from typing import Final

INIT_SCORE: Final[int] = 0
POSITIVE_FEEDBACK_SCORE: Final[int] = 1


class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
