import pandas as pd

def get_data():
    name = "student"
    dataset_type = "class"
    df = pd.read_csv("C:/Users/Maciek/W_my_notebooks/technological/creditcard.csv")

    # create X columns list and set y column
    x_cols = ["Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20", "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"]
    y_col = "Class"
    # set input matrix
    X = df[x_cols]
    # set target vector
    y = df[y_col]

    return X, y, name, dataset_type
