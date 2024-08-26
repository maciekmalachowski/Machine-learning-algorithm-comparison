import pandas as pd
from sklearn.model_selection import train_test_split

def get_data():
    # read data from openml page
    name = "financial"
    dataset_type = "class"
    df = pd.read_csv("https://raw.githubusercontent.com/pplonski/datasets-for-start/master/credit/data.csv")
    # split data
    train, test = train_test_split(df, train_size=0.75, shuffle=True, random_state=42)

    x_cols = ["Id", "RevolvingUtilizationOfUnsecuredLines", "age", "NumberOfTime30-59DaysPastDueNotWorse", "DebtRatio", "MonthlyIncome", "NumberOfOpenCreditLinesAndLoans", "NumberOfTimes90DaysLate", "NumberRealEstateLoansOrLines", "NumberOfTime60-89DaysPastDueNotWorse", "NumberOfDependents"]
    y_col = "SeriousDlqin2yrs"
    # set input matrix
    X_train = train[x_cols]
    # set target vector
    y_train = train[y_col]
    # set input matrix
    X_test = test[x_cols]
    # set target vector
    y_test = test[y_col]

    return name, X_train, X_test, y_train, y_test, dataset_type
