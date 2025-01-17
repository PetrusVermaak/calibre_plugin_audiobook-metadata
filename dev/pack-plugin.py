import os
import zipfile


def zipdir(path, ziph):
    """
    Zip the contents of an entire directory (including subdirectories).

    :param path: Path of the directory to zip.
    :param ziph: ZipFile handle.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            ziph.write(filepath, os.path.relpath(filepath, os.path.dirname(path)))

def create_zip(zip_filename, paths):
    """
    Create a zip archive containing the files and directories in paths.

    :param zip_filename: Name of the zip file to create.
    :param paths: List of filenames and directory paths to include in the zip archive.
    """
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in paths:
            if os.path.isfile(path):
                zipf.write(path, os.path.basename(path))
            elif os.path.isdir(path):
                zipdir(path, zipf)
            else:
                print(f"Path {path} does not exist and will be skipped.")
    print(f"Created zip file {zip_filename} containing {len(paths)} items.")


files_to_zip = ['../tinytag', '../__init__.py', '../plugin-import-name-audiobook_metadata.txt']
zip_filename = 'audiobook_metadata_0.1.1.zip'

create_zip(zip_filename, files_to_zip)
