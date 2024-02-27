# open a csv

import csv

csv.field_size_limit(1000000)

def sorter(csv_file_path):
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
