# Dependencies
import os
import csv
import sys
from collections import defaultdict

# Set path for file
csvpath = os.path.join("Resources", "election_data.csv")

# Function to count occurrences of values in a specific CSV column
def count_column_values(csvpath, column_index):
    value_count = defaultdict(int)  # Dictionary to store counts
    

    # Read the CSV file
    with open(csvpath, encoding='UTF-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        next(csvreader)  # Skip header
       
        # Loop through the rows after the header
        for row in csvreader:
            value = row[column_index]
            value_count[value] += 1            
                       
    return value_count

# Function to calculate percentages and find the value with the highest count
def calculate_percentages_and_largest(value_count):
    total_count = sum(value_count.values())  # Total number of occurrences
    percentages = {}
    
    # Calculate percentage for each value
    for value, count in value_count.items():
        percentages[value] = (count / total_count) * 100

    # Find the value with the largest count
    largest_value = max(value_count, key=value_count.get)

    return percentages, largest_value, total_count

column_index = 2  # Index of the column to count

# Count occurrences of values in the column
value_count = count_column_values(csvpath, column_index)

# Calculate percentages and find the largest value
percentages, largest_value, total_count = calculate_percentages_and_largest(value_count)

# Custom class to duplicate output to console and file
class Tee:
    def __init__(self, file):
        self.file = file
        self.console = sys.stdout  # Save current console output
    
    def write(self, message):
        self.console.write(message)  # Write to console
        self.file.write(message)     # Write to file

    def flush(self):
        # Flush both outputs to make sure everything is written
        self.console.flush()
        self.file.flush()

# Specify the file to write to
output_path = os.path.join("analysis", "poll_analysis.txt")

# Open the text file and redirect output
with open(output_path, 'w') as file:
    # Redirect sys.stdout to both console and file
    tee = Tee(file)
    sys.stdout = tee

    # Print out the results
    print('Election Results')
    print('----------------------------')
    print(f'Total Votes: {total_count}')
    print('----------------------------')
    for value, count in value_count.items():
        percentage = percentages[value]
        print(f'{value}: {percentage:.2f}% ({count})')
    print('----------------------------')
    print(f'Winner: {largest_value}')
    print('----------------------------')

# Restore sys.stdout back to its original state
sys.stdout = sys.__stdout__

# Continue normal console output
# print("Report generation completed. Output saved to fin_analysis.txt.")