import unittest
from scripts.release_policy import decide_release, bump_version


class ReleasePolicyTests(unittest.TestCase):
    def test_bump_version(self):
        self.assertEqual("v2.0.0", bump_version("v1.9.9", "major"))
        self.assertEqual("v1.10.0", bump_version("v1.9.9", "minor"))
        self.assertEqual("v1.9.10", bump_version("v1.9.9", "patch"))

    def test_breaking_is_major(self):
        d = decide_release("v1.2.3", ["feat!: replace API"], ["src/app.js"])
        self.assertEqual("major", d["bump"])
        self.assertEqual("v2.0.0", d["next_tag"])

    def test_feat_and_human_add_are_minor(self):
        self.assertEqual("minor", decide_release("v1.2.3", ["feat: add tool"], ["src/app.js"])["bump"])
        self.assertEqual("minor", decide_release("v1.2.3", ["Add text checker"], ["src/app.js"])["bump"])

    def test_other_product_change_is_patch(self):
        self.assertEqual("patch", decide_release("v1.2.3", ["Harden router"], ["src/app.js"])["bump"])

    def test_docs_tests_workflow_only_skips(self):
        d = decide_release("v1.2.3", ["docs: update"], ["README.md", "tests/a.js", ".github/workflows/ci.yml"])
        self.assertFalse(d["release_needed"])

    def test_memory_bank_only_skips(self):
        d = decide_release("v1.2.3", ["Update memory"], ["memory-bank/progress.md"])
        self.assertFalse(d["release_needed"])


if __name__ == "__main__":
    unittest.main()
