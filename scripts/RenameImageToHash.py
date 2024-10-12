import hashlib
import os
import re
import sys
from enum import StrEnum

import cv2 as cv
from numpy import ndarray


class ImageFormat(StrEnum):
    PNG: str = ".png"
    JPG: str = ".jpg"
    WEBP: str = ".webp"
    JPEG: str = ".jpeg"


class ValidExtension(StrEnum):
    PNG: str = ImageFormat.PNG
    JPG: str = ImageFormat.JPG


class ConvertExtension(StrEnum):
    WEBP: str = ImageFormat.WEBP
    JPEG: str = ImageFormat.JPEG


def convert_format(directory: str, image_name: str, new_format: ValidExtension) -> str:
    file_name: str
    file_name, _ = split_file(image_name)
    new_name: str = file_name + new_format
    read_image_path: str = os.path.join(directory, image_name)
    write_image_path: str = os.path.join(directory, new_name)

    img: ndarray = cv.imread(read_image_path)

    cv.imwrite(write_image_path, img)
    os.remove(read_image_path)

    print(f"Change the format of image {image_name} to format {new_format}")
    return new_name


def convert_image(directory: str, path: str) -> str:
    format_conversion: dict[ConvertExtension, ValidExtension] = {
        ConvertExtension.WEBP: ValidExtension.PNG,
        ConvertExtension.JPEG: ValidExtension.JPG,
    }

    ext: str
    _, ext = split_file(path)
    new_format: ValidExtension = format_conversion[ext]

    return convert_format(directory, path, new_format)


def is_image(file: str) -> bool:
    ext: str
    _, ext = split_file(file)
    return any([ext == format for format in ImageFormat])


def is_valid_format(file: str) -> bool:
    ext: str
    _, ext = split_file(file)
    return any([ext == format for format in ValidExtension])


def generate_sha256_hash(file: str) -> str:
    sha256: hashlib.HASH = hashlib.sha256()

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
            if not is_valid_format(file):
                file = convert_image(directory, file)

            rename_with_hash(directory, file)
        except Exception as err:
            print(f"File named {file} could not be renamed:", err)


def parse(image_directory: str) -> str:
    if not os.path.isdir(image_directory):
        raise RuntimeError('Cannot find image directory')
    
    return image_directory


def main() -> None:
    if len(sys.argv) < 2:
        print("No directory specified")
        return
    
    try: 
        target_dir: str = parse(sys.argv[1])
        rename_image_to_hash(target_dir)
    except RuntimeError as err:
        print(err)


if __name__ == "__main__":
    main()
