from pathlib import Path
import tempfile
import unittest

from scripts.verify_supply_chain import scan_repository

ROOT = Path(__file__).resolve().parents[1]


class SupplyChainTests(unittest.TestCase):
    def _issues(self, workflow: str, name: str = "test.yml") -> list[str]:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / ".github" / "workflows"
            path.mkdir(parents=True)
            (path / name).write_text(workflow, encoding="utf-8")
            return scan_repository(root)

    def test_rejects_floating_external_action(self):
        issues = self._issues("permissions:\n  contents: read\njobs:\n  x:\n    steps:\n      - uses: actions/checkout@v6\n")
        self.assertTrue(any("full commit SHA" in issue for issue in issues))

    def test_rejects_secrets_inherit(self):
        issues = self._issues("permissions:\n  contents: read\njobs:\n  x:\n    secrets: inherit\n")
        self.assertTrue(any("secrets: inherit" in issue for issue in issues))

    def test_rejects_persisted_checkout_credentials(self):
        issues = self._issues("permissions:\n  contents: read\njobs:\n  x:\n    steps:\n      - uses: actions/checkout@1af3b93b6815bc44a9784bd300feb67ff0d1eeb3\n")
        self.assertTrue(any("persist-credentials" in issue for issue in issues))

    def test_accepts_same_commit_nested_workflow_reference(self):
        issues = self._issues("permissions:\n  contents: read\njobs:\n  x:\n    uses: $/.github/workflows/ci-node.yml\n")
        self.assertEqual([], issues)

    def test_release_permissions_are_exact(self):
        good = "permissions:\n  contents: write\njobs:\n  x:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo ok\n"
        self.assertEqual([], self._issues(good, "release.yml"))
        bad = "permissions:\n  contents: write\n  issues: write\njobs:\n  x:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo bad\n"
        self.assertTrue(self._issues(bad, "release.yml"))

    def test_repository_workflows_meet_policy(self):
        self.assertEqual([], scan_repository(ROOT))


if __name__ == "__main__":
    unittest.main()
