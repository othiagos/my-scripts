import os
import re
import sys
import hashlib


def is_image(file):
    _, ext = os.path.splitext(file)
    extension = {'.jpg', '.jpeg', '.png'}
    return ext in extension


def generate_sha256_hash(file):
    sha256 = hashlib.sha256()

    with open(file, 'rb') as f:
        for block in iter(lambda: f.read(4096), b''):
            sha256.update(block)

    return sha256.hexdigest()


def is_folder(path):
    return os.path.isdir(path)


def is_new_name_available(new_file_path):
    return not os.path.isfile(new_file_path)


def is_hash(file_name):
    return re.match(r'^[a-fA-F0-9]{64}$', file_name) is not None


def rename_with_hash(directory, file):
    old_file_path = os.path.join(directory, file)
    file_name, extension = os.path.splitext(file)

    if is_hash(file_name):
        # print(f'File {file} is already a hash. Skipping')
        return

    hash_value = generate_sha256_hash(old_file_path)
    new_name = hash_value + extension
    new_file_path = os.path.join(directory, new_name)

    if is_new_name_available(new_file_path):
        os.rename(old_file_path, new_file_path)
        print(f'File renamed from {file} to {new_name}')
    else:
        print(f'File with the name {new_name} already exists. Skipping the renaming of file {file}')


def rename_image_to_hash(directory):
    if not is_folder(directory):
        print(f'The directory {directory} does not exist')
        return

    for file in os.listdir(directory):
        if not is_image(file):
            continue

        try:
            rename_with_hash(directory, file)
        except Exception as err:
            print(f'File named {file} could not be renamed:', err)


def main():
    if len(sys.argv) < 2:
        print('No directory specified')
        return

    target_dir = sys.argv[1]
    rename_image_to_hash(target_dir)


if __name__ == '__main__':
    main()
