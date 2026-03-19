import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from datetime import datetime
from src.gui.settings_manager import load_settings, save_settings, AUDIT_PROFILES
from src.gui.audit_logic import audit_directory, clean_junk

# RS Identity Constants
RS_AUTHOR = "Robert Salinas"
RS_VERSION = "v1.0.0"
RS_ENGINE = "Standard Analysis Engine"

# RS Design System Constants - Final Optimized Edition
COLOR_BG = "#1A1F2E"       # rs-dark-secondary
COLOR_CARD = "#2D3142"     # rs-dark-primary
COLOR_SIDEBAR = "#0F1419"  # rs-dark-tertiary
COLOR_ACCENT = "#FF7A3D"   # rs-orange
COLOR_ACCENT_HOVER = "#E86A2A" # rs-orange-dark
COLOR_TEXT = "#FFFFFF"     # rs-text-white
COLOR_TEXT_MUTED = "#9CA3AF" # rs-text-muted

COLOR_SUCCESS = "#10B981"  # rs-success
COLOR_ERROR = "#EF4444"    # rs-error
COLOR_WARNING = "#F59E0B"  # rs-warning
COLOR_INFO = "#2196F3"     # keeping blue for info

class RSProjectReadinessApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Project Readiness Checker")
        self.geometry("1000x800")
        
        # Configure Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.settings = load_settings()
        self.selected_path = ""
        self.audit_results = None # Store results for cleaning
        
        # Cargar Icono
        self._load_icon()
        
        self._create_main_panel()
        self._create_settings_panel()
        
        # Show Audit by default
        self.show_audit_panel()

    def _load_icon(self):
        # Buscar el icono en la carpeta assets
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        icon_path = os.path.join(base_path, "assets", "icon.ico")
        
        if os.path.exists(icon_path):
            try:
                # CustomTkinter a veces necesita un delay para aplicar el icono
                self.after(200, lambda: self.iconbitmap(icon_path))
            except Exception:
                pass

    def _create_main_panel(self):
        self.audit_panel = ctk.CTkFrame(self, fg_color=COLOR_BG)
        
        # Header Section
        header = ctk.CTkFrame(self.audit_panel, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(30, 10))
        
        # Title and Branding
        title_container = ctk.CTkFrame(header, fg_color="transparent")
        title_container.pack(side="left")
        
        ctk.CTkLabel(title_container, text="Project Readiness Checker", font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_ACCENT).pack(side="top", anchor="w")
        self.label_author = ctk.CTkLabel(title_container, text=f"By {RS_AUTHOR}", font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_MUTED)
        self.label_author.pack(side="top", anchor="w")

        # Top Buttons (Settings)
        self.btn_settings = ctk.CTkButton(
            header, 
            text="⚙️ Configuración", 
            width=120,
            height=32,
            fg_color=COLOR_CARD, 
            hover_color="#3D4256", 
            command=self.show_settings_panel
        )
        self.btn_settings.pack(side="right", pady=5)
        
        # Path Selector
        path_frame = ctk.CTkFrame(self.audit_panel, fg_color=COLOR_CARD, corner_radius=12)
        path_frame.pack(fill="x", padx=30, pady=10)
        
        self.path_label = ctk.CTkLabel(path_frame, text="Ninguna carpeta seleccionada", text_color=COLOR_TEXT_MUTED)
        self.path_label.pack(side="left", padx=20, pady=15)
        
        ctk.CTkButton(path_frame, text="Examinar", fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, width=100, command=self.browse_folder).pack(side="right", padx=15)

        # KPI Cards Area
        kpi_container = ctk.CTkFrame(self.audit_panel, fg_color="transparent")
        kpi_container.pack(fill="x", padx=30, pady=10)
        kpi_container.grid_columnconfigure((0,1,2,3), weight=1, uniform="equal")

        self.kpi_status = self._create_kpi_card(kpi_container, 0, "Estado", "---", COLOR_TEXT_MUTED)
        self.kpi_junk = self._create_kpi_card(kpi_container, 1, "Limpieza", "0", COLOR_TEXT_MUTED)
        self.kpi_docs = self._create_kpi_card(kpi_container, 2, "Docs", "No", COLOR_TEXT_MUTED)
        self.kpi_size = self._create_kpi_card(kpi_container, 3, "Peso Total", "0B", COLOR_TEXT_MUTED)

        # Action Buttons
        actions_frame = ctk.CTkFrame(self.audit_panel, fg_color="transparent")
        actions_frame.pack(fill="x", padx=30, pady=10)
        
        # Center the action buttons by using a sub-frame
        btns_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
        btns_container.pack(expand=True)
        
        self.btn_run = ctk.CTkButton(
            btns_container, 
            text="EJECUTAR AUDITORÍA", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLOR_ACCENT, 
            hover_color=COLOR_ACCENT_HOVER,
            corner_radius=12,
            height=40,
            width=220,
            command=self.run_audit
        )
        self.btn_run.pack(side="left", padx=10)

        self.btn_clean = ctk.CTkButton(
            btns_container, 
            text="LIMPIEZA AUTOMÁTICA", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent",
            border_color=COLOR_ACCENT,
            border_width=2,
            hover_color="#2D3142",
            corner_radius=12,
            height=40,
            width=220,
            command=self.run_auto_clean
        )
        self.btn_clean.pack(side="left", padx=10)

        # Export Button (Aligned Right per RS Standard)
        self.btn_export = ctk.CTkButton(
            actions_frame,
            text="Exportar Reporte",
            font=ctk.CTkFont(size=12),
            fg_color=COLOR_CARD,
            hover_color="#3D4256",
            corner_radius=8,
            height=32,
            width=140,
            command=self.export_report
        )
        self.btn_export.place(relx=1.0, rely=0.5, anchor="e", x=0) # Aligned right inside actions_frame

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.audit_panel, progress_color=COLOR_ACCENT, height=8)
        self.progress_bar.pack(fill="x", padx=30, pady=(10, 5))
        self.progress_bar.set(0)

        # Results Checklist Area
        self.results_frame = ctk.CTkScrollableFrame(self.audit_panel, label_text="Checklist de Auditoría", label_fg_color=COLOR_SIDEBAR, fg_color=COLOR_CARD, corner_radius=12)
        self.results_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Console Area
        self.console_frame = ctk.CTkFrame(self.audit_panel, height=120, fg_color="#0A0D14", corner_radius=12)
        self.console_frame.pack(fill="x", padx=30, pady=(10, 30))
        
        self.console = ctk.CTkTextbox(self.console_frame, fg_color="transparent", font=ctk.CTkFont(family="Consolas", size=11))
        self.console.pack(fill="both", expand=True, padx=10, pady=10)
        self.console.configure(state="disabled")

    def _create_kpi_card(self, parent, col, title, value, color):
        card = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color="#3D4256")
        card.grid(row=0, column=col, padx=5, sticky="nsew")
        
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_MUTED).pack(pady=(15, 0))
        val_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=18, weight="bold"), text_color=color)
        val_label.pack(pady=(5, 15))
        return val_label

    def _create_settings_panel(self):
        self.settings_panel = ctk.CTkFrame(self, fg_color=COLOR_BG)
        
        header = ctk.CTkFrame(self.settings_panel, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=30)
        
        ctk.CTkLabel(header, text="Configuración del Sistema", font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_ACCENT).pack(side="left")
        
        self.btn_back = ctk.CTkButton(
            header, 
            text=" ⟵ Volver a Auditoría", 
            font=ctk.CTkFont(weight="bold"),
            width=170,
            height=32,
            fg_color=COLOR_CARD, 
            hover_color="#3D4256", 
            text_color=COLOR_ACCENT,
            command=self.show_audit_panel
        )
        self.btn_back.pack(side="right")
        
        # Main Scrollable Area for Settings
        settings_scroll = ctk.CTkScrollableFrame(self.settings_panel, fg_color="transparent")
        settings_scroll.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        form_frame = ctk.CTkFrame(settings_scroll, fg_color=COLOR_CARD, corner_radius=12)
        form_frame.pack(fill="x", pady=10)
        
        inner_form = ctk.CTkFrame(form_frame, fg_color="transparent")
        inner_form.pack(padx=30, pady=30, fill="x")

        # Profile Selection
        ctk.CTkLabel(inner_form, text="Perfil de Auditoría", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.profile_dropdown = ctk.CTkOptionMenu(
            inner_form, 
            values=list(AUDIT_PROFILES.keys()),
            height=35,
            corner_radius=8,
            fg_color="#3D4256",
            button_color=COLOR_ACCENT,
            button_hover_color=COLOR_ACCENT_HOVER,
            command=self._on_profile_change
        )
        self.profile_dropdown.set(self.settings.get("audit_profile", "Estándar"))
        self.profile_dropdown.pack(fill="x", pady=(5, 20))

        # Default Export Path
        ctk.CTkLabel(inner_form, text="Ruta de Exportación Predeterminada", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        export_frame = ctk.CTkFrame(inner_form, fg_color="transparent")
        export_frame.pack(fill="x", pady=(5, 20))
        
        self.export_entry = ctk.CTkEntry(export_frame, height=35, corner_radius=8, border_color="#5C3D2E")
        self.export_entry.insert(0, self.settings.get("export_path", ""))
        self.export_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(export_frame, text="...", width=40, height=35, command=self._browse_export_path).pack(side="right")
        
        # Forbidden Files
        ctk.CTkLabel(inner_form, text="Archivos Prohibidos (separados por coma)", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.forbidden_entry = ctk.CTkEntry(inner_form, height=35, corner_radius=8, border_color="#5C3D2E")
        self.forbidden_entry.insert(0, ", ".join(self.settings.get("forbidden_files", [])))
        self.forbidden_entry.pack(fill="x", pady=(5, 20))

        # Advanced Settings
        ctk.CTkLabel(inner_form, text="Opciones Avanzadas", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.calc_hidden_switch = ctk.CTkSwitch(
            inner_form, 
            text="Calcular peso de carpetas ocultas", 
            progress_color=COLOR_ACCENT,
            font=ctk.CTkFont(size=12)
        )
        if self.settings.get("calc_hidden", False):
            self.calc_hidden_switch.select()
        self.calc_hidden_switch.pack(anchor="w", pady=(5, 20))
        
        self.btn_save = ctk.CTkButton(
            inner_form, 
            text="Guardar Cambios", 
            fg_color=COLOR_ACCENT, 
            hover_color=COLOR_ACCENT_HOVER,
            corner_radius=12,
            height=40,
            command=self.save_settings_action
        )
        self.btn_save.pack(pady=(10, 0))

        # System Status Section
        status_frame = ctk.CTkFrame(settings_scroll, fg_color=COLOR_SIDEBAR, corner_radius=12)
        status_frame.pack(fill="x", pady=20)
        
        inner_status = ctk.CTkFrame(status_frame, fg_color="transparent")
        inner_status.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(inner_status, text="Estado del Sistema", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_ACCENT).pack(anchor="w")
        
        info_grid = ctk.CTkFrame(inner_status, fg_color="transparent")
        info_grid.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(info_grid, text="Versión:", font=ctk.CTkFont(weight="bold"), text_color=COLOR_TEXT_MUTED).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(info_grid, text=RS_VERSION, text_color=COLOR_TEXT).grid(row=0, column=1, sticky="w", padx=10)
        
        ctk.CTkLabel(info_grid, text="Motor:", font=ctk.CTkFont(weight="bold"), text_color=COLOR_TEXT_MUTED).grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(info_grid, text=RS_ENGINE, text_color=COLOR_TEXT).grid(row=1, column=1, sticky="w", padx=10)
        
        ctk.CTkLabel(info_grid, text="Desarrollador:", font=ctk.CTkFont(weight="bold"), text_color=COLOR_TEXT_MUTED).grid(row=2, column=0, sticky="w")
        ctk.CTkLabel(info_grid, text=RS_AUTHOR, text_color=COLOR_TEXT).grid(row=2, column=1, sticky="w", padx=10)

    def _on_profile_change(self, profile_name):
        if profile_name in AUDIT_PROFILES:
            new_files = AUDIT_PROFILES[profile_name]
            self.forbidden_entry.delete(0, "end")
            self.forbidden_entry.insert(0, ", ".join(new_files))
            self.log_info(f"Perfil cambiado a: {profile_name}")

    def _browse_export_path(self):
        path = filedialog.askdirectory()
        if path:
            self.export_entry.delete(0, "end")
            self.export_entry.insert(0, path)

    def show_audit_panel(self):
        self.settings_panel.grid_forget()
        self.audit_panel.grid(row=0, column=0, sticky="nsew")

    def show_settings_panel(self):
        self.audit_panel.grid_forget()
        self.settings_panel.grid(row=0, column=0, sticky="nsew")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_path = folder
            # Shorten path for display
            display_path = folder if len(folder) < 40 else f"...{folder[-37:]}"
            self.path_label.configure(text=display_path, text_color=COLOR_TEXT)
            self.log_info(f"Carpeta seleccionada: {folder}")

    def run_audit(self):
        if not self.selected_path:
            messagebox.showwarning("Atención", "Por favor, selecciona una carpeta primero.")
            return
        
        # Deshabilitar botones para evitar spam
        self.btn_run.configure(state="disabled", text="ANALIZANDO...")
        if hasattr(self, 'btn_clean'): self.btn_clean.configure(state="disabled")
        if hasattr(self, 'btn_settings'): self.btn_settings.configure(state="disabled")
        
        self.log_info(f"Iniciando auditoría en: {self.selected_path}...")
        
        # Iniciar Barra de Progreso
        if hasattr(self, 'progress_bar'):
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()
        
        # Limpiar resultados anteriores
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        # Obtener configuración
        calc_hidden = self.settings.get("calc_hidden", False)
        forbidden = self.settings.get("forbidden_files", [])
        
        # Iniciar Hilo
        thread = threading.Thread(target=self._run_audit_worker, args=(self.selected_path, forbidden, calc_hidden))
        thread.daemon = True
        thread.start()

    def _run_audit_worker(self, path, forbidden, calc_hidden):
        try:
            data = audit_directory(path, forbidden, calc_hidden)
            self.after(0, lambda: self._audit_completed(data))
        except Exception as e:
            self.after(0, lambda: self._audit_completed(None, error_msg=str(e)))

    def _audit_completed(self, data, error_msg=None):
        # Detener Barra de Progreso
        if hasattr(self, 'progress_bar'):
            self.progress_bar.stop()
            self.progress_bar.configure(mode="determinate")
            self.progress_bar.set(0)

        # Re-habilitar botones
        self.btn_run.configure(state="normal", text="EJECUTAR AUDITORÍA")
        if hasattr(self, 'btn_clean'): self.btn_clean.configure(state="normal")
        if hasattr(self, 'btn_settings'): self.btn_settings.configure(state="normal")
        
        if error_msg:
            self.log_error(f"Error en auditoría: {error_msg}")
            messagebox.showerror("Error", f"Ocurrió un error en la auditoría:\n{error_msg}")
            return
            
        if not data:
            self.log_error("No se pudo analizar la carpeta.")
            return
            
        self.audit_results = data
        results = data["results"]
        summary = data["summary"]

        # Actualizar KPIs
        status_color = COLOR_SUCCESS if summary["status"] == "SUCCESS" else COLOR_ERROR
        self.kpi_status.configure(text=summary["status"], text_color=status_color)
        
        junk_color = COLOR_SUCCESS if summary["junk_count"] == 0 else COLOR_ERROR
        self.kpi_junk.configure(text=str(summary["junk_count"]), text_color=junk_color)
        
        docs_color = COLOR_SUCCESS if summary["docs_found"] else COLOR_ERROR
        self.kpi_docs.configure(text="Sí" if summary["docs_found"] else "No", text_color=docs_color)
        
        self.kpi_size.configure(text=summary["total_size"], text_color=COLOR_ACCENT)

        # Mostrar Checklist
        for res in results:
            row = ctk.CTkFrame(self.results_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            ctk.CTkLabel(row, text=res["icon"], font=ctk.CTkFont(size=16)).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=res["name"], font=ctk.CTkFont(weight="bold"), width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=res["msg"], text_color=COLOR_TEXT_MUTED).pack(side="left", padx=5)

            if res["status"] == "SUCCESS": self.log_success(f"{res['name']}: {res['msg']}")
            elif res["status"] == "ERROR": self.log_error(f"{res['name']}: {res['msg']}")
            else: self.log_info(f"{res['name']}: {res['msg']}")

            # Botón de Ayuda / Remediación
            if res.get("remediation"):
                # Capturar res en el lambda con r=res
                btn_help = ctk.CTkButton(
                    row, 
                    text="💡 Ayuda", 
                    width=60, 
                    height=20, 
                    font=ctk.CTkFont(size=10), 
                    fg_color="#3D4256", 
                    hover_color="#4D5266", 
                    command=lambda r=res: messagebox.showinfo("Guía de Remediación", f"Regla: {r['name']}\n\nAcción sugerida:\n{r['remediation']}")
                )
                btn_help.pack(side="right", padx=10)

        self.log_success("Auditoría completada.")


    def run_auto_clean(self):
        if not self.audit_results:
            messagebox.showwarning("Atención", "Primero debes ejecutar una auditoría.")
            return
        
        summary = self.audit_results["summary"]
        if summary["junk_count"] == 0:
            messagebox.showinfo("Limpieza", "No se encontraron archivos basura para eliminar.")
            return
            
        # Get junk files from audit results
        junk_files = []
        for res in self.audit_results["results"]:
            if res["name"] == "Limpieza" and "files" in res:
                junk_files = res["files"]
        
        if not junk_files:
            return

        confirm = messagebox.askyesno("Confirmar Limpieza", f"¿Estás seguro de que quieres eliminar {len(junk_files)} archivos/carpetas basura?")
        if not confirm:
            return
            
        deleted, errors = clean_junk(junk_files)
        
        if deleted > 0:
            self.log_success(f"Se eliminaron {deleted} elementos basura.")
        if errors:
            for err in errors:
                self.log_error(err)
                
        # Rerun audit to refresh
        self.run_audit()

    def export_report(self):
        if not self.audit_results:
            messagebox.showwarning("Atención", "Primero debes ejecutar una auditoría.")
            return
            
        default_dir = self.settings.get("export_path", "")
        if default_dir and not os.path.exists(default_dir):
            try:
                os.makedirs(default_dir)
            except Exception:
                pass

        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("Text files", "*.txt"), ("All files", "*.*")],
            initialdir=default_dir,
            initialfilename=f"Audit_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        )
        
        if not file_path:
            return
            
        try:
            if file_path.endswith(".html"):
                from src.formatters.html_formatter import HTMLFormatter
                from src.models import ProjectReport, CheckResult, Rule, RuleType, Severity
                
                report_results = []
                for res in self.audit_results["results"]:
                    passed = res["status"] == "SUCCESS"
                    # Mapear severidad
                    if res["status"] == "ERROR":
                        sev = Severity.ERROR
                    elif res["status"] == "WARNING":
                        sev = Severity.WARNING
                    else:
                        sev = Severity.INFO
                        
                    rule = Rule(
                        name=res["name"],
                        description="",
                        type=RuleType.FILE_EXISTS, # Dummy para compatibilidad
                        target="",
                        severity=sev
                    )
                    
                    report_results.append(CheckResult(
                        rule=rule,
                        passed=passed,
                        message=res["msg"]
                    ))
                
                # Calcular sumario real para el HTML
                passed_count = sum(1 for r in report_results if r.passed)
                failed_count = sum(1 for r in report_results if not r.passed)
                # Count errors and warnings
                error_count = sum(1 for r in report_results if not r.passed and r.rule.severity == Severity.ERROR)
                warning_count = sum(1 for r in report_results if not r.passed and r.rule.severity == Severity.WARNING)
                
                mapped_summary = {
                    "passed": passed_count,
                    "failed": failed_count,
                    "errors": error_count,
                    "warnings": warning_count
                }
                
                report = ProjectReport(
                    project_name=os.path.basename(self.selected_path) or "Proyecto",
                    project_type=self.settings.get("audit_profile", "Estándar"),
                    results=report_results,
                    summary=mapped_summary
                )
                
                formatter = HTMLFormatter()
                html_content = formatter.format(report)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
            else:
                # Soporte para TXT (Existente)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("========================================\n")
                    f.write("   RS PROJECT READINESS AUDIT REPORT\n")
                    f.write("========================================\n\n")
                    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Proyecto: {self.selected_path}\n")
                    f.write(f"Autor: {RS_AUTHOR}\n\n")
                    
                    summary = self.audit_results["summary"]
                    f.write("RESUMEN GENERAL:\n")
                    f.write(f"- Estado: {summary['status']}\n")
                    f.write(f"- Perfil: {self.settings.get('audit_profile', 'Personalizado')}\n")
                    f.write(f"- Archivos Basura: {summary['junk_count']}\n")
                    f.write(f"- Documentación: {'OK' if summary['docs_found'] else 'FALTA'}\n")
                    f.write(f"- Peso Total: {summary['total_size']}\n\n")
                    
                    f.write("DETALLES DE LA INSPECCIÓN:\n")
                    for res in self.audit_results["results"]:
                        f.write(f"{res['icon']} {res['name']}: {res['msg']}\n")
                        if "files" in res and res["files"]:
                            f.write("   Archivos detectados:\n")
                            for file in res["files"]:
                                f.write(f"     - {file}\n")
                    
                    f.write("\n========================================\n")
                    f.write("   Generado por Project Readiness Checker\n")
                    f.write("========================================\n")
                
            self.log_success(f"Reporte exportado exitosamente a: {file_path}")
            messagebox.showinfo("Éxito", "El reporte ha sido exportado correctamente.")

        except Exception as e:
            self.log_error(f"Error al exportar reporte: {str(e)}")
            messagebox.showerror("Error", f"No se pudo exportar el reporte: {str(e)}")

    def save_settings_action(self):
        new_settings = {
            "export_path": self.export_entry.get(),
            "audit_profile": self.profile_dropdown.get(),
            "calc_hidden": self.calc_hidden_switch.get() == 1,
            "forbidden_files": [x.strip() for x in self.forbidden_entry.get().split(",") if x.strip()]
        }
        save_settings(new_settings)
        self.settings = new_settings
        self.log_success("Configuración guardada correctamente.")
        messagebox.showinfo("Éxito", "Configuración guardada.")

    def log_info(self, msg):
        self._add_log(f"[{datetime.now().strftime('%H:%M:%S')}] [INFO] {msg}", COLOR_INFO)

    def log_success(self, msg):
        self._add_log(f"[{datetime.now().strftime('%H:%M:%S')}] [SUCCESS] {msg}", COLOR_SUCCESS)

    def log_error(self, msg):
        self._add_log(f"[{datetime.now().strftime('%H:%M:%S')}] [ERROR] {msg}", COLOR_ERROR)

    def _add_log(self, full_msg, color):
        self.console.configure(state="normal")
        self.console.insert("end", full_msg + "\n")
        # Apply color to the last line (Simplified for CTkTextbox)
        self.console.configure(state="disabled")
        self.console.see("end")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = RSProjectReadinessApp()
    app.mainloop()
