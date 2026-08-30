from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATE_WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"

EXPECTED_NEEDS = (
    "validate",
    "fixture-node",
    "fixture-python",
    "fixture-go",
    "fixture-maven",
    "fixture-gradle",
    "fixture-dotnet",
    "fixture-rust",
    "fixture-generic",
    "fixture-monorepo",
)


class ValidateWorkflowTests(unittest.TestCase):
    def test_validation_complete_aggregates_every_validation_job(self):
        workflow = VALIDATE_WORKFLOW.read_text(encoding="utf-8")
        marker = "\n  validation-complete:\n"
        self.assertIn(marker, workflow)

        aggregate = workflow.split(marker, 1)[1]
        self.assertIn("if: ${{ always() }}", aggregate)
        self.assertIn("toJSON(needs)", aggregate)
        self.assertIn('data.get("result") != "success"', aggregate)

        for dependency in EXPECTED_NEEDS:
            self.assertIn(f"      - {dependency}\n", aggregate)


if __name__ == "__main__":
    unittest.main()
