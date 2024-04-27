import os
import shutil
from copystatic import copy_files_recursive

static_path = "./static"
public_path = "./public"

def main():
    print("Deleting public directory...", end="")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    print("complete")

    print("Copying files from static to public directory...")
    copy_files_recursive(static_path, public_path)


if __name__ == "__main__":
    main()