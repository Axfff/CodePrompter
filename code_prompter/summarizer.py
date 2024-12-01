import os
from pathlib import Path
from code_prompter import config
import fnmatch
import pyperclip


class TreeNode:
    def __init__(self, name, path, inclusion_level, parent=None):
        self.name = name
        self.path = path
        self.inclusion_level = inclusion_level
        self.children = []
        self.is_dir = os.path.isdir(path)
        self.parent = parent


def check_clipboard_content(new_content):
    try:
        current_content = pyperclip.paste()
        return current_content != new_content
    except Exception as e:
        print(f"Error reading clipboard: {e}")
        return False


def check_file_content(file_path, new_content):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            current_content = f.read()
            return current_content != new_content
    return True  # If file doesn't exist, it's safe to write


def confirm_overwrite(is_clipboard=False, file_path=None):
    if is_clipboard:
        response = input("Clipboard already has content. Do you want to overwrite it? (y/n): ")
    elif file_path:
        response = input(f"{file_path} already has content. Do you want to overwrite it? (y/n): ")
    else:
        return True  # If no content to check, assume overwrite is okay

    return response.lower() == 'y'


def summarize(output_path=None, to_clipboard=False):
    conf = config.load_config()
    default_level = conf.get('default_level', 'TREE-ONLY')

    ignore_patterns = conf.get('IGNORE', [])
    full_patterns = conf.get('FULL', [])
    tree_only_patterns = conf.get('TREE-ONLY', [])

    root_path = '.'
    root_node = TreeNode('project', root_path, default_level)

    build_tree(root_node, ignore_patterns, full_patterns, tree_only_patterns, default_level)

    # Prepare summary
    summary = get_summary(root_node)

    # Handle clipboard
    if to_clipboard:
        if check_clipboard_content(summary):
            if confirm_overwrite(is_clipboard=True):
                pyperclip.copy(summary)
                print("Summary copied to clipboard.")
            else:
                print("Clipboard content was not overwritten.")
        else:
            pyperclip.copy(summary)
            print("Summary copied to clipboard.")

    # Handle file output
    elif output_path:
        if check_file_content(output_path, summary):
            if confirm_overwrite(file_path=output_path):
                with open(output_path, 'w') as f:
                    f.write(summary)
                print(f"Summary written to {output_path}")
            else:
                print("File content was not overwritten.")
        else:
            with open(output_path, 'w') as f:
                f.write(summary)
            print(f"Summary written to {output_path}")

    # Default case, print summary
    else:
        print(summary)


def get_summary(node):
    # Recursively generate the summary
    summary = ""
    summary += print_directory_tree(node, return_summary=True)
    summary += print_file_contents(node, return_summary=True)
    return summary


def build_tree(node, ignore_patterns, full_patterns, tree_only_patterns, default_level):
    if not node.is_dir:
        return

    try:
        entries = os.listdir(node.path)
    except PermissionError:
        print(f"Permission denied: {node.path}")
        return

    entries.sort()  # Optional: sort entries for consistent output

    for entry in entries:
        entry_path = os.path.join(node.path, entry)
        relative_path = os.path.relpath(entry_path, '.')

        # Normalize path
        relative_path = relative_path.replace(os.sep, '/')

        # Check if ignored
        if is_ignored(relative_path, ignore_patterns):
            continue

        # Determine inclusion level
        inclusion_level = get_inclusion_level(relative_path, full_patterns, tree_only_patterns, default_level)

        child_node = TreeNode(entry, entry_path, inclusion_level, parent=node)
        node.children.append(child_node)

        # Recursively build tree
        build_tree(child_node, ignore_patterns, full_patterns, tree_only_patterns, default_level)


def is_ignored(path, ignore_patterns):
    for pattern in ignore_patterns:
        if match_pattern(path, pattern):
            return True
    return False


def get_inclusion_level(path, full_patterns, tree_only_patterns, default_level):
    # Highest priority: FULL
    for pattern in full_patterns:
        if match_pattern(path, pattern):
            return 'FULL'
    # Next priority: TREE-ONLY
    for pattern in tree_only_patterns:
        if match_pattern(path, pattern):
            return 'TREE-ONLY'
    # Default level
    return default_level


def match_pattern(path, pattern):
    # Normalize paths
    path = path.replace(os.sep, '/')
    if path.startswith('./'):
        path = path[2:]
    # Handle patterns ending with '/' to match directories
    if pattern.endswith('/'):
        if os.path.isdir(path) and fnmatch.fnmatch(path + '/', pattern):
            return True
    else:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def print_directory_tree(node, prefix='', return_summary=False):
    summary = ""
    if prefix == '':
        # Root node
        summary += f"{node.name}/\n"
    else:
        branch = '└── ' if is_last_sibling(node) else '├── '
        summary += f"{prefix}{branch}{node.name}{'/' if node.is_dir else ''}\n"

    # Prepare the prefix for child nodes
    new_prefix = prefix + ('    ' if is_last_sibling(node) else '│   ')

    # Handle special cases for directories
    if node.is_dir:
        if not node.children:
            # Empty folder
            summary += f"{new_prefix}[Empty]\n"
        else:
            for child in node.children:
                summary += print_directory_tree(child, new_prefix, return_summary)
            # Check if there are ignored contents
            if has_ignored_content(node.path):
                summary += f"{new_prefix}[...]\n"

    if return_summary:
        return summary
    else:
        print(summary)


def has_ignored_content(path):
    try:
        all_entries = os.listdir(path)
        return len(all_entries) > 0
    except PermissionError:
        return False


def is_last_sibling(node):
    if not node.parent:
        return True
    return node.parent.children.index(node) == len(node.parent.children) - 1


def collect_file_contents(node, file_contents):
    if node.inclusion_level == 'FULL' and not node.is_dir:
        content = read_file_content(node.path)
        if content is not None:
            file_contents.append((node.path, content))
    for child in node.children:
        collect_file_contents(child, file_contents)


def print_file_contents(root_node, return_summary=False):
    file_contents = []
    collect_file_contents(root_node, file_contents)
    summary = ""
    if file_contents:
        summary += "\n[File Content]\n"
        for file_path, content in file_contents:
            summary += f"# {file_path}\n```\n"
            summary += content
            summary += "\n```\n"

    if return_summary:
        return summary
    else:
        print(summary)


def read_file_content(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        return None



