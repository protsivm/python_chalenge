# Dependencies
import os
import csv
import sys

# Set path for file
csvpath = os.path.join("Resources", "budget_data.csv")

# Initialize variables for summing and counting rows
total_sum = 0
row_count = 0
previous_value = None
changes = []  # List to store changes between rows
change = 0

# Read the CSV file
with open(csvpath, encoding='UTF-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    next(csvreader)  # Skip header

    # Loop through the rows after the header
    for row in csvreader:        
        try:
            value = int(row[1])
            total_sum += value
            row_count += 1
        except ValueError:
            print(f"Non-numeric data in row {row}: {row[1]}")  # Handle non-numeric data
    
        if previous_value is not None:
            # Calculate the change using the current and previous values
            change = value - previous_value
            # Append the change to the list
            changes.append(change)

        previous_value = value

# Calculate average change and find max/min changes
if len(changes) > 0:
    average_change = sum(changes) / len(changes)
else: print(f"Mising data in the List to store changes between each month")
max_pos_change = max(changes)
max_neg_change = min(changes)
# Find positions for max and min changes
position1 = changes.index(max_pos_change) + 1
position2 = changes.index(max_neg_change) + 1

# Find the months corresponding to the max/min changes
with open(csvpath, encoding='UTF-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    next(csvreader)  # Skip header

    for current_row_index, row in enumerate(csvreader):
        if current_row_index == position1:           
            increase_month = str(row[0]) 
        if current_row_index == position2:
            decrease_month = str(row[0]) 

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
output_path = os.path.join("analysis", "fin_analysis.txt")

# Open the text file and redirect output
with open(output_path, 'w') as file:
    # Redirect sys.stdout to both console and file
    tee = Tee(file)
    sys.stdout = tee

    print('Financial Analysis')
    print('----------------------------------')
    print(f'Total Months: {row_count}')
    print(f'Total: ${total_sum}')
    print(f'Average Change: ${average_change:.2f}')
    print(f'Greatest Increase in Profits: {increase_month} (${max_pos_change})')
    print(f'Greatest Decrease in Profits: {decrease_month} (${max_neg_change})')

# Restore sys.stdout back to its original state
sys.stdout = sys.__stdout__

# Continue normal console output
# print("Report generation completed. Output saved to fin_analysis.txt.")
