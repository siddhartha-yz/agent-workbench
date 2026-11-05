from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT.parents[1] / ".github" / "workflows" / "gateway-release.yml"


def resolver_script() -> str:
    text = WORKFLOW.read_text(encoding="utf-8")
    start = text.index("          set -euo pipefail", text.index("name: Resolve release tag"))
    end = text.index("\n      - name: Check out tagged source", start)
    return "\n".join(line[10:] for line in text[start:end].splitlines())


class ReleaseWorkflowTests(unittest.TestCase):
    def test_release_uses_component_directory_and_gateway_namespace(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('      - "gateway-v*"', text)
        self.assertIn("working-directory: components/dsh-mcp-gateway", text)
        self.assertIn('git checkout --detach "$TAG"', text)
        self.assertIn('test -f "docs/releases/v$VERSION.md"', text)
        self.assertIn("python -m build --wheel --outdir dist", text)
        self.assertIn('gh release create "$TAG" dist/*', text)
        self.assertIn("--verify-tag", text)
        self.assertIn("--latest=false", text)
        self.assertNotIn("branches:", text)
        self.assertNotIn("git tag --list", text)
        self.assertFalse((ROOT / ".github/workflows/release.yml").exists())

    def test_tag_resolver_accepts_existing_gateway_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.name=Gateway Test",
                            "-c", "user.email=gateway-test@example.invalid", "commit",
                            "--allow-empty", "--no-gpg-sign", "-qm", "fixture"], check=True)
            subprocess.run(["git", "-C", str(root), "tag", "gateway-v0.1.0"], check=True)
            env = dict(os.environ, EVENT_NAME="push", REF_TYPE="tag",
                       REF_NAME="gateway-v0.1.0", INPUT_TAG="",
                       GITHUB_OUTPUT=str(root / "output"))
            subprocess.run(["bash", "-c", resolver_script()], cwd=root, env=env,
                           check=True, capture_output=True, text=True)
            self.assertEqual((root / "output").read_text(encoding="utf-8"),
                             "tag=gateway-v0.1.0\nversion=0.1.0\n")

    def test_tag_resolver_rejects_legacy_tag_and_ordinary_main_push(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for event, ref_type, ref_name, input_tag in [
                ("push", "branch", "main", ""),
                ("push", "tag", "v0.1.0", ""),
                ("workflow_dispatch", "branch", "main", "v0.1.0"),
            ]:
                with self.subTest(event=event, ref=ref_name, tag=input_tag):
                    env = dict(os.environ, EVENT_NAME=event, REF_TYPE=ref_type,
                               REF_NAME=ref_name, INPUT_TAG=input_tag,
                               GITHUB_OUTPUT=str(Path(tmp) / "output"))
                    result = subprocess.run(["bash", "-c", resolver_script()],
                                            check=False, env=env, capture_output=True, text=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse((Path(tmp) / "output").exists())


if __name__ == "__main__":
    unittest.main()
