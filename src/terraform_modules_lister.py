#!/usr/bin/env python3
import os
import re
from typing import List


def list_modules(find_dir: str) -> List[str]:
    modules = []
    for root, dirs, files in os.walk(find_dir):
        if any(os.path.splitext(f)[1] == ".tf" for f in files):
            modules.append(root)
    return modules


def find_name(modules: List[str]) -> List[str]:
    names = []
    for module_path in modules:
        readme_path = os.path.join(module_path, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r") as handle:
                content = handle.read()
                if name := re.search(r"\# *(.+)\n", content, re.IGNORECASE):
                    names.append(name.group(1).strip())
                    continue
        names.append(os.path.basename(os.path.normpath(module_path)))
    return names


def markdown(modules: List[str], names: List[str]) -> str:
    content = ""
    module_tuple = list(zip(modules, names))
    module_tuple.sort(key=lambda tup: tup[1].lower())
    for module_path, name in module_tuple:
        content += f"- [{name}]({module_path})\n"
    return content


def replace_markdown(output_file: str, modules_content: str, tag_suffix: str):
    with open(output_file, "r+") as handle:
        original_content = handle.read()
        new_content = re.sub(
            f'(?s)<!--(?: *)BEGIN_TF_{tag_suffix}(?: *)-->.*<!--(?: *)END_TF_{tag_suffix}(?: *)-->',
            f"<!-- BEGIN_TF_{tag_suffix} -->\n{modules_content}<!-- END_TF_{tag_suffix} -->",
            original_content,
            flags=re.IGNORECASE | re.MULTILINE
        )
        handle.seek(0)
        handle.write(new_content)


def main(output_file: str, find_dir: str, tag_suffix: str):
    modules = list_modules(find_dir)
    modules_name = find_name(modules)
    content = markdown(modules, modules_name)
    replace_markdown(output_file, content, tag_suffix)


if __name__ == "__main__":
    output_file = os.environ["OUTPUT_FILE"]
    find_dir = os.environ["FIND_DIR"]
    tag_suffix = os.environ["TAG_SUFFIX"]
    main(output_file, find_dir, tag_suffix)
