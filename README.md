# Code Prompter

Code Prompter is a Python tool designed to generate prompts for LLMs (Large Language Models) from complex, multi-file codebases.\
**Example output:**
````text
project/
    ├── LICENSE
    ├── README.md
    ├── code_prompter/
    │   ├── __init__.py
    │   ├── cli.py
    │   ├── config.py
    │   ├── default_config.py
    │   ├── main.py
    │   ├── summarizer.py
    │   └── utils.py
    │   [...]
    ├── install.bat
    ├── install.sh
    ├── requirements.txt
    └── setup.py
    [...]

[File Content]
# ./code_prompter/main.py
```
import sys
from code_prompter.cli import main_cli

def main():
    main_cli(sys.argv[1:])

if __name__ == "__main__":
    main()

```
````

## Background

As software projects grow in size and complexity, the structure of code becomes more distributed across multiple files, making it challenging to input the entire code into LLMs for assistance. While advanced AI IDEs can read entire codebases, they often require additional payment and do not support customized models.

This project provides a solution by summarizing the structure of a codebase into a concise, readable prompt format that can be used for LLMs. It offers a free, customizable alternative for those who want to input code into chatbots for coding assistance.


## Features

- Summarizes code directories into a structured prompt that can be used by any chatbot.
- Supports creating and using configuration files to customize the summarization process.
- Provides an easy-to-install package


## Installation

This project is developed under `Python 3.12`, though lower versions may also work.

### Steps:
1. Clone the repository from GitHub:
   ```bash
   git clone https://github.com/yourusername/code-prompter.git
   ```
2. Navigate to the project directory and run the install script.
    - For 
   Linux/macOS:
   ```bash
    bash ./install.sh
   ```
    - For Windows:
   ```bash
    .\install.bat
   ```

   The `.sh` file has been tested, but the `.bat` file **has not been tested** yet.

   The install script will:

   - Set up a Python virtual environment.
   -  Install required dependencies.
   -  Install the program as a package.

Make sure to **activate the virtual environment** before running any commands:
```bash
source venv/bin/activate  # Linux/macOS
```
```bash
venv\Scripts\activate     # Windows
```


## Usage

Once the program is installed and the virtual environment is activated, you can run the `code-prompter` command.

To summarize a codebase, navigate to the directory you want to summarize and run:

```bash
code-prompter summarize [options]
```
**Important:** Currently, the program will summarize the ./ directory by default, and does not support specifying a custom directory. 
**You should `cd` to the directory you want to summarize before running the command.**

### Options:
- `--output`: Specifies a file to write the summary output.
- `--clipboard`: Copies the output summary to the clipboard.

If the specified file (or clipboard) already contains content, the program will prompt the user to confirm overwriting.

## Configuration

The program creates a `.code_prompter_config` file the first time it runs, based on the contents in `default_config.py`. You can customize this configuration file to control which files or patterns to include or exclude from the summary.

Here’s an example config:

``` .code_prompter_config
default_level = TREE-ONLY

[IGNORE]
.*
__pycache__
venv
# Add patterns or files here

[FULL]
code_prompter/main.py
# Add patterns or files here

[TREE-ONLY]
LICENSE
README.md
# Add patterns or files here
```
### Config Customization:
- `default_level`: Specifies which level of detail to summarize by default (e.g., `TREE-ONLY`).
- `[IGNORE]`: Lists files and directories to ignore.
- `[FULL]`: Specifies files that should be included in full detail.
- `[TREE-ONLY]`: Specifies files to include in a simple tree structure.

You can modify the `default_config.py` file to adjust the default configuration. Any future `.code_prompter_config` files generated will inherit these modifications. Alternatively, you can manually edit the `.code_prompter_config` file.


## Future Plans

This project is still in the early stages and has limited features. Future development plans include:

- Developing an easy-to-use GUI for more convenient interaction.
- Allowing users to modify configuration more effectively via CLI.
- Adding a code summary function that shows only relevant code snippets based on AI prompts to improve the accuracy and effectiveness of the output prompt.


## License

This project is open source and is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0.txt).


## AI Declaration

This project was developed with the assistance of AI tools. AI technologies were used to help with various aspects of coding, including generating code snippets, writing documentation, and brainstorming features. The development of this project reflects a combination of human creativity and the capabilities of AI-driven tools.
