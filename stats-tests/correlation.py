import pandas as pd
from scipy.stats import ttest_ind
import argparse

def create_correlation_matrix(df, columns_subset=None):
    if columns_subset:
        df = df[columns_subset]

    if 'Day_of_week' in df.columns and 'Time_of_day' in df.columns:
        df_encoded = pd.get_dummies(df, columns=['Day_of_week', 'Time_of_day'])
        bool_columns = ['Day_of_week_Monday', 'Day_of_week_Tuesday', 'Day_of_week_Wednesday', 'Day_of_week_Thursday', 'Day_of_week_Friday', 'Day_of_week_Saturday', 'Day_of_week_Sunday',
                        'Time_of_day_Morning', 'Time_of_day_Afternoon', 'Time_of_day_Evening', 'Time_of_day_Night']
        df_encoded[bool_columns] = df_encoded[bool_columns].astype(int)
    else:
        df_encoded = df

    numeric_df = df_encoded.select_dtypes(include=['float64', 'int64'])
    return numeric_df.corr()

def create_p_value(df, columns_subset=None):
    if columns_subset:
        df = df[columns_subset]

    if 'Day_of_week' in df.columns and 'Time_of_day' in df.columns:
        df_encoded = pd.get_dummies(df, columns=['Day_of_week', 'Time_of_day'])
        bool_columns = ['Day_of_week_Monday', 'Day_of_week_Tuesday', 'Day_of_week_Wednesday', 'Day_of_week_Thursday', 'Day_of_week_Friday', 'Day_of_week_Saturday', 'Day_of_week_Sunday',
                        'Time_of_day_Morning', 'Time_of_day_Afternoon', 'Time_of_day_Evening', 'Time_of_day_Night']
        df_encoded[bool_columns] = df_encoded[bool_columns].astype(int)
    else:
        df_encoded = df

    numeric_df = df_encoded.select_dtypes(include=['float64', 'int64'])

    if 'Toxic' in numeric_df.columns and 'Time Difference' in numeric_df.columns:
        t_statistic, p_value = ttest_ind(numeric_df['Toxic'], numeric_df['Time Difference'])
        print(f'T-statistic: {t_statistic}')
        print(f'P-value: {p_value}')

    return numeric_df.corr(method='pearson')

def main():
    parser = argparse.ArgumentParser(description='Calculate correlation matrix and p-value for specified columns.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file')
    parser.add_argument('--columns_subset', nargs='+', help='Subset of columns to use in correlation analysis', default=None)

    args = parser.parse_args()

    df = pd.read_csv(args.input_file)

    correlation_matrix = create_correlation_matrix(df, columns_subset=args.columns_subset)
    print('Correlation Matrix:')
    print(correlation_matrix)

    # write to file

    with open('correlation_matrix.csv', 'w') as f:
        f.write(correlation_matrix.to_csv())

    if args.columns_subset:
        if 'Toxic' in args.columns_subset and 'Time Difference' in args.columns_subset:
            p_value = create_p_value(df, columns_subset=args.columns_subset)
            print('\nP-value:')
            print(p_value)

            print('\nNull hypothesis: There is no significant difference between the means of the two columns')

if __name__ == '__main__':
    main()
