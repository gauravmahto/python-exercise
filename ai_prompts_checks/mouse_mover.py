import time
import pyautogui
from pathlib import Path

# Constants
DEFAULT_INTERVAL = 60  # Default interval in seconds
MIN_INTERVAL = 1       # Minimum allowed interval in seconds
MAX_INTERVAL = 3600    # Maximum allowed interval in seconds

# Load MOVE_INTERVAL from .env file
def load_env():
    """
    Reads the MOVE_INTERVAL value from a .env file.
    If the file or the variable is not found, it defaults to 60 seconds.
    """
    env_file = Path('.env')

    # Check if .env file exists
    if not env_file.exists():
        print(".env file not found. Using default interval of 60 seconds.")
        return DEFAULT_INTERVAL

    # Attempt to read and extract the MOVE_INTERVAL value
    try:
        with env_file.open('r') as file:
            for line in file:
                if line.startswith('MOVE_INTERVAL'):
                    _, value = line.strip().split('=')
                    return int(value)
    except (ValueError, FileNotFoundError):
        print("Error reading .env file or invalid format. Using default interval of 60 seconds.")
    
    return DEFAULT_INTERVAL

# Validate interval value
def validate_interval(interval):
    """
    Validates that the interval is an integer and within the allowed range.
    If invalid, defaults to 60 seconds.
    """
    if not isinstance(interval, int) or not (MIN_INTERVAL <= interval <= MAX_INTERVAL):
        print(f"Invalid MOVE_INTERVAL value. Must be between {MIN_INTERVAL} and {MAX_INTERVAL}. Using default interval of 60 seconds.")
        return DEFAULT_INTERVAL
    return interval

# Move the mouse cursor by 1 pixel
def move_cursor():
    """
    Moves the mouse cursor 1 pixel to the right from its current position.
    """
    x, y = pyautogui.position()  # Get the current cursor position
    pyautogui.moveTo(x + 1, y)   # Move the cursor 1 pixel to the right

def main():
    """
    Main function to load and validate the interval, and move the mouse cursor
    at the specified interval.
    """
    # Load and validate the interval
    interval = load_env()
    interval = validate_interval(interval)
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
