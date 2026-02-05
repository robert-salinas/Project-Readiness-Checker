import typer
import yaml
import json
from pathlib import Path
from typing import Optional
from src.models import ProjectConfig
from src.checkers.engine import CheckerEngine
from src.formatters.cli import CLIFormatter
from src.formatters.json_formatter import JSONFormatter
from src.formatters.html_formatter import HTMLFormatter
from rich.console import Console

app = typer.Typer(help="Project Readiness Checker (PRC) - Verifica si tu proyecto está listo.")
console = Console()

@app.command()
def check(
    config_path: Path = typer.Argument(..., help="Ruta al archivo de configuración (YAML o JSON)"),
    format: str = typer.Option("cli", "--format", "-f", help="Formato de salida: cli, json, html"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Ruta para guardar el reporte")
):
    """
    Ejecuta las validaciones definidas en el archivo de configuración.
    """
    if not config_path.exists():
        console.print(f"[red]Error:[/] El archivo {config_path} no existe.")
        raise typer.Exit(code=1)

    try:
        # Cargar configuración
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.suffix in ['.yaml', '.yml']:
                config_data = yaml.safe_load(f)
            else:
                config_data = json.load(f)
        
        config = ProjectConfig(**config_data)
        
        # Ejecutar engine
        engine = CheckerEngine(config)
        report = engine.run_checks()
        
        # Formatear salida
        if format == "cli":
            formatter = CLIFormatter()
            result = formatter.format(report)
            console.print(result)
        elif format == "json":
            formatter = JSONFormatter()
            result = formatter.format(report)
            if not output:
                print(result)
        elif format == "html":
            formatter = HTMLFormatter()
            result = formatter.format(report)
            if not output:
                console.print("[yellow]Advertencia:[/] El formato HTML requiere un archivo de salida (--output).")
        else:
            console.print(f"[red]Error:[/] Formato desconocido: {format}")
            raise typer.Exit(code=1)

        # Guardar en archivo si se especifica
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result)
            console.print(f"[green]Reporte guardado en:[/] {output}")

        # Exit code basado en errores
        if report.summary["errors"] > 0:
            raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def version():
    """Muestra la versión de PRC."""
    console.print("Project Readiness Checker (PRC) v0.1.0")

if __name__ == "__main__":
    app()
