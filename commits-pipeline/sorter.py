import csv

csv.field_size_limit(1000000)

def sorter(csv_file_path):
    """
    Sorts the content of a CSV file in ascending order of Developer name and then ascending order of Timestamp.

    Parameters:
        csv_file_path (str): The file path of the CSV file to be sorted.

    Returns:
        None
    """
    # open a csv file in read mode
    with open(csv_file_path, 'r') as csvfile:
        # read existing content
        rows = list(csv.reader(csvfile))

    # arrange the rows in ascending order of Developer name and then ascending order of Timestamp
    # starting from the second row
    header = rows[0]
    # remove the header row
    rows = rows[1:]

    rows = sorted(rows, key=lambda x: (x[1], x[3]))

    # add the header row back to the arranged rows
    rows.insert(0, header)

    # rewrite the csv file with the arranged rows
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

# To run this script, call the sorter function with the file path of the CSV file to be sorted
# For example:
# sorter("path/to/your/csv_file.csv")
# The sorted content will be written back to the same file.