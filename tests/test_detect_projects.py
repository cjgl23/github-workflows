from pathlib import Path
import unittest

from scripts.detect_projects import detect

FIXTURES = Path(__file__).parent / "fixtures"


class DetectProjectsTests(unittest.TestCase):
    def test_profiles(self):
        self.assertEqual(["."], detect(FIXTURES / "node")["node"])
        self.assertEqual(["."], detect(FIXTURES / "python")["python"])
        self.assertEqual(["."], detect(FIXTURES / "go")["go"])
        self.assertEqual(["."], detect(FIXTURES / "maven")["maven"])
        self.assertEqual(["."], detect(FIXTURES / "gradle")["gradle"])
        self.assertEqual(["."], detect(FIXTURES / "dotnet")["dotnet"])
        self.assertEqual(["."], detect(FIXTURES / "rust")["rust"])
        self.assertEqual(["."], detect(FIXTURES / "generic")["generic"])

    def test_monorepo(self):
        result = detect(FIXTURES / "monorepo")
        self.assertEqual(["web"], result["node"])
        self.assertEqual(["service"], result["python"])
        self.assertEqual([], result["generic"])


if __name__ == "__main__":
    unittest.main()
