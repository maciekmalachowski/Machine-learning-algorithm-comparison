import pandas as pd

def get_data():
    name = "financial"
    dataset_type = "class"
    df = pd.read_csv("https://raw.githubusercontent.com/pplonski/datasets-for-start/master/credit/data.csv")

    x_cols = ["Id", "RevolvingUtilizationOfUnsecuredLines", "age", "NumberOfTime30-59DaysPastDueNotWorse", "DebtRatio", "MonthlyIncome", "NumberOfOpenCreditLinesAndLoans", "NumberOfTimes90DaysLate", "NumberRealEstateLoansOrLines", "NumberOfTime60-89DaysPastDueNotWorse", "NumberOfDependents"]
    y_col = "SeriousDlqin2yrs"
    # set input matrix
    X = df[x_cols]
    # set target vector
    y = df[y_col]

    return X, y, name, dataset_type
