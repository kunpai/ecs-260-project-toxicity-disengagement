import csv

csv.field_size_limit(1000000)

def split_multi_single_devs(csv_file_path):
    # Define file paths for output files
    multi_commit_file = 'multi_commits.csv'
    single_commit_file = 'single_commits.csv'

    # Open output files for writing
    with open(csv_file_path, 'r', newline='') as csvfile, \
         open(multi_commit_file, 'w', newline='') as multi_file, \
         open(single_commit_file, 'w', newline='') as single_file:

        # Define CSV reader and writers
        reader = csv.reader(csvfile)
        multi_writer = csv.writer(multi_file)
        single_writer = csv.writer(single_file)

        # Write headers to output files
        headers = next(reader)
        multi_writer.writerow(headers)
        single_writer.writerow(headers)

        # Count commits for each developer
        commit_counts = {}
        for row in reader:
            developer = row[1]  # Assuming developer's name is in the second column
            commit_counts[developer] = commit_counts.get(developer, 0) + 1

        # Reset file pointer
        csvfile.seek(0)
        next(reader)  # Skip header row

        # Write rows to appropriate files based on commit count
        for row in reader:
            developer = row[1]  # Assuming developer's name is in the second column
            if commit_counts[developer] > 5:
                multi_writer.writerow(row)
            else:
                single_writer.writerow(row)

    print("Splitting completed. Check '{}' and '{}' for results.".format(multi_commit_file, single_commit_file))

if __name__ == '__main__':
    # Replace 'combined_commits_companies.csv' with the path to your CSV file
    split_multi_single_devs('combined_commits_non_profit.csv')
