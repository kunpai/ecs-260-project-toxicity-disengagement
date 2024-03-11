import argparse
from moderate import moderate_issues, moderate_commits, moderate_single_message

def main():
    parser = argparse.ArgumentParser(description="Moderate issues or commits.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', action='store_true', help='Moderate issues')
    group.add_argument('-c', action='store_true', help='Moderate commits')
    group.add_argument('-m', action='store_true', help='Moderate a single message')

    args = parser.parse_args()

    if args.i:
        file_path = input("Enter the file path for issues: ")
        print(moderate_issues(file_path))
    elif args.c:
        file_path = input("Enter the file path for the commits zipfile: ")
        output_path = input("Enter the outputh path: ")
        print(moderate_commits(file_path, output_path))
    elif args.m:
        message=input("Please enter the message you would like to moderate: ")
        print(moderate_single_message(message))

if __name__ == "__main__":
    main()
