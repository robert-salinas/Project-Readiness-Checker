from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class RuleType(str, Enum):
    FILE_EXISTS = "file_exists"
    DIR_EXISTS = "dir_exists"
    FILE_CONTAINS = "file_contains"
    COMMAND_SUCCESS = "command_success"
    ENV_VAR_SET = "env_var_set"

class Rule(BaseModel):
    name: str
    description: str
    type: RuleType
    target: str
    pattern: Optional[str] = None
    severity: Severity = Severity.ERROR
    remediation: Optional[str] = None

class ProjectConfig(BaseModel):
    project_name: str
    project_type: str
    rules: List[Rule]

class CheckResult(BaseModel):
    rule: Rule
    passed: bool
    message: str
    details: Optional[str] = None

class ProjectReport(BaseModel):
    project_name: str
    project_type: str
    results: List[CheckResult]
    summary: Dict[str, int] = Field(default_factory=lambda: {"passed": 0, "failed": 0, "warnings": 0, "errors": 0})
