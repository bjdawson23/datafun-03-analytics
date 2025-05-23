"""
Process a text file to count occurrences of the word "Romeo", "Juliet", "Art", "Love", "Death" and save the result.
"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import sys

# Ensure project root is in sys.path for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent))

# Import local modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

# Define directories for data fetching and processing
FETCHED_DATA_DIR: str = "project_data"
PROCESSED_DIR: str = "project_processed"

#####################################
# Define Functions
#####################################

def count_word_occurrences(file_path: pathlib.Path, words: list) -> dict:
    """Count the occurrences of each word in a list (case-insensitive) in a text file."""
    counts = {}
    try:
        with file_path.open('r') as file:
            content: str = file.read().lower()
            for word in words:
                counts[word] = content.count(word.lower())
        return counts
    except Exception as e:
        logger.error(f"Error reading text file: {e}")
        return {word: 0 for word in words}

def process_text_file():
    """Read a text file, count occurrences of several words, and save the result."""
 
    input_file = pathlib.Path(FETCHED_DATA_DIR, "romeo.txt")
    output_file = pathlib.Path(PROCESSED_DIR, "text_romeo_word_count.txt")

    # List of words to count
    word_to_count = ["Romeo", "Juliet", "Art", "Love", "Death"]

    # Count occurrences for each word
    word_counts = count_word_occurrences(input_file, word_to_count)

    # Create the output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write the results to the output file
    with output_file.open('w') as file:
        file.write("Occurrences of selected words:\n")
        for word, count in word_counts.items():
            file.write(f"  {word}: {count}\n")
    
    logger.info(f"Processed text file: {input_file}, Word counts saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting text processing...")
    process_text_file()
    logger.info("Text processing complete.")
