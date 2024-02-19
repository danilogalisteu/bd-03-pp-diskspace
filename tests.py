
import unittest

import pathlib

from filesystem import DirEntry



class DirEntryTests(unittest.TestCase):
    def test_dir_entry_init(self):
        base_path = pathlib.Path('.')
        entry = DirEntry(base_path)

        self.assertIsNone(
            entry.parent
        )
        self.assertEqual(
            entry.name,
            base_path.name
        )
        self.assertEqual(
            entry.path,
            base_path
        )
        self.assertTrue(
            entry.is_dir
        )
        self.assertGreaterEqual(
            entry.size,
            0
        )
        self.assertGreaterEqual(
            entry.total_size,
            0
        )
        self.assertGreaterEqual(
            entry.mode,
            0
        )
        self.assertGreaterEqual(
            entry.mtime,
            0
        )
        self.assertIsNotNone(
            entry.children
        )
        self.assertIsInstance(
            entry.children,
            list
        )


if __name__ == "__main__":
    unittest.main()
