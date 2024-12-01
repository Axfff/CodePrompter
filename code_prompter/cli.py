import argparse
from code_prompter import summarizer, config

def main_cli(args=None):
    parser = argparse.ArgumentParser(
        description="Code Prompter: Summarize project directories for LLMs"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Summarize command
    summarize_parser = subparsers.add_parser("summarize", help="Summarize the project directory")
    summarize_parser.add_argument("--output", help="file path to store output")
    summarize_parser.add_argument("--clipboard", action="store_true", help="Copy the summary to clipboard")

    # TODO: Config command
    config_parser = subparsers.add_parser("config", help="Configure Code Prompter")

    # TODO: GUI command (placeholder)
    gui_parser = subparsers.add_parser("gui", help="Launch the GUI (future development)")

    args = parser.parse_args(args)

    if args.command == "summarize":
        summarizer.summarize(output_path=args.output, to_clipboard=args.clipboard)
    elif args.command == "config":
        config.run_config_interface()
    elif args.command == "gui":
        print("GUI functionality is under development.")

