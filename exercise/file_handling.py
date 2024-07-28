import os
import csv
import io

def read_file_safe(file_path):
    """
    Reads the content of a file from the provided path and returns the data.
    Handles exceptions and ensures platform-agnostic code.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        tuple: A tuple containing a status indicator and the content or error message.
               The first element is True if successful, False otherwise.
               The second element is the file content if successful, otherwise an error message.
    """
    try:
        # Get the absolute path relative to the script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(base_path, file_path)
        normalized_path = os.path.normpath(absolute_path)

        if not os.path.isfile(normalized_path):
            return (False, "Error: File does not exist.")

        with open(normalized_path, "r", encoding="utf-8") as file:
            data = file.read()
            return (True, data)

    except FileNotFoundError:
        return (False, "Error: File not found.")
    except IOError:
        return (False, "Error: An IOError occurred while reading the file.")
    except Exception as e:
        return (False, f"An unexpected error occurred: {e}")

if __name__ == "__main__":

    # Example usage
    file_path = "../data/Batting/ODI data.csv"  # This can be a relative path to the script's directory
    status, content = read_file_safe(file_path)

    if status:
        # Use io.StringIO to convert the string data to a file-like object
        csvfile = io.StringIO(content)
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            print(row)
    else:
        print("An error occurred:")
        print(content)
