from textnode import *
from htmlnode import *
import os
import shutil
from funcs import *



dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_directory(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)



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