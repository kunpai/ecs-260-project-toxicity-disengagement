import json
import csv
import time
from moderation_caller import create_client, moderate
import zipfile
import csv
import shutil
import os


def moderate_issues(csv_file_path):
    # Load the CSV file
    with open(csv_file_path, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        issues_data = list(csv_reader)

    # Create a client for the moderation API
    client_instance = create_client()

    # Write flagged comments to a new CSV file (initialize the writer)
    output_csv_file_path = csv_file_path.replace('.csv', '_flagged.csv')
    with open(output_csv_file_path, 'w', newline='') as output_file:
        fieldnames = ['Issue ID', 'Flagged Comment', 'Flagged Categories']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        writer.writeheader()
        total_issues = len(issues_data)
        for idx, issue in enumerate(issues_data, start=1):
            issue_id = issue['Issue ID']

            # Iterate through each comment in the issue
            comment_authors = issue['Comment Author'].split(';')
            comments = issue['Comment'].split(';')
            total_comments = min(len(comment_authors), len(comments))
            for comment_author, comment in zip(comment_authors, comments):
                print(f"Current moderating issue {idx} out of {total_issues}")

                # Moderate the comment using the moderation API
                moderation_result = moderate(client_instance, comment)
                time.sleep(0.05)

                # Check if the comment is flagged
                if moderation_result.flagged:
                    flagged_categories = [category_name for category_name, field in moderation_result.categories.__fields__.items() if getattr(moderation_result.categories, category_name)]
                    # Write flagged comment to CSV after moderation
                    writer.writerow({'Issue ID': issue_id, 'Flagged Comment': comment, 'Flagged Categories': ', '.join(flagged_categories)})

    return output_csv_file_path



def moderate_commits(zip_file_path, output_directory):
    # Create a temporary directory for unzipping
    temp_directory = os.path.join(os.path.dirname(zip_file_path), "temp_unzip")
    os.makedirs(temp_directory, exist_ok=True)

    # Unzip the provided zip file into the temporary directory
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_directory)

    # Iterate over each extracted CSV file
    for root, _, files in os.walk(temp_directory):
        for file in files:
            if file.endswith('.csv'):
                csv_file_path = os.path.join(root, file)
                # Load commits from CSV file
                commits = []
                with open(csv_file_path, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        commits.append(row)

                # Create a client for the moderation API
                client_instance = create_client()

                # Write flagged commits to a new CSV file (initialize the writer)
                output_csv_file_path = os.path.join(root, f"{os.path.splitext(file)[0]}_flagged.csv")
                with open(output_csv_file_path, 'w', newline='') as output_file:
                    fieldnames = ['Flagged Message', 'Flagged Categories']
                    writer = csv.DictWriter(output_file, fieldnames=fieldnames)

                    writer.writeheader()

                    # Iterate through each commit
                    total_commits = len(commits)
                    for idx, commit in enumerate(commits, start=1):
                        print(f"Moderating commit {idx} in file {file} out of {total_commits}")
                        # Moderate the commit message using the moderation API
                        moderation_result = moderate(client_instance, commit['Message'])
                        # time.sleep(0.75)
                        # Check if the commit message is flagged
                        if moderation_result.flagged:
                            flagged_categories = [category_name for category_name, field in moderation_result.categories.__fields__.items() if getattr(moderation_result.categories, category_name)]
                            # Write flagged commit to CSV after moderation
                            writer.writerow({'Flagged Message': commit['Message'], 'Flagged Categories': ', '.join(flagged_categories)})

                # Move the flagged CSV file to the output directory
                shutil.move(output_csv_file_path, output_directory)

    # Clean up the temporary directory
    shutil.rmtree(temp_directory)

    return "finished"


def moderate_single_message(message):
    # Create a client for the moderation API
    client_instance = create_client()

    # Moderate the message using the moderation API
    moderation_result = moderate(client_instance, message)
    time.sleep(0.75)

    # Check if the message is flagged
    if moderation_result.flagged:
        flagged_categories = [category_name for category_name, field in moderation_result.categories.__fields__.items() if getattr(moderation_result.categories, category_name)]
        return {'Flagged Message': message, 'Flagged Categories': ', '.join(flagged_categories)}
    else:
        return "Not flagged"




