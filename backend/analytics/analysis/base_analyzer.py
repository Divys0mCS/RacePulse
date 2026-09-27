from abc import ABC, abstractmethod
from app.models.lap import Lap


class BaseAnalyzer(ABC):
    """Common interface for every analytics engine that operates on a list of Laps."""

    @abstractmethod
    def analyze(self, laps: list[Lap]) -> dict:
        """Compute this analyzer's metrics over the given laps and return them as a dict."""
        raise NotImplementedError