import os
import subprocess
import re
from src.models import Rule, RuleType, CheckResult, ProjectConfig, ProjectReport, Severity

class CheckerEngine:
    """Motor encargado de ejecutar las validaciones configuradas."""
    def __init__(self, config: ProjectConfig):
        """Inicializa el motor con una configuración de proyecto."""
        self.config = config

    def run_checks(self) -> ProjectReport:
        """Ejecuta todas las reglas y genera un reporte consolidado."""
        results = []
        summary = {"passed": 0, "failed": 0, "warnings": 0, "errors": 0}

        for rule in self.config.rules:
            result = self._evaluate_rule(rule)
            results.append(result)
            
            if result.passed:
                summary["passed"] += 1
            else:
                summary["failed"] += 1
                if rule.severity == Severity.ERROR:
                    summary["errors"] += 1
                elif rule.severity == Severity.WARNING:
                    summary["warnings"] += 1

        return ProjectReport(
            project_name=self.config.project_name,
            project_type=self.config.project_type,
            results=results,
            summary=summary
        )

    def _evaluate_rule(self, rule: Rule) -> CheckResult:
        """Evalúa una regla individual según su tipo."""
        if rule.type == RuleType.FILE_EXISTS:
            passed = os.path.isfile(rule.target)
            return CheckResult(
                rule=rule,
                passed=passed,
                message=f"Archivo '{rule.target}' {'encontrado' if passed else 'no encontrado'}"
            )

        elif rule.type == RuleType.DIR_EXISTS:
            passed = os.path.isdir(rule.target)
            return CheckResult(
                rule=rule,
                passed=passed,
                message=f"Directorio '{rule.target}' {'encontrado' if passed else 'no encontrado'}"
            )

        elif rule.type == RuleType.FILE_CONTAINS:
            if not os.path.isfile(rule.target):
                return CheckResult(rule=rule, passed=False, message=f"Archivo '{rule.target}' no existe para validar contenido")
            
            try:
                with open(rule.target, 'r', encoding='utf-8') as f:
                    content = f.read()
                    passed = bool(re.search(rule.pattern, content)) if rule.pattern else True
                    return CheckResult(
                        rule=rule,
                        passed=passed,
                        message=f"Patrón '{rule.pattern}' {'encontrado' if passed else 'no encontrado'} en {rule.target}"
                    )
            except Exception as e:
                return CheckResult(rule=rule, passed=False, message=f"Error leyendo archivo {rule.target}: {str(e)}")

        elif rule.type == RuleType.COMMAND_SUCCESS:
            try:
                # Use shell=True for convenience in CLI tools, but be careful with untrusted input
                # Here we assume the rule target is a trusted command from the config file
                result = subprocess.run(rule.target, shell=True, capture_output=True, text=True)
                passed = result.returncode == 0
                return CheckResult(
                    rule=rule,
                    passed=passed,
                    message=f"Comando '{rule.target}' ejecutado con éxito" if passed else f"Comando '{rule.target}' falló con código {result.returncode}",
                    details=result.stderr if not passed else result.stdout
                )
            except Exception as e:
                return CheckResult(rule=rule, passed=False, message=f"Error ejecutando comando: {str(e)}")

        elif rule.type == RuleType.ENV_VAR_SET:
            passed = rule.target in os.environ
            return CheckResult(
                rule=rule,
                passed=passed,
                message=f"Variable de entorno '{rule.target}' {'está definida' if passed else 'no está definida'}"
            )

        return CheckResult(rule=rule, passed=False, message=f"Tipo de regla desconocido: {rule.type}")
