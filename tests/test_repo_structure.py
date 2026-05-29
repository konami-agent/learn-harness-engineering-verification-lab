import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_01 = ROOT / "chapters" / "chapter-01"


class RepoStructureTest(unittest.TestCase):
    def test_chapter_01_learning_layout_exists(self):
        required_paths = [
            CHAPTER_01 / "README.md",
            CHAPTER_01 / "source.md",
            CHAPTER_01 / "lesson-map.md",
            CHAPTER_01 / "exercise.md",
            CHAPTER_01 / "expected-results.md",
            CHAPTER_01 / "fixtures" / "positive" / "report.json",
            CHAPTER_01 / "smoke" / "deterministic" / "manifest-with-agents.json",
            CHAPTER_01 / "smoke" / "deterministic" / "manifest-no-agents.json",
            CHAPTER_01 / "smoke" / "deterministic" / "manifest-self-report-only.json",
            CHAPTER_01 / "smoke" / "deterministic" / "adapters" / "write_valid_report.py",
            CHAPTER_01 / "smoke" / "deterministic" / "adapters" / "write_self_report_only.py",
            CHAPTER_01 / "smoke" / "live" / "github-copilot-cli" / "README.md",
            CHAPTER_01 / "smoke" / "live" / "github-copilot-cli" / "manifest.json",
            CHAPTER_01 / "smoke" / "live" / "github-copilot-cli" / "run.sh",
            ROOT / "harness_lab" / "validators" / "chapter01.py",
            ROOT / "tests" / "chapter_01" / "test_validator.py",
        ]
        for path in required_paths:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.exists(), f"missing {path.relative_to(ROOT)}")

    def test_legacy_top_level_chapter_01_layout_is_not_the_learning_entrypoint(self):
        obsolete_paths = [
            ROOT / "experiments" / "chapter-01",
            ROOT / "smoke" / "chapter-01",
        ]
        for path in obsolete_paths:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertFalse(path.exists(), f"obsolete layout still exists: {path.relative_to(ROOT)}")

    def test_root_readme_points_to_learning_path(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for phrase in [
            "chapters/chapter-01/",
            "Chapter 01 learning path",
            "chapters/chapter-01/exercise.md",
            "harness_lab/validators/",
            "tests/chapter_01/",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
