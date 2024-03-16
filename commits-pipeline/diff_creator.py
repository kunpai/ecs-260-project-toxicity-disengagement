import csv
from datetime import datetime

def create_diff_column(csv_file_path):
    """
    Adds a new column 'Time Difference' to a CSV file containing commit data,
    representing the time difference between consecutive commits for each developer.

    Args:
        csv_file_path (str): The file path to the CSV file containing commit data.

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

    header.append('Time Difference')

    # for every row, calculate the difference between the current row's timestamp and the next row's timestamp and insert it as a new column
    # only do it if the developer name is the same
    for i in range(len(rows) - 1):
        current_row = rows[i]
        next_row = rows[i + 1]
        current_developer = current_row[0]
        next_developer = next_row[0]
        current_timestamp = datetime.strptime(current_row[3], "%Y-%m-%d %H:%M:%S")
        next_timestamp = datetime.strptime(next_row[3], "%Y-%m-%d %H:%M:%S")
        time_difference = next_timestamp - current_timestamp
        # convert the time difference to seconds
        time_difference = time_difference.total_seconds()
        if current_developer == next_developer:
            current_row.append(str(time_difference))
        else:
            # we are starting a new developer's commits, so we need a time difference until today
            current_row.append(str((datetime.now() - current_timestamp).total_seconds()))
        rows[i] = current_row

    # write the updated rows to the new file
    rows.insert(0, header)

    with open(csv_file_path.replace('.csv', '.csv'), 'w', newline='') as csvfile: # write to the same file
        writer = csv.writer(csvfile)
        writer.writerows(rows)


if __name__ == '__main__':
    # Replace 'gem5_gem5_commits.csv' with the path to your CSV file
    create_diff_column('gem5_gem5_commits.csv')
