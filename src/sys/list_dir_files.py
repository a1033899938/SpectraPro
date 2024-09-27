import os


def list_dir_files(dir_path, filters=None):
    if filters is None:
        filters = []
    files = [
        f for f in os.listdir(dir_path)
        if not any(f.endswith(ext) for ext in filters)
    ]
    return files


if __name__ == '__main__':
    dir_path = r'D:\GitProject\SpectraPro\tests\pass'
    filters = ['.txt', '.png']
    files = list_dir_files(dir_path, filters)
    print(files)