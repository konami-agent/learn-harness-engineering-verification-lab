import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class Chapter01DocumentationContractTest(unittest.TestCase):
    def test_experiment_doc_records_chapter01_contract_and_commands(self):
        doc = ROOT / "chapters" / "chapter-01" / "README.md"
        self.assertTrue(doc.exists(), "Chapter 01 experiment README is missing")
        text = doc.read_text(encoding="utf-8")
        required_phrases = [
            "Capability does not imply reliability",
            "Source grounding",
            "Deterministic validator",
            "Positive fixture",
            "Negative fixtures",
            "python3 -m harness_lab.validators.chapter01 validate",
            "python3 -m unittest discover -s tests -v",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_readme_lists_chapter01_deliverables(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        required_phrases = [
            "Chapter 01",
            "deterministic validator",
            "chapters/chapter-01/fixtures",
            "harness_lab/validators/chapter01.py",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_issue_seed_marks_chapter01_completed_deliverables(self):
        text = (ROOT / "docs" / "issue-seed.yaml").read_text(encoding="utf-8")
        required_phrases = [
            'title: "Chapter 01 map: pilot the verification design"',
            'status: "done"',
            'title: "Deterministic verification framework"',
            'Chapter 01 validator exists at `harness_lab/validators/chapter01.py`.',
            'title: "Chapter 1-4 experiment set"',
            'Chapter 01 experiment fixtures exist under `chapters/chapter-01/fixtures/`.',
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
