# CLI entry point.

from cli.log_input import get_log_input
from cli.report_runner import analyze_and_show


def main():
    """
        Get a valid log from the user and analyze it.
    """
    log = get_log_input()
    analyze_and_show(log)


if __name__ == "__main__":
    main()