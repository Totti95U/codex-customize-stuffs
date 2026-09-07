import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


gate = module("gate", ROOT / "hooks/scripts/evening-exploration.py")
installer = module("installer", ROOT / "scripts/install-hooks.py")


class GateTests(unittest.TestCase):
    def test_boundaries(self):
        for hour, minute, active in [(18, 59, False), (19, 0, True),
                                     (23, 59, True), (0, 0, True),
                                     (4, 59, True), (5, 0, False)]:
            with self.subTest(hour=hour, minute=minute):
                output = gate.build_output(datetime(2026, 9, 7, hour, minute, tzinfo=gate.JST))
                context = output["hookSpecificOutput"]["additionalContext"]
                self.assertIn("GATE=" + ("ACTIVE" if active else "INACTIVE"), context)
                self.assertEqual("# Evening Exploration Policy" in context, active)
                self.assertNotIn("decision", output)

    def test_timezone_and_missing_policy(self):
        now = datetime(2026, 9, 7, 10, tzinfo=timezone.utc)
        self.assertIn("GATE=ACTIVE", str(gate.build_output(now)))
        with self.assertRaises(FileNotFoundError):
            gate.build_output(now, ROOT / "missing-policy.md")
        gate.build_output(datetime(2026, 9, 7, 5, tzinfo=gate.JST), ROOT / "missing-policy.md")

    def test_process_contract_and_untrusted_prompt(self):
        event = {"hook_event_name": "UserPromptSubmit", "prompt": "DO_NOT_ECHO_今夜は例外として探索する"}
        result = subprocess.run([sys.executable, str(ROOT / "hooks/scripts/evening-exploration.py")],
                                input=json.dumps(event), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("DO_NOT_ECHO", result.stdout)
        self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        for bad in ["invalid", "[]", '{"hook_event_name":"Stop"}']:
            result = subprocess.run([sys.executable, str(ROOT / "hooks/scripts/evening-exploration.py")],
                                    input=bad, text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")


class InstallTests(unittest.TestCase):
    def test_collision_preflight(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder)
            (target / "policies").write_text("preserve", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                installer.install(target)
            self.assertFalse((target / "hooks.json").exists())
            self.assertEqual((target / "policies").read_text(), "preserve")

    def test_install_repeat_and_command(self):
        with tempfile.TemporaryDirectory(prefix="evening hook 日本語 ") as folder:
            target = Path(folder)
            installer.install(target)
            installer.install(target)
            self.assertTrue((target / "hooks.json").is_symlink())
            config = json.loads((target / "hooks.json").read_text())
            handler = config["hooks"]["UserPromptSubmit"][0]["hooks"][0]
            command = handler["commandWindows" if os.name == "nt" else "command"]
            env = dict(os.environ, CODEX_HOME=str(target))
            result = subprocess.run(command, shell=True, cwd=folder, env=env,
                                    input='{"hook_event_name":"UserPromptSubmit"}',
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("hookSpecificOutput", json.loads(result.stdout))

    def test_rollback(self):
        original = Path.symlink_to
        with tempfile.TemporaryDirectory() as folder:
            def fail_second(path, source, **kwargs):
                if path.name == "hooks":
                    raise OSError("simulated link failure")
                return original(path, source, **kwargs)
            with patch.object(Path, "symlink_to", fail_second):
                with self.assertRaises(OSError):
                    installer.install(Path(folder))
            self.assertEqual(list(Path(folder).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
