# Copyright 2017, Inderpreet Singh, All rights reserved.

import unittest
from datetime import datetime

from model import ModelFile


class TestModelFile(unittest.TestCase):
    def test_name(self):
        file = ModelFile("test", False)
        self.assertEqual("test", file.name)

    def test_is_dir(self):
        file = ModelFile("test", False)
        self.assertEqual(False, file.is_dir)
        file = ModelFile("test", True)
        self.assertEqual(True, file.is_dir)

    def test_state(self):
        file = ModelFile("test", False)

        file.state = ModelFile.State.DOWNLOADING
        self.assertEqual(ModelFile.State.DOWNLOADING, file.state)

        with self.assertRaises(TypeError):
            file.state = "BadState"

    def test_local_size(self):
        file = ModelFile("test", False)

        file.local_size = 100
        self.assertEqual(100, file.local_size)
        file.local_size = None
        self.assertEqual(None, file.local_size)

        with self.assertRaises(TypeError):
            file.local_size = "BadValue"
        with self.assertRaises(ValueError):
            file.local_size = -100

    def test_remote_size(self):
        file = ModelFile("test", False)

        file.remote_size = 100
        self.assertEqual(100, file.remote_size)
        file.remote_size = None
        self.assertEqual(None, file.remote_size)

        with self.assertRaises(TypeError):
            file.remote_size = "BadValue"
        with self.assertRaises(ValueError):
            file.remote_size = -100

    def test_downloading_speed(self):
        file = ModelFile("test", False)

        file.downloading_speed = 100
        self.assertEqual(100, file.downloading_speed)
        file.downloading_speed = None
        self.assertEqual(None, file.downloading_speed)

        with self.assertRaises(TypeError):
            file.downloading_speed = "BadValue"
        with self.assertRaises(ValueError):
            file.downloading_speed = -100

    def test_update_timestamp(self):
        file = ModelFile("test", False)

        from datetime import datetime
        now = datetime.now()
        file.update_timestamp = now
        self.assertEqual(now, file.update_timestamp)

        with self.assertRaises(TypeError):
            file.update_timestamp = 100

    def test_eta(self):
        file = ModelFile("test", False)

        file.eta = 100
        self.assertEqual(100, file.eta)
        file.eta = None
        self.assertEqual(None, file.eta)

        with self.assertRaises(TypeError):
            file.eta = "BadValue"
        with self.assertRaises(ValueError):
            file.eta = -100

    def test_equality_operator(self):
        # check that timestamp does not affect equality
        now = datetime.now()
        file1 = ModelFile("test", False)
        file1.local_size = 100
        file1.update_timestamp = now
        file2 = ModelFile("test", False)
        file2.local_size = 200
        file2.update_timestamp = now
        self.assertFalse(file1 == file2)

        file2.local_size = 100
        file2.update_timestamp = datetime.now()
        self.assertTrue(file1 == file2)

    def test_child(self):
        file_parent = ModelFile("parent", True)
        file_child1 = ModelFile("child1", True)
        file_child2 = ModelFile("child2", False)
        self.assertEqual(0, len(file_parent.get_children()))
        file_parent.add_child(file_child1)
        self.assertEqual([file_child1], file_parent.get_children())
        file_parent.add_child(file_child2)
        self.assertEqual([file_child1, file_child2], file_parent.get_children())

    def test_fail_add_child_to_nondir(self):
        file_parent = ModelFile("parent", False)
        file_child1 = ModelFile("child1", True)
        with self.assertRaises(TypeError) as context:
            file_parent.add_child(file_child1)
        self.assertTrue(str(context.exception).startswith("Cannot add child to a non-directory"))

    def test_fail_add_child_twice(self):
        file_parent = ModelFile("parent", True)
        file_parent.add_child(ModelFile("child1", True))
        file_parent.add_child(ModelFile("child2", True))
        with self.assertRaises(ValueError) as context:
            file_parent.add_child(ModelFile("child1", True))
        self.assertTrue(str(context.exception).startswith("Cannot add child more than once"))
        with self.assertRaises(ValueError) as context:
            file_parent.add_child(ModelFile("child2", True))
        self.assertTrue(str(context.exception).startswith("Cannot add child more than once"))

    def test_full_path(self):
        file_a = ModelFile("a", True)
        file_aa = ModelFile("aa", True)
        file_a.add_child(file_aa)
        file_aaa = ModelFile("aaa", True)
        file_aa.add_child(file_aaa)
        file_ab = ModelFile("ab", True)
        file_a.add_child(file_ab)
        self.assertEqual("a", file_a.full_path)
        self.assertEqual("a/aa", file_aa.full_path)
        self.assertEqual("a/aa/aaa", file_aaa.full_path)
        self.assertEqual("a/ab", file_ab.full_path)
