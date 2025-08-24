
import click
import os
import random
import shutil

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

    all_files = []
    for root, _, files in os.walk(src_dir):
        for file in files:
            all_files.append(os.path.join(root, file))

    sampled_files = random.sample(all_files, min(num_files, len(all_files)))

    for file_path in sampled_files:
        relative_path = os.path.relpath(file_path, src_dir)
        destination_path = os.path.join(dst_dir, relative_path)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy2(file_path, destination_path)

    print(f"Successfully sampled {len(sampled_files)} files.")

if __name__ == "__main__":
    sample_files()
