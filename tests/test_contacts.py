import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.contacts import (
    CONTACTS_FILENAME,
    contact_alias_count,
    describe_contact_aliases,
    parse_contact_alias_candidate,
    read_contact_aliases,
    remove_contact_alias,
    save_contact_alias,
)


class ContactAliasTests(unittest.TestCase):
    def test_contact_alias_store_writes_reads_and_removes_aliases(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            alias, target = parse_contact_alias_candidate("小王 => 微信联系人王工")
            saved = save_contact_alias(paths, alias, target, source="config-candidate")
            aliases_after_save = read_contact_aliases(paths)
            count_after_save = contact_alias_count(paths)
            description = describe_contact_aliases(paths)
            removed = remove_contact_alias(paths, alias)
            aliases_after_remove = read_contact_aliases(paths)

            self.assertEqual(alias, "小王")
            self.assertEqual(target, "微信联系人王工")
            self.assertEqual(saved.alias, "小王")
            self.assertEqual(saved.target, "微信联系人王工")
            self.assertEqual(len(aliases_after_save), 1)
            self.assertEqual(count_after_save, 1)
            self.assertIn("联系人别名：", description)
            self.assertIn("小王 -> 微信联系人王工", description)
            self.assertTrue((paths.config_dir / CONTACTS_FILENAME).exists())
            self.assertTrue(removed)
            self.assertEqual(aliases_after_remove, ())
            self.assertEqual(contact_alias_count(paths), 0)

    def test_contact_alias_candidate_requires_alias_and_target(self):
        with self.assertRaises(ValueError) as missing_target:
            parse_contact_alias_candidate("小王")

        with self.assertRaises(ValueError) as missing_alias:
            parse_contact_alias_candidate("=> 微信联系人王工")

        self.assertIn("联系人别名候选格式", str(missing_target.exception))
        self.assertIn("联系人别名候选格式", str(missing_alias.exception))


if __name__ == "__main__":
    unittest.main()
