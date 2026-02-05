from jinja2 import Template
from src.models import ProjectReport
from src.formatters.base import Formatter

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Preparación - {{ report.project_name }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px; background-color: #f4f7f6; }
        h1, h2 { color: #2c3e50; }
        .summary { display: flex; gap: 20px; margin-bottom: 30px; }
        .summary-card { flex: 1; padding: 15px; border-radius: 8px; text-align: center; color: white; font-weight: bold; }
        .passed { background-color: #27ae60; }
        .failed { background-color: #e74c3c; }
        .warnings { background-color: #f39c12; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #34495e; color: white; }
        tr:hover { background-color: #f1f1f1; }
        .status-badge { padding: 4px 8px; border-radius: 4px; font-size: 0.85em; font-weight: bold; }
        .status-passed { background-color: #d4edda; color: #155724; }
        .status-failed { background-color: #f8d7da; color: #721c24; }
        .status-warning { background-color: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <h1>Reporte de Preparación del Proyecto</h1>
    <p><strong>Proyecto:</strong> {{ report.project_name }} | <strong>Tipo:</strong> {{ report.project_type }}</p>

    <div class="summary">
        <div class="summary-card passed">Pasados: {{ report.summary.passed }}</div>
        <div class="summary-card failed">Errores: {{ report.summary.errors }}</div>
        <div class="summary-card warnings">Advertencias: {{ report.summary.warnings }}</div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Estado</th>
                <th>Regla</th>
                <th>Mensaje</th>
                <th>Severidad</th>
            </tr>
        </thead>
        <tbody>
            {% for res in report.results %}
            <tr>
                <td>
                    {% if res.passed %}
                        <span class="status-badge status-passed">PASSED</span>
                    {% elif res.rule.severity == 'warning' %}
                        <span class="status-badge status-warning">WARNING</span>
                    {% else %}
                        <span class="status-badge status-failed">FAILED</span>
                    {% endif %}
                </td>
                <td>{{ res.rule.name }}</td>
                <td>{{ res.message }}</td>
                <td>{{ res.rule.severity }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

class HTMLFormatter(Formatter):
    def format(self, report: ProjectReport) -> str:
        template = Template(HTML_TEMPLATE)
        return template.render(report=report)
