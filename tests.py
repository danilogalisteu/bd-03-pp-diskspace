
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
        self.assertEqual(
            sorted([e.name for e in entry.children]),
            sorted([p.name for p in base_path.iterdir()])
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
    
    def test_dir_entry_methods(self):
        base_path = pathlib.Path('.')
        entry = DirEntry(base_path)

        self.assertIsInstance(
            entry.get_mode_str(),
            str
        )
        self.assertTrue(
            entry.get_mode_str().startswith('d')
        )
        self.assertIsInstance(
            entry.get_mtime_str(),
            str
        )
        self.assertIsInstance(
            entry.get_info(),
            tuple
        )
        self.assertIsInstance(
            entry.get_tree_info_r(),
            dict
        )


if __name__ == "__main__":
    unittest.main()
