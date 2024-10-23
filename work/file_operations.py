import csv
from dataclasses import dataclass, asdict, fields
import json
from os.path import join
from pathlib import Path
from typing import List, Tuple, TypedDict

# Define the filename and path for the CSV and JSON files
filename = join("data", "persons.ignore.csv")

# Modern Python way
data_dir = Path("data")
filename_json = data_dir / "persons.ignore.json"

# Ensure the directory exists
data_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class Person:
    """
    A dataclass representing a person with name, age, and city.
    """

    name: str
    age: int
    city: str

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the Person instance.

        :return: A string representation of the Person instance.
        """
        return f"name='{self.name}', age={self.age}, city='{self.city}'"

    def __repr__(self) -> str:
        """
        Returns an unambiguous string representation of the Person instance.

        :return: A string that can be used to recreate the Person instance.
        """
        return f"Person(name={repr(self.name)}, age={self.age}, city={repr(self.city)})"

    def serialize(self) -> "PersonDict":
        """
        Serialize the Person instance to a dictionary.

        :return: A dictionary representing the Person instance.
        """
        return asdict(self)

    @staticmethod
    def deserialize(data: "PersonDict") -> "Person":
        """
        Deserialize a dictionary to a Person instance, with type conversion if necessary.

        :param data: A dictionary with keys matching the Person fields.
        :return: A Person instance.
        """
        # Convert age to int, since it might be a string if read from sources like JSON or CSV
        name = data["name"]
        age = int(data["age"])  # Ensure 'age' is an integer
        city = data["city"]

        return Person(name=name, age=age, city=city)


# Instead of using a TypedDict dataclass, we can use a Dynamically created TypedDict below
# class PersonDict(TypedDict):
#     name: str
#     age: int
#     city: str


# Dynamically create the TypedDict based on the Person dataclass
def create_typed_dict_from_dataclass(cls):
    """
    Dynamically creates a TypedDict based on a dataclass.

    :param cls: The dataclass to convert.
    :return: A dynamically created TypedDict class.
    """
    annotations = {field.name: field.type for field in fields(cls)}
    return TypedDict(f"{cls.__name__}Dict", annotations, total=True)


# Create the PersonDict dynamically
PersonDict = create_typed_dict_from_dataclass(Person)


class FileOperations:

    def __init__(self):
        pass

    def read_count_lines_words(self, filename: str) -> Tuple[int, int]:
        """
        Reads a file and returns the number of lines and words.

        :param filename (str): The name of the file to read.

        :return Tuple[int, int]: A tuple containing the number of lines and words.
        """
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                num_lines = len(lines)
                num_words = sum(len(line.split()) for line in lines)

                return num_lines, num_words
        except FileNotFoundError:
            print("File not found.")
            return 0, 0
        except PermissionError:
            print("Permission denied.")
            return 0, 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0, 0

    def read(self, filename: str) -> str:
        """
        Reads a file and returns the data as a string.

        Args:
            filename (str): The name of the file to read.

        Returns:
            str: A string containing the data from the file.
        """

        try:
            with open(filename, "r") as file:
                data = file.read()
                return data
        except FileNotFoundError:
            print("File not found.")
            return ""
        except PermissionError:
            print("Permission denied.")
            return ""
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

    def read_csv(self, filename: str) -> List[Person]:
        """
        Reads a CSV file and returns the data as a list of Person instances.

        :param filename (str): The name of the file to read.

        :return List[Person]: A list of Person instances.
        """
        persons: List[Person] = []

        try:
            with open(filename, "r") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    try:
                        person = Person.deserialize(row)
                        persons.append(person)
                    except KeyError as e:
                        key_name = e.args[0]
                        print(
                            f"Missing key: '{key_name}' in row {row}. Using default value."
                        )

                        # Handle missing 'age' key specifically
                        if key_name == "age":
                            person = Person(
                                name=row.get("name", "Unknown"),
                                age=0,
                                city=row.get("city", "Unknown"),
                            )
                            persons.append(person)
                        else:
                            print(f"Skipping row due to missing key: '{key_name}'.")

                    except ValueError as e:
                        # Capture invalid value scenarios
                        invalid_key = None
                        for key, value in row.items():
                            try:
                                # Assuming the expected value types:
                                # 'name' as str, 'age' as int, 'city' as str
                                if key == "age":
                                    int(value)  # Check if 'age' can be converted to int
                                elif key in ["name", "city"]:
                                    if (
                                        not isinstance(value, str) or not value.strip()
                                    ):  # Check for non-empty string
                                        raise ValueError(
                                            f"Invalid value for '{key}': {value}"
                                        )
                            except ValueError:
                                invalid_key = key
                                break

                        if invalid_key == "age":
                            print(
                                f"ValueError for row {row}: {e}. using default value 0."
                            )
                            person = Person(
                                name=row.get("name", "Unknown"),
                                age=0,
                                city=row.get("city", "Unknown"),
                            )
                            persons.append(person)
                        else:
                            print(f"ValueError for row {row}: {e}. Skipping row.")

        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Permission denied.")
        except csv.Error as e:
            print(f"CSV error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return persons

    def write_csv(self, filename: str, data: List[Person]):
        """
        Writes data to a CSV file.

        :param filename (str): The name of the file to write to.
        :param data (List[Person]): The data to write to the file.
        """

        try:
            with open(filename, "w", newline="") as file:
                fieldnames = ["name", "age", "city"]
                csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
                csv_writer.writeheader()
                for person in data:
                    csv_writer.writerow(person.serialize())
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Permission denied.")
        except csv.Error as e:
            print(f"CSV error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def write_json(self, filename: str, data: List[Person]):
        """
        Writes data to a JSON file.

        :param filename (str): The name of the file to write to.
        :param data (List[Person]): The data to write to the file.
        """

        try:
            with open(filename, "w") as file:
                json_data = [person.serialize() for person in data]
                json.dump(json_data, file, indent=4)
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Permission denied.")
        except json.JSONDecodeError as e:
            print(f"JSON error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def read_json(self, filename: str) -> List[Person]:
        """
        Reads a JSON file and returns the data as a list of Person instances.

        :param filename (str): The name of the file to read.

        :return List[Person]: A list of Person instances.
        """

        try:
            with open(filename, "r") as file:
                json_data = json.load(file)
                persons = []
                for person_data in json_data:
                    try:
                        person = Person.deserialize(person_data)
                        persons.append(person)
                    except (KeyError, ValueError) as e:
                        print(f"Invalid JSON structure: {e}")
                return persons
        except FileNotFoundError:
            print("File not found.")
            return []
        except PermissionError:
            print("Permission denied.")
            return []
        except json.JSONDecodeError as e:
            print(f"JSON error: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []


if __name__ == "__main__":

    file_operations = FileOperations()

    data_to_write = [
        Person(name="John", age=30, city="New York"),
        Person(name="Jane", age=25, city="London"),
        Person(name="Bob", age=40, city="Paris"),
        Person(name="Alice", age=35, city="Tokyo"),
    ]
    file_operations.write_csv(filename, data_to_write)

    persons = file_operations.read_csv(filename=filename)
    print(persons)
    print("\n".join(map(str, persons)))

    file_operations.write_json(filename_json, data_to_write)

    persons_from_json = file_operations.read_json(filename_json)
    print(persons_from_json)
    print("\n".join([str(person) for person in persons_from_json]))

    num_lines, num_words = file_operations.read_count_lines_words(filename)
    print(f"Number of lines: {num_lines}, Number of words: {num_words}")
