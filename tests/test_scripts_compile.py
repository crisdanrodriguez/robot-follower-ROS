from pathlib import Path
import py_compile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"


class ScriptCompilationTests(unittest.TestCase):
    def test_all_python_scripts_compile(self):
        failures = []

        for script_path in sorted(SCRIPTS_DIR.glob("*.py")):
            try:
                py_compile.compile(str(script_path), doraise=True)
            except py_compile.PyCompileError as error:
                failures.append(f"{script_path.name}: {error.msg}")

        self.assertFalse(failures, "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
