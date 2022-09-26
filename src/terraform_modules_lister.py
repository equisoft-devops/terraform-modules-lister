#!/usr/bin/env python3
import os
import re
from typing import List


def list_modules(find_dir: str) -> List[str]:
    modules = []
    for f in os.listdir(find_dir):
        f_path = os.path.join(find_dir, f)
        if os.path.isdir(f_path) and any(
            [sub_module_file for sub_module_file in os.listdir(f_path) if os.path.splitext(sub_module_file)[1] == ".tf"]
        ):
            modules.append(f_path)
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


def replace_markdown(output_file: str, modules_content: str):
    with open(output_file, "r+") as handle:
        original_content = handle.read()
        new_content = re.sub(
            '(?s)<!-- BEGIN_TF_MODULES -->.*<!-- END_TF_MODULES -->',
            f"<!-- BEGIN_TF_MODULES -->\n{modules_content}<!-- END_TF_MODULES -->",
            original_content,
            re.IGNORECASE | re.MULTILINE
        )
        handle.seek(0)
        handle.write(new_content)


def main(output_file: str, find_dir: str):
    modules = list_modules(find_dir)
    modules_name = find_name(modules)
    content = markdown(modules, modules_name)
    replace_markdown(output_file, content)


if __name__ == "__main__":
    output_file = os.environ["OUTPUT_FILE"]
    find_dir = os.environ["FIND_DIR"]
    main(output_file, find_dir)
