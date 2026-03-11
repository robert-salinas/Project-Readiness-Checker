import os
import shutil
from pathlib import Path

def get_directory_size(path, calc_hidden=False):
    total_size = 0
    try:
        for entry in os.scandir(path):
            if not calc_hidden and entry.name.startswith("."):
                continue
            if entry.is_file():
                total_size += entry.stat().st_size
            elif entry.is_dir():
                total_size += get_directory_size(entry.path, calc_hidden)
    except (PermissionError, OSError):
        pass
    return total_size

def format_size(size_bytes):
    if size_bytes == 0: return "0B"
    size_name = ("B", "KB", "MB", "GB")
    import math
    try:
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
    except Exception:
        return "0B"

def audit_directory(path_str, forbidden_files, calc_hidden=False):
    path = Path(path_str)
    if not path.exists() or not path.is_dir():
        return None
    
    results = []
    summary = {
        "status": "SUCCESS",
        "junk_count": 0,
        "docs_found": False,
        "total_size": format_size(get_directory_size(path, calc_hidden))
    }
    
    # 1. Documentación
    readme = path / "README.md"
    if readme.exists():
        size = readme.stat().st_size
        if size > 10:
            results.append({"name": "README.md", "status": "SUCCESS", "msg": f"Encontrado ({size} bytes)", "icon": "✅"})
            summary["docs_found"] = True
        else:
            results.append({"name": "README.md", "status": "WARNING", "msg": "Existe pero está vacío", "icon": "⚠️"})
            summary["docs_found"] = True
    else:
        results.append({"name": "README.md", "status": "ERROR", "msg": "No se encontró README.md", "icon": "❌"})
        summary["status"] = "ERROR"

    # 2. Dependencias
    deps = ["requirements.txt", "package.json", "pyproject.toml"]
    found_deps = [d for d in deps if (path / d).exists()]
    if found_deps:
        results.append({"name": "Dependencias", "status": "SUCCESS", "msg": f"Detectado: {', '.join(found_deps)}", "icon": "✅"})
    else:
        results.append({"name": "Dependencias", "status": "WARNING", "msg": "No se detectaron archivos de dependencias", "icon": "⚠️"})

    # 3. Estructura
    essential = ["src", "tests"]
    missing = [d for d in essential if not (path / d).exists()]
    if not missing:
        results.append({"name": "Estructura", "status": "SUCCESS", "msg": "Carpetas /src y /tests presentes", "icon": "✅"})
    else:
        results.append({"name": "Estructura", "status": "WARNING", "msg": f"Faltan carpetas: {', '.join(missing)}", "icon": "⚠️"})

    # 4. Limpieza (Archivos prohibidos)
    found_forbidden = []
    for pattern in forbidden_files:
        if "*" in pattern:
            import fnmatch
            for root, dirs, files in os.walk(path):
                for name in fnmatch.filter(files + dirs, pattern):
                    found_forbidden.append(os.path.join(root, name))
        else:
            for root, dirs, files in os.walk(path):
                if pattern in dirs or pattern in files:
                    found_forbidden.append(os.path.join(root, pattern))

    if found_forbidden:
        summary["junk_count"] = len(found_forbidden)
        results.append({"name": "Limpieza", "status": "ERROR", "msg": f"Se encontraron {len(found_forbidden)} archivos/carpetas basura", "icon": "❌", "files": found_forbidden})
        summary["status"] = "ERROR"
    else:
        results.append({"name": "Limpieza", "status": "SUCCESS", "msg": "Proyecto limpio de archivos prohibidos", "icon": "✅"})
        
    return {"results": results, "summary": summary}

def clean_junk(files_list):
    deleted_count = 0
    errors = []
    for f_path in files_list:
        try:
            path = Path(f_path)
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            deleted_count += 1
        except Exception as e:
            errors.append(f"Error eliminando {f_path}: {str(e)}")
    return deleted_count, errors
