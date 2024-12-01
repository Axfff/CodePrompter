from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from code_prompter import default_config


CONFIG_FILENAME = ".code_prompter_config"
DEFAULT_CONFIG = default_config.DEFAULT_CONFIG


def parse_config_file(config_path):
    config_data = {
        'default_level': 'TREE-ONLY',
        'IGNORE': [],
        'FULL': [],
        'TREE-ONLY': []
    }
    current_section = None

    with open(config_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Ignore comments and blank lines
            if not line or line.startswith(';') or line.startswith('#'):
                continue
            # Check for default_level
            if line.startswith('default_level'):
                key, value = line.split('=', 1)
                config_data['default_level'] = value.strip()
            # Check for section headers
            elif line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1].strip()
                if current_section not in ['IGNORE', 'FULL', 'TREE-ONLY']:
                    print(f"Warning: Unknown section '{current_section}' in config file.")
            # Read patterns under current section
            elif current_section:
                config_data[current_section].append(line)
            else:
                print(f"Warning: Line outside of any section: '{line}'")
    return config_data


def get_config_path():
    return Path.cwd() / CONFIG_FILENAME

def create_default_config():
    config_path = get_config_path()
    if not config_path.exists():
        config_path.write_text(DEFAULT_CONFIG)
        print(f"Created default config at {config_path}")
    else:
        print(f"Config file already exists at {config_path}")

def load_config():
    config_path = get_config_path()
    if not config_path.exists():
        create_default_config()
    config_data = parse_config_file(config_path)
    return config_data

def run_config_interface():
    conf = load_config()
    sections = conf.sections()
    print("Current Configuration:")
    for section in sections:
        print(f"[{section}]")
        for key in conf[section]:
            print(f"{key} = {conf[section][key]}")
        print()

    action = prompt("Do you want to (a)dd, (e)dit, or (d)elete a rule? (q to quit): ")
    while action.lower() != 'q':
        if action.lower() == 'a':
            add_rule(conf)
        elif action.lower() == 'e':
            edit_rule(conf)
        elif action.lower() == 'd':
            delete_rule(conf)
        else:
            print("Invalid option.")
        action = prompt("Do you want to (a)dd, (e)dit, or (d)elete a rule? (q to quit): ")

    # Save the updated config
    save_config(conf)

def add_rule(conf):
    sections = ['IGNORE', 'FULL', 'TREE-ONLY']
    section_completer = WordCompleter(sections)
    section = prompt("Select section to add a rule (IGNORE, FULL, TREE-ONLY): ", completer=section_completer)
    if section not in sections:
        print("Invalid section.")
        return
    rule = prompt("Enter the file/folder/pattern to add: ")
    if rule:
        conf.set(section, rule, '')
        print(f"Added rule '{rule}' to [{section}]")

def edit_rule(conf):
    print("Edit functionality is under development.")

def delete_rule(conf):
    print("Delete functionality is under development.")

def save_config(conf):
    config_path = get_config_path()
    with open(config_path, 'w') as configfile:
        conf.write(configfile)
    print(f"Configuration saved to {config_path}")

