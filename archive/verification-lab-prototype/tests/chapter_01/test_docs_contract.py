import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class Chapter01DocumentationContractTest(unittest.TestCase):
    def test_root_readme_defines_upstream_companion_boundary(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        required_phrases = [
            "walkinglabs/learn-harness-engineering",
            "https://github.com/walkinglabs/learn-harness-engineering",
            "executable verification companion",
            "does not replace the upstream course",
            "Read the course there. Run verification labs here.",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_experiment_doc_records_chapter01_contract_and_commands(self):
        doc = ROOT / "chapters" / "chapter-01" / "README.md"
        self.assertTrue(doc.exists(), "Chapter 01 experiment README is missing")
        text = doc.read_text(encoding="utf-8")
        required_phrases = [
            "Capability does not imply reliability",
            "Source grounding",
            "verification lab",
            "upstream Lecture 01",
            "upstream Project 01",
            "does not replace the upstream course",
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
            "executable verification companion",
            "deterministic validator",
            "chapters/chapter-01/fixtures",
            "harness_lab/validators/chapter01.py",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_verification_map_links_source_claims_to_local_artifacts(self):
        path = ROOT / "chapters" / "chapter-01" / "verification-map.md"
        self.assertTrue(path.exists(), "Chapter 01 verification-map.md is missing")
        text = path.read_text(encoding="utf-8")
        required_phrases = [
            "Source claim",
            "Verification hypothesis",
            "Implemented artifact",
            "upstream Lecture 01",
            "upstream Project 01",
            "manifest-with-agents.json",
            "manifest-no-agents.json",
            "self_report",
            "manual observation",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_lab_doc_is_verification_lab_not_replacement_exercise(self):
        path = ROOT / "chapters" / "chapter-01" / "lab.md"
        self.assertTrue(path.exists(), "Chapter 01 lab.md is missing")
        text = path.read_text(encoding="utf-8")
        required_phrases = [
            "verification lab",
            "does not replace the upstream Project 01 exercise",
            "Read the course there. Run verification labs here.",
            "deterministic validator",
            "deterministic smoke",
            "live GitHub Copilot CLI smoke",
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
