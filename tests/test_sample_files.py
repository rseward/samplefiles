import os
import shutil
import unittest
from click.testing import CliRunner

from sample_files import sample_files

class TestSampleFiles(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.src_dir = "test_src"
        self.dst_dir = "test_dst"
        os.makedirs(self.src_dir, exist_ok=True)
        # Create some dummy files and directories
        os.makedirs(os.path.join(self.src_dir, "dir1"), exist_ok=True)
        with open(os.path.join(self.src_dir, "file1.txt"), "w") as f:
            f.write("file1")
        with open(os.path.join(self.src_dir, "dir1", "file2.txt"), "w") as f:
            f.write("file2")

    def tearDown(self):
        if os.path.exists(self.src_dir):
            shutil.rmtree(self.src_dir)
        if os.path.exists(self.dst_dir):
            shutil.rmtree(self.dst_dir)

    def test_sample_files_creates_dst_dir(self):
        result = self.runner.invoke(sample_files, [self.src_dir, self.dst_dir, "--num-files", "1"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.exists(self.dst_dir))

    def test_sample_files_correct_number_of_files(self):
        result = self.runner.invoke(sample_files, [self.src_dir, self.dst_dir, "--num-files", "1"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(os.listdir(self.dst_dir)), 1)

    def test_sample_files_preserves_structure(self):
        # Create a file in a subdirectory
        os.makedirs(os.path.join(self.src_dir, "dir2"))
        with open(os.path.join(self.src_dir, "dir2", "file3.txt"), "w") as f:
            f.write("file3")

        # Run the script to sample all files
        result = self.runner.invoke(sample_files, [self.src_dir, self.dst_dir, "--num-files", "3"])
        self.assertEqual(result.exit_code, 0)

        # Check if the directory structure is preserved
        self.assertTrue(os.path.exists(os.path.join(self.dst_dir, "dir1")))
        self.assertTrue(os.path.exists(os.path.join(self.dst_dir, "dir2")))
        self.assertTrue(os.path.exists(os.path.join(self.dst_dir, "file1.txt")) or \
                        os.path.exists(os.path.join(self.dst_dir, "dir1", "file2.txt")) or \
                        os.path.exists(os.path.join(self.dst_dir, "dir2", "file3.txt")))


    def test_sample_more_files_than_exist(self):
        result = self.runner.invoke(sample_files, [self.src_dir, self.dst_dir, "--num-files", "10"])
        self.assertEqual(result.exit_code, 0)
        # Check that all files were copied
        num_files_in_dst = 0
        for _, _, files in os.walk(self.dst_dir):
            num_files_in_dst += len(files)
        self.assertEqual(num_files_in_dst, 2)


    def test_empty_src_directory(self):
        # Create a new empty source directory
        empty_src_dir = "empty_src"
        os.makedirs(empty_src_dir)
        result = self.runner.invoke(sample_files, [empty_src_dir, self.dst_dir, "--num-files", "10"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.exists(self.dst_dir))
        self.assertEqual(len(os.listdir(self.dst_dir)), 0)
        shutil.rmtree(empty_src_dir)

if __name__ == "__main__":
    unittest.main()
