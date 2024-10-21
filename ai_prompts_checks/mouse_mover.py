import time
import pyautogui
from pathlib import Path

# Constants
DEFAULT_INTERVAL = 60  # Default interval in seconds
MIN_INTERVAL = 1  # Minimum allowed interval in seconds
MAX_INTERVAL = 3600  # Maximum allowed interval in seconds

# Constants
DEFAULT_INTERVAL = 60  # Default interval in seconds


def load_env():
    """
    Reads the MOVE_INTERVAL value from a .env file.
    If the file or the variable is not found, it defaults to 60 seconds.
    Only reads lines starting with 'MOVE_INTERVAL=' to ensure correct parsing.
    """
    env_file = Path(".env")

    # Check if .env file exists
    if not env_file.exists():
        print(".env file not found. Using default interval of 60 seconds.")
        return DEFAULT_INTERVAL

    try:
        # Read the .env file line by line
        with env_file.open("r") as file:
            return parse_move_interval(file)
    except FileNotFoundError:
        print(".env file not found. Using default interval of 60 seconds.")
    except Exception as e:
        print(f"Error reading .env file: {e}. Using default interval of 60 seconds.")

    return DEFAULT_INTERVAL


def parse_move_interval(file):
    """
    Parses the MOVE_INTERVAL value from the file.
    Returns the interval if found and valid; otherwise, returns the default.
    """
    for line in file:
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        # Match only the exact key 'MOVE_INTERVAL'
        if line.startswith("MOVE_INTERVAL="):
            key, value = line.split("=", 1)
            if key.strip() == "MOVE_INTERVAL":
                return convert_to_int(value.strip())

    return DEFAULT_INTERVAL


def convert_to_int(value):
    """
    Converts the given value to an integer.
    Returns the default interval if conversion fails.
    """
    try:
        return int(value)
    except ValueError:
        print(
            "Invalid MOVE_INTERVAL value in .env file. Using default interval of 60 seconds."
        )
        return DEFAULT_INTERVAL


# Validate interval value
def validate_interval(interval):
    """
    Validates that the interval is within the allowed range.
    If invalid, defaults to 60 seconds.
    """
    try:
        interval = int(interval)
    except ValueError:
        print(
            f"Invalid MOVE_INTERVAL value. Must be an integer. Using default interval of {DEFAULT_INTERVAL} seconds."
        )
        return DEFAULT_INTERVAL

    if not (MIN_INTERVAL <= interval <= MAX_INTERVAL):
        print(
            f"Invalid MOVE_INTERVAL value. Must be between {MIN_INTERVAL} and {MAX_INTERVAL}. Using default interval of {DEFAULT_INTERVAL} seconds."
        )
        return DEFAULT_INTERVAL

    return interval


# Move the mouse cursor by 1 pixel
def move_cursor():
    """
    Moves the mouse cursor 1 pixel to the right from its current position.
    """
    x, y = pyautogui.position()  # Get the current cursor position
    screen_width, _ = pyautogui.size()

    # Ensure the cursor doesn't move outside the screen boundaries
    if x + 1 < screen_width:
        pyautogui.moveTo(x + 1, y)
    else:
        print("Cursor is at the right edge of the screen.")


def main():
    """
    Main function to load and validate the interval, and move the mouse cursor
    at the specified interval.
    """
    # Load and validate the interval
    interval = validate_interval(load_env())
    print(f"Mouse cursor will move every {interval} seconds.")

    try:
        # Infinite loop to move the mouse cursor at each interval
        while True:
            move_cursor()
            time.sleep(interval)

    except KeyboardInterrupt:
        # Handle user interruption (Ctrl+C)
        print("\nProgram terminated by user.")
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
