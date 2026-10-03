# Asks the user for a system log and keeps asking until log is valid.

from validations.input_validation import validate_log


def get_log_input():
    """
        Ask for a system log until a valid one is entered, then return it.
    """
    log = input("Enter system log: ").strip()

    while True:
        validation = validate_log(log)
        if validation["log_valid"]:
            break
        print(f"Invalid log: {validation['log_reason']}")
        log = input("Enter system log: ").strip()

    return log