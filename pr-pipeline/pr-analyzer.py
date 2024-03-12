import csv
from github import Github
import os
import sys
from datetime import datetime
from datetime import timezone
from dotenv import load_dotenv 
sys.path.append('..')
from toxicity_detector.toxicity_detector import classify_sentence
from toxicity_detector.toxicity_detector import nltk_classify_sentence
load_dotenv()

def extract_pull_requests_and_comments(repository_url, output_file, github_token):
    # Create a Github instance
    g = Github(github_token)

    # Get the repository
    repo = g.get_repo(repository_url)

    # Open a CSV file for writing
    csv_file_path = 'output_' + repository_url.replace("/", "_") + '.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write header row
        csv_writer.writerow(['Pull Request ID', 'Title', 'Body', 'State', 'Created at', 'Closed at', 'Author', 'Comment Author', 'Comment', 'Commented at', 'Toxicity', 'NLTK Sentiment'])

        try:
            for pr in repo.get_pulls(state='all'):
                # Write pull request information to CSV
                csv_writer.writerow([pr.number, pr.title, pr.body, pr.state, pr.created_at, pr.closed_at, pr.user.login, '', '', '', '', ''])

                # Check if the user already exists before adding a new entry
                user_exists = False
                comment = pr.body if pr.body is not None else "There is no body for this pull request."

                csv_writer.writerow(['', '', '', '', '', '', '', pr.user.login, comment, pr.created_at, classify_sentence(comment), nltk_classify_sentence(comment)])

                # Write comments information to CSV
                for comment in pr.get_review_comments():
                    csv_writer.writerow(['', '', '', '', '', '', '', comment.user.login, comment.body, comment.created_at, classify_sentence(comment.body), nltk_classify_sentence(comment.body)])

        except Exception as e:
            print(e)
            print(f"Error occurred while processing the pull request {pr.number}. Skipping to the next pull request.")
            pass

if __name__ == "__main__":
    # Replace 'username/repo' with the actual repository path
    repository_url = 'helloparthshah/StadiaWireless'

    # Specify the output file
    output_file = 'output_' + repository_url.replace("/", "_") + '.csv'

    # Add your GitHub token here
    github_token = os.environ.get('GITHUB_TOKEN')

    extract_pull_requests_and_comments(repository_url, output_file, github_token)
