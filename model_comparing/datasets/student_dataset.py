import pandas as pd
from sklearn.model_selection import train_test_split

def get_data():
    name = "student"
    dataset_type = "class"
    df = pd.read_csv("C:/Users/Maciek/W_my_notebooks/student/student-por.csv", delimiter=";")
    
    # create X columns list and set y column
    x_cols = ["school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob", "reason", "guardian", "traveltime", "studytime", "failures", "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic", "famrel", "freetime", "goout", "Dalc", "Walc", "health", "absences"]
    y_col = "G3"
    # set input matrix
    X = df[x_cols]
    # set target vector
    y = df[y_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.90, shuffle=True, random_state=42)

    return name, X_train, X_test, y_train, y_test, dataset_type
