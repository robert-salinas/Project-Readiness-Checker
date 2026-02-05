import json
from src.models import ProjectReport
from src.formatters.base import Formatter

class JSONFormatter(Formatter):
    def format(self, report: ProjectReport) -> str:
        return report.model_dump_json(indent=4)
