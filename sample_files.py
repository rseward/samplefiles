#!/usr/bin/env python

import click
import os
import random
import shutil
import tqdm
import time

@click.command()
@click.argument("src_dir")
@click.argument("dst_dir")
@click.option("-n", "--num-files", default=100, help="Number of files to sample.")
def sample_files(src_dir, dst_dir, num_files):
    """
    Samples a specified number of files from a source directory and copies them
    to a destination directory, preserving the directory structure.
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    print(f"Analyzing source directory: {src_dir} ...")
    t1 = time.time()
    tlast = t1
    all_files = []
    for root, _, files in os.walk(src_dir):
        for file in files:
            all_files.append(os.path.join(root, file))
        t2 = time.time()

        if t2 - tlast > 15:
            print(f"- {len(all_files)} files processed in {t2 - t1:.2f} seconds.")
            tlast = t2

    print(f"- {len(all_files)} files processed in {t2 - t1:.2f} seconds.")

    sampled_files = random.sample(all_files, min(num_files, len(all_files)))

    print(f"Sampling {len(sampled_files)} files to destination directory: {dst_dir}...")
    for file_path in tqdm.tqdm(sampled_files):
        relative_path = os.path.relpath(file_path, src_dir)
        destination_path = os.path.join(dst_dir, relative_path)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy2(file_path, destination_path)

    print(f"Successfully sampled {len(sampled_files)} files.")

if __name__ == "__main__":
    sample_files()
