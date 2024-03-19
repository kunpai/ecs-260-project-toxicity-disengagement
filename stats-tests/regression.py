import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def regression_analysis_disengagement_2(df, category):
    """
    Performs multilinear regression analysis to estimate the impact of average sentiment
    on the number of unique developers
    Take in effect of a lot of factors
    """


    df = df.groupby('Year').agg({
        'NLTK_Compound_Sentiment': 'mean',
        'Toxic': 'mean',
        'SLOC': 'sum',
        'Developer': 'nunique',
    })

    # calculate Variance Inflation Factor (VIF) to check for multicollinearity
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tools.tools import add_constant

    # Create a constant term
    X = add_constant(df)

    # Calculate VIF
    vif = pd.DataFrame()
    vif["variables"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    print(vif)

    X = df[['NLTK_Compound_Sentiment', 'Toxic', 'SLOC']]  # Add more variables
    y = df['Developer']

    # Create a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Print the coefficients
    print(f'Coefficients: {model.coef_}')
    print(f'Intercept: {model.intercept_}')
    print(f'R^2: {model.score(X, y)}')

    # Predict the number of unique developers
    y_pred = model.predict(X)

    # Plot the actual vs. predicted number of unique developers
    plt.figure(figsize=(8, 6))
    plt.plot(df.index, y, label='Actual')
    plt.plot(df.index, y_pred, label='Predicted')
    plt.xlabel('Year', fontsize=14)
    # format x-axis as year not decimal
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.ylabel('Number of Unique Developers', fontsize=14)
    plt.title('Actual vs. Predicted Number of Unique Developers for ' + category, fontsize=14)
    plt.legend()
    plt.show()


def regression_analysis_disengagement_1(df, category):
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tools.tools import add_constant

    """
    Performs multilinear regression analysis to estimate the impact of average sentiment
    on the time difference, considering various factors.
    """

    # Remove rows with NaN values
    df = df.dropna()

    # Group by Developer and aggregate data
    df = df.groupby('Developer').agg({
        'Time Difference': 'mean',
        'NLTK_Compound_Sentiment': 'mean',
        'Toxic': 'mean'
    })

    # Convert categorical variables to one-hot encoding
    # df = pd.get_dummies(df, columns=['Day_of_week', 'Time_of_day'], drop_first=True)

    # Calculate Variance Inflation Factor (VIF) to check for multicollinearity
    # X = add_constant(df)
    # vif = pd.DataFrame()
    # vif["variables"] = X.columns
    # vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    # print("VIF:\n", vif)

    # Select relevant variables for the regression model
    X = df[['NLTK_Compound_Sentiment', 'Toxic']]
    y = df['Time Difference']

    # Create and fit a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Print regression results
    print(f'Regression Coefficients: {model.coef_}')
    print(f'Intercept: {model.intercept_}')
    print(f'R^2 (Coefficient of Determination): {model.score(X, y)}')



    # Predict sentiment based on the model
    y_pred = model.predict(X)

    # Plot actual vs. predicted sentiment
    # plt.figure(figsize=(8, 6))
    # plt.scatter(df['Previous_Compound_Sentiment'], y, label='Actual', color='blue')
    # plt.plot(df['Previous_Compound_Sentiment'], y_pred, label='Predicted', color='red')
    # plt.xlabel('Previous Commit Sentiment')
    # plt.ylabel('Commit Message Sentiment')
    # plt.title('Actual vs. Predicted Commit Message Sentiment for ' + category)
    # plt.legend()
    # plt.show()

def regression_analysis_toxic(df, category):
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tools.tools import add_constant

    """
    Performs multilinear regression analysis to estimate the impact of average sentiment
    on the time difference, considering various factors.
    """

    # Remove rows with NaN values
    df = df.dropna()

    # Group by Developer and aggregate data
    df = df.groupby('Developer').agg({
        'NLTK_Compound_Sentiment': 'mean',
        'Toxic': 'mean',
        'Previous_Compound_Sentiment': 'mean',
        'Previous_Toxic': 'mean',
    })

    # Convert categorical variables to one-hot encoding
    # df = pd.get_dummies(df, columns=['Day_of_week', 'Time_of_day'], drop_first=True)

    # Calculate Variance Inflation Factor (VIF) to check for multicollinearity
    # X = add_constant(df)
    # vif = pd.DataFrame()
    # vif["variables"] = X.columns
    # vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    # print("VIF:\n", vif)

    # Select relevant variables for the regression model
    X = df[['Previous_Compound_Sentiment', 'Previous_Toxic']]
    y = df['NLTK_Compound_Sentiment']

    # Create and fit a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Print regression results
    print(f'Regression Coefficients: {model.coef_}')
    print(f'Intercept: {model.intercept_}')
    print(f'R^2 (Coefficient of Determination): {model.score(X, y)}')



    # Predict sentiment based on the model
    y_pred = model.predict(X)

    # Plot actual vs. predicted sentiment
    # plt.figure(figsize=(8, 6))
    # plt.scatter(df['Previous_Compound_Sentiment'], y, label='Actual', color='blue')
    # plt.plot(df['Previous_Compound_Sentiment'], y_pred, label='Predicted', color='red')
    # plt.xlabel('Previous Commit Sentiment')
    # plt.ylabel('Commit Message Sentiment')
    # plt.title('Actual vs. Predicted Commit Message Sentiment for ' + category)
    # plt.legend()
    # plt.show()

if __name__ == '__main__':
    import argparse

    argparse = argparse.ArgumentParser()
    argparse.add_argument('--path', type=str, default='data.csv', help='Path to the dataset')
    argparse.add_argument('--category', type=str, default='category', help='Category to analyze')

    csv_path = argparse.parse_args().path
    # Load the dataset
    df = pd.read_csv(csv_path)
    # Convert 'Timestamp' to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Extract 'Year' from 'Timestamp'
    df['Year'] = df['Timestamp'].dt.year

    # Perform regression analysis
    regression_analysis_disengagement_1(df, argparse.parse_args().category)
    regression_analysis_disengagement_2(df, argparse.parse_args().category)
    regression_analysis_toxic(df, argparse.parse_args().category)
