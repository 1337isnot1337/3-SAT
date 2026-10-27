import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.sources import verify_sources


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "upstream/openai-eth-2026/example.tex"
        self.path.parent.mkdir(parents=True)
        data = b"frozen source\n"
        self.path.write_bytes(data)
        commit = "a" * 40
        self.manifest = {"schema_version": 1, "upstream_commit": commit, "files": [{
            "path": self.path.relative_to(self.root).as_posix(),
            "upstream_path": "example.tex",
            "url": f"https://raw.githubusercontent.com/openai/math/{commit}/example.tex",
            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
        }]}
        self.save()

    def save(self):
        (self.root / "SOURCES.json").write_text(json.dumps(self.manifest))

    def test_accept_pinned_file_and_reject_mutation(self):
        self.assertEqual(verify_sources(self.root), 1)
        self.path.write_bytes(b"altered source")
        with self.assertRaisesRegex(ValueError, "mismatch"):
            verify_sources(self.root)

    def test_reject_missing_and_undeclared_files(self):
        extra = self.path.parent / "unlisted.txt"
        extra.write_text("extra")
        with self.assertRaisesRegex(ValueError, "inventory"):
            verify_sources(self.root)
        extra.unlink()
        self.path.unlink()
        with self.assertRaisesRegex(ValueError, "inventory"):
            verify_sources(self.root)

    def test_reject_unpinned_url_and_duplicate_entry(self):
        self.manifest["files"][0]["url"] = "https://example.com/latest"
        self.save()
        with self.assertRaisesRegex(ValueError, "commit"):
            verify_sources(self.root)
        self.manifest["files"] *= 2
        self.manifest["files"][0]["url"] = f"https://raw.githubusercontent.com/openai/math/{'a' * 40}/example.tex"
        self.save()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            verify_sources(self.root)

    def test_reject_symlink_even_with_identical_bytes(self):
        target = self.root / "same-bytes"
        target.write_bytes(self.path.read_bytes())
        self.path.unlink()
        self.path.symlink_to(target)
        with self.assertRaisesRegex(ValueError, "symlink"):
            verify_sources(self.root)


if __name__ == "__main__":
    unittest.main()
