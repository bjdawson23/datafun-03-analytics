"""
Process a CSV file on 2020 Happiness ratings by country to analyze the `Healthy life expectancy` column and save statistics.
"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import csv
import statistics
import sys

# Ensure project root is in sys.path for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent))

# Import local modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

FETCHED_DATA_DIR: str = "project_data"
PROCESSED_DIR: str = "project_processed"

#####################################
# Define Functions
#####################################

# Add or replace this with a function that reads and processes your CSV file

def analyze_healthy_life_expectancy(file_path: pathlib.Path) -> dict:
    """Analyze the Healthy life expectancy column to calculate min, max, mean, stdev, and regional averages."""
    try:
        score_list = []
        regional_scores = {}  # store scores by region
        print("Looking for file at:", file_path.resolve())
        print(file_path.as_posix())
        with file_path.open('r') as file:
            dict_reader = csv.DictReader(file)
            for row in dict_reader:
                try:
                    score = float(row["Healthy life expectancy"])
                    score_list.append(score)
                    # collect by region
                    region = row.get("Regional indicator", "Unknown")
                    regional_scores.setdefault(region, []).append(score)
                except ValueError as e:
                    logger.warning(f"Skipping invalid row: {row} ({e})")
        
        # Calculate statistics
        stats = {
            "min": min(score_list),
            "max": max(score_list),
            "mean": statistics.mean(score_list),
            "stdev": statistics.stdev(score_list) if len(score_list) > 1 else 0,
        }
        # calculate average by region
        regional_averages = {
            region: statistics.mean(scores) for region, scores in regional_scores.items() if scores
        }
        stats["regional_averages"] = regional_averages
        return stats
    except Exception as e:
        logger.error(f"Error processing CSV file: {e}")
        return {}

def process_csv_file():
    """Read a CSV file, analyze Healthy life expectancy, and save the results."""
    
    # Replace with path to your CSV data file
    input_file = pathlib.Path(FETCHED_DATA_DIR, "2020_happiness.csv")
    
    # Replace with path to your CSV processed file
    output_file = pathlib.Path(PROCESSED_DIR, "happiness_healthy_life_expectancy_stats.txt")
    
    # Call your new function to process YOUR CSV file
    stats = analyze_healthy_life_expectancy(input_file)

    # Create the output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Open the output file in write mode and write the results
    with output_file.open('w') as file:
        file.write("Healthy Life Expectancy:\n")
        file.write(f"Minimum: {stats['min']:.2f}\n")
        file.write(f"Maximum: {stats['max']:.2f}\n")
        file.write(f"Mean: {stats['mean']:.2f}\n")
        file.write(f"Standard Deviation: {stats['stdev']:.2f}\n\n")
        # regional averages
        file.write("Average Healthy Life Expectancy by Regional Indicator:\n")
        for region, avg in stats.get("regional_averages", {}).items():
            file.write(f"{region}: {avg:.2f}\n")
    
    # Log the processing of the CSV file
    logger.info(f"Processed CSV file: {input_file}, Statistics saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting CSV processing...")
    process_csv_file()
    logger.info("CSV processing complete.")
