import argparse
import shutil
from pathlib import Path
import sys


def traverse(src: Path, dst: Path, ext: Path):
    try:
        src_path = src.resolve(True)
        dst_path = dst.resolve(True)
    except OSError as err:
        print(err)
        sys.exit(1)

    def dfs(current_path: Path):
        if current_path not in visited:

            dst_dir = dst_path.joinpath(current_path.relative_to(src_path))
            files = [file for file in current_path.glob(f"*.{ext}")]
            if files:
                dst_dir.mkdir(parents=True, exist_ok=True)

            for file in files:
                dst_file = dst_path.joinpath(file.relative_to(src_path))
                if not dst_file.exists():
                    shutil.copy(src=file, dst=dst_file)

            visited.add(current_path)
            for child in current_path.iterdir():
                if child.is_dir():
                    dfs(child)

    visited = set()
    dfs(src_path)


def main():
    parser = argparse.ArgumentParser(
        description="Traverse directory and copy files with specific extension."
    )
    parser.add_argument("src", type=Path, help="Source directory path")
    parser.add_argument("dst", type=Path, help="Destination directory path")
    parser.add_argument("ext", type=str, help="Extension of files to copy")
    args = parser.parse_args()

    traverse(args.src, args.dst, args.ext)


if __name__ == "__main__":
    main()
