import shutil
from pathlib import Path


def traverse(root: str, dest: str, ext: str):
    try:
        src_path = Path(root).resolve(True)
        dst_path = Path(dest).resolve(True)
    except OSError as err:
        print(err)

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


traverse("/home/abdulrahman/repos/", "/home/abdulrahman/test", "png")
