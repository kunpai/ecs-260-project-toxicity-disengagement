import csv
from github import Github
import os
import sys
from datetime import datetime
from datetime import timezone
from dotenv import load_dotenv  
sys.path.append('..')

from toxicity_detector.toxicity_detector import classify_sentence, nltk_classify_sentence
load_dotenv()  # Load environment variables from .env file

def extract_issues_and_comments(repository_url, output_file, github_token):
    # Create a Github instance
    g = Github(github_token)

    # Get the repository
    repo = g.get_repo(repository_url)

    # Open a CSV file for writing
    csv_file_path = 'output_' + repository_url.replace("/", "_") + '.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write header row
        csv_writer.writerow(['Issue ID', 'Title', 'Body', 'State', 'Created at', 'Closed at', 'Original Author', 'Comment Author', 'Comment', 'Commented at', 'Toxicity', 'NLTK Sentiment'])

        try:
            for issue in repo.get_issues(state='all'):
                # Reset set for each new issue
                existing_users = set()

                # Write issue information to CSV
                csv_writer.writerow([issue.number, issue.title, issue.body, issue.state, issue.created_at, issue.closed_at, issue.user.login, '', '', '', '', ''])

                # Check if the user already exists before adding a new entry
                if issue.user.login not in existing_users:
                    comment = issue.body if issue.body is not None else "There is no body for this issue."
                    csv_writer.writerow(['', '', '', '', '', '', '', issue.user.login, comment, issue.created_at, classify_sentence(comment), nltk_classify_sentence(comment)])
                    existing_users.add(issue.user.login)

                # Write comments information to CSV
                for comment in issue.get_comments():
                    if comment.user.login not in existing_users:
                        csv_writer.writerow(['', '', '', '', '', '', '', comment.user.login, comment.body, comment.created_at, classify_sentence(comment.body), nltk_classify_sentence(comment.body)])
                        existing_users.add(comment.user.login)

        except Exception as e:
            print(e)
            print(f"Error occurred while processing the issue {issue.number}. Skipping to the next issue.")
            pass

if __name__ == "__main__":
    # Replace 'username/repo' with the actual repository path
    repository_url = 'helloparthshah/StadiaWireless'

    # Specify the output file
    output_file = 'output_' + repository_url.replace("/", "_") + '.csv'

    # Add your GitHub token here
    github_token = os.environ.get('GITHUB_TOKEN')
    print(f"Repository URL: {repository_url}")
    print(f"GitHub Token: {github_token}")

    extract_issues_and_comments(repository_url, output_file, github_token)
