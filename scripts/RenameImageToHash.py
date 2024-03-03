from hashlib import _Hash as Hash
import os
import re
import sys
import hashlib


def is_image(file: str) -> bool:
    ext: str
    _, ext = os.path.splitext(file)
    extension: set[str] = {".jpg", ".jpeg", ".png"}
    return ext in extension


def generate_sha256_hash(file: str) -> str:
    sha256: Hash = hashlib.sha256()

    with open(file, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()


def is_folder(path: str) -> bool:
    return os.path.isdir(path)


def is_new_name_available(new_file_path: str) -> bool:
    return not os.path.isfile(new_file_path)


def is_hash(file_name: str) -> bool:
    return re.match(r"^[a-fA-F0-9]{64}$", file_name) is not None


def split_file(file_name: str) -> tuple[str, str]:
    return os.path.splitext(file_name)


def rename_with_hash(directory: str, file: str) -> None:
    old_file_path: str = os.path.join(directory, file)

    file_name: str
    extension: str
    file_name, extension = split_file(file)

    if is_hash(file_name):
        # print(f"File {file} is already a hash. Skipping")
        return

    hash_value: str = generate_sha256_hash(old_file_path)
    new_name: str = hash_value + extension
    new_file_path: str = os.path.join(directory, new_name)

    if is_new_name_available(new_file_path):
        os.rename(old_file_path, new_file_path)
        print(f"File renamed from {file} to {new_name}")
    else:
        print(f"File with the name {new_name} already exists. Skipping the renaming of file {file}")


def rename_image_to_hash(directory: str) -> None:
    if not is_folder(directory):
        print(f"The directory {directory} does not exist")
        return

    for file in os.listdir(directory):
        if not is_image(file):
            continue

        try:
            rename_with_hash(directory, file)
        except Exception as err:
            print(f"File named {file} could not be renamed:", err)


def main() -> None:
    if len(sys.argv) < 2:
        print("No directory specified")
        return

    target_dir = sys.argv[1]
    rename_image_to_hash(target_dir)


if __name__ == "__main__":
    main()
