from abc import ABC, abstractmethod
from src.models import ProjectReport

class Formatter(ABC):
    @abstractmethod
    def format(self, report: ProjectReport) -> str:
        pass
