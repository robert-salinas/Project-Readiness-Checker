from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from src.models import ProjectReport, Severity
from src.formatters.base import Formatter
import io

class CLIFormatter(Formatter):
    def format(self, report: ProjectReport) -> str:
        console = Console(file=io.StringIO(), force_terminal=True, width=100)
        
        console.print(Panel(f"[bold blue]Reporte de Preparación: {report.project_name}[/]\n[italic]Tipo: {report.project_type}[/]", expand=False))
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Estado", width=12)
        table.add_column("Regla")
        table.add_column("Mensaje")
        table.add_column("Severidad")

        for res in report.results:
            status = "[green]PASSED[/]" if res.passed else "[red]FAILED[/]"
            if not res.passed and res.rule.severity == Severity.WARNING:
                status = "[yellow]WARNING[/]"
            
            severity_style = "white"
            if res.rule.severity == Severity.ERROR: severity_style = "bold red"
            elif res.rule.severity == Severity.WARNING: severity_style = "yellow"
            
            table.add_row(
                status,
                res.rule.name,
                res.message,
                f"[{severity_style}]{res.rule.severity.value}[/]"
            )

        console.print(table)
        
        summary = report.summary
        console.print(f"\n[bold]Resumen:[/] [green]{summary['passed']} Pasados[/], [red]{summary['errors']} Errores[/], [yellow]{summary['warnings']} Advertencias[/]")
        
        return console.file.getvalue()
