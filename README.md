# Sample Files Utility

## Description

This utility samples a specified number of files from a source directory and copies them to a destination directory, preserving the directory structure. This is useful for creating a smaller subset of a large dataset for testing or analysis.

## Usage

```bash
python sample_files.py <src_dir> <dst_dir> [--num-files <num_files>]
```

### Arguments

- `src_dir`: The source directory to sample files from.
- `dst_dir`: The destination directory to copy the sampled files to.
- `--num-files`: The number of files to sample. Defaults to 100.

### Example

```bash
python sample_files.py /path/to/source /path/to/destination --num-files 500
```

This will sample 500 files from `/path/to/source` and copy them to `/path/to/destination`, preserving the directory structure.

## Design

The utility is written in Python and uses the `click` module to parse command-line arguments. It walks through the source directory to get a list of all files, then uses the `random.sample()` function to select a random subset of those files. Finally, it copies the selected files to the destination directory, creating the necessary subdirectories to preserve the original structure.
