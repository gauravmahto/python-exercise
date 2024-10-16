import csv
from dataclasses import dataclass, asdict, fields
import json
from typing import List, TypedDict

filename = "data/persons.ignore.csv"
filename_json = "data/persons.ignore.json"


@dataclass
class Person:
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

    def read(self, filename: str) -> str:
        """
        Reads a file and returns the data as a string.

        Args:
            filename (str): The name of the file to read.

        Returns:
            str: A string containing the data from the file.
        """
        with open(filename, "r") as file:
            data = file.read()
            return data

    def read_csv(self, filename: str) -> List[Person]:
        """
        Reads a CSV file and returns the data as a list of lists.

        Args:
            filename (str): The name of the file to read.

        Returns:
            list: A list of lists, where each sublist contains the data from a row in the CSV file.
        """
        persons: List[Person] = []

        with open(filename, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                person = Person.deserialize(row)
                persons.append(person)

        return persons

    def write_csv(self, filename: str, data: List[Person]):
        """
        Writes data to a CSV file.

        Args:
            filename (str): The name of the file to write to.
            data (MyCsvData): The data to write to the file.
        """
        with open(filename, "w", newline="") as file:
            fieldnames = ["name", "age", "city"]
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for person in data:
                csv_writer.writerow(person.serialize())

    def write_json(self, filename: str, data: List[Person]):
        """
        Writes data to a JSON file.

        Args:
            filename (str): The name of the file to write to.
            data (MyJsonData): The data to write to the file.
        """
        with open(filename, "w") as file:
            json_data = [person.serialize() for person in data]
            json.dump(json_data, file, indent=4)

    def read_json(self, filename: str) -> List[Person]:
        """
        Reads a JSON file and returns the data as a list of Person objects.

        Args:
            filename (str): The name of the file to read.

        Returns:
            list: A list of Person objects.
        """
        with open(filename, "r") as file:
            json_data = json.load(file)
            return [Person(**person) for person in json_data]


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
