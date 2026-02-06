from src.models import ProjectConfig, Rule, RuleType
from src.checkers.engine import CheckerEngine

def test_file_exists_rule(tmp_path):
    # Crear un archivo temporal
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")
    
    config = ProjectConfig(
        project_name="Test",
        project_type="software",
        rules=[
            Rule(
                name="File Exists",
                description="Test rule",
                type=RuleType.FILE_EXISTS,
                target=str(test_file)
            ),
            Rule(
                name="File Not Exists",
                description="Test rule fail",
                type=RuleType.FILE_EXISTS,
                target="non_existent.txt"
            )
        ]
    )
    
    engine = CheckerEngine(config)
    report = engine.run_checks()
    
    assert report.results[0].passed is True
    assert report.results[1].passed is False
    assert report.summary["passed"] == 1
    assert report.summary["failed"] == 1

def test_dir_exists_rule(tmp_path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    
    config = ProjectConfig(
        project_name="Test",
        project_type="software",
        rules=[
            Rule(
                name="Dir Exists",
                description="Test rule",
                type=RuleType.DIR_EXISTS,
                target=str(test_dir)
            )
        ]
    )
    
    engine = CheckerEngine(config)
    report = engine.run_checks()
    
    assert report.results[0].passed is True

def test_file_contains_rule(tmp_path):
    test_file = tmp_path / "version.txt"
    test_file.write_text("version: 1.2.3")
    
    config = ProjectConfig(
        project_name="Test",
        project_type="software",
        rules=[
            Rule(
                name="Contains Version",
                description="Test rule",
                type=RuleType.FILE_CONTAINS,
                target=str(test_file),
                pattern=r"1\.2\.3"
            ),
            Rule(
                name="Does not contain",
                description="Test rule fail",
                type=RuleType.FILE_CONTAINS,
                target=str(test_file),
                pattern=r"2\.0\.0"
            )
        ]
    )
    
    engine = CheckerEngine(config)
    report = engine.run_checks()
    
    assert report.results[0].passed is True
    assert report.results[1].passed is False

def test_command_success_rule():
    config = ProjectConfig(
        project_name="Test",
        project_type="software",
        rules=[
            Rule(
                name="Command Success",
                description="Test rule",
                type=RuleType.COMMAND_SUCCESS,
                target="echo hello"
            ),
            Rule(
                name="Command Fail",
                description="Test rule fail",
                type=RuleType.COMMAND_SUCCESS,
                target="exit 1"
            )
        ]
    )
    
    engine = CheckerEngine(config)
    report = engine.run_checks()
    
    assert report.results[0].passed is True
    assert report.results[1].passed is False
