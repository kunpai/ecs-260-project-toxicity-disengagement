import argparse
from moderate import moderate_issues, moderate_commits

def main():
    parser = argparse.ArgumentParser(description="Moderate issues or commits.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', action='store_true', help='Moderate issues')
    group.add_argument('-c', action='store_true', help='Moderate commits')

    args = parser.parse_args()

    if args.i:
        file_path = input("Enter the file path for issues: ")
        print(moderate_issues(file_path))
    elif args.c:
        file_path = input("Enter the file path for commits: ")
        print(moderate_commits(file_path))

if __name__ == "__main__":
    main()
