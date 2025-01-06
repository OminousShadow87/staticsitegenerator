from textnode import *
import os
import shutil


def main():
    public_dir = "/home/breeze/workspace/github.com/breeze/staticsitegenerator/public"
    static_dir = "/home/breeze/workspace/github.com/breeze/staticsitegenerator/static"
    copy_directory(static_dir, public_dir)

def copy_directory(current_dir, destination_dir):
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.mkdir(destination_dir)
    dir_list = os.listdir(current_dir)
    for item in dir_list:
        current_path = os.path.join(current_dir, item)
        destination_path = os.path.join(destination_dir, item)
        if os.path.isfile(current_path):
            shutil.copy(current_path, destination_path)
        elif os.path.isdir(current_path):
            copy_directory(current_path, destination_path)     

if __name__ == "__main__":
    main()