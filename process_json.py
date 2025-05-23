"""
Process a JSON file to count and list the astronauts by spacecraft and save the result.

JSON file is in the format where people is a list of dictionaries with keys "craft" and "name".

{
    "people": [
        {
            "craft": "ISS",
            "name": "Oleg Kononenko"
        },
        {
            "craft": "ISS",
            "name": "Nikolai Chub"
        }
    ],
    "number": 2,
    "message": "success"
}

"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import json
import pathlib
import sys

# Ensure project root is in sys.path for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent))

# Import local modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

# Define the directory structure for the project
FETCHED_DATA_DIR: str = "project_data"
PROCESSED_DIR: str = "project_processed"

#####################################
# Define Functions
#####################################

# Function to read and processes JSON file

def count_astronauts_by_craft(file_path: pathlib.Path) -> dict:
    """Count the number of astronauts on each spacecraft from a JSON file."""
    try:
        # Open the JSON file using the file_path passed in as an argument
        with file_path.open('r') as file:

            # Use the json module load() function 
            # to read data file into a Python dictionary
            astronaut_dictionary = json.load(file)  

            # initialize an empty dictionary to store the counts
            craft_counts_dictionary = {}

            # Get the list of people from the dictionary
            people_list: list = astronaut_dictionary.get("people", [])

            # For each person in the list, get the craft and count them
            for person_dictionary in people_list:  

                # Get the craft from the person dictionary
                # If the key "craft" is not found, default to "Unknown"
                craft = person_dictionary.get("craft", "Unknown")

                # Update the craft counts dictionary for that craft
                # If the craft is not in the dictionary, initialize it to 0
                # Add 1 to the count for the current craft
                craft_counts_dictionary[craft] = craft_counts_dictionary.get(craft, 0) + 1

            # Return the dictionary with counts of astronauts by spacecraft    
            return craft_counts_dictionary
    except Exception as e:
        logger.error(f"Error reading or processing JSON file: {e}")
        return {} # return an empty dictionary if error

def astronauts_by_craft(file_path: pathlib.Path) -> dict:
    """Return a dictionary mapping each craft to a list of astronaut names."""
    try:
        with file_path.open('r') as file:
            data = json.load(file)
            people_list = data.get("people", [])
            craft_astronauts = {}
            for person in people_list:
                craft = person.get("craft", "Unknown")
                name = person.get("name", "Unknown")
                craft_astronauts.setdefault(craft, []).append(name)
            return craft_astronauts
    except Exception as e:
        logger.error(f"Error reading or processing JSON file: {e}")
        return {}

def process_json_file():
    """Read JSON file, show astronauts by spacecraft, and save the result."""

    input_file: pathlib.Path = pathlib.Path(FETCHED_DATA_DIR, "astros.json")
    output_file: pathlib.Path = pathlib.Path(PROCESSED_DIR, "json_astronauts_by_craft.txt")
    
    # Get count by craft
    craft_counts = count_astronauts_by_craft(input_file)

    # Get astronauts by craft
    craft_astronauts = astronauts_by_craft(input_file)

    # Create the output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Open the output file in write mode and write the results
    with output_file.open('w') as file:
        file.write("Astronauts on each spacecraft:\n")
        for craft, names in craft_astronauts.items():
            file.write(f"{craft} ({len(names)}):\n")
            for name in names:
                file.write(f"  - {name}\n")
            file.write("\n")
    
    # Log the processing of the JSON file
    logger.info(f"Processed JSON file: {input_file}, Results saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting JSON processing...")
    process_json_file()
    logger.info("JSON processing complete.")
