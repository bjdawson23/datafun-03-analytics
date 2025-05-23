"""
Process an Excel file to count occurrences of a specific word or words in a columns.

"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import sys

# Import from external packages
import openpyxl

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

def count_word_in_column(file_path: pathlib.Path, column_letter: str, word: str) -> int:
    """Count the occurrences of a specific word in a given column of an Excel file."""
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        count = 0
        for cell in sheet[column_letter]:
            if cell.value and isinstance(cell.value, str):
                count += cell.value.lower().count(word.lower())
        return count
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        return 0

def process_excel_file():
    """Read an Excel file, count occurrences of 'GitHub' in specific columns, and save the result."""
    
    # Excel data file
    input_file = pathlib.Path(FETCHED_DATA_DIR, "Feedback.xlsx")

    # Excel processed file
    output_file = pathlib.Path(PROCESSED_DIR, "excel_feedback_github_count.txt")

    # List of columns to check
    column_to_check = ["A", "B", "C", "D", "E", "F"]

    # Word to count
    word_to_count = "GitHub"

    # Count occurrences in each column and sum
    total_count = 0
    column_counts = {}
    for col in column_to_check:
        count = count_word_in_column(input_file, col, word_to_count)
        column_counts[col] = count
        total_count += count
    
    # Write the results to the output file    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open('w') as file:
        file.write(f"Occurrences of '{word_to_count}' in columns {column_to_check}:\n")
        for col, count in column_counts.items():
            file.write(f"  Column {col}: {count}\n")
        file.write(f"Total occurrences: {total_count}\n")
    
    logger.info(f"Processed Excel file: {input_file}, Word count saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting Excel processing...")
    process_excel_file()
    logger.info("Excel processing complete.")
