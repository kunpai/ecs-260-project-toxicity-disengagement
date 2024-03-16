import argparse
import pandas as pd
import matplotlib.pyplot as plt

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate a heatmap of toxic comments from a CSV file")
    parser.add_argument("csv_file", help="Path to the CSV file containing the data")
    parser.add_argument("--title", help="Title of the heatmap", default="Toxic Comments Heatmap")
    return parser.parse_args()

def main():
    args = parse_arguments()

    try:
        df = pd.read_csv(args.csv_file)
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return

    print(len(df))

    title = args.title

    toxic_comments = df[df['Toxic'] > 0.1]

    print(len(toxic_comments))

    print(len(toxic_comments) / len(df) * 100)

    toxic_categories = ['Obscene', 'Insult', 'Threat', 'Identity_hate', 'Severe_toxic']

    strength_values = toxic_comments[toxic_categories].values

    plt.figure(figsize=(8, 7))
    heatmap = plt.imshow(strength_values, cmap='coolwarm', aspect='auto', interpolation='nearest')
    color = plt.colorbar(heatmap)
    color.set_label('Toxicity Strength', fontsize=15)

    xtick_labels = [label.replace('_', '\n') if '_' in label else label for label in toxic_categories]
    xtick_labels = [label.title() for label in xtick_labels]

    plt.xticks(range(len(toxic_categories)), xtick_labels)
    plt.yticks(range(len(toxic_comments)), "")
    plt.ylabel('Toxic Comments', fontsize=15)
    plt.xlabel('Toxicity Categories', fontsize=15)

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.title(title, fontsize=15)

    plt.show()

if __name__ == "__main__":
    main()
