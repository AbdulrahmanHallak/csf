import os
import shutil
from pathlib import Path


def traverse(root: str, dest: str, ext: str):
    try:
        src_path = Path(root).resolve(True)
        dest_path = Path(dest).resolve(True)
    except OSError as err:
        print(err)

    def dfs(current_path: str):
        if current_path not in visited:

            # for preserving dir structure where files are found.
            relative_path = os.path.relpath(current_path, src_path)
            dest_dir = dest_path.joinpath(relative_path)
            files = [
                os.path.join(current_path, path)
                for path in os.listdir(current_path)
                if os.path.isfile(os.path.join(current_path, path)) and path.endswith(f'.{ext}')
            ]
            if files and not os.path.exists(dest_dir):
                dest_dir.mkdir(parents=True)

            for file in files:
                # Get the relative path of the file from the source root
                file_rel_path = os.path.relpath(file, src_path)
                # Copy the file to the destination preserving directory structure
                if file not in os.listdir(dest_path.joinpath(relative_path)):
                    shutil.copy(src=file, dst=dest_path.joinpath(file_rel_path), )

            visited.add(current_path)
            child_dirs = [
                os.path.join(current_path, path)
                for path in os.listdir(current_path)
                if os.path.isdir(os.path.join(current_path, path))
            ]
            for child in child_dirs:
                dfs(child)

    visited = set()
    dfs(root)


# Example usage:
traverse('/home/abdulrahman/repos', '/home/abdulrahman/test', 'png')

# def remove_empty_dirs(directory):
#     for root, dirs, files in os.walk(directory, topdown=False):
#         for dir_name in dirs:
#             dir_path = os.path.join(root, dir_name)
#             if not os.listdir(dir_path):
#                 print(f"Removing empty directory: {dir_path}")
#                 os.rmdir(dir_path)

# # Example usage:
# # remove_empty_dirs('/home/abdulrahman/test')
