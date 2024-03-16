from pydriller import Repository
import csv
csv.field_size_limit(1000000)


def sloc(repository, csv_file):
    """
    Calculate the Source Lines of Code (SLOC) for each commit in a repository and add the information to a CSV file.

    Parameters:
        repository (str): The path or URL of the repository to analyze.
        csv_file (str): The file path of the CSV file containing commit information.

    Returns:
        None
    """

    commits_info = {}  # Dictionary to store commit hash and corresponding SLOC

    with open(csv_file, 'r') as csvfile:
        # read existing content
        rows = list(csv.reader(csvfile))

    for row in rows[1:]:  # Skip the header row
        commit_hash = row[0]
        commits_info[commit_hash] = None  # Initialize with None, to be filled later

    for commit in Repository(repository).traverse_commits():
        commit_hash = commit.hash
        if commit_hash in commits_info:
            sloc = abs(commit.insertions - commit.deletions)
            commits_info[commit_hash] = sloc

    with open(csv_file, 'w', newline='') as csvfile:
        # add a new column to the csv file
        fieldnames =['Commit SHA', 'Developer', 'Message', 'Timestamp', 'Sentiment', 'NLTK_Sentiment', 'NLTK_Positive_Sentiment', 'NLTK_Negative_Sentiment', 'NLTK_Neutral_Sentiment', 'NLTK_Compound_Sentiment', 'Toxic', 'Severe_toxic', 'Obscene', 'Threat', 'Insult', 'Identity_hate', 'Day_of_week', 'Time_of_day', 'Pull_Request', 'Type', 'Previous_Positive_Sentiment', 'Previous_Negative_Sentiment', 'Previous_Neutral_Sentiment', 'Previous_Compound_Sentiment', 'Previous_Toxic', 'Previous_Severe_toxic', 'Previous_Obscene', 'Previous_Threat', 'Previous_Insult', 'Previous_Identity_hate', 'Previous_Timestamp','SLOC']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows[1:]:  # Skip the header row
            commit_hash = row[0]
            sloc = commits_info.get(commit_hash, 0)
            row.append(sloc)
            writer.writerow(dict(zip(fieldnames, row)))

    return


if __name__ == "__main__":
    print(sloc("clones/gem5-resources-website", "gem5_gem5-resources-website_commits.csv"))
