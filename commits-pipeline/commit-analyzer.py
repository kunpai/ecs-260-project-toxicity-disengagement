import argparse
import json
import os
import sys
import shutil
import csv
from sloc_adder import sloc
from sorter import sorter
from diff_creator import create_diff_column
sys.path.append('..')
from pydriller import Repository
from toxicity_detector.toxicity_detector import classify_sentence, nltk_classify_sentence

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def clone_repository(remote_url, local_path):
    os.system(f"git clone {remote_url} {local_path}")

def generate_commits_csv(repository_path, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Commit SHA', 'Developer', 'Message', 'Timestamp', 'Sentiment', 'NLTK_Sentiment', 'NLTK_Positive_Sentiment', 'NLTK_Negative_Sentiment', 'NLTK_Neutral_Sentiment', 'NLTK_Compound_Sentiment', 'Toxic', 'Severe_toxic', 'Obscene', 'Threat', 'Insult', 'Identity_hate', 'Day_of_week', 'Time_of_day', 'Pull_Request', 'Type', 'Previous_Positive_Sentiment', 'Previous_Negative_Sentiment', 'Previous_Neutral_Sentiment', 'Previous_Compound_Sentiment', 'Previous_Toxic', 'Previous_Severe_toxic', 'Previous_Obscene', 'Previous_Threat', 'Previous_Insult', 'Previous_Identity_hate', 'Previous_Commit']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        prev_positive_sentiment = 0
        prev_negative_sentiment = 0
        prev_neutral_sentiment = 0
        prev_compound_sentiment = 0
        prev_toxic_sentiment = 0
        prev_severe_toxic_sentiment = 0
        prev_obscene_sentiment = 0
        prev_threat_sentiment = 0
        prev_insult_sentiment = 0
        prev_identity_hate_sentiment = 0
        prev_commit_timestamp = None

        for commit in Repository(repository_path).traverse_commits():
            developer_name = commit.author.name
            sentiment = nltk_classify_sentence(commit.msg)
            positive_sentiment = sentiment['pos']
            negative_sentiment = sentiment['neg']
            neutral_sentiment = sentiment['neu']
            compound_sentiment = sentiment['compound']
            if len(commit.msg) > 512:
                toxic_message = commit.msg[:512]
            else:
                toxic_message = commit.msg
            toxic = classify_sentence(toxic_message)
            toxic_sentiment = toxic['Toxic']
            severe_toxic_sentiment = toxic['Severe_toxic']
            obscene_sentiment = toxic['Obscene']
            threat_sentiment = toxic['Threat']
            insult_sentiment = toxic['Insult']
            identity_hate_sentiment = toxic['Identity_hate']

            timestamp = commit.author_date.strftime("%Y-%m-%d %H:%M:%S")
            # get day of the week from timestamp
            day_of_week = commit.author_date.strftime("%A")
            # get hour of the day from timestamp
            hour_of_day = commit.author_date.strftime("%H")
            # classify hour into morning, afternoon, evening, night
            if 6 <= int(hour_of_day) < 12:
                time_of_day = "Morning"
            elif 12 <= int(hour_of_day) < 17:
                time_of_day = "Afternoon"
            elif 17 <= int(hour_of_day) < 20:
                time_of_day = "Evening"
            else:
                time_of_day = "Night"

            if commit.msg.startswith('Merge') or commit.msg.startswith('\"Merge') or "Merge" in commit.msg:
                pull_request = 1
            else:
                pull_request = 0

            if prev_commit_timestamp is None:
                prev_commit=0
            else:
                # subtract the previous commit's timests from the current timestamp and get difference in seconds
                prev_commit = (commit.author_date - prev_commit_timestamp).total_seconds()

            commit_info = {
                'Commit SHA': commit.hash,
                'Developer': developer_name,
                'Message': commit.msg,
                'Timestamp': timestamp,
                'Sentiment': toxic,
                'Toxic': toxic_sentiment,
                'Severe_toxic': severe_toxic_sentiment,
                'Obscene': obscene_sentiment,
                'Threat': threat_sentiment,
                'Insult': insult_sentiment,
                'Identity_hate': identity_hate_sentiment,
                'NLTK_Sentiment': sentiment,
                'NLTK_Positive_Sentiment': positive_sentiment,
                'NLTK_Negative_Sentiment': negative_sentiment,
                'NLTK_Neutral_Sentiment': neutral_sentiment,
                'NLTK_Compound_Sentiment': compound_sentiment,
                'Day_of_week': day_of_week,
                'Time_of_day': time_of_day,
                'Pull_Request': pull_request,
                "Type": "Commit",
                "Previous_Positive_Sentiment": prev_positive_sentiment,
                "Previous_Negative_Sentiment": prev_negative_sentiment,
                "Previous_Neutral_Sentiment": prev_neutral_sentiment,
                "Previous_Compound_Sentiment": prev_compound_sentiment,
                "Previous_Toxic": prev_toxic_sentiment,
                "Previous_Severe_toxic": prev_severe_toxic_sentiment,
                "Previous_Obscene": prev_obscene_sentiment,
                "Previous_Threat": prev_threat_sentiment,
                "Previous_Insult": prev_insult_sentiment,
                "Previous_Identity_hate": prev_identity_hate_sentiment,
                "Previous_Commit": prev_commit,
            }
            writer.writerow(commit_info)

            prev_positive_sentiment = positive_sentiment
            prev_negative_sentiment = negative_sentiment
            prev_neutral_sentiment = neutral_sentiment
            prev_compound_sentiment = compound_sentiment
            prev_toxic_sentiment = toxic_sentiment
            prev_severe_toxic_sentiment = severe_toxic_sentiment
            prev_obscene_sentiment = obscene_sentiment
            prev_threat_sentiment = threat_sentiment
            prev_insult_sentiment = insult_sentiment
            prev_identity_hate_sentiment = identity_hate_sentiment
            prev_commit_timestamp = commit.author_date

def main(repository_url):
    local_directory = "clones"
    repo_name = repository_url.split("/")[-1].replace(".git", "")
    repository_path = os.path.join(local_directory, repo_name)

    ensure_directory_exists(local_directory)

    print(f"Cloning repository {repository_url} to {repository_path}")

    if not os.path.exists(repository_path):
        clone_repository(repository_url, repository_path)

    username = repository_url.split("/")[-2]
    repo = repository_url.split("/")[-1].replace(".git", "")

    output_csv_path = f"{username}_{repo}_commits.csv"

    generate_commits_csv(repository_path, output_csv_path)

    print(f"Commits CSV written to {output_csv_path}")

    return repository_path, output_csv_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate CSV containing commit information from a Git repository.")
    parser.add_argument("--repo", type=str, help="URL of the Git repository")
    args = parser.parse_args()

    ret = main(args.repo)
    print("Adding SLOC to the CSV")
    sloc(ret[0], ret[1])
    print("Sorting the CSV")
    sorter(ret[1])
    print("Done")
    print("Creating time difference column")
    create_diff_column(ret[1])
    print("Done")
