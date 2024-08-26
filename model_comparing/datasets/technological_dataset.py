import pandas as pd
from sklearn.model_selection import train_test_split

def get_data():
    name = "student"
    dataset_type = "class"
    df = pd.read_csv("C:/Users/Maciek/W_my_notebooks/technological/creditcard.csv")
    
    train, test = train_test_split(df, train_size=0.95, shuffle=True, random_state=42)

    # create X columns list and set y column
    x_cols = ["Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20", "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"]
    y_col = "Class"
    # set input matrix
    X_train = train[x_cols]
    # set target vector
    y_train = train[y_col]
    # set input matrix
    X_test = test[x_cols]
    # set target vector
    y_test = test[y_col]

    return name, X_train, X_test, y_train, y_test, dataset_type
