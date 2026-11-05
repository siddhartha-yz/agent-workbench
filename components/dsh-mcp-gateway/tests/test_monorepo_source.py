from __future__ import annotations

import io
import os
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "scripts/component-source.sh"


class MonorepoSourceTests(unittest.TestCase):
    def test_component_export_omits_siblings_and_keeps_standalone_layout(self) -> None:
        for monorepo in (False, True):
            with self.subTest(monorepo=monorepo), tempfile.TemporaryDirectory() as tmp:
                repo = Path(tmp) / "repo with spaces"
                component = repo / "components/dsh-mcp-gateway" if monorepo else repo
                module = component / "src/dsh_mcp_gateway/__init__.py"
                module.parent.mkdir(parents=True)
                module.write_text('__version__ = "0.1.0"\n', encoding="utf-8")
                (component / "pyproject.toml").write_text("# gateway\n", encoding="utf-8")
                if monorepo:
                    (repo / "unrelated.txt").write_text("sibling component\n", encoding="utf-8")
                subprocess.run(["git", "init", "-q", str(repo)], check=True)
                subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
                subprocess.run(["git", "-C", str(repo), "-c", "user.name=Gateway Test",
                                "-c", "user.email=gateway-test@example.invalid", "commit",
                                "--no-gpg-sign", "-qm", "fixture"], check=True)
                for source in {repo, component}:
                    env = dict(os.environ, SOURCE_CANDIDATE=str(source), HELPER=str(HELPER))
                    exported = subprocess.check_output(["bash", "-c",
                        ('set -euo pipefail; source "$HELPER"; '
                        'root=$(gateway_source_root "$SOURCE_CANDIDATE"); '
                        'ref=$(gateway_archive_ref "$root" HEAD); '
                        'git_root=$(git -C "$root" rev-parse --show-toplevel); '
                        'git -C "$git_root" archive "$ref"')], env=env)
                    with tarfile.open(fileobj=io.BytesIO(exported)) as archive:
                        files = {entry.name for entry in archive.getmembers() if entry.isfile()}
                        self.assertEqual(files, {"pyproject.toml", "src/dsh_mcp_gateway/__init__.py"})
                        self.assertEqual(archive.extractfile("pyproject.toml").read(), b"# gateway\n")

    def test_non_gateway_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(["bash", "-c", 'source "$1"; gateway_source_root "$2"',
                                     "bash", str(HELPER), tmp], check=False, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("gateway component not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
