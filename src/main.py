import os
import shutil

from htmlnode import generate_page, recurse_generate_pages
from textnode import TextNode, TextType


def main():
    cwd = os.getcwd()
    if not os.path.exists(os.path.relpath("static")):
        os.mkdir("static")
    if not os.path.exists(os.path.relpath("public")):
        os.mkdir("public")

    dst = os.path.relpath(os.path.join(cwd, "public"))
    src = os.path.relpath(os.path.join(cwd, "static"))

    if len(os.listdir(dst)) > 0 or not os.path.exists(dst):
        print("public directory is not empty deleting tree and remaking directory.")
        shutil.rmtree(dst)
        os.mkdir(dst)

    recurse_static_to_public(src, dst)

    from_path = "content/"
    to_path = "public/"
    template_path = "template.html"

    recurse_generate_pages(from_path, template_path, to_path)


def recurse_static_to_public(src, dst):
    items = os.listdir(src)

    for item in items:
        from_path = os.path.join(src, item)
        to_path = os.path.join(dst, item)
        print(f"Current Working Item: {from_path}")
        if os.path.isfile(from_path):
            print(f"{from_path} is a file, copying to {dst}")
            shutil.copy(from_path, dst)
        else:
            print(f"{from_path} is a dir, creating {to_path} and recursing.")
            if not os.path.exists(to_path):
                os.mkdir(to_path)

            recurse_static_to_public(from_path, to_path)


main()
